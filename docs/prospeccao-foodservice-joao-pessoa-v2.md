# Spec: Piloto de Inteligência de Mercado para Segmentação de Tráfego Pago — Restaurantes em João Pessoa

## Objetivo

Validar um pipeline que coleta restaurantes em João Pessoa via Google Places e transforma esses dados em **parâmetros concretos de segmentação manual** para uma campanha de tráfego pago no Meta Ads (raio geográfico, bairros prioritários, interesses/criativos por categoria de estabelecimento) — sem fazer upload de nenhum dado de contato como Custom Audience.

Resultado que importa: sair de "lista de estabelecimentos" para "campanha ativa rodando com segmentação geográfica e por interesse definida por dados reais", e produzir um relatório de densidade/perfil que sirva de base para as próximas iterações (outros nichos/regiões).

## Requisitos

**Obrigatório:**

1. **Coleta de leads** via MCP `mcp-google-map` (Google Places API), buscando restaurantes em João Pessoa. Campos por lead: nome, endereço, bairro, `place_id`, latitude/longitude, tipo/categoria, rating, `price_level`, presença de website (sim/não, sem necessidade de extrair o e-mail).
2. **Deduplicação automática** por `place_id` — se o mesmo estabelecimento aparecer em buscas diferentes (ex: buscas por bairro sobrepostas), mantém um único registro.
3. **Exclusão de estabelecimentos permanentemente fechados** (sinalizado pelo Google Places) — não faz sentido incluir na análise de segmentação.
4. **Armazenamento** em um projeto Supabase novo (schema com pelo menos: place_id, nome, endereço, bairro, lat, long, tipo, rating, price_level, tem_website, data_coleta).
5. **Análise de densidade e perfil**: agregação por bairro (contagem de estabelecimentos), por categoria (restaurante/pizzaria/hamburgueria/etc.), por faixa de preço e por rating — usada para recomendar raio(s) geográfico(s) e prioridades de segmentação.
6. **Criação de conta** Meta Business Manager + conta de anúncios (única conta necessária neste piloto — Hunter.io e Apollo.io saem do escopo obrigatório, ver abaixo).
7. **Configuração de segmentação manual no Meta Ads** com base na análise do item 5: raio/bairros definidos pelos dados de densidade, e detalhamento demográfico/interesses definidos pelo perfil dominante de categoria observado.
8. **Criação e ativação de uma campanha** no Meta Ads usando essa segmentação manual — sem meta de orçamento definida, campanha de teste exploratório.

**Fora do escopo obrigatório deste piloto (reservado para fase futura):**
- Enriquecimento de e-mail via Hunter.io e de decisor via Apollo.io — só fazem sentido numa fase posterior de qualificação de leads *inbound* gerados pela própria campanha (quem responde ao anúncio), não como insumo de segmentação.
- Upload de Custom Audience / Lookalike Audience a partir de dados coletados — removido por risco de violar os Termos de Dados de Público Personalizado do Meta (dados coletados publicamente, sem relação prévia com os titulares, não têm base clara para esse uso específico).
- Automatizar a repetição do pipeline para outros nichos/regiões.

## Restrições

- **Fonte de dados:** apenas dados institucionais e agregados do Google Places (nome do estabelecimento, localização, categoria, rating, presença de site). Nenhum dado pessoal de indivíduo é coletado neste piloto.
- **Sem orçamento de mídia definido** — a campanha é um teste exploratório, sem meta de gasto diário/total.
- **Escopo geográfico:** apenas João Pessoa, apenas restaurantes, para este piloto.
- **Volume:** lote de teste de 100 estabelecimentos (N=100).
- **Nenhum dado é enviado ao Meta como lista de contatos** — a segmentação é 100% nativa da plataforma (geolocalização + detalhamento demográfico/interesses), configurada manualmente com base na análise dos dados coletados.

## Casos extremos a tratar

| Caso | Comportamento esperado |
|---|---|
| Mesmo `place_id` retornado em buscas diferentes | Deduplicado automaticamente, mantém um único registro |
| Estabelecimento permanentemente fechado (sinalizado pelo Google Places) | Excluído da base (não entra na análise de densidade) |
| Estabelecimento sem website | Mantido na base (é só um campo informativo de maturidade digital, não critério de corte) |
| Bairro ausente/mal formatado no retorno do Places | Normalizar via reverse geocoding antes de agregar (evitar bairros duplicados por grafia, como já ocorreu na base CNPJá) |

## Definição de "Concluído"

1. Base final contém **100 restaurantes únicos** de João Pessoa (N=100), sem duplicados por `place_id`, sem estabelecimentos permanentemente fechados.
2. **Relatório de densidade e perfil produzido**, com: contagem por bairro, contagem por categoria, distribuição de `price_level` e rating.
3. **Raio(s) geográfico(s) recomendado(s)** definidos a partir do relatório (ex: concentração em Manaíra/Tambaú/Cabo Branco → raio prioritário nessa área).
4. Conta Meta Business Manager + conta de anúncios criada e funcional.
5. Segmentação manual configurada no Meta Ads Manager (geolocalização + detalhamento demográfico/interesses) refletindo o relatório do item 2.
6. Existe **uma campanha ativa** no Meta Ads utilizando essa segmentação — status "ativa", independentemente do valor de gasto.
