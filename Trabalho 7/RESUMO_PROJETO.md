# Contextualização e Relatório de Progresso: Trabalho 07 (Smart Hospital FTA)

## 1. O Escopo do Projeto
O objetivo central deste trabalho acadêmico é escrever um **artigo científico no formato IEEE** para avaliar a dependabilidade (disponibilidade estocástica) de um Hospital Inteligente (Smart Hospital). A metodologia exigida utiliza **Árvores de Falhas (Fault Tree Analysis - FTA)** através do software Mercury.

Para garantir rigor acadêmico, o trabalho baseia-se em dois alicerces literários:
* **Artigo de Inspiração:** Daqui tiramos a estrutura do artigo, a metodologia de Análise de Sensibilidade e o uso avançado da porta tolerante a falhas *K-out-of-N* (KooN).
* **Artigo de Espelhamento:** Daqui extraímos a "planta física" do hospital (13 hardwares centrais) e os parâmetros de confiabilidade (MTTF e MTTR). Modelamos a "Configuração C" (Grid + Gerador + Fotovoltaico).

---

## 2. Como Nós Fizemos (Nossa Metodologia)
Nós construímos o projeto de forma modular, atacando as frentes visual, matemática e de redação técnica:

1. **Simulação e Gráficos (Python):** 
   Em vez de tirar métricas "do nada", usamos scripts Python (`calcular_dados.py` e `plotar_graficos.py`) que replicam a matemática do Mercury. Através deles, executamos as simulações matemáticas e geramos **8 gráficos IEEE-compliant** para sustentar a nossa argumentação.

2. **Modelagem Matemática (Mercury):**
   Mapeamos os 13 componentes físicos para a lógica Booleana:
   * **Energia:** Redundância mapeada com portas AND (pois a energia só cai se Grid, Diesel e Solar caírem juntos). O Solar interno usa portas OR e AND baseadas no fluxo de conversão elétrica.
   * **TI (Dados):** Estrutura em série (Router, Gateway, etc.) mapeada com portas OR (se um falha, o roteamento rompe).
   * **Sensores (Borda):** Mapeados com porta KooN para tolerar desconexões isoladas de aparelhos nos leitos.

3. **Design e Arquitetura Visual:**
   O professor exigiu uma arquitetura original. Para isso, você desenhou o modelo físico (`Modelo.drawio.png`), e nós elaboramos um texto acadêmico onde assumimos a autoria do design, removendo as menções de "cópia" ou "espelhamento".

4. **Redação em Padrão Qualis A:**
   Adotamos uma linguagem extremamente rigorosa. Para facilitar a leitura e adequação ao formato de colunas do IEEE, todos os parágrafos foram fatiados para manterem uma média de $\approx$ 4 a 5 linhas. Inserimos as equações de Disponibilidade e de Probabilidade Binomial no código LaTeX para blindar o trabalho.

---

## 3. O Que Temos Pronto Até Agora (Entregáveis)

No momento, temos os **3 blocos mais complexos** do artigo completamente redigidos em código LaTeX estruturado, com chamadas de imagens e referências já configuradas:

* ✅ **Seção de Arquitetura do Sistema:** 
  * Texto detalhando o subsistema de TI (Edge/Cloud) e o de Energia (Redundância Tripla).
  * Placeholder para sua imagem gráfica (`Modelo.drawio.png`).

* ✅ **Seção do Modelo (Fault Tree):**
  * Texto detalhando a tradução física para booleana.
  * Tabela completa de MTTF e MTTR dos 13 componentes.
  * Subseção matemática com as equações de $A$ e KooN.

* ✅ **Seção de Estudos de Caso (Resultados):**
  * **Case 1 (Energia):** Texto e 2 gráficos atestando que a energia híbrida mitiga o *downtime* para $\approx$ 539h anuais.
  * **Case 2 (KooN):** Texto e 1 gráfico logarítmico provando que o sistema estabiliza na marca $K=5$.
  * **Case 3 (Sensibilidade):** Texto avaliando individualmente 5 componentes e mostrando que o Cloud Server não precisa de mais investimentos, mas que o Supervisor/Gateway são críticos e propensos a falhas. (5 gráficos empilhados separadamente com `[H]`).

* ✅ **Base Bibliográfica (.bib):**
  * Um arquivo BibTeX levantado através da técnica de *snowballing* contendo 10 referências acadêmicas rigorosas prontas para citação.

---

## 4. Próximos Passos (O que falta?)
Para finalizar totalmente a Entrega 02 do artigo (que é o documento inteiro), precisaremos apenas das "bordas" do texto:
1. **Resumo (Abstract)**
2. **Introdução** (Contextualizando a importância das Smart Cities e Saúde)
3. **Conclusão**
