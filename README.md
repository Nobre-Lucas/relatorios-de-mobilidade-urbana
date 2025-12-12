# RelatoriosMobilidadeBrasil — Auditor de Mobilidade Urbana

Documento contendo arquitetura técnica, backlog priorizado, estrutura de pastas, especificação de APIs, modelo de dados, critérios de validação e plano de testes automatizados (aceitação, integração, regressão).

---

## 0. Problema

O direito ao transporte é um direito social previsto pela constituição e que tem influência sobre outros direitos, como o de ir e vir. Entretanto, pode ser observar que em Belém do Pará um transporte público de qualidade é um sonho distante para a maior parte da população paraense.

Não faltam aumentos de tarifa, ônibus sucateados, motoristas e cobradores mal treinados e sem treinamento, estressados com as péssimas condições de trabalho que são submetidos. Há pouco tempo, inclusive, nos "geladões", ônibus com ar-condicionados, os motoristas agora exercem também as funções de cobradores, diminuindo a velocidade do transporte para os passageiros e para motoristas de carros pessoais também, além de acumular mais uma carga de estresse sobre o trabalhador.

Nesse contexto, faltam ferramentas apropriadas para que os cidadãos e entidades civís interessadas possam monitorar a qualidade do transporte na região, como agregadores de notícias e painéis de inteligência de dados.

## 1. Visão geral

**Objetivo:** analisar comunicados, notícias e relatórios públicos sobre transporte urbano e gerar laudos objetivos e auditáveis que avaliem impacto social, acessibilidade e riscos para trabalhadores e populações periféricas.

**Princípios:** objetividade, regras explícitas, auditabilidade, testabilidade, objetividade acima de criatividade.

**Entrega mínima:** API que recebe texto/PDF/HTML e retorna laudo JSON + interface Streamlit simples + armazenamento de logs (Postgres).

---

## 2. Stack sugerido

- Backend principal: **Spring Boot (Java)** — endpoints de ingestão, auditoria, e gestão de regras.
- Serviço de IA / agente: **LangGraph** em Python (adapter) + **Ollama (on-prem)** para inferência LLM local.
- Indexação leve (opcional): **PGVector** (Postgres + extensão pgvector) para storing snippets e buscar contexto histórico.
- Ingestão de documentos: **Apache Tika** (ou python-docx + pdfminer) para extrair texto.
- Frontend: **Streamlit** (Python) para UI minimalista e testes manuais.
- Banco de dados: **Postgres** (dados e pgvector); para testes usar Docker Compose.
- Testes: **pytest** + **pytest-bdd** (cenários de aceitação), **JUnit** para testes de integração do Spring Boot.
- CI: GitHub Actions (linters, build, tests, container build).

---

## 3. Arquitetura (alto nível)

```
[Streamlit UI] <---> [API Gateway (Spring Boot)] <---> [Agent Service (LangGraph Python)]
                                           |                           |
                                           |                           +--> [Ollama (local LLM)]
                                           +--> [Postgres + pgvector]
                                           +--> [Audit DB / Logs]
```

**Fluxo:**
1. Usuário envia texto ou arquivo via UI ou curl para Spring Boot.
2. Spring Boot salva raw input no Audit DB, extrai texto (se necessário) e chama Agent Service.
3. Agent Service realiza extração de entidades (tarifa, bairros, horários), aplica heurísticas, consulta PGVector se necessário, chama Ollama para interpretar trechos ambíguos e retorna laudo estruturado.
4. Spring Boot valida laudo contra regras duras (ex.: presença de campo `tarifa` como número quando detectado), armazena resultado e expõe via API.

---

## 4. Módulos e responsabilidades

