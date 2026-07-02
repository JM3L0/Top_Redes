# Trabalho 07 — Árvore de Falha: Explicação Completa

---

## Parte 1 — O que é o trabalho e como você vai fazê-lo

### O que é pedido

Escrever um **artigo científico no formato IEEE** (mínimo 8 páginas, 2 colunas) usando **Árvore de Falha (Fault Tree Analysis — FTA)** para avaliar a **disponibilidade** de um sistema hospitalar inteligente.

### A lógica geral em 3 pontos

**Artigo de Inspiração** (*"Quantifying the Impact of Resource Redundancy on Smart City System Dependability"*)
→ É o modelo que você deve **imitar na estrutura e no formato**. Ele avalia uma Cidade Inteligente usando Árvore de Falha + Markov Chain, tem estudos de caso com KooN, análise de sensibilidade e mostra como a disponibilidade melhora com diferentes configurações.

**Artigo de Espelhamento** (*"Model-driven Impact Quantification of Energy Resource Redundancy and Server Rejuvenation on Dependability of Medical Sensor Networks in Smart Hospitals"*)
→ Fornece o **contexto e os parâmetros** que você usa. Ele modela um Hospital Inteligente com três configurações de energia (A: rede+gerador, B: +solar, C: +rejuvenescimento). A **Figura 6** é o Modelo B — hospital com sistema solar completo — e é essa arquitetura que você espelha.

**Seu trabalho**
→ Pegar os componentes e parâmetros do artigo de espelhamento e modelá-los com **Árvore de Falha** (em vez de Redes de Petri), seguindo a estrutura do artigo de inspiração.

### Diferença fundamental entre SPN e FTA

| | SPN (artigo de espelhamento) | FTA (seu trabalho) |
|---|---|---|
| Tipo de modelo | Rede de Petri estocástica com fichas e transições | Árvore booleana com portas lógicas (OR, AND, KooN) |
| O que modela | Dinâmica temporal, aging, rejuvenescimento | Combinações de falhas que causam falha do sistema |
| Complexidade | Alta — guard expressions, estados, aging | Média — portas lógicas, probabilidades de falha |
| Ferramenta | Mercury (módulo SPN) | Mercury (módulo Fault Tree) ← **seu XML usa exatamente isso** |

> **Importante:** O enunciado diz explicitamente que você pode **abstrair as guard expressions** do SPN. Ou seja, você não precisa replicar a lógica de controle interna do artigo de espelhamento — só a arquitetura de componentes.

### Estrutura do artigo (Entrega 01)

Para a Entrega 01 você precisa escrever as seções **Modelo** e **Estudos de Caso**. As demais seções (Título, Resumo, Introdução, Arquitetura, Conclusão) ficam para a Entrega 02.

---

## Parte 2 — Verificação e explicação do modelo

### ✅ O modelo se encaixa perfeitamente no proposto

O arquivo `model_trab07.xml` já contém uma **Árvore de Falha completa e correta** construída no Mercury, espelhando a arquitetura da Figura 6 do artigo de espelhamento (Modelo B: hospital + sistema fotovoltaico + gerador).

Confirmação da correspondência entre os dois:

| Componente (artigo de espelhamento) | Componente (seu XML) | ID no XML |
|---|---|---|
| Power Grid | Power Grid | e3 |
| Emergency Diesel Generator | Power Gen | e4 |
| Switch Power | Sw Power | e6 |
| Solar Inverter | Sol Inv | e7 |
| Charger Control | Chg Ctrl | e8 |
| Solar Panel | Sol Painel | e10 |
| Battery Storage | Battery | e11 |
| Cloud Server | Cloud Srv | e12 |
| Edge Server | Edge svr | e13 |
| Router | Router | e14 |
| Gateway | Gateway | e15 |
| Supervisor | Superv | e16 |
| Sensors / Beds | Sensors + KooN Beds | e19 + kn1 |

