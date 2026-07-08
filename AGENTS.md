# AGENTS.md — Consultoria Food Service

## Projeto

Projeto de consultoria de inteligência de mercado para foodservice. Piloto inicial: segmentação de tráfego pago para restaurantes em João Pessoa usando dados reais do Google Places API.

## Layout

- `docs/` — documentos de prospecção, planos e outputs.
- `docs/plans/` — planos de execução seguindo padrão de `YYYY-MM-DD-<slug>/`:
  - `README.md` — referência rápida do agente
  - `spec.md` — especificação completa
  - `stats.json` — fonte da verdade: issues, skills, status, dependências
- `docs/output/` — entregáveis do piloto: relatórios, CSVs, pitches.
- `src/` — scripts Python de coleta, normalização e análise.
- `tests/` — testes dos scripts Python.
- `.env` — variáveis de ambiente (não versionar).

## Ambientes

| Ambiente | Branch | Uso |
|---|---|---|
| **Dev** | `feature/*` | Desenvolvimento de cada feature/piloto |
| **Staging** | `develop` | Integração e validação de features concluídas |
| **Produção** | `main` | Código aprovado e pronto para produção |

### Trabalhando em uma feature

1. Criar branch a partir de `develop`: `git checkout -b feature/<slug> develop`
2. Desenvolver com TDD (testes antes da implementação)
3. Se houver mudanças de schema, criar migration SQL idempotente em `supabase/migrations/`
4. Atualizar `stats.json` da feature conforme issues avançam/resolvam
5. Abrir PR para `develop` quando a feature estiver completa
6. Após merge em `develop`, validar em staging
7. Após validação, abrir PR de `develop` → `main` para produção

## Convenções

- Python 3.11+.
- Use `requirements.txt` para dependências.
- Sempre salvar outputs em `docs/output/`.
- Nunca versionar `.env` nem dados brutos.
- Para APIs, usar `.env` e `src/config.py` para leitura.
- Commits seguem Conventional Commits.
- Nunca fazer push direto em `main` ou `develop` — sempre via PR.

## Plans & Skills Tracking

Features com plano persistido ficam em `docs/plans/YYYY-MM-DD-<slug>/`:

- `stats.json` — fonte da verdade: skill primária e secundária por issue, status, dependências, links.
- `README.md` — workflow do agente e referência rápida das skills.
- `spec.md` — especificação completa da feature.

**Ao trabalhar em qualquer issue de uma feature com plan:**

1. Identificar a feature pela branch: `git branch --show-current` → match com `docs/plans/*/stats.json` (campo `branch`)
2. Carregar a `primary_skill` da issue via `Skill()` tool.
3. Carregar `secondary_skills` conforme o trabalho exigir.
4. Ao resolver a issue, atualizar `stats.json`:
   - `issues[<n>].status`: `open|in_progress|blocked` → `resolved`
   - `issues[<n>].resolved_at`: ISO 8601 UTC
   - `issues[<n>].resolved_skill_used`: a skill que **realmente** guiou
   - `issues[<n>].pr_url`: link do PR
   - `issues[<n>].notes`: aprendizados, desvios, blockers
   - `summary`: decrementar contador de origem, incrementar `resolved` e `skills_used_count[skill]`

## Comandos

```bash
# Instalar dependências
pip install -r requirements.txt

# Coletar restaurantes
python src/collect.py

# Gerar relatório
python src/analyze.py

# Rodar testes
pytest tests/

# Criar e trocar para branch de feature
FEATURE=2026-07-08-piloto-segmentacao-trafego-pago
git checkout -b feature/$FEATURE develop
```

## CI/CD

```
feature/*  → PR → CI (lint + testes)
      ↓ merge
develop    → PR → staging
      ↓ merge
main       → produção
```

- Nenhum deploy automático configurado neste projeto piloto.
- Testes via GitHub Actions devem rodar `pytest tests/`.

## Histórico de planos

- `docs/plans/2026-07-08-piloto-segmentacao-trafego-pago/` — Piloto de Inteligência de Mercado para Segmentação de Tráfego Pago — Restaurantes em João Pessoa.

## Regras Não-Negociáveis

- Nunca versionar `.env`.
- Nunca fazer push direto em `main` ou `develop`.
- Toda feature deve ter branch `feature/<slug>` partindo de `develop`.
- Toda alteração de código deve passar por PR para `develop`.
