#!/usr/bin/env python3
"""Coleta restaurantes de João Pessoa com dados enriquecidos e salva no Supabase.

Uso:
    python scripts/coletar.py
    python scripts/coletar.py --target 100
    python scripts/coletar.py --query "pizzarias em João Pessoa"
"""

import argparse
import os
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import load_config
from src.db import get_supabase_client, fetch_restaurants, upsert_restaurants
from src.collect import collect_restaurants


def main():
    parser = argparse.ArgumentParser(description="Coletar restaurantes de João Pessoa")
    parser.add_argument("--target", type=int, default=100, help="Número alvo de restaurantes")
    parser.add_argument("--query", type=str, default="restaurantes em João Pessoa", help="Query de busca")
    parser.add_argument("--no-enrich", action="store_true", help="Não enriquecer com place-details")
    parser.add_argument("--min-rating", type=float, default=None, help="Rating mínimo (1.0-5.0)")
    parser.add_argument("--open-now", action="store_true", help="Apenas abertos agora")
    parser.add_argument("--clear", action="store_true", help="Limpar base antes de coletar")
    args = parser.parse_args()

    c = load_config()
    client = get_supabase_client(c)

    if args.clear:
        existing = fetch_restaurants(client)
        for r in existing:
            client.table("restaurantes").delete().eq("place_id", r["place_id"]).execute()
        print(f"Base limpa: {len(existing)} removidos")

    print(f"Coletando: '{args.query}' (target={args.target}, enrich={not args.no_enrich})...")

    results = collect_restaurants(
        queries=[args.query],
        target=args.target,
        enrich_details=not args.no_enrich,
        min_rating=args.min_rating,
        open_now=args.open_now,
    )

    if not results:
        print("Nenhum resultado.")
        sys.exit(1)

    data = [r.to_dict() for r in results]
    upsert_restaurants(client, data)
    print(f"\nPersistidos: {len(data)} restaurantes\n")

    bairros = Counter(r.bairro for r in results)
    for b, n in bairros.most_common():
        print(f"  {b}: {n}")

    ratings = [r.rating for r in results if r.rating]
    avg = sum(ratings) / len(ratings) if ratings else 0
    com_site = sum(1 for r in results if r.tem_website)
    com_delivery = sum(1 for r in results if r.dining_options and r.dining_options.get("delivery"))
    com_telefone = sum(1 for r in results if r.telefone)

    print(f"\nRating médio: {avg:.1f}")
    print(f"Com website: {com_site}/{len(results)}")
    print(f"Com delivery: {com_delivery}/{len(results)}")
    print(f"Com telefone: {com_telefone}/{len(results)}")


if __name__ == "__main__":
    main()
