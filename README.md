# Documento de Projeto  
## Plataforma Inteligente para Monitoramento da Qualidade do Transporte Público Urbano  
### Aplicação de IA Generativa – PoC e MVP  

## 1. Introdução

O transporte público urbano é um direito social assegurado pela Constituição Federal e exerce papel central na garantia de outros direitos fundamentais, como acesso ao trabalho, à saúde e à educação. No município de Belém do Pará, entretanto, a população enfrenta problemas recorrentes relacionados à qualidade do serviço, tais como aumento frequente de tarifas, frota sucateada, superlotação, atrasos constantes e condições precárias de trabalho para motoristas e cobradores.  

Apesar da recorrência desses problemas, as informações que evidenciam a degradação do transporte público encontram-se dispersas em múltiplas fontes não estruturadas, como notícias, redes sociais e relatos informais de usuários. A ausência de mecanismos sistemáticos de coleta, análise e síntese dessas informações dificulta o monitoramento contínuo do serviço e limita a atuação de entidades civis, jornalistas e órgãos de controle.  

## 2. Problema

Atualmente, não existem ferramentas integradas que permitam a agregação, interpretação e análise sistemática de informações textuais relacionadas à qualidade do transporte público em Belém do Pará. Os dados disponíveis são majoritariamente não estruturados, fragmentados e distribuídos em diferentes canais, o que inviabiliza análises consistentes e baseadas em evidências.  

Como consequência, decisões e ações de mobilização social são frequentemente fundamentadas em percepções isoladas, sem apoio analítico robusto, reduzindo o impacto de iniciativas de fiscalização e advocacy.  

## 3. Objetivo Geral

Desenvolver uma solução baseada em Inteligência Artificial Generativa capaz de transformar dados textuais não estruturados sobre o transporte público urbano em inteligência acionável, promovendo maior transparência, monitoramento contínuo e suporte à tomada de decisão por entidades civis e sociedade em geral.  

## 4. Objetivos Específicos

- Agregar informações dispersas sobre o transporte público a partir de fontes textuais diversas.  
- Aplicar modelos de linguagem para classificar, interpretar e sintetizar relatos sobre problemas recorrentes.  
- Validar tecnicamente o uso de IA generativa por meio de uma Prova de Conceito (PoC).  
- Entregar valor prático a usuários reais por meio de um Produto Mínimo Viável (MVP).  

## 5. Hipótese de Uso de IA Generativa

Se modelos de linguagem forem utilizados para coletar, interpretar semanticamente, classificar e sintetizar relatos textuais relacionados ao transporte público, então será possível gerar inteligência acionável de forma automatizada, reduzindo o esforço humano de análise e ampliando a capacidade de monitoramento e fiscalização do serviço.  

A aplicação de IA generativa justifica-se pela natureza não estruturada dos dados e pela necessidade de compreensão semântica, extração de padrões e geração de explicações acessíveis a usuários não técnicos.  

## 6. Prova de Conceito (PoC)

### 6.1 Objetivo da PoC

Validar a viabilidade técnica do uso de Inteligência Artificial Generativa para transformar textos livres relacionados ao transporte público em informações estruturadas e sintetizadas.  

### 6.2 Escopo da PoC

**Fontes de dados:**  
- Notícias de portais locais  
- Relatos textuais públicos ou simulados  

**Volume estimado:** 100 a 500 textos  
**Período analisado:** últimos 3 meses  

### 6.3 Funcionalidades

- Ingestão de textos não estruturados  
- Processamento com modelos de linguagem para:  
  - Classificação dos problemas (ex.: atraso, superlotação, tarifa, frota)  
  - Extração de entidades relevantes (linha, bairro, tipo de ocorrência)  
- Geração automática de:  
  - Resumos analíticos periódicos  
  - Listagem dos problemas mais recorrentes  

### 6.4 Critérios de Sucesso

- Coerência semântica mínima de 80% na classificação (avaliada manualmente)  
- Redução significativa do tempo de análise humana  
- Capacidade de gerar sínteses compreensíveis e úteis  

## 7. Produto Mínimo Viável (MVP)

### 7.1 Usuário-Alvo

- Organizações não governamentais  
- Coletivos urbanos  
- Jornalistas de dados  

### 7.2 Proposta de Valor

Disponibilizar uma plataforma simples e acessível que converta relatos dispersos sobre o transporte público em evidências organizadas, facilitando análises, denúncias e ações de mobilização social.  

### 7.3 Funcionalidades do MVP

- Coleta manual ou automática de textos  
- Classificação automática dos relatos  
- Painel visual com:  
  - Principais tipos de problemas  
  - Evolução temporal das ocorrências  
- Geração de relatórios explicativos automatizados  

## 8. Arquitetura de Referência (Alto Nível)

A solução será composta pelas seguintes camadas:  

- Coleta de Dados: scraping ou upload manual de textos  
- Engenharia de Dados: pré-processamento e armazenamento  
- Camada Inteligente: modelos de linguagem e embeddings  
- Apresentação: painel analítico e geração de relatórios  

A separação entre engenharia de dados, inteligência artificial e camada de produto garante modularidade e escalabilidade da solução.  

## 9. Métricas de Avaliação

### 9.1 Métricas Técnicas

- Precisão da classificação semântica  
- Taxa de erro de extração  
- Tempo médio de processamento  

### 9.2 Métricas de Valor

- Tempo economizado na análise manual  
- Frequência de uso da plataforma  
- Utilização prática dos relatórios gerados  

## 10. Roadmap de Evolução

Após a validação do MVP, a solução poderá evoluir para incluir:  

- Aprendizado com feedback humano  
- Detecção automática de anomalias  
- Comparações entre regiões e linhas  
- Interface conversacional para exploração dos dados  

## 11. Considerações Finais

Este projeto propõe o uso estratégico de Inteligência Artificial Generativa para enfrentar um problema social relevante, explorando sua capacidade de interpretação semântica e síntese de informações. A separação clara entre PoC e MVP garante rigor técnico, validação progressiva e entrega de valor real à sociedade.
