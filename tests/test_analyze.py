from collections import Counter
from datetime import datetime, timezone

from src.analyze import (
    aggregate_by_field,
    build_meta_ads_params,
    compute_radius,
    compute_stats,
    generate_report,
    price_label,
    tipo_label,
)


SAMPLE = [
    {
        "place_id": "a",
        "nome": "Rest A",
        "bairro": "Manaíra",
        "tipo": "restaurant",
        "rating": 4.5,
        "price_level": 2,
        "tem_website": True,
        "lat": -7.11,
        "lng": -34.84,
    },
    {
        "place_id": "b",
        "nome": "Rest B",
        "bairro": "Manaíra",
        "tipo": "italian_restaurant",
        "rating": 4.2,
        "price_level": 3,
        "tem_website": False,
        "lat": -7.10,
        "lng": -34.83,
    },
    {
        "place_id": "c",
        "nome": "Rest C",
        "bairro": "Tambaú",
        "tipo": "restaurant",
        "rating": 4.7,
        "price_level": 2,
        "tem_website": True,
        "lat": -7.12,
        "lng": -34.82,
    },
    {
        "place_id": "d",
        "nome": "Rest D",
        "bairro": "Cabo Branco",
        "tipo": "seafood_restaurant",
        "rating": None,
        "price_level": None,
        "tem_website": False,
        "lat": -7.14,
        "lng": -34.83,
    },
]


def test_aggregate_by_bairro():
    result = aggregate_by_field(SAMPLE, "bairro")
    assert len(result) == 3
    assert result[0] == ("Manaíra", 2)
    singles = {b for b, c in result if c == 1}
    assert singles == {"Cabo Branco", "Tambaú"}


def test_aggregate_by_tipo():
    result = aggregate_by_field(SAMPLE, "tipo")
    assert len(result) == 3
    assert result[0] == ("restaurant", 2)
    assert result[1] == ("italian_restaurant", 1)
    assert result[2] == ("seafood_restaurant", 1)


def test_aggregate_by_price_level():
    result = aggregate_by_field(SAMPLE, "price_level")
    no_price = sum(1 for r in result if r[0] is None)
    assert no_price == 1
    with_price = sum(1 for r in result if r[0] is not None)
    assert with_price == 2


def test_compute_stats():
    stats = compute_stats(SAMPLE)
    assert stats["total"] == 4
    assert abs(stats["avg_rating"] - 4.47) < 0.05
    assert stats["above_45"] == 2
    assert stats["com_website"] == 2
    assert stats["sem_website"] == 2


def test_compute_radius():
    lat, lng, radius_km = compute_radius(SAMPLE)
    assert -7.13 < lat < -7.10
    assert -34.85 < lng < -34.81
    assert radius_km > 0


def test_price_label():
    assert price_label(0) == "0 (Grátis)"
    assert price_label(1) == "1 ($)"
    assert price_label(2) == "2 ($$)"
    assert price_label(3) == "3 ($$$)"
    assert price_label(None) == "Não classificado"


def test_tipo_label():
    assert tipo_label("restaurant") == "Restaurante"
    assert tipo_label("italian_restaurant") == "Restaurante italiano"
    assert tipo_label("steak_house") == "Churrascaria"
    assert tipo_label("unknown_type") == "unknown_type"


def test_build_meta_ads_params():
    params = build_meta_ads_params(
        bairros_top=["Manaíra", "Tambaú"],
        center_lat=-7.11,
        center_lng=-34.83,
        radius_km=3.3,
        tipos_top=["restaurant"],
        total=4,
    )
    assert "Manaíra" in params["bairros_incluidos"]
    assert "3.3 km" in params["raio"]
    assert "restaurant" in params["interesses"]
    assert "João Pessoa" in params["localizacao"]


def test_generate_report_contains_required_sections():
    report = generate_report(
        SAMPLE,
        bairro_dist=[("Manaíra", 2)],
        tipo_dist=[("restaurant", 2)],
        preco_dist=[(2, 2)],
        stats={
            "total": 4,
            "avg_rating": 4.47,
            "above_45": 2,
            "com_website": 2,
            "sem_website": 2,
        },
        centro=(-7.11, -34.83),
        raio_km=3.3,
    )
    assert "Distribuição Geográfica" in report
    assert "Categoria Dominante" in report
    assert "Perfil de Preço" in report
    assert "Rating" in report
    assert "Maturidade Digital" in report
    assert "Segmentação Manual" in report
    assert "O Que o Gestor Ganha" in report
