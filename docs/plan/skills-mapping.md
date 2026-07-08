# Mapeamento de Skills por Atividade — Piloto Segmentação de Tráfego Pago

## Atividade 1: Setup de contas e ambiente

**Objetivo:** Criar contas Google Cloud, Supabase e Meta; configurar `.env` e estrutura de pastas.

**Skills recomendadas:**
- **Primária:** `backend-patterns` — arquitetura da camada de dados, configuração de Supabase, organização de projeto
- **Secundária:** `security-review` — proteção de chaves, `.env`, `.gitignore`
- **Opcional (skills.sh):** `kostja94/marketing-skills@meta-ads` — se precisar de detalhes sobre Meta Business Manager

---

## Atividade 2: Coleta e persistência de dados

**Objetivo:** Coletar 100 restaurantes via Google Places API, normalizar bairros, deduplicar, excluir fechados e persistir no Supabase.

**Skills recomendadas:**
- **Primária:** `python-patterns` — scripts Python idiomáticos, tratamento de dados
- **Secundária:** `api-design` — consumo de Google Places API, modelagem de dados, rate limiting
- **Secundária:** `backend-patterns` — conexão com Supabase, schema, migrations
- **Opcional (skills.sh):** `aj-geddes/useful-ai-prompts@api-rate-limiting` — se houver problemas de rate limit

---

## Atividade 3: Análise e relatório de densidade

**Objetivo:** Agregar dados por bairro, categoria, price_level e rating; gerar relatório Markdown e CSV.

**Skills recomendadas:**
- **Primária:** `python-patterns` — Pandas, análise de dados, geração de relatórios
- **Secundária:** `backend-patterns` — leitura de dados do Supabase
- **Opcional:** `highcharts-visualizer` — se quiser gerar visualizações gráficas do relatório

---

## Atividade 4: Meta Ads e campanha ativa

**Objetivo:** Criar conta Meta Business Manager, configurar segmentação geográfica e por interesse, criar e ativar campanha piloto.

**Skills recomendadas:**
- **Primária:** `analytics-tracking` — configuração de tracking, segmentação e medidas no Meta Ads
- **Secundária:** `paid-ads` — estratégia de campanha, targeting, orçamento
- **Opcional (skills.sh):** `kostja94/marketing-skills@meta-ads` (1.7K installs) — referência específica de Meta Ads

---

## Atividade 5: Material de venda (achismo vs dados)

**Objetivo:** Reconstruir segmentação "do achismo", comparar com dados, calcular ruído evitado e gerar pitch.

**Skills recomendadas:**
- **Primária:** `copywriting` — texto de venda, argumentação, pitch
- **Secundária:** `python-patterns` — cálculo de métricas comparativas
- **Opcional:** `gerador-slides` — se quiser transformar o pitch em apresentação de slides

---

## Resumo

| Atividade | Skill primária | Skills secundárias |
|---|---|---|
| 1. Setup de contas e ambiente | `backend-patterns` | `security-review` |
| 2. Coleta e persistência de dados | `python-patterns` | `api-design`, `backend-patterns` |
| 3. Análise e relatório de densidade | `python-patterns` | `backend-patterns` |
| 4. Meta Ads e campanha ativa | `analytics-tracking` | `paid-ads` |
| 5. Material de venda | `copywriting` | `python-patterns` |

## Skills a instalar (se necessário)

Se as skills locais não forem suficientes:

```bash
# Meta Ads (1.7K installs)
npx skills add kostja94/marketing-skills@meta-ads -g -y

# API rate limiting (556 installs)
npx skills add aj-geddes/useful-ai-prompts@api-rate-limiting -g -y
```

---

## Atualização do stats.json

As skills acima devem ser registradas no `stats.json` da feature:

- Issue 1: `primary_skill: backend-patterns`, `secondary_skills: [security-review]`
- Issue 2: `primary_skill: python-patterns`, `secondary_skills: [api-design, backend-patterns]`
- Issue 3: `primary_skill: python-patterns`, `secondary_skills: [backend-patterns]`
- Issue 4: `primary_skill: analytics-tracking`, `secondary_skills: [paid-ads]`
- Issue 5: `primary_skill: copywriting`, `secondary_skills: [python-patterns]`
