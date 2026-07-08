# Spec: Piloto de Inteligência de Mercado para Segmentação de Tráfego Pago — Restaurantes em João Pessoa

**Versão:** 1.0
**Status:** Aprovada
**Autor:** Agente
**Data:** 2026-07-08

---

## 1. Resumo

Executar um piloto de 5 a 7 dias que colete 100 restaurantes de João Pessoa via Google Places API, transforme os dados em recomendações concretas de segmentação para Meta Ads (raio geográfico, bairros prioritários, interesses/criativos por categoria) e ative uma campanha de teste com segmentação 100% baseada em dados reais.

**Resultado que importa:** sair de "lista de estabelecimentos" para "campanha ativa rodando com segmentação geográfica e por interesse definida por dados reais", e produzir um relatório de densidade/perfil que sirva de base para as próximas iterações.

---

## 2. Contexto e Motivação

**Problema raiz:** A segmentação de tráfego pago é feita manualmente e no achismo. O gestor de tráfego escolhe raio e interesse "no olho", e a SDR recebe a sobra de leads fora da persona.

**Evidências:** Não há dados de densidade real de restaurantes por bairro, categoria dominante ou faixa de preço antes de subir campanha. O raio é genérico, o interesse é amplo, e o ruído chega ao SDR.

**Por que agora:** A spec do piloto já está aprovada. O Google Places API fornece dados institucionais suficientes (nome, localização, categoria, rating, price_level, presença de site) para calibrar a segmentação antes de gastar em mídia. Não é necessário coletar dados pessoais de indivíduos.

---

## 3. Goals

- G-01: Coletar 100 restaurantes únicos de João Pessoa via Google Places API
- G-02: Produzir relatório de densidade e perfil com agregação por bairro, categoria, price_level e rating
- G-03: Recomendar raio(s) geográfico(s) e interesses para Meta Ads baseados nos dados
- G-04: Criar conta Meta Business Manager + conta de anúncios
- G-05: Configurar e ativar uma campanha piloto no Meta Ads com segmentação manual baseada no relatório
- G-06: Produzir material de venda comparando segmentação "achismo" vs "dados" sobre o N=100

---

## 4. Non-Goals

- NG-01: Não fazer upload de lista de contatos como Custom Audience no Meta
- NG-02: Não enriquecer e-mail ou decisor via Hunter.io/Apollo.io (fase futura)
- NG-03: Não automatizar repetição para outros nichos/regiões (fase futura)
- NG-04: Não definir meta de orçamento de mídia (campanha exploratória)
- NG-05: Não coletar dados pessoais de indivíduos (só dados institucionais do Places)

---

## 5. Usuários e Personas

**Gestor de tráfego:** Configura campanha no Meta Ads. Precisa de parâmetros concretos (raio, bairros, interesses) em vez de achismo.

**SDR:** Recebe leads inbound. Precisa que a segmentação prévia filtre ruído antes do lead chegar.

**Cliente/Stakeholder:** Decide se continua investindo no piloto. Precisa de prova numérica (quanto ruído foi evitado).

---

## 6. Requisitos Funcionais

### 6.1 Requisitos Principais

| ID | Requisito | Prio | Critério de Aceite |
|----|-----------|------|-------------------|
| RF-01 | Coletar restaurantes em João Pessoa via Google Places API (New) com campos mínimos: nome, endereço, bairro, place_id, lat, lng, tipo/categoria, rating, price_level, presença de website | Must | 100 registros únicos no banco |
| RF-02 | Deduplicar automaticamente por place_id | Must | Zero duplicados na base final |
| RF-03 | Excluir estabelecimentos permanentemente fechados | Must | Zero fechados na base final |
| RF-04 | Normalizar bairro via reverse geocoding antes de agregar | Must | Bairros consistentes (sem grafias duplicadas) |
| RF-05 | Persistir dados em projeto Supabase novo com schema mínimo | Must | Tabela `restaurantes` com colunas obrigatórias populadas |
| RF-06 | Gerar relatório de densidade e perfil com agregações por bairro, categoria, price_level e rating | Must | Arquivo Markdown em `docs/output/relatorio-densidade-jp.md` |
| RF-07 | Recomendar raio(s) geográfico(s) a partir do relatório de densidade | Must | Raio justificado por concentração real de restaurantes |
| RF-08 | Recomendar interesses/criativos a partir da categoria dominante observada | Must | Interesse alinhado à categoria com maior contagem |
| RF-09 | Criar conta Meta Business Manager + conta de anúncios | Must | BM e ad account funcionais |
| RF-10 | Configurar segmentação manual no Meta Ads (geolocalização + detalhamento demográfico/interesses) refletindo o relatório | Must | Público salvo no Ads Manager |
| RF-11 | Criar e ativar campanha piloto no Meta Ads usando a segmentação configurada | Must | Status "ativa" no Ads Manager |
| RF-12 | Reconstruir segmentação "do achismo" e comparar com a segmentação "dos dados" sobre o N=100 | Must | Documento `docs/output/achismo-vs-dados.md` |
| RF-13 | Calcular percentual de ruído evitado pelo uso de dados | Must | KPI numérico no material de venda |

