"""Análise de densidade e perfil de restaurantes."""

import csv
import math
from collections import Counter
from pathlib import Path

OUTPUT_DIR = Path("docs/output")
PRICE_LABELS = {
    0: "0 (Grátis)",
    1: "1 ($)",
    2: "2 ($$)",
    3: "3 ($$$)",
    4: "4 ($$$$)",
    None: "Não classificado",
}

TIPO_LABELS: dict[str, str] = {
    "restaurant": "Restaurante",
    "italian_restaurant": "Restaurante italiano",
    "seafood_restaurant": "Frutos do mar",
    "steak_house": "Churrascaria",
    "barbecue_restaurant": "Churrascaria",
    "buffet_restaurant": "Buffet",
    "bar": "Bar",
    "cocktail_bar": "Bar/Coquetelaria",
}


def aggregate_by_field(data: list[dict], field: str) -> list[tuple]:
    counts: Counter = Counter()
    for row in data:
        val = row.get(field)
        counts[val] += 1
    return counts.most_common()


def price_label(level: int | None) -> str:
    return PRICE_LABELS.get(level, "Não classificado")


def tipo_label(tipo: str) -> str:
    return TIPO_LABELS.get(tipo, tipo)


def compute_stats(data: list[dict]) -> dict:
    ratings = [r["rating"] for r in data if r.get("rating") is not None]
    total = len(data)
    return {
        "total": total,
        "avg_rating": round(sum(ratings) / len(ratings), 2) if ratings else 0,
        "above_45": sum(1 for r in ratings if r >= 4.5),
        "com_website": sum(1 for r in data if r.get("tem_website")),
        "sem_website": sum(1 for r in data if not r.get("tem_website")),
    }


def compute_radius(data: list[dict], coverage: float = 0.70) -> tuple[float, float, float]:
    lats = [r["lat"] for r in data if r.get("lat") and r.get("lng")]
    lngs = [r["lng"] for r in data if r.get("lat") and r.get("lng")]
    if not lats:
        return 0.0, 0.0, 0.0

    center_lat = sum(lats) / len(lats)
    center_lng = sum(lngs) / len(lngs)

    distances = []
    for lat, lng in zip(lats, lngs):
        d = math.sqrt((lat - center_lat) ** 2 + (lng - center_lng) ** 2)
        distances.append(d)

    distances.sort()
    idx = min(int(len(distances) * coverage), len(distances) - 1)
    d_deg = distances[idx] if distances else 0
    radius_km = d_deg * 111.32

    return center_lat, center_lng, round(radius_km, 1)


def build_meta_ads_params(
    bairros_top: list[str],
    center_lat: float,
    center_lng: float,
    radius_km: float,
    tipos_top: list[str],
    total: int,
) -> dict:
    return {
        "localizacao": f"João Pessoa + raio {radius_km} km centrado em {center_lat:.3f}, {center_lng:.3f}",
        "raio": f"{radius_km} km",
        "bairros_incluidos": bairros_top,
        "bairros_excluidos": [],
        "interesses": tipos_top,
        "faixa_etaria": "25-55 anos",
        "genero": "Todos",
        "total_restaurantes": total,
    }


def generate_report(
    data: list[dict],
    bairro_dist: list[tuple],
    tipo_dist: list[tuple],
    preco_dist: list[tuple],
    stats: dict,
    centro: tuple[float, float],
    raio_km: float,
) -> str:
    total = stats["total"]
    bairro_pct = [(b, c, round(100 * c / total)) for b, c in bairro_dist]
    tipo_pct = [(t, c, round(100 * c / total)) for t, c in tipo_dist]

    bairro_table = "\n".join(
        f"| {b} | {c} | {p}% |" for b, c, p in bairro_pct
    )
    tipo_table = "\n".join(
        f"| **{tipo_label(t)}** | {c} | {p}% |" for t, c, p in tipo_pct
    )

    return f"""\
# Relatório de Densidade e Perfil — Restaurantes em João Pessoa

**Piloto:** Segmentação de Tráfego Pago  
**Data:** 2026-07-08  
**Amostra:** {total} restaurantes

---

## 1. Distribuição Geográfica (Raio Recomendado)

| Bairro | Restaurantes | % |
|---|---|---|
{bairro_table}
| **Total** | **{total}** | 100% |

**Recomendação:** Raio de {raio_km} km centrado em ({centro[0]:.3f}, {centro[1]:.3f}) cobre ~70% da base.

---

## 2. Categoria Dominante (Interesses para Meta Ads)

| Categoria | Qtd | % |
|---|---|---|
{tipo_table}

**Interesses Meta Ads:** {', '.join(f'`{t}`' for t, _, _ in tipo_pct)}

---

## 3. Perfil de Preço

| Faixa | Qtd |
|---|---|
{chr(10).join(f'| {price_label(p)} | {c} |' for p, c in preco_dist)}

---

## 4. Rating e Qualidade

| Indicador | Valor |
|---|---|
| Rating médio | **{stats['avg_rating']}** |
| ≥ 4.5 | {stats['above_45']}/{total} ({round(100*stats['above_45']/total)}%) |

---

## 5. Maturidade Digital (Website)

| Presença | Qtd |
|---|---|
| Com website | {stats['com_website']} ({round(100*stats['com_website']/total)}%) |
| Sem website | {stats['sem_website']} ({round(100*stats['sem_website']/total)}%) |

---

## 6. Segmentação Manual Recomendada (Meta Ads)

| Parâmetro | Valor |
|---|---|
| Localização | João Pessoa + raio {raio_km} km |
| Bairros incluídos | {', '.join(b for b, _, _ in bairro_pct)} |
| Interesses | {', '.join(tipo_label(t) for t, _, _ in tipo_pct)} |
| Faixa etária | 25-55 anos |
| Gênero | Todos |

---

## 7. O Que o Gestor Ganha

| Sem dados (achismo) | Com dados (este relatório) |
|---|---|
| Raio genérico de 10 km | Raio calibrado de {raio_km} km baseado em densidade real |
| Interesse amplo "restaurantes" | Interesse focado em {len(tipo_dist)} categorias reais |
| Sem filtro de preço | Distribuição real de preço dos {total} restaurantes |
| Não sabe maturidade digital | {round(100*stats['com_website']/total)}% com website |

**Evite o achismo. Use dados.**
"""


def analyze_and_export(data: list[dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    bairro_dist = aggregate_by_field(data, "bairro")
    tipo_dist = aggregate_by_field(data, "tipo")
    preco_dist = aggregate_by_field(data, "price_level")
    stats = compute_stats(data)
    lat, lng, raio = compute_radius(data)

    report = generate_report(data, bairro_dist, tipo_dist, preco_dist, stats, (lat, lng), raio)
    (OUTPUT_DIR / "relatorio-densidade-jp.md").write_text(report, encoding="utf-8")

    csv_path = OUTPUT_DIR / "base-restaurantes-jp.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "place_id", "nome", "bairro", "endereco", "tipo", "rating",
            "price_level", "tem_website", "lat", "lng",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(data)

    print(f"Relatório: {OUTPUT_DIR / 'relatorio-densidade-jp.md'}")
    print(f"CSV: {csv_path}")
    print(f"Total: {len(data)} | Bairros: {len(bairro_dist)} | Categorias: {len(tipo_dist)}")
