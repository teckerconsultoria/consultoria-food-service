import json
import logging
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

from src.models import Restaurante

logger = logging.getLogger(__name__)

MCP_PACKAGE = "@cablate/mcp-google-map"

PRICE_LEVEL_MAP = {
    "PRICE_LEVEL_UNSPECIFIED": None,
    "PRICE_LEVEL_FREE": 0,
    "PRICE_LEVEL_INEXPENSIVE": 1,
    "PRICE_LEVEL_MODERATE": 2,
    "PRICE_LEVEL_EXPENSIVE": 3,
    "PRICE_LEVEL_VERY_EXPENSIVE": 4,
}


def _mcp_exec(tool: str, params: dict) -> dict:
    cmd = [
        "npx", "-y", MCP_PACKAGE, "exec", tool,
        json.dumps(params, ensure_ascii=False),
    ]
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=30,
    )
    if result.returncode != 0:
        logger.error("MCP exec %s failed: %s", tool, result.stderr[:500])
        raise RuntimeError(
            f"MCP exec '{tool}' failed (code {result.returncode}): {result.stderr[:300]}"
        )
    return json.loads(result.stdout) if result.stdout.strip() else {}


def search_places(query: str, **kwargs) -> list[dict]:
    params = {"query": query}

    for key, val in kwargs.items():
        if val is not None:
            params[key] = val

    data = _mcp_exec("search-places", params)
    if not data.get("success"):
        logger.warning("search-places returned error: %s", data.get("error", ""))
        return []
    return data.get("data", [])


def get_place_details(place_id: str) -> dict:
    data = _mcp_exec("place-details", {"placeId": place_id})
    if not data.get("success"):
        logger.warning("place-details failed for %s: %s", place_id, data.get("error", ""))
        return {}
    return data.get("data", {})


def _extract_bairro_from_address(address: str) -> str:
    import re
    match = re.search(
        r"\s-\s([^-]+),\s*Jo[aã]o\s+Pessoa\s*-",
        address,
        re.IGNORECASE,
    )
    return match.group(1).strip() if match else ""


def reverse_geocode_mcp(lat: float, lng: float) -> str | None:
    return None


def deduplicate(places: list[dict]) -> list[dict]:
    seen = set()
    unique = []
    for place in places:
        pid = place.get("place_id", "")
        if pid and pid not in seen:
            seen.add(pid)
            unique.append(place)
    return unique


def _get_price_level(raw: str | None) -> int | None:
    return PRICE_LEVEL_MAP.get(raw) if raw else None


def parse_place(raw: dict) -> Restaurante:
    lat = raw.get("location", {}).get("lat", 0.0)
    lng = raw.get("location", {}).get("lng", 0.0)

    endereco = raw.get("address", "")
    bairro = reverse_geocode_mcp(lat, lng) or _extract_bairro_from_address(endereco)

    return Restaurante(
        place_id=raw.get("place_id", ""),
        nome=raw.get("name", ""),
        endereco=endereco,
        bairro=bairro,
        lat=lat,
        lng=lng,
        tipo=raw.get("primary_type", ""),
        rating=raw.get("rating"),
        price_level=_get_price_level(raw.get("price_level")),
        tem_website=bool(raw.get("website")),
        permanently_closed=False,
        data_coleta=datetime.now(timezone.utc),
    )


def collect_restaurants(
    queries: list[str],
    target: int = 100,
    enrich_details: bool = True,
    min_rating: float | None = None,
    open_now: bool = False,
    included_type: str | None = None,
) -> list[Restaurante]:
    all_raw: list[dict] = []

    search_kwargs = {
        "minRating": min_rating,
        "openNow": open_now if open_now else None,
        "includedType": included_type,
    }

    for query in queries:
        if len(all_raw) >= target:
            break
        results = search_places(query, **search_kwargs)
        all_raw.extend(results)
        logger.info("Query '%s' returned %d results", query, len(results))

    deduped = deduplicate(all_raw)
    logger.info("Collected %d raw, %d after dedup", len(all_raw), len(deduped))

    parsed = []
    enriched = deduped[:target]

    if enrich_details:
        logger.info("Enriching %d places with details (parallel)...", len(enriched))

        def enrich_one(place):
            details = get_place_details(place["place_id"])
            return {**place, **(details or {})}

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {executor.submit(enrich_one, p): i for i, p in enumerate(enriched)}
            result_list = [None] * len(enriched)
            for future in as_completed(futures):
                idx = futures[future]
                try:
                    result_list[idx] = future.result(timeout=15)
                except Exception as e:
                    logger.warning("enrich failed for idx %d: %s", idx, e)
                    result_list[idx] = enriched[idx]

            enriched = [r for r in result_list if r is not None]

    for place in enriched:
        parsed.append(parse_place(place))

    logger.info("Final collection: %d restaurantes", len(parsed))
    return parsed


def collect_from_config(config_path: str = "config/search.yaml") -> list[Restaurante]:
    from src.search_config import SearchConfig, load_config

    cfg = load_config(config_path)

    queries = cfg.build_queries()
    logger.info(
        "Search config: nichos=%s bairros=%s min_rating=%s open_now=%s target=%d",
        cfg.nichos, cfg.bairros, cfg.min_rating, cfg.open_now, cfg.target,
    )

    return collect_restaurants(
        queries=queries,
        target=cfg.target,
        enrich_details=cfg.enrich_details,
        min_rating=cfg.min_rating,
        open_now=cfg.open_now,
        included_type=cfg.included_type,
    )