Todos os 13 componentes do artigo de espelhamento estão presentes no seu modelo.

---

### Estrutura completa da Fault Tree

```
SYS FAIL [OR — Raiz]
│
│  O sistema falha se o HOSPITAL falhar OU se a ENERGIA falhar.
│
├── HOSP FAIL [OR]
│   │
│   │  O hospital falha se QUALQUER componente interno falhar.
│   │
│   ├── Cloud Srv   (e12)
│   ├── Edge svr    (e13)
│   ├── Router      (e14)
│   ├── Gateway     (e15)
│   ├── Superv      (e16)
│   └── Beds [KooN k=5, n=10]
│       │
│       │  O subsistema de leitos falha se 5 ou mais
│       │  dos 10 sensores falharem simultaneamente.
│       │
│       └── Sensors (e19)  ← 10 instâncias
│
└── PWR FAIL [AND]
    │
    │  A alimentação falha SOMENTE se TODAS as
    │  três fontes falharem ao mesmo tempo.
    │
    ├── Power Grid  (e3)
    ├── Power Gen   (e4)
    └── SOLAR SYS  [OR]
        │
        │  O sistema solar falha se QUALQUER
        │  componente fotovoltaico falhar.
        │
        ├── Sw Power   (e6)
        ├── Sol Inv    (e7)
        ├── Chg Ctrl   (e8)
        └── SOL + BAT  [AND]
            │
            │  Falha apenas se o painel E a bateria
            │  falharem juntos.
            │
            ├── Sol Painel (e10)
            └── Battery    (e11)
```

---

### Justificativa de cada porta lógica

**OR na raiz (Sys Fail):**
O sistema hospitalar é considerado indisponível se o sistema de saúde interno falhar **ou** se a alimentação elétrica colapsar. Qualquer um dos dois basta para tirar o hospital do ar.

**OR no Hospital (Hosp Fail):**
Todos os componentes internos do hospital são essenciais para a operação do sistema de monitoramento de pacientes. Se o Cloud Server cair, o backup remoto dos dados é perdido. Se o Gateway cair, os sensores param de transmitir. Se o Supervisor cair, a análise de emergência fica indisponível. Qualquer falha individual compromete o sistema completo — por isso OR.

**AND na Energia (Pwr Fail):**
O hospital possui **redundância tripla** de energia: rede elétrica pública, gerador diesel de emergência e sistema fotovoltaico. A alimentação só colapsa se as três fontes falharem simultaneamente. Isso modela exatamente o comportamento descrito no artigo de espelhamento: o solar é a fonte principal, a rede pública é o fallback, e o gerador só entra quando as demais falham.

**OR no Sistema Solar (Solar Sys):**
O sistema fotovoltaico é uma cadeia de componentes em série funcional: o Switch Power direciona a energia, o Inversor Solar converte DC em AC, o Charger Control regula a carga das baterias. Se qualquer um falhar, o subsistema solar como um todo fica indisponível — por isso OR.

**AND no Sol + Bat:**
O painel solar e a bateria formam um subsistema com redundância parcial: se apenas o painel falhar, a bateria ainda sustenta o hospital por um período curto; se apenas a bateria falhar, o painel ainda fornece energia diretamente (enquanto houver sol). O subsistema só colapsa se **ambos** falharem — por isso AND.

**KooN nos Beds (k=5, n=10):**
O hospital tem 10 leitos com sensores. O modelo considera que o subsistema de monitoramento de leitos ainda pode funcionar (de forma degradada) com até 4 sensores falhando. Somente quando 5 ou mais sensores falham o subsistema é considerado indisponível. Isso reflete a realidade hospitalar: tolerância a falhas parciais nos dispositivos de borda.

---

### Tabela completa de parâmetros (extraída do XML)

A disponibilidade de cada componente é calculada por: **A = MTTF / (MTTF + MTTR)**

