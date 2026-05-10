# Resumo Detalhado do Contexto: Trabalho 04 - Validação (PASID Validator)

Este documento descreve detalhadamente o estado atual do trabalho acadêmico "TRABALHO 04 - VALIDAÇÃO" e fornece o passo a passo técnico exato (nível de código e configuração) para concluir a atividade, gerar o artigo e gravar o vídeo.

---

## 🎯 1. Objetivo do Trabalho
O trabalho exige a comparação de uma arquitetura baseada em microsserviços (criada em Java localmente) com um modelo analítico de Redes de Petri Estocásticas (SPN), validando o desempenho do sistema através da métrica de Tempo Médio de Resposta (MRT). 

**Entregáveis:**
1. **Artigo:** Tabelas de parâmetros, tabela comparativa (Modelo vs Experimento) com Teste *t* de Student, e Gráfico de Linhas com **5 pontos no eixo X**.
2. **Vídeo:** Execução do cenário de forma **distribuída**, provando a comunicação via rede.

---

## 📍 2. Ponto Atual (O que já foi feito)

### ✅ Configuração
- **Ambiente de Desenvolvimento:** IntelliJ IDEA com Java 11. `mercuryauto.jar` na pasta `lib` e configurado no *classpath*.
- **Working Directory** corrigido no `workspace.xml` para `pasid-validator-main/` (resolve erros de path).
- **VirtualBox** instalado e pronto para criar as 2 VMs.

### ✅ Etapa 1 — Feeding (Concluída)
Rodou `LocalTest_Services` com `modelFeedingStage=true`. Tempos coletados:
- `T1 = 31.67`
- `T2 = 32.33`
- `T3 = 125.0`
- `T4 = 20.33`
- `T5 = 2037.33`

### ✅ Etapa 2 — Modelo SPN (Concluída)
- `model.xml` atualizado no Mercury com os tempos T1-T5.
- `MercuryCall_Services.java` atualizado com 5 pontos: `new Double[]{1.0, 2.0, 3.0, 4.0, 5.0}`.
- Rodou `MercuryCall_Services`. Resultados do modelo:
  ```
  variatingServices.qtdServices=1,2,3,4,5
  mrtsFromModel=409349.11,204644.08,136857.28,103048.66,82790.55
  sdvsFromModel=1254.19,628.70,421.26,317.77,255.73
  ```
- Gráficos gerados em `src/tests/model/graphs_services/`.

### ✅ Etapa 3 — Validação Experimental (Concluída)
- `source.properties` atualizado: `modelFeedingStage=false`, 5 pontos de `qtdServices`, `mrtsFromModel` e `sdvsFromModel`.
- `maxConsideredMessagesExpected=100`
- Rodou `LocalTest_Services`. Resultados:

| Serviços | Model Mean | Model SD | Exp. Mean | Exp. SD | t Value | p Value |
|---|---|---|---|---|---|---|
| 1 | 409349.11 | 1254.19 | 167956.53 | 15268.78 | 70.47 | 0.00* |
| 2 | 204644.08 | 628.70 | 82446.05 | 7495.10 | 72.66 | 0.00* |
| 3 | 136857.28 | 421.26 | 52262.63 | 4751.15 | 79.32 | 0.00* |
| 4 | 103048.66 | 317.77 | 35487.79 | 3226.16 | 93.20 | 0.00* |
| 5 | 82790.55 | 255.73 | 26255.32 | 2386.85 | 105.32 | 0.00* |

- Gráfico (Modelo vs Experimento) salvo em `src/tests/validation/graphs/`.
- Tabela LaTeX gerada no console (pronta para o artigo).

---

## 🚀 3. Próximos Passos

### ⏳ Etapa 4: Execução Distribuída (Vídeo)
O objetivo é provar que os componentes funcionam via rede, deixando de usar o `localhost`.

1. **Criar as 2 VMs no VirtualBox:**
   - Instale um S.O. leve (Ubuntu Server ou Windows leve) em duas VMs.
   - **Crucial:** Vá nas configurações de rede de cada VM e mude para **"Placa em Modo Bridge" (Bridged Adapter)**.
   - Ligue as VMs e pegue os IPs locais (ex: execute `ipconfig` ou `ip a`). Suponhamos:
     - **Host (Seu PC):** IP `192.168.0.10`
     - **VM 1:** IP `192.168.0.11`
     - **VM 2:** IP `192.168.0.12`

2. **Liberar Portas:**
   - Desative temporariamente o firewall ou libere as portas TCP **1000, 2000 e 3000** em todas as máquinas.
   - Instale o **Java 11** nas VMs e copie a pasta `out` (classes compiladas) e os `.properties` para elas.

3. **Configuração Exata dos Arquivos:**

   * **A) Na VM 1 (Rodará o Server 2):**
     - Renomeie `loadbalancer2.properties` para `loadbalancer.properties`.
     - Configure: `server.loadBalancerPort=3000`
     - Configure: `service.serviceTargetIp=192.168.0.10` *(IP do Host / Source)*
     - Configure: `service.serviceTargetPort=1000` *(Porta do Source)*
     - Execute no terminal: `java -cp ... domain.LoadBalancerProxy`

   * **B) Na VM 2 (Rodará o Server 1):**
     - Renomeie `loadbalancer1.properties` para `loadbalancer.properties`.
     - Configure: `server.loadBalancerPort=2000`
     - Configure: `service.serviceTargetIp=192.168.0.11` *(IP da VM 1 / Server 2)*
     - Configure: `service.serviceTargetPort=3000`
     - Execute no terminal: `java -cp ... domain.LoadBalancerProxy`

   * **C) No Host / Seu PC (Rodará o Source):**
     - Edite o `source.properties`:
     - `targetIp=192.168.0.12` *(IP da VM 2 / Server 1)*
     - `targetPort=2000`
     - `variatingServices.variatedServerLoadBalancerIp=192.168.0.11` *(IP da VM 1 / Server 2)*
     - `variatingServices.variatedServerLoadBalancerPort=3000`
     - `sourcePort=1000`
     - Execute no terminal ou IntelliJ: `domain.Source` (garanta que o *working directory* aponte para a pasta com o `source.properties`).

4. **Gravação:**
   - Inicie o Server 2, depois o Server 1 e, por último, o Source. 
   - Mostre os consoles nas 3 telas respondendo às requisições provando que o tráfego de rede está passando pelos IPs e não pelo `localhost`.
