#!/usr/bin/env python3
"""Coleta por batch: 10 restaurantes por vez, com pausa e progresso.

Uso:
    python scripts/coletar_batch.py
    python scripts/coletar_batch.py --target 100 --batch 10
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import load_config
from src.db import get_supabase_client, fetch_restaurants, upsert_restaurants
from src.collect import collect_restaurants


def _load_bairros() -> list[str]:
    import yaml
    from pathlib import Path
    path = Path("config/bairros_jp.yaml")
    if path.exists():
        with open(path) as f:
            data = yaml.safe_load(f) or {}
        return data.get("bairros", [])
    return []


def main():
    parser = argparse.ArgumentParser(description="Coleta batch de restaurantes")
    parser.add_argument("--target", type=int, default=100)
    parser.add_argument("--batch", type=int, default=10, help="Tamanho do lote")
    parser.add_argument("--clear", action="store_true")
    parser.add_argument("--query", type=str, default="restaurantes", help="Nicho (ex: pizzarias, sushi)")
    args = parser.parse_args()

    c = load_config()
    client = get_supabase_client(c)

    if args.clear:
        existing = fetch_restaurants(client)
        for r in existing:
            client.table("restaurantes").delete().eq("place_id", r["place_id"]).execute()
        print(f"Base limpa: {len(existing)} removidos\n")

    bairros = _load_bairros()
    if not bairros:
        print("ERRO: config/bairros_jp.yaml não encontrado ou vazio")
        sys.exit(1)
    print(f"Bairros carregados: {len(bairros)}")

    collected: list = []
    all_ids: set[str] = set()
    batch_num = 0

    for bairro in bairros:
        if len(all_ids) >= args.target:
            break

        batch_num += 1
        query = f"{args.query} em {bairro}, João Pessoa"
        print(f"Batch {batch_num}: '{query}'...", end=" ", flush=True)

        try:
            results = collect_restaurants(
                queries=[query],
                target=args.target - len(all_ids),
                enrich_details=True,
                min_rating=None,
                open_now=False,
            )
        except Exception as e:
            print(f"ERRO: {e}")
            time.sleep(2)
            continue

        new = [r for r in results if r.place_id not in all_ids]
        if not new:
            print(f"0 novos")
            continue

        all_ids.update(r.place_id for r in new)
        collected.extend(new)

        data = [r.to_dict() for r in new]
        upsert_restaurants(client, data)

        print(f"+{len(new)} (total: {len(all_ids)}/{args.target})")

        if bairro != BAIRROS[-1]:
            time.sleep(1)

    print(f"\n=== FINAL: {len(all_ids)} restaurantes ===")
    bairros_count = Counter(r.bairro for r in collected)
    for b, n in bairros_count.most_common():
        print(f"  {b}: {n}")

    ratings = [r.rating for r in collected if r.rating]
    avg = sum(ratings) / len(ratings) if ratings else 0
    com_site = sum(1 for r in collected if r.tem_website)
    com_tel = sum(1 for r in collected if r.telefone)
    com_delivery = sum(1 for r in collected if r.dining_options and r.dining_options.get("delivery"))
    print(f"\nRating médio: {avg:.1f}")
    print(f"Com site: {com_site}/{len(collected)}")
    print(f"Com tel: {com_tel}/{len(collected)}")
    print(f"Com delivery: {com_delivery}/{len(collected)}")


if __name__ == "__main__":
    main()
