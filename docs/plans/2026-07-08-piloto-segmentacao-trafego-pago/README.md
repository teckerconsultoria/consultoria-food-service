# Piloto de Inteligência de Mercado para Segmentação de Tráfego Pago — Restaurantes em João Pessoa

> Plano de execução de piloto de negócio + tecnologia. Stack: Python 3.12 + Supabase + mcp-google-map + Meta Ads.

**Spec completa:** [`spec.md`](./spec.md)

---

## O que este plano constrói

1. Base de restaurantes de João Pessoa coletada via `mcp-google-map` (MCP server).
2. Relatório de densidade/perfil: bairros, categoria, faixa de preço, rating, maturidade digital.
3. Recomendação de raio(s) e interesses para Meta Ads baseada em dados reais.
4. Conta Meta Business Manager + campanha piloto ativa.
5. Argumento de venda: comparação "achismo vs dados".

---

## Arquitetura

```
mcp-google-map (MCP) → collect.py → normalização → Supabase
                                    ↓
                         analyze.py (TODO)
                                    ↓
                         Relatório Markdown + CSV
                                    ↓
                         Meta Ads Manager (manual)
```

---

## Issues

| # | Issue | Status |
|---|---|---|
| 1 | Setup de contas e ambiente | ✅ resolved |
| 2 | Coleta e persistência de dados | ✅ resolved |
| 3 | Análise e relatório de densidade | open |
| 4 | Meta Ads e campanha ativa | open |
| 5 | Material de venda | open |

Veja `stats.json` para detalhes.

---

## Comandos

```bash
# Instalar dependências
pip install -r requirements.txt

# Coletar restaurantes + gerar relatório
python -c "
from src.config import load_config
from src.db import get_supabase_client, upsert_restaurants
from src.collect import collect_restaurants

config = load_config()
client = get_supabase_client(config)
results = collect_restaurants([
    'restaurantes em Manaíra, João Pessoa',
    'restaurantes em Tambaú, João Pessoa',
    'restaurantes em Cabo Branco, João Pessoa',
    'restaurantes em Jardim Oceania, João Pessoa',
    'restaurantes em Bessa, João Pessoa',
], target=50, enrich_details=True)
upsert_restaurants(client, [r.to_dict() for r in results])
print(f'{len(results)} restaurantes persistidos')
"

# Rodar testes
pytest tests/
```

---

## Skills utilizadas

- `backend-patterns` — Supabase, schema, RLS
- `python-patterns` — scripts Python, TDD
- `api-design` — mcp-google-map como MCP server
- `analytics-tracking` — Meta Ads

---

## Checklist de execução

- [x] Validar spec com cliente/gestor
- [x] Coletar acesso e chaves (Google Maps, Supabase)
- [x] Resolver Issue 1: setup de contas e ambiente
- [x] Resolver Issue 2: coleta e persistência
- [ ] Resolver Issue 3: análise e relatório
- [ ] Resolver Issue 4: Meta Ads e campanha ativa
- [ ] Resolver Issue 5: material de venda
- [ ] Coletar acesso Meta Business Manager (cliente)
- [x] Atualizar `stats.json` ao final de cada issue
