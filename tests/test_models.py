from datetime import datetime, timezone

from src.models import Restaurante


def test_restaurante_to_dict_returns_expected_fields():
    restaurante = Restaurante(
        place_id="ChIJ_123",
        nome="Restaurante A",
        endereco="Rua 1, 123",
        bairro="Manaíra",
        lat=-7.115,
        lng=-34.823,
        tipo="restaurant",
        rating=4.5,
        price_level=2,
        tem_website=True,
        permanently_closed=False,
        data_coleta=datetime(2026, 7, 8, 12, 0, 0, tzinfo=timezone.utc),
    )

    data = restaurante.to_dict()

    assert data["place_id"] == "ChIJ_123"
    assert data["nome"] == "Restaurante A"
    assert data["bairro"] == "Manaíra"
    assert data["lat"] == -7.115
    assert data["rating"] == 4.5
    assert data["price_level"] == 2
    assert data["tem_website"] is True
    assert data["permanently_closed"] is False
    assert data["data_coleta"] == "2026-07-08T12:00:00+00:00"
