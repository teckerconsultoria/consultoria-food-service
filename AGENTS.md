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

## Convenções

- Python 3.11+.
- Use `requirements.txt` para dependências.
- Sempre salvar outputs em `docs/output/`.
- Nunca versionar `.env` nem dados brutos.
- Para APIs, usar `.env` e `src/config.py` para leitura.

## Plans & Skills Tracking

Features com plano persistido ficam em `docs/plans/YYYY-MM-DD-<slug>/`:

- `stats.json` — fonte da verdade: skill primária e secundária por issue, status, dependências, links.
- `README.md` — workflow do agente e referência rápida das skills.
- `spec.md` — especificação completa da feature.

**Ao trabalhar em qualquer issue de uma feature com plan:**

1. Identificar a feature pela branch ou pelo diretório em `docs/plans/`.
2. Carregar a `primary_skill` da issue via `Skill()` tool.
3. Carregar `secondary_skills` conforme o trabalho exigir.
4. Ao resolver a issue, atualizar `stats.json`:
   - `issues[<n>].status`: `open|in_progress|blocked` → `resolved`
   - `issues[<n>].resolved_at`: ISO 8601 UTC
   - `issues[<n>].resolved_skill_used`: a skill que **realmente** guiou
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
```

## Histórico de planos

- `docs/plans/2026-07-08-piloto-segmentacao-trafego-pago/` — Piloto de Inteligência de Mercado para Segmentação de Tráfego Pago — Restaurantes em João Pessoa.
