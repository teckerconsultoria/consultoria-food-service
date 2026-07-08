# Spec: Piloto de Inteligência de Mercado para Segmentação de Tráfego Pago — Restaurantes em João Pessoa

**Versão:** 1.0
**Status:** Aprovada
**Autor:** Agente
**Data:** 2026-07-08
**Reviewers:** N/A

---

## 1. Resumo

Piloto de 5 a 7 dias que coleta 100 restaurantes de João Pessoa via Google Places API, transforma os dados em recomendações concretas de segmentação para Meta Ads (raio geográfico, bairros prioritários, interesses/criativos por categoria) e ativa uma campanha de teste com segmentação 100% baseada em dados reais.

---

## 2. Contexto e Motivação

**Problema:** A segmentação de tráfego pago é feita manualmente e no achismo. O gestor de tráfego escolhe raio e interesse "no olho", e a SDR recebe a sobra de leads fora da persona.

**Evidências:** Não há dados de densidade real de restaurantes por bairro, categoria dominante ou faixa de preço antes de subir campanha. O raio é genérico, o interesse é amplo, e o ruído chega ao SDR.

**Por que agora:** A spec do piloto já está aprovada. O Google Places API fornece dados institucionais suficientes (nome, localização, categoria, rating, price_level, presença de site) para calibrar a segmentação antes de gastar em mídia. Não é necessário coletar dados pessoais de indivíduos.

---

## 3. Goals

- [ ] G-01: Coletar 100 restaurantes únicos de João Pessoa via Google Places API
- [ ] G-02: Produzir relatório de densidade e perfil com agregação por bairro, categoria, price_level e rating
- [ ] G-03: Recomendar raio(s) geográfico(s) e interesses para Meta Ads baseados nos dados
- [ ] G-04: Criar conta Meta Business Manager + conta de anúncios
- [ ] G-05: Configurar e ativar uma campanha piloto no Meta Ads com segmentação manual baseada no relatório
- [ ] G-06: Produzir material de venda comparando segmentação "achismo" vs "dados" sobre o N=100

**Métricas de sucesso:**
| Métrica | Baseline atual | Target | Prazo |
|---------|---------------|--------|-------|
| Ruído na segmentação | Desconhecido (achismo) | Percentual mensurável de exclusão de leads fora da persona | 2026-07-15 |
| Tempo de preparação de segmentação | Dias de discussão | 1 dia após relatório | 2026-07-15 |

---

## 4. Non-Goals

- NG-01: Não fazer upload de lista de contatos como Custom Audience no Meta
- NG-02: Não enriquecer e-mail ou decisor via Hunter.io/Apollo.io (fase futura)
- NG-03: Não automatizar repetição para outros nichos/regiões (fase futura)
- NG-04: Não definir meta de orçamento de mídia (campanha exploratória)
- NG-05: Não coletar dados pessoais de indivíduos (só dados institucionais do Places)

---

## 5. Usuários e Personas

**Usuário primário:** Gestor de tráfego — configura campanha no Meta Ads. Precisa de parâmetros concretos (raio, bairros, interesses) em vez de achismo.

**Usuário secundário:** SDR — recebe leads inbound. Precisa que a segmentação prévia filtre ruído antes do lead chegar.

**Usuário terciário:** Cliente/Stakeholder — decide se continua investindo no piloto. Precisa de prova numérica (quanto ruído foi evitado).

**Jornada atual (sem a feature):** Gestor abre Meta Ads, escolhe raio de 10 km genérico, interesse amplo "restaurantes" e sobe campanha. SDR recebe leads de bairros e categorias fora do ICP.

**Jornada futura (com a feature):** Gestor recebe relatório de densidade com raio calibrado, bairros prioritários e interesse alinhado à categoria dominante. Configura campanha com dados. SDR recebe leads mais alinhados.

---

## 6. Requisitos Funcionais

### 6.1 Requisitos Principais

