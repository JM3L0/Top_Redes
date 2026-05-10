# Roteiro de Gravação: Execução Distribuída PASID

Este guia deve ser utilizado no momento exato de gravar a tela e rodar as VMs, assumindo que ambas estão desligadas.

## Passo 1: Preparar as Máquinas (VirtualBox)

1. Abra o VirtualBox.
2. Inicie a **VM1** e inicie a **VM_2** (pode deixar elas iniciarem minimizadas).
3. Aguarde cerca de 1 minuto para que ambas inicializem completamente na rede.

## Passo 2: Preparar os Terminais (PowerShell)

Para mostrar de forma clara os três nós se comunicando, divida sua tela do Windows:
- Esquerda: Janela do IntelliJ
- Direita (cima): PowerShell da VM2 (Server 1)
- Direita (baixo): PowerShell da VM1 (Server 2)

**No PowerShell do Server 2 (VM1):**
```bash
ssh ubuntu@192.168.1.16
# senha: ubuntu
cd ~/pasid
```

**No PowerShell do Server 1 (VM2):**
```bash
ssh ubuntu@192.168.1.15
# senha: ubuntu
cd ~/pasid
```

## Passo 3: Iniciar o Tráfego (Em Ordem)

Para evitar erros de conexão (`Connection Refused`), a ordem de inicialização é estritamente do destino final até a origem:

**1. Iniciar Server 2 (Destino Final - VM1)**
No PowerShell conectado em `192.168.1.16`:
```bash
java -cp . domain.LoadBalancerProxy loadbalancer.properties
```
*Aguarde a mensagem "service300x enabled to receive messages".*

**2. Iniciar Server 1 (Intermediário - VM2)**
No PowerShell conectado em `192.168.1.15`:
```bash
java -cp . domain.LoadBalancerProxy loadbalancer.properties
```
*Aguarde a mensagem "service200x enabled to receive messages".*

**3. Iniciar Source (Origem - IntelliJ)**
No IntelliJ (Host Windows):
- Certifique-se de que a aba `LocalTest_Services.java` está aberta.
- Clique em **Run**.

## O que deve acontecer na tela:
1. O console do IntelliJ começará a gerar logs de mensagens enviadas.
2. O PowerShell da VM2 (Server1) mostrará tráfego sendo recebido na porta 2000.
3. O PowerShell da VM1 (Server2) mostrará tráfego sendo recebido na porta 3000.
4. O IntelliJ validará os resultados e encerrará a execução gerando o gráfico final.

Isso demonstra o fluxo: `Host -> VM2 -> VM1 -> Host` funcionando perfeitamente em rede Bridge.
