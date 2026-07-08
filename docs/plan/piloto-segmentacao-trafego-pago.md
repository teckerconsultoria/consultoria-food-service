# Plano Aprovado: Piloto de Inteligência de Mercado para Segmentação de Tráfego Pago — Restaurantes em João Pessoa

**Status:** Aprovado
**Data:** 2026-07-08

## Resumo Executivo

Piloto de 5 a 7 dias para coletar 100 restaurantes de João Pessoa via Google Places API, transformar dados em recomendações de segmentação para Meta Ads (raio, bairros, interesses) e ativar uma campanha de teste com segmentação 100% baseada em dados reais.

## Problema que Resolve

Segmentação de tráfego pago feita no achismo: gestor escolhe raio e interesse "no olho", SDR recebe leads fora da persona. A solução usa dados reais de densidade e perfil para calibrar a segmentação antes da campanha subir.

## Entregáveis

1. Base de 100 restaurantes únicos no Supabase.
2. Relatório de densidade e perfil (`docs/output/relatorio-densidade-jp.md`).
3. Recomendações de raio e interesses para Meta Ads.
4. Conta Meta Business Manager + conta de anúncios criada.
5. Campanha piloto ativa no Meta Ads.
6. Material de venda: comparação achismo vs dados (`docs/output/achismo-vs-dados.md` + `pitch-gestor.md`).

## Atividades

| # | Atividade | Skill sugerida | Saída |
|---|---|---|---|
| 1 | Setup de contas e ambiente | `backend-patterns` | `.env`, estrutura, contas |
| 2 | Coleta e persistência de dados | `python-patterns` + `api-design` | 100 restaurantes no Supabase |
| 3 | Análise e relatório de densidade | `python-patterns` | Relatório Markdown + CSV |
| 4 | Meta Ads e campanha ativa | `analytics-tracking` | Campanha ativa |
| 5 | Material de venda (achismo vs dados) | `copywriting` | Pitch comercial |

## Custo Estimado

R$ 50–200 (Google Places API + teste de mídia Meta Ads).

## Cronograma

| Dia | Foco | Entrega |
|---|---|---|
| 1 | Setup | Contas e ambiente |
| 2 | Coleta | 100 restaurantes |
| 3 | Análise | Relatório de densidade |
| 4 | Meta Ads | Campanha ativa |
| 5 | Venda | Material achismo vs dados |
| 6-7 | Buffer | Ajustes e validação |

## Dependências Críticas

- Cartão de crédito para Google Cloud billing (cliente)
- Cartão para Meta Ads (cliente)
- Acesso ao Meta Business Manager (cliente)
- Definição do ICP comercial (gestor)

## Próximos Passos

1. Criar SDD spec via skill `sdd-spec`.
2. Definir skills de cada atividade via skill `find-skill`.
3. Criar issues no GitHub via skill `sdd-to-github`.
