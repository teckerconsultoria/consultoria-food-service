import json
from unittest.mock import MagicMock, patch

from src.collect import (
    collect_restaurants,
    deduplicate,
    parse_place,
    search_places,
)


def make_mcp_place(
    place_id="ChIJ_123",
    name="Restaurante A",
    address="Rua 1, 123 - Manaíra, João Pessoa - PB, 58038-000, Brazil",
    lat=-7.115,
    lng=-34.823,
    primary_type="restaurant",
    rating=4.5,
    price_level=None,
    website="",
):
    return {
        "place_id": place_id,
        "name": name,
        "address": address,
        "location": {"lat": lat, "lng": lng},
        "primary_type": primary_type,
        "rating": rating,
        "price_level": price_level,
        "website": website,
    }


def make_mock_run(stdout_data):
    mock = MagicMock()
    mock.returncode = 0
    mock.stdout = json.dumps(stdout_data, ensure_ascii=False)
    mock.stderr = ""
    return mock


def make_mcp_response(data_list):
    return {"success": True, "data": data_list}


def test_deduplicate_removes_duplicates():
    places = [
        make_mcp_place(place_id="A"),
        make_mcp_place(place_id="B"),
        make_mcp_place(place_id="A"),
    ]
    result = deduplicate(places)
    assert len(result) == 2
    assert [p["place_id"] for p in result] == ["A", "B"]


def test_deduplicate_preserves_order():
    places = [
        make_mcp_place(place_id="C"),
        make_mcp_place(place_id="A"),
        make_mcp_place(place_id="B"),
    ]
    result = deduplicate(places)
    assert [p["place_id"] for p in result] == ["C", "A", "B"]


def test_parse_place_extracts_bairro_from_address():
    raw = make_mcp_place(
        place_id="ChIJ_456",
        name="Pastelão",
        address="Av 1, 456 - Manaíra, João Pessoa - PB, 58038-000, Brazil",
        lat=-7.11,
        lng=-34.82,
        primary_type="steak_house",
        rating=4.2,
        price_level="PRICE_LEVEL_MODERATE",
        website="https://pasteis.com.br",
    )
    result = parse_place(raw)

    assert result.place_id == "ChIJ_456"
    assert result.nome == "Pastelão"
    assert result.endereco == "Av 1, 456 - Manaíra, João Pessoa - PB, 58038-000, Brazil"
    assert result.bairro == "Manaíra"
    assert result.lat == -7.11
    assert result.lng == -34.82
    assert result.tipo == "steak_house"
    assert result.rating == 4.2
    assert result.price_level == 2
    assert result.tem_website is True


def test_parse_place_extracts_tambau():
    raw = make_mcp_place(
        place_id="X",
        name="Local X",
        address="Av. Alm. Tamandaré, 199 - Tambaú, João Pessoa - PB, 58039-010, Brazil",
    )
    result = parse_place(raw)
    assert result.bairro == "Tambaú"


def test_parse_place_extracts_cabo_branco():
    raw = make_mcp_place(
        place_id="Y",
        name="Local Y",
        address="Av. Epitácio Pessoa, 108 - Cabo Branco, João Pessoa - PB, 58040-000, Brazil",
    )
    result = parse_place(raw)
    assert result.bairro == "Cabo Branco"


def test_parse_place_defaults_empty_for_unknown_format():
    raw = make_mcp_place(
        place_id="Z",
        name="Local Z",
        address="Endereço sem formato conhecido",
    )
    result = parse_place(raw)
    assert result.bairro == ""


def test_search_places_returns_data_list():
    mock_run = make_mock_run(make_mcp_response([
        make_mcp_place(place_id="p1", name="R1"),
        make_mcp_place(place_id="p2", name="R2"),
    ]))

    with patch("src.collect.subprocess.run", return_value=mock_run):
        results = search_places("restaurantes em Manaíra")

    assert len(results) == 2
    assert results[0]["place_id"] == "p1"


def test_search_places_returns_empty_on_error():
    mock_run = make_mock_run({"success": False, "error": "Something went wrong"})

    with patch("src.collect.subprocess.run", return_value=mock_run):
        results = search_places("query")

    assert results == []


def test_collect_restaurants_returns_up_to_target():
    sample = [
        make_mcp_place(
            place_id=f"p{i}",
            name=f"R{i}",
            address=f"Rua {i} - Centro, João Pessoa - PB, Brazil",
        )
        for i in range(15)
    ]

    mock_search = make_mock_run(make_mcp_response(sample))

    with patch("src.collect.subprocess.run", return_value=mock_search):
        results = collect_restaurants(
            queries=["restaurantes João Pessoa"],
            target=8,
            enrich_details=False,
        )

    assert len(results) == 8
    assert all(r.bairro == "Centro" for r in results)


def test_collect_restaurants_deduplicates_across_queries():
    place_a = make_mcp_place(place_id="dup", name="Duplicado")

    mock_search = make_mock_run(make_mcp_response([place_a]))

    with patch("src.collect.subprocess.run", return_value=mock_search):
        results = collect_restaurants(
            queries=["q1", "q2"],
            target=10,
            enrich_details=False,
        )

    assert len(results) == 1