| Componente | ID | MTTF (h) | MTTR (h) | Disponibilidade |
|---|---|---|---|---|
| Power Grid | e3 | 8.757 | 4.807 | 64.56% |
| Solar Inverter | e7 | 24.82 | 8.0 | 75.62% |
| Switch Power | e6 | 25.0 | 8.0 | 75.76% |
| Battery | e11 | 47.829 | 8.0 | 85.67% |
| Charger Control | e8 | 70.08 | 8.0 | 89.75% |
| Power Generator | e4 | 636.0 | 37.0 | 94.50% |
| Solar Panel | e10 | 219.0 | 8.0 | 96.48% |
| Supervisor | e16 | 44.957 | 1.0 | 97.82% |
| Gateway | e15 | 480.77 | 8.0 | 98.36% |
| Router | e14 | 698.22 | 8.0 | 98.87% |
| Sensors (cada) | e19 | 300.0 | 1.0 | 99.67% |
| Edge Server | e13 | 940.0 | 1.37 | 99.85% |
| Cloud Server | e12 | 760.0 | 0.74 | 99.90% |

> **Nota sobre os valores:** No artigo de espelhamento, os parâmetros de Sensores, Gateway, Router e Solar Panel estão em dezenas de milhares de horas (componentes eletrônicos individuais muito confiáveis). No seu XML, os valores estão calibrados para a escala do *sistema como um todo* — o que é compatível com o nível de abstração da Árvore de Falha proposta.

---

### Métricas globais (calculadas pelo Mercury no XML)

| Métrica | Valor |
|---|---|
| Disponibilidade do sistema | **93.99%** |
| MTTF do sistema | 33.06 horas |
| MTTR do sistema | 2.11 horas |
| Downtime anual estimado | ≈ 526 horas/ano |

> **Por que 93.99% parece baixo?** Porque o componente de pior disponibilidade — a **Rede Elétrica (Power Grid)** com apenas **64.56%** — tem um impacto enorme no sistema quando não há redundância suficiente. Os estudos de caso vão mostrar como diferentes configurações de energia melhoram esse número.

---

## Parte 3 — Estudos de Caso e como gerar os gráficos

Os estudos de caso seguem o mesmo padrão do artigo de inspiração: você parte de um modelo base e varia parâmetros para mostrar o impacto na disponibilidade. Cada estudo de caso gera pelo menos um gráfico.

---

### Estudo de Caso 1 — Impacto da Configuração de Energia

**Pergunta:** O que acontece com a disponibilidade do hospital conforme adicionamos fontes de energia redundantes?

**Três cenários para comparar:**

| Configuração | Fontes de energia presentes | O que representa |
|---|---|---|
| Config. A | Apenas Power Grid | Hospital sem backup — raro mas existe |
| Config. B | Power Grid + Gerador | Hospital convencional com gerador diesel |
| Config. C (baseline) | Power Grid + Gerador + Solar | Modelo completo do seu XML |

**Como calcular:**
- **Config A:** A_sistema = A_hospital × A_grid
- **Config B:** A_sistema = A_hospital × [1 − (1−A_grid)×(1−A_gen)]
- **Config C:** A_sistema = resultado direto do Mercury (93.99%)

**Gráfico:** Dois gráficos de barras lado a lado — um com Disponibilidade (%) e outro com Downtime anual (horas/ano) para as três configurações.

**O que o gráfico vai mostrar:** A diferença brutal entre ter apenas a rede elétrica (~61%) versus ter redundância com solar (~94%), quantificando em horas de downtime por ano a diferença entre cada nível de redundância.

---

### Estudo de Caso 2 — Variação do Parâmetro KooN nos Sensores

**Pergunta:** Como a exigência de disponibilidade dos leitos (tolerância a falhas nos sensores) afeta o sistema como um todo?

**O que variar:** O valor de k na porta KooN dos Beds, de k=1 até k=10, mantendo n=10 sensores fixo.