- **spring-api/**
  - endpoints: `/analyze`, `/audit/log`, `/audit/report`, `/rules`.
  - responsabilidades: receber input, persistir raw, orquestrar chamada ao agent, validação final, retornar response, autenticação básica (token).

- **agent-service/** (python)
  - endpoint interno (gRPC/HTTP) consumido por spring-api.
  - responsabilidades: limpeza do texto, extração regex, chamada a Ollama para interpretação, aplicação de heurísticas, montagem do laudo JSON.

- **streamlit-ui/**
  - app de demo: upload de arquivo, campo texto, visualização do laudo e logs.

- **infrastructure/**
  - docker-compose para Postgres (+pgvector), Ollama (se disponível), reverse proxy, serviços.

- **tests/**
  - acceptance/ (pytest-bdd scenarios)
  - integration/ (JUnit + pytest integration tests)

---

## 5. Contratos / API

### `POST /analyze`
**Request** (multipart/form-data ou application/json)
```json
{
  "source_id": "string (opcional)",
  "input_type": "text|pdf|docx|html",
  "content": "..." (base64 or plain text),
  "meta": {"origem":"noticia|comunicado|relatorio","data_publicacao":"YYYY-MM-DD"}
}
```

**Response** 200
```json
{
  "analysis_id":"uuid",
  "status":"ok|rejected|needs_more_info",
  "laudo": { ... },
  "applied_rules": ["regra_x","regra_y"],
  "audit_ref":"uuid"
}
```

### `GET /audit/report?analysis_id=...`
Retorna a entrada bruta, a saída, as regras aplicadas e a versão do modelo no momento da análise.

---

## 6. Modelo de dados (Postgres)

- `audit_inputs` (id uuid, source_id, raw_text, input_type, meta jsonb, created_at, user_id)
- `analysis_results` (id uuid, input_id fk, status, laudo jsonb, applied_rules jsonb, model_version, created_at)
- `ruleset` (id, name, expression/json, description, active)

---

## 7. Especificação do laudo JSON

```json
{
  "summary": "texto curto",
  "extracted": {
    "tarifa": {"value":4.50, "currency":"BRL","confidence":0.95},
    "bairros": [{"name":"X","confidence":0.9}],
    "linhas_afetadas": [{"id":"23","confidence":0.8}],
    "datas": [{"date":"2025-11-20","type":"inicio"}]
  },
  "impacto_social": "positivo|neutro|negativo|indeterminado",
  "justificativa": ["aumento de tarifa","redução de cobertura"],
  "alertas": ["afeta trabalhadores da periferia","beneficia operadora privada X"],
  "confidence_overall": 0.87
}
```

---

## 8. Regras e heurísticas (exemplos explicitos e testáveis)

1. **Aumento de tarifa**: se `tarifa` extraída > tarifa_base_local OR texto contém expressão "aumenta"/"reajuste" relacionada a preço ⇒ `impacto_social = negativo`.
2. **Corte de linha periférica**: se `linhas_afetadas` inclui bairros com `indice_renda < threshold` (consulta externa opcional) ⇒ `impacto_social = negativo` + alerta.
3. **Expansão de cobertura**: se menção explícita a extensão para bairros periféricos ⇒ `impacto_social = positivo`.
4. **Falta de dados**: se campo crítico (`tarifa` ou `bairros`) não extraído e texto > 200 palavras ⇒ status `needs_more_info`.
5. **Proibição de inventar**: nunca preencher `bairros`/`tarifa` por inferência > 0.6 confidence; se confidence baixa, deixar vazio e sinalizar.

Cada regra tem uma id única (`rule_001`) e descrição curta — armazenar no DB.

---

## 9. Plano de testes automatizados (detalhado)

### 9.1 Testes de aceitação (pytest-bdd)
Formato Gherkin minimalista. Exemplos:

**Cenário 1 — classificar aumento de tarifa**
```
Dado um comunicado que menciona "reajuste de tarifa para R$ 4,60"
Quando o sistema analisar o documento
Então o laudo deve conter "tarifa": {"value":4.60}
E impacto_social deve ser "negativo"
E applied_rules deve conter "rule_001"
```

**Cenário 2 — linha estendida para periferia**
```
Dado um texto que diz "linha 12 será estendida para Bairro X (zona leste)"
Quando o sistema analisar
Então impacto_social deve ser "positivo"
E justificativa deve conter "expansão de cobertura"
```

**Cenário 3 — falta de dados críticos**
```
Dado um comunicado extenso que não menciona tarifa
Quando o sistema analisar
Então status deve ser "needs_more_info"
```

### 9.2 Testes de integração
- Simular Spring Boot chamando agent-service (usar docker compose com serviço de teste do agent que responde fixture JSON).
- Testar persistência em Postgres em GitHub Actions (matrix: JUnit + pytest).

### 9.3 Testes de regressão
- Conjunto fixo de 30 documentos (csv + expected JSON) rodados automaticamente; comparar fields chave com tolerância para confidences.

### 9.4 Testes de propriedade (property-based)
- Usar Hypothesis (python) para gerar variações de frases de aumento de tarifa e assegurar extração correta do número.

---

## 10. Exemplo de fixtures e casos de teste (pequena amostra)

**Fixture 1 — comunicado simples**
```
"A partir de 01/01/2026 haverá reajuste da tarifa para R$ 4,60 nas linhas municipais."
```
Esperado: tarifa 4.60; impacto_social = negativo; rule_001 aplicado.

**Fixture 2 — nota sobre extensão**
```
"Linha 12 será estendida até o bairro Nova Esperança, beneficiando moradores da zona leste."
```
Esperado: impacto_social = positivo; justificativa contains "expansão".

**Fixture 3 — aviso sem dados**
```
"Prefeitura anuncia revisão do sistema de transporte. Mais detalhes serão divulgados em seguida."
```
Esperado: status = needs_more_info; laudo.extracted quase vazio.

---

## 11. Métricas e indicadores para demo

- **Taxa de extração correta**: % de campos-chave extraídos corretamente (tarifa, bairros, datas) no conjunto de teste.
- **Falsos positivos nas classificações**: casos onde impacto_social difere da expectativa.
- **Tempo médio de resposta**: objetivo < 2s para análise textual simples (sem LLM), < 4s com Ollama.
- **Audit coverage**: % de análises com audit log completo (raw + laudo + rules).

---

## 12. Segurança e privacidade

- Não enviar dados sensíveis para serviços externos; usar Ollama on-prem ou stub.
- Logs devem mascarar informações pessoais identificáveis (se houver) — regra no pipeline de ingestão.
- Controlar acesso à API com token básico e, em produção, integrar com OAuth/Keycloak.

---

## 13. Runbook de demo (passo-a-passo)

1. `docker compose up` (Postgres + Ollama stub + spring-api + agent-service)
2. Subir Streamlit: `streamlit run app.py`.
3. Abrir UI, colar fixture 1, clicar analisar.
4. Mostrar output JSON, explicar regras aplicadas no audit report.
5. Rodar testes de aceitação: `pytest tests/acceptance` e mostrar que passam.

---

## 14. Próximos passos / melhorias futuras

- Integração com bases socioeconômicas (IBGE) para checar renda por bairro.
- Dashboard analítico agregando múltiplas análises (heatmap de impacto por região).
- Interface para managers editarem regras no DB e reavaliar análises.
- Detector de mudança de narrativa (comparar versão atual vs comunicado anterior para detectar retrocesso de políticas).
- Scrapping em sites de notícias/portais oficiais para alertas com pouco atraso.