### 6.2 Casos Extremos

| Caso | Comportamento esperado |
|---|---|
| Mesmo place_id retornado em buscas diferentes | Deduplicado, mantém um único registro |
| Estabelecimento permanentemente fechado | Excluído da base |
| Estabelecimento sem website | Mantido na base (campo informativo) |
| Bairro ausente/mal formatado | Normalizado via reverse geocoding |
| Busca retornar menos de 100 restaurantes | Expandir com variações de query por bairro até atingir N=100 |
| Límite de API do Google Places | Pausar, logar, continuar após delay |

---

## 7. Design Técnico

### 7.1 Arquitetura

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

### 7.2 Stack

| Camada | Ferramenta |
|---|---|
| Coleta | Python 3.11 + Google Places API (New) + `requests` |
| Normalização de bairro | OpenStreetMap Nominatim (gratuito) ou Google Geocoding API |
| Banco | Supabase (plano Free) — PostgreSQL |
| Análise | Python + Pandas + SQLAlchemy |
| Relatório | Markdown + CSV |
| Campanha | Meta Business Manager + Meta Ads Manager |
| Testes | `pytest` (scripts Python) |

### 7.3 Estrutura de Arquivos

```
consultoria-food-service/
├── .env                              # não versionar
├── .gitignore
├── .claude/
│   └── settings.json
├── docs/
│   ├── prospeccao-foodservice-joao-pessoa-v2.md
│   ├── plans/
│   │   └── 2026-07-08-piloto-segmentacao-trafego-pago/
│   │       ├── README.md
│   │       ├── spec.md
│   │       └── stats.json
│   └── output/
│       ├── relatorio-densidade-jp.md
│       ├── base-100-restaurantes.csv
│       ├── achismo-vs-dados.md
│       └── pitch-gestor.md
├── src/
│   ├── __init__.py
│   ├── collect.py
│   ├── models.py
│   ├── geocode.py
│   ├── db.py
│   ├── analyze.py
│   └── config.py
├── scripts/
│   ├── run_collect.sh
│   └── run_analyze.sh
└── tests/
    ├── test_collect.py
    ├── test_geocode.py
    └── test_analyze.py
```

### 7.4 Modelo de Dados

Tabela `restaurantes`:

| Coluna | Tipo | Descrição |
|---|---|---|
| place_id | text PRIMARY KEY | ID único do Google Places |
| nome | text | Nome do estabelecimento |
| endereco | text | Endereço completo |
| bairro | text | Bairro normalizado |
| lat | float | Latitude |
| lng | float | Longitude |
| tipo | text | Categoria principal (restaurant, pizza, etc.) |
| rating | float | Avaliação média |
| price_level | int | Faixa de preço (0-4) |
| tem_website | boolean | Possui website |
| permanently_closed | boolean | Fechado permanentemente |
| data_coleta | timestamptz | Data da coleta |

### 7.5 Configuração de Variáveis de Ambiente

Arquivo `.env` (não versionar):

```bash
GOOGLE_PLACES_API_KEY=<chave>
SUPABASE_URL=<url>
SUPABASE_SERVICE_ROLE_KEY=<chave>
# Opcional: fallback para geocoding
GOOGLE_GEOCODING_API_KEY=<chave>
```

---

## 8. Plano de Implementação

