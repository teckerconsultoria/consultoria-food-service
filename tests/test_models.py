from datetime import datetime, timezone

from src.models import Restaurante


def test_restaurante_to_dict_returns_base_fields():
    r = Restaurante(
        place_id="ChIJ_123",
        nome="Teste",
        endereco="Rua 1",
        bairro="Centro",
        lat=-7.1,
        lng=-34.8,
        tipo="restaurant",
        rating=4.5,
        price_level=2,
        tem_website=True,
        permanently_closed=False,
        data_coleta=datetime(2026, 7, 8, 12, 0, 0, tzinfo=timezone.utc),
    )

    d = r.to_dict()
    assert d["place_id"] == "ChIJ_123"
    assert d["rating"] == 4.5
    assert d["telefone"] is None
    assert d["dining_options"] is None
    assert d["serves"] is None


def test_restaurante_to_dict_includes_rich_data():
    r = Restaurante(
        place_id="X",
        nome="Rich Rest",
        endereco="Rua A",
        bairro="Tambaú",
        lat=-7.11, lng=-34.82,
        tipo="italian_restaurant",
        rating=4.7,
        price_level=2,
        tem_website=True,
        permanently_closed=False,
        data_coleta=datetime(2026, 7, 8, tzinfo=timezone.utc),
        telefone="(83) 99999-0000",
        dining_options={"dine_in": True, "delivery": True},
        serves={"beer": True, "wine": True},
        atmosphere={"outdoor_seating": True},
        payment_options={"acceptsCreditCards": True},
        photo_count=15,
        review_summary="Ótimo restaurante italiano.",
    )

    d = r.to_dict()
    assert d["telefone"] == "(83) 99999-0000"
    assert d["dining_options"]["delivery"] is True
    assert d["serves"]["beer"] is True
    assert d["photo_count"] == 15
    assert d["review_summary"] == "Ótimo restaurante italiano."


def test_restaurante_all_optional_fields_default_none():
    r = Restaurante(
        place_id="A", nome="A", endereco="R", bairro="B",
        lat=0, lng=0, tipo="", rating=None, price_level=None,
        tem_website=False, permanently_closed=False,
        data_coleta=datetime.now(timezone.utc),
    )
    assert r.telefone is None
    assert r.horarios is None
    assert r.parking is None
    assert r.accessibility is None
    assert r.editorial_summary is None