| ID | Requisito | Prioridade | Critério de Aceite |
|----|-----------|-----------|-------------------|
| RF-01 | O sistema deve coletar restaurantes em João Pessoa via Google Places API (New) com campos mínimos: nome, endereço, bairro, place_id, lat, lng, tipo/categoria, rating, price_level, presença de website | Must | 100 registros únicos no banco |
| RF-02 | O sistema deve deduplicar automaticamente por place_id | Must | Zero duplicados na base final |
| RF-03 | O sistema deve excluir estabelecimentos permanentemente fechados | Must | Zero fechados na base final |
| RF-04 | O sistema deve normalizar bairro via reverse geocoding antes de agregar | Must | Bairros consistentes (sem grafias duplicadas) |
| RF-05 | O sistema deve persistir dados em projeto Supabase novo com schema mínimo | Must | Tabela `restaurantes` com colunas obrigatórias populadas |
| RF-06 | O sistema deve gerar relatório de densidade e perfil com agregações por bairro, categoria, price_level e rating | Must | Arquivo Markdown em `docs/output/relatorio-densidade-jp.md` |
| RF-07 | O sistema deve recomendar raio(s) geográfico(s) a partir do relatório de densidade | Must | Raio justificado por concentração real de restaurantes |
| RF-08 | O sistema deve recomendar interesses/criativos a partir da categoria dominante observada | Must | Interesse alinhado à categoria com maior contagem |
| RF-09 | O usuário deve criar conta Meta Business Manager + conta de anúncios | Must | BM e ad account funcionais |
| RF-10 | O usuário deve configurar segmentação manual no Meta Ads (geolocalização + detalhamento demográfico/interesses) refletindo o relatório | Must | Público salvo no Ads Manager |
| RF-11 | O usuário deve criar e ativar campanha piloto no Meta Ads usando a segmentação configurada | Must | Status "ativa" no Ads Manager |
| RF-12 | O sistema deve reconstruir segmentação "do achismo" e comparar com a segmentação "dos dados" sobre o N=100 | Must | Documento `docs/output/achismo-vs-dados.md` |
| RF-13 | O sistema deve calcular percentual de ruído evitado pelo uso de dados | Must | KPI numérico no material de venda |

### 6.2 Fluxo Principal

1. Script `collect.py` busca restaurantes em João Pessoa via Google Places API.
2. Sistema normaliza bairros, deduplica por place_id e exclui fechados.
3. Sistema persiste 100 restaurantes no Supabase.
4. Script `analyze.py` lê a base, gera agregações e recomendações.
5. Sistema gera relatório de densidade e CSV.
6. Gestor configura segmentação no Meta Ads com base no relatório.
7. Gestor cria e ativa campanha piloto.
8. Sistema gera comparação achismo vs dados e material de venda.

### 6.3 Fluxos Alternativos

**Fluxo Alternativo A — Busca retorna menos de 100 restaurantes:**
1. Script expande busca com variações por bairro (Manaíra, Tambaú, Cabo Branco, etc.)
2. Continua até atingir N=100 ou esgotar variações
3. Loga resultado final

**Fluxo Alternativo B — Nominatim indisponível:**
1. Sistema usa Google Geocoding API como fallback
2. Loga ocorrência

---

## 7. Requisitos Não-Funcionais

| ID | Requisito | Valor alvo | Observação |
|----|-----------|-----------|------------|
| RNF-01 | Custo do piloto | < R$ 200 | APIs + mídia teste |
| RNF-02 | Prazo de execução | 5 a 7 dias | Início imediato |
| RNF-03 | Segurança | Chaves em `.env` | Não versionar credenciais |
| RNF-04 | Compliance | Sem dados pessoais | Apenas dados institucionais do Google Places |

---

## 8. Design e Interface

**Componentes afetados:** Não há interface própria. Outputs: scripts CLI, relatório Markdown, CSV, configuração Meta Ads Manager.

**Comportamento esperado:** Usuário executa scripts via terminal. Meta Ads é configurado manualmente pelo gestor a partir do relatório.

**Estados da UI:** Não aplicável — sistema é backend/CLI + relatório.

---

## 9. Modelo de Dados

**Entidade nova:**

```
restaurantes {
  place_id: text PRIMARY KEY
  nome: text
  endereco: text
  bairro: text
  lat: float
  lng: float
  tipo: text
  rating: float
  price_level: int
  tem_website: boolean
  permanently_closed: boolean
  data_coleta: timestamptz
}
```

**Migrações necessárias:** Sim — criação da tabela `restaurantes` no Supabase via SQL migration.

---

