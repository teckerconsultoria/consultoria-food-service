import json
import logging
import subprocess
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


def search_places(query: str) -> list[dict]:
    data = _mcp_exec("search-places", {"query": query})
    return data.get("places", [])


def get_place_details(place_id: str) -> dict:
    data = _mcp_exec("place-details", {"place_id": place_id})
    return data


def reverse_geocode(lat: float, lng: float) -> str | None:
    try:
        data = _mcp_exec("reverse-geocode", {"latlng": f"{lat},{lng}"})
        results = data.get("results", [])
        if results:
            address = results[0].get("address_components", [])
            for comp in address:
                if "sublocality" in comp.get("types", []):
                    return comp.get("short_name")
            for comp in address:
                if "neighborhood" in comp.get("types", []):
                    return comp.get("short_name")
        return None
    except Exception:
        return None


def deduplicate(places: list[dict]) -> list[dict]:
    seen = set()
    unique = []
    for place in places:
        pid = place.get("id", "")
        if pid and pid not in seen:
            seen.add(pid)
            unique.append(place)
    return unique


def filter_closed(places: list[dict]) -> list[dict]:
    return [
        p for p in places
        if p.get("businessStatus", "") != "CLOSED_PERMANENTLY"
    ]


def _get_price_level(raw: str | None) -> int | None:
    return PRICE_LEVEL_MAP.get(raw) if raw else None


def parse_place(raw: dict) -> Restaurante:
    lat = raw.get("location", {}).get("latitude", 0.0)
    lng = raw.get("location", {}).get("longitude", 0.0)

    bairro = reverse_geocode(lat, lng) or ""

    tipos = raw.get("types", [])
    tipo = tipos[0] if tipos else ""

    return Restaurante(
        place_id=raw.get("id", ""),
        nome=(raw.get("displayName") or {}).get("text", ""),
        endereco=raw.get("formattedAddress", ""),
        bairro=bairro,
        lat=lat,
        lng=lng,
        tipo=tipo,
        rating=raw.get("rating"),
        price_level=_get_price_level(raw.get("priceLevel")),
        tem_website=bool(raw.get("websiteUri")),
        permanently_closed=raw.get("businessStatus") == "CLOSED_PERMANENTLY",
        data_coleta=datetime.now(timezone.utc),
    )


def collect_restaurants(
    queries: list[str],
    target: int = 100,
) -> list[Restaurante]:
    all_raw: list[dict] = []

    for query in queries:
        if len(all_raw) >= target:
            break

        results = search_places(query)
        all_raw.extend(results)
        logger.info("Query '%s' returned %d results", query, len(results))

    deduped = deduplicate(all_raw)
    open_places = filter_closed(deduped)
    logger.info(
        "Collected %d raw, %d after dedup, %d after removing closed",
        len(all_raw), len(deduped), len(open_places),
    )

    result = [parse_place(p) for p in open_places[:target]]
    logger.info("Final collection: %d restaurantes", len(result))
    return result
