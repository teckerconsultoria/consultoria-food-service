"""Carrega e valida a configuração de busca personalizada."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass
class SearchConfig:
    nichos: list[str]
    bairros: list[str]
    cidade: str = "João Pessoa"
    min_rating: float | None = None
    open_now: bool = False
    included_type: str | None = None
    enrich_details: bool = True
    target: int = 50

    def build_queries(self) -> list[str]:
        queries = []
        for bairro in self.bairros:
            for nicho in self.nichos:
                query = f"{nicho} em {bairro}, {self.cidade}"
                queries.append(query)
        return queries

    def build_search_params(self, query: str) -> dict:
        params: dict = {"query": query}

        if self.min_rating is not None:
            params["minRating"] = self.min_rating

        if self.open_now:
            params["openNow"] = True

        if self.included_type:
            params["includedType"] = self.included_type

        return params


def load_config(path: str = "config/search.yaml") -> SearchConfig:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(p) as f:
        raw = yaml.safe_load(f) or {}

    return SearchConfig(
        nichos=raw.get("nichos", ["restaurante"]),
        bairros=raw.get("bairros", ["Manaíra"]),
        cidade=raw.get("cidade", "João Pessoa"),
        min_rating=raw.get("filtros", {}).get("min_rating"),
        open_now=raw.get("filtros", {}).get("open_now", False),
        included_type=raw.get("filtros", {}).get("included_type"),
        enrich_details=raw.get("enrich_details", True),
        target=raw.get("target", 50),
    )