| k | Interpretação | Tolerância |
|---|---|---|
| k=1 | Falha com 1 sensor falhando | Nenhuma tolerância |
| k=2 | Falha com 2 sensores | Muito rígido |
| k=5 | **Baseline do seu modelo** | Tolerância média |
| k=8 | Falha com 8 sensores | Alta tolerância |
| k=10 | Nunca falha por sensores | Total tolerância |

**Como fazer no Mercury:** Abrir o modelo, localizar a porta KooN "Beds" (nó `kn1`), alterar o valor de `k` e rodar a análise estacionária. Anotar a disponibilidade para cada valor de k.

**Gráfico:** Linha contínua com k no eixo X e Disponibilidade (%) no eixo Y. Marcar o ponto baseline (k=5) com uma cor ou marcador diferente.

**O que o gráfico vai mostrar:** A curva de saturação — acima de um certo valor de k, os sensores param de ser o fator limitante e a disponibilidade estabiliza, dominada pelo resto do sistema. Isso explica por que o KooN precisa ser calibrado: exigir demais (k=1) penaliza sem necessidade; exigir de menos (k=10) cria risco real de falha não detectada.

---

### Estudo de Caso 3 — Análise de Sensibilidade (Componente mais crítico)

**Pergunta:** Qual componente, ao ter seu MTTF melhorado, mais impacta a disponibilidade do sistema? Em outras palavras — onde vale mais a pena investir em hardware mais confiável?

**O que variar:** O MTTF de cada componente candidato, em 5 pontos: −50%, −25%, baseline (100%), +25%, +50%.

**Componentes candidatos para analisar:**
- Power Grid (o de menor disponibilidade)
- Supervisor (MTTF baixo: 44.9h)
- Gateway (MTTF moderado: 480.8h)
- Edge Server (crítico no artigo de espelhamento)
- Cloud Server (crítico no artigo de espelhamento)

**Como fazer:** Para cada componente, rodar o Mercury 5 vezes variando apenas o MTTF daquele componente. Manter todos os outros no valor original.

**Gráfico:** Linhas múltiplas — cada linha representa um componente diferente. Eixo X = fator de variação (−50% a +50%), eixo Y = disponibilidade do sistema (%). Uma linha tracejada horizontal marca o valor baseline.

**O que o gráfico vai mostrar:** A inclinação de cada curva revela a sensibilidade. O componente com a curva mais íngreme é o mais crítico — aquele que mais impacta a disponibilidade quando seu MTTF muda. Esse resultado orienta decisões de compra: vale mais trocar o Supervisor por um mais confiável do que melhorar o Cloud Server.

---

## Resumo de o que escrever (Entrega 01)

### Seção: Model
1. Descrever a arquitetura (dois blocos: hospital + energia)
2. Apresentar o diagrama da Fault Tree (desenhado por você — não copiar)
3. Explicar cada porta lógica com justificativa
4. Tabela completa de parâmetros (MTTF, MTTR, A de cada componente)
5. Fórmulas de disponibilidade (OR, AND, KooN, A = MTTF/MTTF+MTTR)
6. Resultado baseline: A = 93.99%, Downtime ≈ 526h/ano

### Seção: Case Studies
1. **Case Study 1** — Comparação de configurações de energia (Config A, B, C)
2. **Case Study 2** — Variação do KooN nos sensores (k de 1 a 10)
3. **Case Study 3** — Análise de sensibilidade (qual componente é mais crítico)

Para cada estudo: texto explicativo + tabela de resultados + gráfico gerado.

---

## Como gerar os gráficos (quando quiser)

Os gráficos podem ser gerados com Python usando `matplotlib` e `scipy`. Já existe o script `gerar_graficos.py` na pasta `Trabalho 7` com os 3 estudos de caso implementados. Quando quiser rodar, basta executar:

```bash
python gerar_graficos.py
```

Os três arquivos de imagem serão salvos na pasta `Trabalho 7`:
- `case_study_1_energy.png`
- `case_study_2_koon.png`
- `case_study_3_sensitivity.png`
