# Piloto de Inteligência de Mercado para Segmentação de Tráfego Pago — Restaurantes em João Pessoa

> Plano de execução de piloto de negócio + tecnologia. Não é plano de código puro — inclui setup de APIs, banco, campanha Meta e entregáveis comerciais.

**Spec completa:** [`spec.md`](./spec.md)

---

## O que este plano constrói

Piloto de 5 a 7 dias que produz:

1. Base de **100 restaurantes únicos de João Pessoa** coletada via Google Places API.
2. Relatório de densidade/perfil com bairros prioritários, categoria dominante, faixa de preço e rating.
3. Recomendação de raio(s) geográfico(s) e interesses para Meta Ads.
4. Conta Meta Business Manager + conta de anúncios criada.
5. Campanha piloto ativa no Meta Ads com segmentação manual baseada nos dados.
6. Argumento de venda com prova: comparação "achismo vs dados" sobre o N=100.

---

## Arquitetura

```
Google Places API → Script Python (collect) → Normalização → Supabase
                                                          ↓
                                              Script Python (analyze)
                                                          ↓
                                             Relatório Markdown + CSV
                                                          ↓
                                              Meta Ads Manager (manual)
                                                          ↓
                                             Campanha ativa + pitch
```

---

## Issues

| # | Issue | Status | Skill principal |
|---|---|---|---|
| 1 | Setup de contas e ambiente | open | `backend-patterns` |
| 2 | Coleta e persistência de dados | open | `python-patterns` + `api-design` |
| 3 | Análise e relatório de densidade | open | `python-patterns` |
| 4 | Meta Ads e campanha ativa | open | `analytics-tracking` |
| 5 | Material de venda (achismo vs dados) | open | `copywriting` |

Veja `stats.json` para a fonte da verdade.

---

## Comandos

```bash
# Instalar dependências
pip install -r requirements.txt

# Coletar restaurantes
python src/collect.py

# Gerar relatório
python src/analyze.py
```

---

## Skills

- `backend-patterns` — arquitetura da camada de dados e Supabase
- `python-patterns` — scripts Python idiomáticos
- `api-design` — consumo de Google Places API e estrutura de dados
- `analytics-tracking` — configuração de campanha e segmentação no Meta Ads
- `writing-plans` — decompor em tarefas executáveis

---

## Checklist de execução

- [ ] Validar spec com cliente/gestor
- [ ] Coletar acesso e chaves (Google Cloud, Supabase, Meta BM)
- [ ] Resolver Issue 1: setup de contas e ambiente
- [ ] Resolver Issue 2: coleta e persistência
- [ ] Resolver Issue 3: análise e relatório
- [ ] Resolver Issue 4: Meta Ads e campanha ativa
- [ ] Resolver Issue 5: material de venda
- [ ] Atualizar `stats.json` ao final de cada issue
