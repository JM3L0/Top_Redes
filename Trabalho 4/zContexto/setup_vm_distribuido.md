# Setup: Execução Distribuída com VirtualBox (VM1 — Server2 e VM2 — Server1)

Este documento registra o passo a passo completo realizado para configurar o ambiente de execução distribuída do PASID.

---

## IPs do Ambiente

| Máquina | Papel | IP |
|---|---|---|
| Host (Windows) | Source | `192.168.1.5` |
| VM1 | Server2 (porta 3000) | `192.168.1.16` |
| VM2 | Server1 (porta 2000) | `192.168.1.15` |

---

## PARTE 1 — Criar a VM1 no VirtualBox

### 1.1 Nova VM
1. Abra o **Oracle VirtualBox Gerenciador**
2. Clique em **Novo**
3. Preencha:
   - **VM Name:** `VM1`
   - **ISO Image:** selecione o arquivo `ubuntu-XX.XX-live-server-amd64.iso`
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
- Login: `ubuntu` | Senha: `ubuntu`

---

## PARTE 2 — Configurar Java na VM1

### 2.1 Instalar Java 11 e SSH Server
Na janela da VM, digite:
```bash
sudo apt install -y openjdk-11-jdk openssh-server
```

---

## PARTE 3 — Compartilhar Arquivos via Pasta Compartilhada

### 3.1 Adicionar Pasta Compartilhada
Na **janela da VM1** → menu superior → **Dispositivos → Pastas Compartilhadas → Configurações de Pastas Compartilhadas...**
Clique no ícone **+** e configure:
- **Caminho da Pasta:** (Caminho do projeto no Windows)
- **Nome da Pasta:** `Trabalho_4`
- ✅ **Montar Automaticamente** | ✅ **Make Machine-permanent**

### 3.2 Montar a pasta na VM
Na VM:
```bash
sudo mkdir -p /mnt/pasid
sudo mount -t vboxsf Trabalho_4 /mnt/pasid
```

---

## PARTE 4 — Copiar Classes e Configurar o LoadBalancer da VM1

No PowerShell (já conectado por `ssh ubuntu@192.168.1.16`):
```bash
cp -r /mnt/pasid/domain ~/pasid/
```

Criar arquivo de configuração da VM1 (Server2):
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

---

## PARTE 5 — Criar a VM2 Clonando a VM1

Devido a travamentos no instalador do Ubuntu na criação manual, a VM2 foi criada clonando a VM1, que já possuía Java e SSH instalados.

### 5.1 Descartar Estado da VM1
1. Certifique-se de que a VM1 não está "Salva". Clique com botão direito na VM1 → **Descartar estado salvo...** (A VM deve estar totalmente desligada).

### 5.2 Processo de Clone
1. Clique com o botão direito na **VM1** → **Clonar...**
2. **Nome:** `VM_2` (ou `VM2` caso o nome não exista)
3. **Política de Endereço MAC (Crucial):** Selecione **"Gerar novos endereços MAC para todas as placas de rede"**.
4. **Tipo de Clone:** Clone Completo.
5. Inicie a VM_2.

### 5.3 Renovar IP e Hostname na VM2
Como as VMs foram clonadas, a VM2 pode herdar configurações de rede idênticas. Para forçar DHCP diferente e alterar o nome visível no terminal, rode na VM2:
```bash
# Limpa o ID da máquina para forçar IP novo
sudo rm /etc/machine-id
sudo systemd-machine-id-setup

# Renomeia a máquina para VM2
sudo hostnamectl set-hostname VM2
sudo sed -i 's/VM1/VM2/g' /etc/hosts

sudo reboot
```
Após reiniciar, a VM2 assumiu o IP `192.168.1.15`.

---

## PARTE 6 — Configurar LoadBalancer na VM2

Conecte via PowerShell na VM2 (`ssh ubuntu@192.168.1.15`) e altere as propriedades para rodar o Server 1:

```bash
cat > ~/pasid/loadbalancer.properties << 'EOF'
server.loadBalancerName=Server1
server.loadBalancerPort=2000
server.queueLoadBalancerMaxSize=100
server.qtdServices=4

service.serviceTargetIp=192.168.1.16
service.serviceTargetPort=3000
service.serviceTime=100.0
service.std=2.0
service.targetIsSource=false
EOF
```

---

## PARTE 7 — Configurar o Source (Host / IntelliJ)

Arquivo `source.properties` modificado no Windows para refletir os IPs:
- `targetIp=192.168.1.15` (Aponta para Server 1 / VM2)
- `variatingServices.variatedServerLoadBalancerIp=192.168.1.16` (Aponta para Server 2 / VM1)