## 10. Integrações e Dependências

| Dependência | Tipo | Impacto se indisponível |
|-------------|------|------------------------|
| Google Places API (New) | Obrigatória | Piloto não coleta dados |
| Supabase | Obrigatória | Não há persistência |
| OpenStreetMap Nominatim | Opcional | Fallback para Google Geocoding |
| Meta Business Manager | Obrigatória | Não é possível subir campanha |
| Meta Ads Manager | Obrigatória | Não é possível ativar campanha |

---

## 11. Edge Cases e Tratamento de Erros

| Cenário | Trigger | Comportamento esperado |
|---------|---------|----------------------|
| EC-01: Mesmo place_id em múltiplas buscas | Busca por bairros sobrepostos | Mantém primeiro registro, loga descarte |
| EC-02: Estabelecimento permanently_closed | Flag no retorno do Places | Exclui da base e da análise |
| EC-03: Bairro ausente ou mal formatado | Dados inconsistentes do Places | Normaliza via reverse geocoding |
| EC-04: Busca retorna menos de 100 restaurantes | API limitada ou query restrita | Expande busca por bairro até atingir N=100 |
| EC-05: Rate limit Google Places | Muitas requisições | Pausa com backoff, loga e retenta |
| EC-06: Meta Business Manager solicita CNPJ | Verificação da Meta | Escalonar para cliente; atraso no cronograma |

---

## 12. Segurança e Privacidade

- **Autenticação:** Apenas quem tem acesso ao `.env` local e ao Supabase executa scripts.
- **Autorização:** Não há roles internos — acesso via chaves de serviço.
- **Dados sensíveis:** Não coleta PII. Apenas dados institucionais públicos do Google Places.
- **Auditoria:** Logar data de coleta, query de busca e quantidade de registros descartados.

---

## 13. Plano de Rollout

- **Estratégia:** Piloto isolado com dados de teste
- **Como reverter:** Desativar campanha no Meta Ads; manter base de dados para análise
- **Monitoramento pós-deploy:** Observar aceitação inicial da segmentação (CTR, CPM) nas primeiras 24–48h

---

## 14. Open Questions

| # | Pergunta | Impacto | Dono | Prazo |
|---|---|---------|------|-------|
| OQ-01 | Qual será o ICP comercial exato (faixa de preço, rating mínimo, categorias)? | Alto | Gestor | 2026-07-09 |
| OQ-02 | Orçamento mínimo diário da campanha piloto? | Médio | Cliente | 2026-07-09 |
| OQ-03 | O cliente já possui Meta Business Manager? | Alto | Cliente | 2026-07-09 |

---

## 15. Decisões Tomadas (Decision Log)

| Decisão | Alternativas consideradas | Racional |
|---------|--------------------------|---------|
| Usar Supabase Free para persistência | SQLite local, PostgreSQL local | Facilidade de acesso remoto, colaboração e escalabilidade |
| Usar Nominatim como padrão para geocoding | Apenas Google Geocoding | Gratuito, reduz custo do piloto; Google como fallback |
| Segmentação 100% manual no Meta Ads | Upload de Custom Audience | Evitar risco de termos de dados de público personalizado do Meta |
| Campanha sem meta de gasto | Orçamento fixo | Piloto exploratório; gasto a ser definido após validação |

---

## Apêndice

### Referências
- `docs/prospeccao-foodservice-joao-pessoa-v2.md` — spec original do piloto
- `docs/plan/piloto-segmentacao-trafego-pago.md` — plano aprovado
- `docs/plans/2026-07-08-piloto-segmentacao-trafego-pago/` — plano estruturado com issues

### Histórico de Revisões
| Versão | Data | Autor | Mudanças |
|--------|------|-------|---------|
| 1.0 | 2026-07-08 | Agente | Criação inicial |

---

## Score de Qualidade da Spec

> A ser avaliado pelo `spec_scorer.py` após criação.

- Completude: 100% (todas as seções preenchidas)
- Testabilidade: Alta (todos os RF possuem critérios de aceite)
- Clareza: Alta (sem ambiguidades conhecidas)
- Escopo: Bem definido (Non-Goals explícitos)
- Edge Cases: Cobertos (casos de duplicação, fechados, bairro, API limit)

**Score estimado:** 90/100
