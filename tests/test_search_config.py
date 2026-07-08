import tempfile
from pathlib import Path

import pytest

from src.search_config import SearchConfig, load_config


def test_build_queries_combines_nichos_and_bairros():
    cfg = SearchConfig(
        nichos=["restaurante", "pizzaria"],
        bairros=["Manaíra", "Tambaú"],
        cidade="João Pessoa",
    )
    queries = cfg.build_queries()

    assert len(queries) == 4
    assert "restaurante em Manaíra, João Pessoa" in queries
    assert "pizzaria em Tambaú, João Pessoa" in queries


def test_build_search_params_with_filters():
    cfg = SearchConfig(
        nichos=["restaurante"],
        bairros=["Manaíra"],
        min_rating=4.0,
        open_now=True,
        included_type="restaurant",
    )
    params = cfg.build_search_params("restaurante em Manaíra, João Pessoa")

    assert params["query"] == "restaurante em Manaíra, João Pessoa"
    assert params["minRating"] == 4.0
    assert params["openNow"] is True
    assert params["includedType"] == "restaurant"


def test_build_search_params_without_optional_filters():
    cfg = SearchConfig(
        nichos=["restaurante"],
        bairros=["Manaíra"],
    )
    params = cfg.build_search_params("test query")

    assert params["query"] == "test query"
    assert "minRating" not in params
    assert "openNow" not in params
    assert "includedType" not in params


def test_load_config_from_yaml():
    yaml_content = """
nichos:
  - sushi
  - comida japonesa
bairros:
  - Cabo Branco
filtros:
  min_rating: 4.5
  open_now: false
enrich_details: true
target: 30
cidade: João Pessoa
"""

    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
        f.write(yaml_content)
        tmp = f.name

    try:
        cfg = load_config(tmp)
        assert cfg.nichos == ["sushi", "comida japonesa"]
        assert cfg.bairros == ["Cabo Branco"]
        assert cfg.min_rating == 4.5
        assert cfg.open_now is False
        assert cfg.enrich_details is True
        assert cfg.target == 30
    finally:
        Path(tmp).unlink()


def test_load_config_defaults_when_missing_file():
    with pytest.raises(FileNotFoundError):
        load_config("config/nao_existe.yaml")


def test_build_search_params_open_now_false_not_in_params():
    cfg = SearchConfig(
        nichos=["restaurante"],
        bairros=["Tambaú"],
        open_now=False,
    )
    params = cfg.build_search_params("q")

    assert "openNow" not in params