### Issue 1: Setup de contas e ambiente
- Criar projeto Google Cloud e ativar Google Places API
- Criar projeto Supabase novo
- Criar `.env` local com chaves
- Criar `.gitignore` para `.env`, `.firecrawl/`, `__pycache__`
- Criar estrutura inicial de pastas (`src/`, `tests/`, `scripts/`, `docs/output/`)

### Issue 2: Coleta e persistência de dados
- Criar `src/models.py` com Pydantic/dataclass
- Criar `src/db.py` para conexão Supabase
- Criar `src/geocode.py` para normalização de bairro
- Criar `src/collect.py` para busca no Google Places
- Implementar deduplicação por place_id
- Implementar exclusão de fechados
- Rodar coleta até atingir N=100
- Persistir no Supabase

### Issue 3: Análise e relatório de densidade
- Criar `src/analyze.py`
- Agregar por bairro, categoria, price_level, rating
- Calcular raio(s) recomendado(s)
- Identificar categoria dominante e interesses
- Gerar `docs/output/relatorio-densidade-jp.md`
- Gerar `docs/output/base-100-restaurantes.csv`

### Issue 4: Meta Ads e campanha ativa
- Criar/validar Meta Business Manager
- Criar conta de anúncios
- Configurar segmentação geográfica baseada no relatório
- Configurar interesses/detalhamento demográfico baseado na categoria dominante
- Criar criativo e campanha piloto
- Ativar campanha com orçamento mínimo

### Issue 5: Material de venda (achismo vs dados)
- Reconstruir segmentação "do achismo" com parâmetros típicos
- Aplicar ambos os filtros sobre os 100 restaurantes
- Calcular percentual de ruído evitado
- Gerar `docs/output/achismo-vs-dados.md`
- Gerar `docs/output/pitch-gestor.md`

---

## 9. Dependências e Bloqueios

| Dependência | Quem resolve | Risco se não resolver |
|---|---|---|
| Cartão de crédito para Google Cloud billing | Cliente | Google Places API não ativa |
| Cartão para Meta Ads (mínimo de gasto) | Cliente | Campanha não sobe |
| CNPJ para Meta Business Manager (se solicitado) | Cliente | Atraso na criação da conta |
| Definição do ICP comercial (preço, categoria, rating) | Gestor | Filtros de segmentação errados |
| Acesso ao Meta Business Manager do cliente | Cliente | Não dá para configurar campanha |

---

## 10. Cronograma

| Dia | Foco | Entrega |
|---|---|---|
| 1 | Setup de contas e ambiente | Contas prontas, `.env` configurado, estrutura criada |
| 2 | Coleta de dados | 100 restaurantes no Supabase |
| 3 | Análise e relatório | Relatório de densidade pronto |
| 4 | Meta Ads | Campanha ativa |
| 5 | Material de venda | Pitch achismo vs dados |
| 6-7 | Buffer | Ajustes, reunião, documentação |

---

## 11. Critérios de Sucesso

1. Base final com 100 restaurantes únicos, sem duplicados, sem fechados.
2. Relatório de densidade publicado em `docs/output/relatorio-densidade-jp.md`.
3. Raio(s) e interesses recomendados extraídos dos dados.
4. Campanha ativa no Meta Ads com segmentação baseada no relatório.
5. Material de venda mostrando percentual de ruído evitado pelo uso de dados.

---

## 12. Custo Estimado

| Item | Custo estimado |
|---|---|
| Google Places API (New) | $5–15 por 100 estabelecimentos |
| Supabase (Free tier) | Grátis até 500 MB |
| Google Geocoding (fallback) | ~$5 |
| Meta Ads (teste) | R$ 5–20/dia, mínimo a definir |
| **Total do piloto** | **R$ 50–200** |

---

## 13. Próximos Passos

1. Validar esta spec com o cliente/gestor.
2. Coletar acesso e chaves (Google Cloud, Supabase, Meta BM).
3. Escolher modo de execução: subagentes nesta sessão ou sessão paralela com `executing-plans`.

---

## Skills Necessárias

- `backend-patterns` — arquitetura da camada de dados e Supabase
- `python-patterns` — scripts Python idiomáticos
- `api-design` — consumo de Google Places API e estrutura de dados
- `analytics-tracking` — configuração de campanha e segmentação no Meta Ads
- `prd-elaborator` — caso precise refinar a spec
- `writing-plans` — para decompor em tarefas executáveis
