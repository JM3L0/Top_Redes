# Setup: Execução Distribuída com VirtualBox (VM1 — Server2)

Este documento registra o passo a passo completo para configurar uma VM com Ubuntu Server e executar o componente `LoadBalancerProxy` do PASID de forma distribuída.

---

## IPs do Ambiente

| Máquina | Papel | IP |
|---|---|---|
| Host (Windows) | Source | `192.168.1.5` |
| VM1 | Server2 (porta 3000) | `192.168.1.11` |
| VM2 | Server1 (porta 2000) | *(a definir)* |

---

## PARTE 1 — Criar a VM no VirtualBox

### 1.1 Nova VM
1. Abra o **Oracle VirtualBox Gerenciador**
2. Clique em **Novo**
3. Preencha:
   - **VM Name:** `VM1`
   - **ISO Image:** selecione o arquivo `ubuntu-XX.XX-live-server-amd64.iso` (baixar em https://ubuntu.com/download/server)
   - **OS:** Linux | **Distribution:** Ubuntu | **Version:** Ubuntu (64-bit)
   - Marque **"Proceed with Unattended Installation"**
4. Clique **Próximo**

### 1.2 Usuário e senha
- **User Name:** `ubuntu`
- **Password:** `ubuntu`
- **Confirm Password:** `ubuntu`
- Clique **Próximo**

### 1.3 Hardware
- **Base Memory:** `1024 MB`
- **CPUs:** `1`
- **Disk Size:** `10 GB`
- Clique **Próximo** → **Finalizar**

### 1.4 ⚠️ Configurar Rede para Bridge (OBRIGATÓRIO)
**Antes de ligar a VM:**
1. Selecione VM1 → **Configurações → Rede**
2. Adaptador 1 → **"Conectado a:"** → mude de `NAT` para **`Placa em Modo Bridge`**
3. Em **"Nome:"** selecione o adaptador Wi-Fi ou Ethernet do seu PC
4. Clique **OK**

### 1.5 Ligar a VM
- Clique **Iniciar** e aguarde a instalação automática (pode levar 5–15 min)
- Quando aparecer o prompt de login, pressione **Enter** se necessário
- Login: `ubuntu` | Senha: `ubuntu`

---

## PARTE 2 — Configurar Java na VM

### 2.1 Instalar Java 11
Na janela da VM, digite:
```bash
sudo apt install -y openjdk-11-jdk
```
Senha: `ubuntu`

Verifique:
```bash
java -version
# Esperado: openjdk version "11.0.x"
```

### 2.2 Instalar SSH Server
```bash
sudo apt install -y openssh-server
```

---

## PARTE 3 — Compartilhar Arquivos via Pasta Compartilhada do VirtualBox

> **Dica:** O terminal da VM não suporta Ctrl+V. Use SSH pelo PowerShell do Windows para colar comandos facilmente.

### 3.1 Adicionar Pasta Compartilhada
Na **janela da VM1** → menu superior → **Dispositivos → Pastas Compartilhadas → Configurações de Pastas Compartilhadas...**

Clique no ícone **+** e configure:
- **Caminho da Pasta:** `C:\Users\jsous\OneDrive\Área de Trabalho\Top_Redes\Trabalho 4\out\production\Trabalho 4`
- **Nome da Pasta:** `Trabalho_4`
- ✅ **Montar Automaticamente**
- ✅ **Make Machine-permanent**
- Clique **OK**

### 3.2 Montar a pasta na VM
Na VM:
```bash
sudo mkdir -p /mnt/pasid
sudo mount -t vboxsf Trabalho_4 /mnt/pasid
ls /mnt/pasid
# Esperado: domain  tests  tests2
```

---

## PARTE 4 — Usar o PowerShell do Windows como terminal da VM (Recomendado)

> Isso permite colar comandos com Ctrl+V no terminal, muito mais prático.

### 4.1 Conectar via SSH do PowerShell
Abra o **PowerShell** no Windows e execute:
```powershell
ssh ubuntu@192.168.1.11
```
- Na primeira vez, responda `yes` para aceitar o fingerprint
- Senha: `ubuntu`

A partir daqui você controla a VM pelo PowerShell e pode colar com **Ctrl+V**.

---

## PARTE 5 — Copiar Classes e Configurar o LoadBalancer

### 5.1 Copiar classes compiladas
No PowerShell (já conectado por SSH):
```bash
cp -r /mnt/pasid/domain ~/pasid/
```

### 5.2 Criar arquivo de configuração da VM1 (Server2)
```bash
cat > ~/pasid/loadbalancer.properties << 'EOF'
server.loadBalancerName=Server2
server.loadBalancerPort=3000
server.queueLoadBalancerMaxSize=100
server.qtdServices=4

service.serviceTargetIp=192.168.1.5
service.serviceTargetPort=1000
service.serviceTime=2000.0
service.std=2.0
service.targetIsSource=true
EOF
```

Verifique:
```bash
ls ~/pasid/
# Esperado: domain/  loadbalancer.properties  (+ .class files)
```

---

## PARTE 6 — Rodar o Server2 na VM1

```bash
cd ~/pasid && java -cp . domain.LoadBalancerProxy loadbalancer.properties
```

### Saída esperada no console:
```
Load Balancer Parameters:
Load Balancer Name: Server2
Local Port: 3000
Queue Load Balancer Max Size: 100
Qtd Services List: [4]
====================================
Starting service3001
Starting service3002
...
service3001 enabled to receive messages.
...
```

✅ **Server2 está rodando e aguardando conexões na porta 3000.**

---

## PARTE 7 — Salvar Estado da VM para retomar depois

Na janela da VM → clique no **X** → selecione **"Salvar o estado da máquina"** → OK

Para retomar: basta clicar **Iniciar** no VirtualBox — a VM volta exatamente onde parou.

---

## ✅ Status Atual

| Etapa | Status |
|---|---|
| VM1 criada e configurada | ✅ Concluído |
| Java 11 instalado na VM1 | ✅ Concluído |
| SSH funcionando | ✅ Concluído |
| Pasta compartilhada configurada | ✅ Concluído |
| Classes copiadas para VM1 | ✅ Concluído |
| Server2 (porta 3000) testado e funcionando | ✅ Concluído |

---

## ⏳ Próximos Passos

### 1. Criar VM2 (Server1 — porta 2000)
Processo **idêntico** ao da VM1. Após subir, anotar o IP (ex: `192.168.1.12`).

Arquivo de configuração para VM2:
```bash
cat > ~/pasid/loadbalancer.properties << 'EOF'
server.loadBalancerName=Server1
server.loadBalancerPort=2000
server.queueLoadBalancerMaxSize=100
server.qtdServices=4

service.serviceTargetIp=192.168.1.11
service.serviceTargetPort=3000
service.serviceTime=100.0
service.std=2.0
service.targetIsSource=false
EOF
```

Rodar na VM2:
```bash
cd ~/pasid && java -cp . domain.LoadBalancerProxy loadbalancer.properties
```

### 2. Configurar o Host (Source) para apontar para as VMs
Editar `pasid-validator-main/src/tests/validation/source.properties`:
```properties
modelFeedingStage=false
sourcePort=1000
targetIp=192.168.1.12        # IP da VM2 (Server1)
targetPort=2000
maxConsideredMessagesExpected=100

variatingServices.arrivalDelay=100
variatingServices.variatedServerLoadBalancerIp=192.168.1.11   # IP da VM1 (Server2)
variatingServices.variatedServerLoadBalancerPort=3000

variatingServices.qtdServices=1,2,3,4,5
mrtsFromModel=409349.11,204644.08,136857.28,103048.66,82790.55
sdvsFromModel=1254.19,628.70,421.26,317.77,255.73
```

### 3. Ordem de inicialização para o vídeo
1. ▶ Iniciar **Server2** na VM1: `cd ~/pasid && java -cp . domain.LoadBalancerProxy loadbalancer.properties`
2. ▶ Iniciar **Server1** na VM2: `cd ~/pasid && java -cp . domain.LoadBalancerProxy loadbalancer.properties`
3. ▶ Iniciar **Source** no Host: rodar `LocalTest_Services` no IntelliJ (com `source.properties` apontando para as VMs)

### 4. Gravar o vídeo
- Mostre os 3 consoles simultaneamente (Host + VM1 + VM2)
- Grave as mensagens sendo trocadas entre IPs reais (não localhost)
