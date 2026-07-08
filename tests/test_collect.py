import json
from datetime import datetime
from unittest.mock import MagicMock, patch

from src.collect import (
    _mcp_exec,
    collect_restaurants,
    deduplicate,
    filter_closed,
    parse_place,
    search_places,
)


def make_places_api_place(
    place_id="ChIJ_123",
    nome="Restaurante A",
    endereco="Rua 1, 123",
    lat=-7.115,
    lng=-34.823,
    tipos=None,
    rating=4.5,
    price_level=None,
    tem_website=False,
    business_status="OPERATIONAL",
):
    if tipos is None:
        tipos = ["restaurant"]

    return {
        "id": place_id,
        "displayName": {"text": nome},
        "formattedAddress": endereco,
        "location": {"latitude": lat, "longitude": lng},
        "types": tipos,
        "rating": rating,
        "priceLevel": price_level,
        "websiteUri": "https://restaurante.com.br" if tem_website else None,
        "businessStatus": business_status,
    }


def make_mock_run(stdout_data):
    mock = MagicMock()
    mock.returncode = 0
    mock.stdout = json.dumps(stdout_data, ensure_ascii=False)
    mock.stderr = ""
    return mock


def test_deduplicate_removes_duplicates():
    places = [
        make_places_api_place(place_id="A"),
        make_places_api_place(place_id="B"),
        make_places_api_place(place_id="A"),
    ]
    result = deduplicate(places)
    assert len(result) == 2
    assert [p["id"] for p in result] == ["A", "B"]


def test_deduplicate_preserves_order():
    places = [
        make_places_api_place(place_id="C"),
        make_places_api_place(place_id="A"),
        make_places_api_place(place_id="B"),
    ]
    result = deduplicate(places)
    assert [p["id"] for p in result] == ["C", "A", "B"]


def test_filter_closed_removes_permanently_closed():
    places = [
        make_places_api_place(place_id="A", business_status="OPERATIONAL"),
        make_places_api_place(place_id="B", business_status="CLOSED_PERMANENTLY"),
        make_places_api_place(place_id="C", business_status="OPERATIONAL"),
    ]
    result = filter_closed(places)
    assert len(result) == 2
    assert [p["id"] for p in result] == ["A", "C"]


def test_filter_closed_preserves_temporarily_closed():
    places = [
        make_places_api_place(place_id="A", business_status="CLOSED_TEMPORARILY"),
    ]
    result = filter_closed(places)
    assert len(result) == 1


def test_parse_place_converts_to_restaurante():
    mock_rev = make_mock_run({
        "results": [{
            "address_components": [
                {"short_name": "Manaíra", "types": ["sublocality"]},
            ]
        }]
    })

    with patch("src.collect.subprocess.run", return_value=mock_rev):
        raw = make_places_api_place(
            place_id="ChIJ_456",
            nome="Pastelão",
            endereco="Av 1, 456",
            lat=-7.11,
            lng=-34.82,
            tipos=["restaurant", "food"],
            rating=4.2,
            price_level="PRICE_LEVEL_MODERATE",
            tem_website=True,
        )
        result = parse_place(raw)

    assert result.place_id == "ChIJ_456"
    assert result.nome == "Pastelão"
    assert result.bairro == "Manaíra"
    assert result.rating == 4.2
    assert result.price_level == 2
    assert result.tem_website is True
    assert result.permanently_closed is False


def test_parse_place_uses_neighborhood_fallback():
    mock_rev = make_mock_run({
        "results": [{
            "address_components": [
                {"short_name": "Cabo Branco", "types": ["neighborhood"]},
            ]
        }]
    })

    with patch("src.collect.subprocess.run", return_value=mock_rev):
        raw = make_places_api_place(place_id="X")
        result = parse_place(raw)

    assert result.bairro == "Cabo Branco"


def test_parse_place_defaults_empty_bairro_when_none():
    mock_rev = make_mock_run({"results": []})

    with patch("src.collect.subprocess.run", return_value=mock_rev):
        raw = make_places_api_place(place_id="Z", endereco="Rua Z")
        result = parse_place(raw)

    assert result.bairro == ""


def test_search_places_calls_mcp_exec():
    mock_run = make_mock_run({
        "places": [
            {"id": "place_1", "displayName": {"text": "P1"}},
            {"id": "place_2", "displayName": {"text": "P2"}},
        ]
    })

    with patch("src.collect.subprocess.run", return_value=mock_run):
        results = search_places("restaurantes em Manaíra, João Pessoa")

    assert len(results) == 2
    assert results[0]["id"] == "place_1"


def test_collect_restaurants_returns_up_to_target():
    sample_places = [make_places_api_place(place_id=f"p{i}") for i in range(15)]

    mock_search = MagicMock()
    mock_search.returncode = 0
    mock_search.stdout = json.dumps({"places": sample_places}, ensure_ascii=False)
    mock_search.stderr = ""

    mock_rev = make_mock_run({"results": [{"address_components": [
        {"short_name": "Centro", "types": ["sublocality"]}
    ]}]})

    with patch("src.collect.subprocess.run") as mock_run:
        mock_run.side_effect = [mock_search] + [mock_rev] * 15

        results = collect_restaurants(
            queries=["restaurantes João Pessoa"],
            target=8,
        )

    assert len(results) == 8
    assert all(r.bairro == "Centro" for r in results)


def test_collect_restaurants_deduplicates_across_queries():
    place_a = make_places_api_place(place_id="dup", nome="Duplicado")

    mock_search = MagicMock()
    mock_search.returncode = 0
    mock_search.stdout = json.dumps({"places": [place_a]}, ensure_ascii=False)
    mock_search.stderr = ""

    mock_rev = make_mock_run({
        "results": [{"address_components": [
            {"short_name": "Tambaú", "types": ["sublocality"]}
        ]}]
    })

    with patch("src.collect.subprocess.run") as mock_run:
        mock_run.side_effect = [mock_search, mock_search, mock_rev]

        results = collect_restaurants(
            queries=["q1", "q2"],
            target=10,
        )

    assert len(results) == 1
