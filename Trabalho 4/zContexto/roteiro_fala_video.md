# Roteiro de Fala para Gravação do Vídeo (PASID Distribuído)

Este documento contém o roteiro exato do que falar e onde focar a câmera (celular) durante a gravação do experimento distribuído.

---

## 1. Introdução (Apresentando o ambiente)
*Aponte a câmera para a tela inteira, mostrando as janelas divididas (IntelliJ de um lado, os dois terminais do PowerShell do outro).*

🗣️ **O que falar:** 
> "Olá professor, este é o vídeo de validação do projeto PASID rodando de forma 100% distribuída. Como o senhor pode ver, eu comentei a inicialização dos LoadBalancers aqui no código local do IntelliJ..." 

📸 *[Mostre a tela do IntelliJ focando no trecho de código `LocalTest_Services.java` onde as linhas `new LoadBalancerProxy(...)` estão comentadas]*

🗣️ **Continue falando:**
> "...O meu Windows vai atuar apenas como o componente Source."

---

## 2. Mostrando as Máquinas Virtuais
*Aponte a câmera para os terminais do PowerShell.*

🗣️ **O que falar:** 
> "Para a execução distribuída, eu subi duas Máquinas Virtuais no VirtualBox rodando Ubuntu Server, ambas em rede Bridge. Aqui no terminal de cima..."

📸 *[Aponte para o PowerShell da VM2]*

🗣️ **Continue falando:**
> "...estou conectado via SSH na **VM2**, que tem o IP Final 15, rodando o **Server 1** na porta 2000. E aqui no terminal de baixo..."

📸 *[Aponte para o PowerShell da VM1]*

🗣️ **Continue falando:**
> "...estou na **VM1**, com o IP Final 16, rodando o **Server 2** na porta 3000."

---

## 3. Iniciando a Execução
*Aponte a câmera para você executando os comandos.*

🗣️ **O que falar:** 
> "Vou iniciar primeiro o Server 2, que é o destino final..." 
*📸 [Dê Enter no comando da VM1 e mostre a mensagem 'Server2 enabled']*

🗣️ **Continue falando:** 
> "...Agora o Server 1, que é o intermediário..."
*📸 [Dê Enter no comando da VM2 e mostre a mensagem 'Server1 enabled']*

🗣️ **Continue falando:** 
> "...Com os servidores prontos na rede, vou disparar o Source no IntelliJ." 
*📸 [Clique no botão Run do IntelliJ e mostre que ele começou a rodar]*

---

## 4. Mostrando o Tráfego em Tempo Real
*Aproxime a câmera e mostre os logs subindo nos terminais das VMs e no IntelliJ alternadamente.*

🗣️ **O que falar:** 
> "Aqui podemos ver claramente as requisições saindo do host Windows, passando pela rede até o Server 1 na VM2, sendo repassadas para o Server 2 na VM1, que por sua vez cria os serviços sob demanda e responde até a origem. Todo o tráfego está ocorrendo por rede real."

---

## 5. Conclusão e Resultados
*Espere o teste terminar. Quando a execução acabar, aponte a câmera para o console do IntelliJ onde saiu a tabela, e depois mostre o gráfico que abriu na tela.*

🗣️ **O que falar:** 
> "A execução finalizou com sucesso. Aqui no console temos o resultado do Teste-T validando os dados..."
*📸 [Mostre a tabela de resultados no IntelliJ]*

🗣️ **Continue falando:** 
> "...E aqui está o gráfico final. Podemos ver que o nosso Experimento prático executado nas VMs (linha verde) acompanhou quase perfeitamente a curva do Modelo Teórico SPN (linha azul). Conforme o número de serviços aumenta de 1 para 5, o Tempo de Resposta cai como esperado, provando que o sistema distribuído e o balanceamento de carga estão funcionando e o modelo está validado."
