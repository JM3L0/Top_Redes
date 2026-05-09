# Remoção de ligação com repositório Git
_Exported on 5/9/2026 at 17:14:34 GMT-3 from Cursor (3.3.27)_

---

**User**

a pasta @pasid-validator-main tem ligação com um repositorio do git, remova essa ligação

---

**Cursor**

Vou desvincular a pasta `pasid-validator-main` do Git removendo os metadados de repositório dela (sem apagar seu código). Primeiro vou verificar se ela tem um `.git` próprio e, em seguida, remover essa pasta oculta.

Encontrei o ponto: a pasta `pasid-validator-main` **não é um repositório Git próprio**, ela só aparece ligada porque está dentro do repositório pai (`Top_Redes`). Vou desvincular isso fazendo o Git do projeto pai ignorar essa pasta.

Removi a ligação da pasta `pasid-validator-main` com o Git **do repositório pai**.

O que fiz:
- Adicionei `Trabalho 4/pasid-validator-main/` em `.git/info/exclude` do repo `Top_Redes`.
- Validei com `git check-ignore` que ela está sendo ignorada.
- `git status` não mostra mais essa pasta.

Resultado: o conteúdo da pasta continua intacto, mas o Git não monitora mais nada dentro dela nesse repositório.

Se você quiser, também posso te orientar a transformar essa pasta em um projeto totalmente independente (fora do repo `Top_Redes`).

---

**User**

ok, obrigado

---

**Cursor**

Perfeito! Se quiser, posso também verificar rapidamente se há mais alguma pasta em `Trabalho 4` ainda sendo rastreada pelo Git.

---

**User**

seguinte, preciso de ajuda urgente com um trabalho @TRABALHO 04 - VALIDAÇÃO (1).pdf  esse é o trabalho, falta a etapa de rodar o pasid validador porem não sei como fazer isso, estou lhe mandando o manual que o professor passou @MANUAL DO PASID-VALIDATOR.docx.pdf preciso que você olhe toda a pasta @pasid-validator-main entenda como funciona e me explique como fazer o que eu preciso para o meu trabalho e como fazer, monte um panho e veja toda a estrutura do projeto, olhe se o modelo ja esta la (o professor falou que era o que tava na pasta teste)
quero que sejá minuncioso para entender completamente como o pasid validaor funciona 

---

**Cursor**

Perfeito — vou analisar o manual, o PDF do trabalho e toda a estrutura do `pasid-validator-main` para te entregar um guia completo de execução (incluindo checar se o modelo da pasta de teste já está pronto). Começo mapeando os arquivos e os pontos de entrada do validador.

Achei um ponto importante: o `README.md` está genérico e não explica uso. Agora vou extrair o funcionamento diretamente do código (`src/domain` e `src/tests`) e cruzar com o manual/PDF para montar o passo a passo exato para você executar.

Já confirmei que existe um cenário de validação pronto em `src/tests/validation` (com `source.properties` e dois load balancers). Agora vou checar os arquivos de modelo (`model.xml`, `DP.csv`) e os outros testes para confirmar se o “modelo da pasta teste” já está disponível para o seu trabalho.

Vou validar o que é executável agora no seu ambiente para te passar um roteiro realista (sem suposições): vou tentar compilar o projeto do jeito que está e identificar exatamente o que falta.

Perfeito, fiz uma análise completa do que está na sua pasta e já te passo o caminho exato para concluir a etapa do trabalho.

## O que eu verifiquei no seu projeto

- A estrutura principal está correta em `pasid-validator-main`:
  - `src/domain`: implementação dos componentes (`Source`, `LoadBalancerProxy`, `ServiceProxy`).
  - `src/tests/validation`: cenário de experimento local (`LocalTest_Services` + arquivos `.properties`).
  - `src/tests/model`: execução do modelo SPN (`MercuryCall_Services` + `model.xml`).
- Seu Java está ok: Java 11 instalado (`openjdk 11.0.30`).
- **Maven não está instalado** (não é bloqueante, dá para rodar pelo IntelliJ).
- Em `lib` existem: `commons-math3`, `xchart`, `json-simple`.
- **Falta o JAR do MercuryAuto** (esse é necessário para rodar `MercuryCall_Services`).
- Sobre o “modelo da pasta teste”:  
  - `src/tests/model/model.xml` **existe** (sim, o modelo já está lá).
  - `src/tests/model/graphs_services/DP.csv` existe.
  - `MRT.csv` não está presente agora (normal se o modelo ainda não foi executado nesta máquina).

## Como o PASID Validator funciona (visão completa)

Fluxo real do código:

1. `Source` gera requisições com timestamp.
2. Envia para `LoadBalancer1` (porta 2000).
3. `LoadBalancer1` distribui para pool de `ServiceProxy`.
4. Esses services encaminham para `LoadBalancer2` (porta 3000).
5. `LoadBalancer2` distribui para outro pool de `ServiceProxy`.
6. O último estágio devolve ao `Source` (porta 1000).
7. `Source` calcula MRT experimental e, no fim, gera gráfico + teste t comparando com o modelo.

Ponto importante:
- A variação de capacidade ocorre no **segundo load balancer** via mensagem:
  - `config;<qtdServices>;`
- Isso é disparado automaticamente pelo `Source` com base em `variatingServices.qtdServices`.

## O que você precisa fazer para o trabalho (passo a passo)

## 1) Preparar ambiente (uma vez)

1. Abrir o projeto no IntelliJ.
2. Definir SDK do projeto para Java 11.
3. Adicionar o JAR do MercuryAuto na pasta `lib` e também como dependência do módulo.
   - O manual já traz o link do JAR.
4. Confirmar que as classes compilam no IntelliJ.

Sem o MercuryAuto, a etapa do modelo (etapa 2) não roda.

## 2) Etapa 1 — Feeding (coletar tempos intermediários)

Arquivo: `src/tests/validation/source.properties`

- Trocar:
  - `modelFeedingStage=true`

Depois:
- Rodar `tests.validation.LocalTest_Services` no IntelliJ.

Saída esperada no console:
- Linhas do tipo `T1 = ...`, `T2 = ...`, etc.
- Esses valores alimentam as transições do seu `model.xml`.

## 3) Etapa 2 — Rodar modelo SPN

Classe:
- `tests.model.MercuryCall_Services`

Ela usa:
- `src/tests/model/model.xml`
- gera saídas em `src/tests/model/graphs_services` (incluindo `MRT.csv`).

Depois de rodar:
- A própria classe imprime no console algo como:
  - `variatingServices.qtdServices=...`
  - `mrtsFromModel=...`
  - `sdvsFromModel=...`

Copie esses 3 vetores para `src/tests/validation/source.properties`.

## 4) Etapa 3 — Validação experimental

Arquivo: `src/tests/validation/source.properties`

- Voltar para:
  - `modelFeedingStage=false`
- Garantir que os vetores de modelo (`mrtsFromModel`, `sdvsFromModel`) estejam preenchidos com os valores da etapa 2.
- Rodar novamente `tests.validation.LocalTest_Services`.

Resultado:
- O `Source` coleta MRT experimental por ciclo.
- Compara modelo x experimento.
- Gera gráfico de linha (MRT vs quantidade de services).
- Imprime tabela de teste t no console.

## 5) Etapa 4 — Comparação para o artigo

No seu texto, você usa:
- Tabela de parâmetros (properties + tempos).
- Tabela hardware/software.
- Tabela modelo vs experimento + teste t.
- Gráfico de linhas final.

## Ajustes para bater exatamente seu enunciado

Seu enunciado pede **5 pontos no eixo X**.  
Hoje o seu `source.properties` está com 4 pontos:

- `variatingServices.qtdServices=1,2,3,4`

Você deve usar 5 valores (ex.: `1,2,3,4,5`) **e** garantir que:
- `mrtsFromModel` tenha 5 valores
- `sdvsFromModel` tenha 5 valores

Todos com o mesmo tamanho.

## Onde está o “coração” da validação

- `tests.validation.LocalTest_Services`: orquestra tudo localmente.
- `domain.Source`: gera carga, envia configuração de ciclo, calcula MRT experimental e compara com o modelo.
- `domain.LoadBalancerProxy`: recebe requisições e distribui para services.
- `domain.ServiceProxy`: simula tempo de serviço e encaminha.
- `domain.utils.LinePlot`: gera gráfico e calcula/mostra teste t.

## Diagnóstico final para sua urgência

Você está muito perto de rodar tudo.  
O bloqueio real agora é só este:

- **adicionar o JAR MercuryAuto na `lib` e no classpath do IntelliJ**.

Depois disso, o pipeline completo roda.

Se você quiser, no próximo passo eu te guio **clicando em cada menu do IntelliJ** (sem pular nada) para:
1) adicionar o JAR,  
2) configurar `source.properties` para cada etapa,  
3) executar as classes na ordem certa e validar a saída final do seu trabalho.

---

**User**

eu poderia fazer aqui no cursor mesmo?

---

**Cursor**

Sim, **pode fazer no Cursor**.

Você só precisa de 2 coisas no ambiente:
- Java 11 (você já tem).
- JAR do MercuryAuto na `lib` + classpath do projeto.

### O que dá para rodar no Cursor agora
- `LocalTest_Services` (etapa 1 e etapa 3) roda via terminal `javac/java`.
- A etapa 2 (`MercuryCall_Services`) só roda quando o JAR do MercuryAuto estiver disponível.

### Fluxo prático no Cursor

1. Coloque o JAR do MercuryAuto em `pasid-validator-main/lib`.
2. No terminal do Cursor, dentro de `pasid-validator-main`, compile:
   - `javac -encoding UTF-8 -cp "lib/*" -d out src/domain/*.java src/domain/utils/*.java src/tests/validation/*.java src/tests/model/*.java`
3. Rode:
   - Etapa 1 ou 3: `java -cp "out;lib/*" tests.validation.LocalTest_Services`
   - Etapa 2: `java -cp "out;lib/*" tests.model.MercuryCall_Services`

No Windows PowerShell, o separador de classpath é `;` (como acima).

Se quiser, eu te acompanho agora em tempo real e te digo exatamente o próximo comando em cada etapa (feeding → modelo → validação).

---

**User**

não entendi ainda o que eu preciso do mercuryauto, me explique melhor 

---

**Cursor**

O MercuryAuto é a **biblioteca que executa o modelo SPN** (`model.xml`).  
Sem ele, você consegue rodar o experimento “real” (Source/LBs/services), mas **não consegue gerar os resultados do modelo** para comparar.

## Em termos simples

Seu trabalho tem 2 lados:

- **Lado A (experimento real/sintético):** classes `Source`, `LoadBalancerProxy`, `ServiceProxy`  
  -> isso roda sem MercuryAuto.
- **Lado B (modelo analítico SPN):** classe `MercuryCall_Services` + `model.xml`  
  -> isso **depende do MercuryAuto**.

A validação exige comparar A vs B.  
Então, sem MercuryAuto, falta metade da validação.

## Onde isso aparece no código

A classe `tests.model.MercuryCall_Services` importa classes assim:

- `org.ufpi.mercurycall.util.facade.general.GeneralEvaluationLinePlotNonAbsorbingModel`
- `org.ufpi.mercurycall.util.facade.utils.EssentialParametersGroup`
- etc.

Essas classes **não existem no seu projeto**; elas vêm do JAR do MercuryAuto.  
Por isso a compilação falha com “package ... does not exist”.

## O que o MercuryAuto te entrega na prática

Quando você roda `MercuryCall_Services`, ele:

1. Lê `src/tests/model/model.xml`.
2. Resolve/simula o modelo SPN.
3. Gera CSVs/saídas do modelo (ex.: `MRT.csv`).
4. Imprime os vetores para você colar em `source.properties`:
   - `variatingServices.qtdServices=...`
   - `mrtsFromModel=...`
   - `sdvsFromModel=...`

Esses vetores são usados na etapa final para comparar com o experimento.

## Resumo direto

- **Precisa do MercuryAuto?** Sim, para a etapa do modelo (etapa 2).
- **Sem ele:** dá para rodar só feeding/experimento, mas não fecha a validação completa.
- **Com ele:** você consegue gerar os números do modelo e concluir o trabalho corretamente.

Se quiser, te passo agora exatamente como adicionar o JAR no Cursor e já testar com um comando curto para confirmar que ele foi reconhecido.

---

**User**

então deixe-me ver se eu entendi eu vou ter que criar o meu modelo rodar no mercury auto pegar o ponto jar dele e trazer para o base de validator?

---

**Cursor**

Quase isso, com um ajuste importante:

- Você **não precisa criar o JAR do MercuryAuto**.
- Você só precisa **baixar o JAR pronto do MercuryAuto** (link do manual) e colocar em `pasid-validator-main/lib`.

O fluxo correto é:

1. Usar o modelo que já está em `src/tests/model/model.xml` (ou adaptar para seu cenário).
2. Adicionar o JAR do MercuryAuto no projeto.
3. Rodar `MercuryCall_Services` para obter `mrtsFromModel` e `sdvsFromModel`.
4. Colar esses valores em `src/tests/validation/source.properties`.
5. Rodar `LocalTest_Services` para a validação experimental e comparação.

Então, resumindo em uma frase:  
você vai **usar** o MercuryAuto como dependência do validator, não “construir” o MercuryAuto.

---

**User**

@MANUAL DO PASID-VALIDATOR.docx.pdf como rodar, me dê o paso a passo detalhado

---

**Cursor**

Segue um **passo a passo detalhado** alinhado ao manual e ao que o seu projeto realmente faz.

---

## Pré-requisitos

1. **Java 11**  
   O manual recomenda Zulu 11 com JavaFX (`zulu11.68.17-ca-fx-jdk11.0.21`). No seu PC já apareceu Temurin 11 — em geral funciona; se o MercuryAuto reclamar de JavaFX, use a Zulu indicada no manual.

2. **Projeto**  
   Pasta base: `pasid-validator-main`.

3. **MercuryAuto (obrigatório para a etapa do modelo)**  
   - Baixe o JAR do link do manual (Google Drive).  
   - Coloque o arquivo em:  
     `pasid-validator-main\lib\`  
   - No **IntelliJ**: *File → Project Structure → Libraries* → adicione esse JAR.  
   - No **Cursor (só terminal)**: use `-cp "out;lib\*"` incluindo o novo `.jar` na pasta `lib`.

---

## Visão geral das 4 etapas (como no manual)

| Etapa | O quê | Onde |
|--------|--------|------|
| 1 | Coleta de tempos para **alimentar** o modelo (feeding) | `source.properties` + `LocalTest_Services` |
| 2 | **Rodar o modelo SPN** e obter MRT (média/desvio) | `MercuryCall_Services` + `model.xml` |
| 3 | **Rodar o experimento** variando serviços | `source.properties` + `LocalTest_Services` |
| 4 | **Comparar** modelo × experimento (teste t, gráfico) | Automático ao terminar a etapa 3 |

---

## Etapa 1 — Execução experimental de coleta (feeding)

**Objetivo:** obter `T1, T2, T3…` para colocar nas transições do `model.xml` no Mercury/MercuryAuto.

1. Abra:  
   `pasid-validator-main\src\tests\validation\source.properties`

2. Defina:  
   `modelFeedingStage=true`

3. **Ordem de subida dos componentes** (no código de teste local isso já está na classe `LocalTest_Services`):
   - Primeiro o load balancer da porta **3000** (`loadbalancer2.properties`),
   - Depois o da porta **2000** (`loadbalancer1.properties`),
   - Por último o `Source` (lê a pasta onde está o `source.properties`).

4. Execute a classe:  
   `tests.validation.LocalTest_Services`  
   (Run no IntelliJ, ou compile e rode pelo terminal se preferir.)

5. **Saída esperada:** no console, algo como:  
   `The times to feed the models transitions are following:`  
   `T1 = ...`, `T2 = ...`, etc.

6. **Use esses valores** para ajustar os tempos das transições correspondentes no `model.xml` (no Mercury/MercuryAuto, conforme o professor ensinou — o manual diz que esses são os tempos intermediários do modelo).

7. O processo costuma encerrar com `System.exit` após processar as mensagens de feeding.

---

## Etapa 2 — Execução do modelo (MercuryAuto)

**Objetivo:** gerar `mrtsFromModel` e `sdvsFromModel` para colar no `source.properties`.

1. Garanta que o **JAR do MercuryAuto** está em `lib` e no classpath do projeto.

2. Abra e, se precisar, confira:  
   `pasid-validator-main\src\tests\model\MercuryCall_Services.java`  
   Ele aponta para `src/tests/model/`, arquivo `model.xml`, parâmetros `AD`, `C`, pasta de gráficos `graphs_services`.

3. Execute:  
   `tests.model.MercuryCall_Services`

4. **Saída:**  
   - Gráficos/CSVs em `src\tests\model\graphs_services\` (ex.: `MRT.csv`).  
   - No console, linhas no formato que o manual mostra, por exemplo:  
     `variatingServices.qtdServices=1,2,3,4`  
     `mrtsFromModel=...`  
     `sdvsFromModel=...`

5. **Copie exatamente** essas três linhas (ou ajuste a lista de serviços se o trabalho pedir **5 pontos** no eixo X — veja nota abaixo).

---

## Etapa 3 — Execução experimental para validação

**Objetivo:** medir MRT no “sistema” (simulado pelos proxies) para cada quantidade de serviços.

1. Abra de novo:  
   `src\tests\validation\source.properties`

2. Defina:  
   `modelFeedingStage=false`

3. **Cole** (ou mantenha, se já bater com o modelo) os valores que saíram da etapa 2:  
   - `variatingServices.qtdServices=...`  
   - `mrtsFromModel=...`  
   - `sdvsFromModel=...`  
   Os três vetores devem ter o **mesmo número de valores** (um MRT e um SD por cada ponto do eixo X).

4. Confira se os `.properties` dos load balancers batem com o cenário (IPs `localhost`, portas 2000 / 3000 / 1000, tempos de serviço, etc.), alinhados ao que você modelou.

5. Execute de novo:  
   `tests.validation.LocalTest_Services`  
   (mesma ordem: LB2 → LB1 → Source.)

6. O `Source` vai, para cada valor em `qtdServices`, mandar `config;N;` ao load balancer variável, disparar as requisições e ir acumulando respostas.

---

## Etapa 4 — Comparação (modelo × experimento)

Isso **não é um passo separado** no código: ao concluir os ciclos (ou após o timeout interno), o validador:

- Gera o **gráfico de linhas** (pasta `graphs` relativa ao diretório de trabalho do processo),
- Imprime no console uma **tabela em LaTeX** com médias, desvios, **t** e **p** (teste t de duas amostras), como descrito no manual.

Use esse material no artigo (tabelas + gráfico).

---

## Nota sobre o **trabalho** (5 pontos no eixo X)

O PDF do trabalho pede **5 pontos** no eixo X (quantidade de services). No exemplo do manual/propriedades costuma aparecer `1,2,3,4`. Para bater com o enunciado:

- Em `MercuryCall_Services`, onde monta o vetor de `C`, inclua **5 valores** (ex.: `1,2,3,4,5`).
- Rode de novo o modelo e atualize `source.properties` com **5** MRTs e **5** SDs.
- O experimento seguirá a mesma lista em `variatingServices.qtdServices`.

---

## Observação do manual sobre “teste local”

O manual diz que `LocalTest_Services` é **ilustrativo** e que o ideal é rodar **distribuído** (VMs/containers). Para a entrega com **vídeo distribuído**, você sobe **o mesmo trio de processos** em máquinas diferentes, trocando `localhost` pelos IPs reais nos três arquivos `.properties`. A lógica das etapas 1–4 é a mesma.

---

## Resumo em uma frase

**Feeding** (`modelFeedingStage=true`) → ajustar `model.xml` → **MercuryAuto** (`MercuryCall_Services`) → copiar MRT/SD para `source.properties` → **validação** (`modelFeedingStage=false`, `LocalTest_Services`) → usar gráfico e tabela do teste t no artigo.

Se quiser, no próximo passo você diz se vai usar **IntelliJ** ou **só terminal no Cursor** que eu monto os comandos exatos (compile + `java -cp ...`) para o seu Windows.

---

**User**

como eu faço o passo de adicionar @pasid-validator-main/lib/mercuryauto.jar na lib?

---

**Cursor**

Você faz em **duas partes**: (1) o arquivo estar na pasta `lib`; (2) o projeto **enxergar** esse JAR no classpath.

---

### 1) Colocar o JAR na pasta `lib`

1. Baixe o `mercuryauto.jar` (link do manual).
2. Copie o arquivo para:
   ```text
   pasid-validator-main\lib\mercuryauto.jar
   ```
Pelos seus arquivos recentes, **isso já parece feito** — o nome pode ser `mercuryauto.jar` ou outro; o importante é estar **dentro** de `lib`.

---

### 2) “Adicionar na lib” no IntelliJ (classpath)

Só copiar para `lib` **não** adiciona sozinho no IntelliJ. Faça:

1. **File → Project Structure…** (ou `Ctrl+Alt+Shift+S`).
2. **Libraries** (lado esquerdo).
3. **+** → **Java**.
4. Navegue até `pasid-validator-main\lib\mercuryauto.jar` → **OK**.
5. Quando perguntar o módulo, marque **pasid-validator** (ou o módulo do projeto) → **OK** → **Apply** → **OK**.

Assim o `MercuryCall_Services` compila e roda com as classes `org.ufpi.mercurycall...`.

---

### 3) Se você for rodar só pelo terminal (Cursor), sem IntelliJ

Não precisa “cadastrar” em lugar nenhum: inclua o JAR no classpath:

```powershell
cd "c:\Users\jsous\OneDrive\Área de Trabalho\Top_Redes\Trabalho 4\pasid-validator-main"
javac -encoding UTF-8 -cp "lib\*" -d out (Get-ChildItem -Path src -Recurse -Filter *.java | ForEach-Object { $_.FullName })
java -cp "out;lib\*" tests.model.MercuryCall_Services
```

O `lib\*` já pega `mercuryauto.jar` junto com os outros JARs.

---

**Resumo:** “adicionar na lib” = **arquivo em `lib\` + marcar o JAR como Library no IntelliJ** (ou usar `-cp "lib\*"` no `javac`/`java`).

---

**User**

o que marcar aqui?

---

**Cursor**

Nesse menu **“Mark Directory As”** o que importa para o seu projeto é o seguinte:

### Pasta `src` (a raiz onde estão `domain` e `tests`)

Marque como **Sources Root** (pasta azul de código-fonte).

- **Não** marque `src` inteira como **Test Sources Root** (verde). Isso é para testes no estilo JUnit; aqui o `tests` é código Java “normal” que chama `main` e precisa compilar junto com `domain`.

Se no submenu só aparecem *Test Sources Root*, *Resources*, etc., é porque **`src` já está como Sources Root**. Nesse caso você **não precisa mudar nada** — ou use **Unmark as Sources Root** só se quiser reconfigurar do zero (geralmente não é necessário).

### Subpastas (`domain`, `tests`, …)

Deixe **dentro** de `src` sem marcar cada uma separadamente: com `src` como **Sources Root**, o IntelliJ já trata tudo como fonte.

### Pasta `lib` (com `mercuryauto.jar`)

**Não** use “Mark Directory As” na `lib`.  
O JAR entra em **File → Project Structure → Libraries → + → Java** e você escolhe o `mercuryauto.jar`.

### Quando usar **Resources Root**

Só faria sentido se você quisesse carregar `.properties` pelo **classpath** (`getResource`). No seu caso o `LocalTest_Services` usa caminho em disco (`src/tests/validation/`), então **Resources Root não é obrigatório** para rodar.

**Resumo:** em `src`, o certo é **Sources Root**; `mercuryauto.jar` vai por **Libraries**, não por “Mark Directory As”.

---

**User**

qual o provimo passo

---

**Cursor**

Assumindo que o `mercuryauto.jar` já está em `lib` e o `src` está como **Sources Root**, o próximo passo é fechar a configuração e **começar a etapa 1 do manual**.

### Próximo passo imediato

1. **Confirmar o JAR no IntelliJ**  
   **File → Project Structure → Libraries** → veja se `mercuryauto.jar` aparece. Se não aparecer: **+ → Java** → selecione o arquivo em `lib`.

2. **Rodar a etapa de feeding (coleta de tempos T1, T2, …)**  
   - Abra `src/tests/validation/source.properties`  
   - Coloque: `modelFeedingStage=true`  
   - Execute a classe **`tests.validation.LocalTest_Services`** (Run).

3. **Anote a saída** no console (`T1 = ...`, `T2 = ...`, etc.) e use isso para ajustar as transições no **`model.xml`** (como o manual descreve).

Depois disso, o passo seguinte será: **`modelFeedingStage=false`**, rodar **`tests.model.MercuryCall_Services`**, copiar `mrtsFromModel` / `sdvsFromModel` para o `source.properties`, e rodar de novo o **`LocalTest_Services`** para a validação.

Se você me disser se o JAR já está em **Libraries** ou só na pasta `lib`, eu te digo só **um** próximo passo (só o que falta).

---

**User**

Execute a classe tests.validation.LocalTest_Services

onde esta isso?

---

**Cursor**

A classe está neste arquivo:

**Caminho no disco**

`pasid-validator-main\src\tests\validation\LocalTest_Services.java`

Ou seja: pasta **`src` → `tests` → `validation` →** arquivo **`LocalTest_Services.java`**.

O nome completo da classe é `tests.validation.LocalTest_Services` porque o pacote no topo do `.java` é `package tests.validation;`.

---

### Como executar no IntelliJ

1. Abra o **Project** (árvore de pastas à esquerda).
2. Vá em **`src` → `tests` → `validation`**.
3. Clique em **`LocalTest_Services.java`**.
4. Clique com o botão direito no arquivo (ou no ícone verde ao lado do `main`) → **Run 'LocalTest_Services.main()'**.

Ou use **Ctrl+Shift+N** (Go to File), digite `LocalTest_Services`, abra o arquivo e use o botão **Run** na linha do `public static void main`.

---

**Importante:** o **Working Directory** do run configuration deve ser a raiz do projeto **`pasid-validator-main`** (onde o código monta caminhos como `src/tests/validation/`). No IntelliJ isso costuma ser o padrão ao rodar pela classe; se der erro de arquivo não encontrado, em **Run → Edit Configurations → Working directory** coloque o caminho completo da pasta `pasid-validator-main`.

---

**User**

C:\Users\jsous\.jdks\openjdk-26.0.1\bin\java.exe "-javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2026.1\lib\idea_rt.jar=52728" -Dfile.encoding=UTF-8 -Dsun.stdout.encoding=UTF-8 -Dsun.stderr.encoding=UTF-8 -classpath "C:\Users\jsous\OneDrive\Área de Trabalho\Top_Redes\Trabalho 4\out\test\Trabalho 4;C:\Users\jsous\OneDrive\Área de Trabalho\Top_Redes\Trabalho 4\out\production\Trabalho 4;C:\Users\jsous\OneDrive\Área de Trabalho\Top_Redes\Trabalho 4\pasid-validator-main\lib\mercuryauto.jar" tests.validation.LocalTest_Services
Exception in thread "main" java.lang.RuntimeException: Error reading properties file
	at domain.LoadBalancerProxy.<init>(LoadBalancerProxy.java:61)
	at tests.validation.LocalTest_Services.executeStage(LocalTest_Services.java:25)
	at tests.validation.LocalTest_Services.main(LocalTest_Services.java:16)
Caused by: java.io.FileNotFoundException: C:\Users\jsous\OneDrive\Área de Trabalho\Top_Redes\Trabalho 4\src\tests\validation\loadbalancer2.properties (O sistema não pode encontrar o caminho especificado)
	at java.base/java.io.FileInputStream.open0(Native Method)
	at java.base/java.io.FileInputStream.open(FileInputStream.java:185)
	at java.base/java.io.FileInputStream.<init>(FileInputStream.java:139)
	at java.base/java.io.FileInputStream.<init>(FileInputStream.java:109)
	at domain.LoadBalancerProxy.<init>(LoadBalancerProxy.java:58)

rodei e deu isso

---

**Cursor**

O erro não é do Java em si: o programa está procurando os `.properties` **no lugar errado**.

Ele monta o caminho assim: **`user.dir` + `src/tests/validation/`**.  
No seu caso, `user.dir` é a pasta **`Trabalho 4`**, então ele busca:

`...\Trabalho 4\src\tests\validation\loadbalancer2.properties`

Mas os arquivos estão em:

`...\Trabalho 4\pasid-validator-main\src\tests\validation\`

---

## O que fazer (recomendado)

**Ajustar o diretório de trabalho da execução** para a raiz do validador:

1. No IntelliJ: **Run → Edit Configurations…**
2. Selecione a configuração de **`LocalTest_Services`**.
3. Em **Working directory**, coloque exatamente:

   `C:\Users\jsous\OneDrive\Área de Trabalho\Top_Redes\Trabalho 4\pasid-validator-main`

4. **Apply** → **OK** → rode de novo.

Assim `user.dir` vira `pasid-validator-main` e o caminho `src/tests/validation/loadbalancer2.properties` passa a existir.

---

## Alternativa (estrutura do projeto)

Abrir/importar o projeto com a pasta **`pasid-validator-main`** como raiz do módulo (em vez de `Trabalho 4`), para o working directory padrão já ser o certo.

---

## Observação extra

O log mostra **`openjdk-26.0.1`**. O manual pede **Java 11** (Zulu 11). Para o **MercuryAuto** pode dar problema com Java 26. Se depois aparecer erro estranho no modelo, mude o **SDK** da run configuration (e do projeto) para **11**.

Depois de corrigir o working directory, rode de novo; se aparecer outra mensagem, manda o stack trace.

---

**User**

como mudar a versão JDK no intelij

---

**Cursor**

No IntelliJ você muda o JDK em **dois lugares** que importam: o **projeto/módulo** e a **configuração de execução**.

---

### 1) Instalar o JDK (se ainda não tiver o 11)

Baixe e instale o JDK 11 (o manual indica Zulu 11 com JavaFX). Depois siga os passos abaixo.

---

### 2) Registrar o JDK no IntelliJ

**File → Settings** (ou **Ctrl+Alt+S**) → **Build, Execution, Deployment → Build Tools** não — o caminho correto é:

**File → Settings → Build, Execution, Deployment → Build Tools →** (às vezes o JDK fica em outro lugar)

Na verdade no IntelliJ moderno:

**File → Project Structure** (`Ctrl+Alt+Shift+S`) → **Platform Settings → SDKs**  
- Clique **+** → **Add JDK…**  
- Aponte para a pasta de instalação do JDK 11 (ex.: `C:\Program Files\Java\jdk-11` ou Zulu).

---

### 3) Usar JDK 11 no projeto

**File → Project Structure** (`Ctrl+Alt+Shift+S`)

- Aba **Project**  
  - **SDK:** escolha **11**  
  - **Language level:** deixe alinhado (ex.: **11**)

- Aba **Modules**  
  - Selecione seu módulo **Trabalho 4** (ou o que for)  
  - Aba **Dependencies** (ou **Sources**): em **Module SDK** escolha **11**

**Apply → OK**

---

### 4) Usar JDK 11 ao rodar o programa

**Run → Edit Configurations…**  
- Selecione **LocalTest_Services** (e depois **MercuryCall_Services**, etc.)  
- **Modify options** (se aparecer) → marque **Add VM options** só se precisar  
- O importante: campo **JRE** ou **Runtime** → escolha **11** (ou “Project SDK” se o projeto já está em 11)

**Apply → OK**

---

### Atalho mental

- **Project Structure → Project SDK** = compila com qual Java.  
- **Run Configuration → JRE** = com qual Java o `main` roda (deve bater com o projeto, idealmente 11 para esse trabalho).

Se no **SDKs** não aparecer o 11, é porque o IntelliJ ainda não conhece essa instalação: use **Add JDK** e selecione a pasta do JDK 11.

---

**User**

ta to nessa tela 

---

**Cursor**

Você está no lugar certo (**Project → SDK**). Faça assim:

### 1) Trocar o SDK
1. Clique no campo **SDK** (hoje está `openjdk-26 Oracle OpenJDK 26.0.1`).
2. Na lista, escolha **11** se já aparecer (ex.: `11` ou `corretto-11`, `temurin-11`, `zulu-11`).

### 2) Se **não** aparecer JDK 11 na lista
1. No mesmo dropdown, clique em **Add SDK → Download JDK…** (ou **Add JDK…** se você já instalou o 11 no PC).
2. **Version:** **11**  
   **Vendor:** pode ser **Eclipse Temurin**, **Azul Zulu**, **Oracle**, etc.  
3. Confirme o download/instalação; o IntelliJ registra sozinho.
4. Volte ao campo **SDK** e selecione o **11** que acabou de ser adicionado.

### 3) Ajustar o Language level
1. Em **Language level**, mude de `26` para **11** (ou **SDK default** se essa opção existir e apontar para 11).

### 4) Aplicar
1. **Apply** → **OK**.

### 5) Conferir a execução
**Run → Edit Configurations…** → sua config do `LocalTest_Services` → **JRE** deve ser **Project SDK** (ou explicitamente 11).

Assim o projeto deixa de usar o 26 e passa a usar o 11, como o manual recomenda para o MercuryAuto.

---

**User**

ta assim

---

**Cursor**

Quase perfeito: o **SDK** já está certo (**ms-11 / 11.0.31**).

Só falta alinhar o **Language level**, que ainda está em **26** — isso não combina com o JDK 11 e pode gerar comportamento estranho.

### O que fazer

1. No mesmo campo **Language level**, abra o menu.
2. Escolha **11** (ou **SDK default**, se essa opção existir e estiver ligada ao 11).
3. Clique **Apply** → **OK**.

Assim projeto, compilador e linguagem ficam todos em Java 11.

**Depois:** em **Run → Edit Configurations…**, confira se o **JRE** da sua execução é **Project SDK** (ou **11**), para não rodar de novo com 26 por engano.

---

**User**

seria isso?

---

**Cursor**

Sim, **é isso** — ficou correto:

- **SDK:** `ms-11` (Java **11.0.31**)
- **Language level:** **11**
- **Compiler output:** pasta `out` do projeto **Trabalho 4** (ok)

Só não esqueça de:

1. **Run → Edit Configurations…** → na execução do `LocalTest_Services`, **JRE** = **Project SDK** (ou **11**).
2. **Working directory** =  
   `...\Trabalho 4\pasid-validator-main`  
   (para achar `src/tests/validation/*.properties`).

Com isso você pode rodar de novo o `LocalTest_Services`.

---

**User**

C:\Users\jsous\.jdks\ms-11.0.31\bin\java.exe "-javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2026.1\lib\idea_rt.jar=64802" -Dfile.encoding=UTF-8 -classpath "C:\Users\jsous\OneDrive\Área de Trabalho\Top_Redes\Trabalho 4\out\production\Trabalho 4;C:\Users\jsous\OneDrive\Área de Trabalho\Top_Redes\Trabalho 4\pasid-validator-main\lib\mercuryauto.jar" tests.validation.LocalTest_Services
Exception in thread "main" java.lang.RuntimeException: Error reading properties file
	at domain.LoadBalancerProxy.<init>(LoadBalancerProxy.java:61)
	at tests.validation.LocalTest_Services.executeStage(LocalTest_Services.java:25)
	at tests.validation.LocalTest_Services.main(LocalTest_Services.java:16)
Caused by: java.io.FileNotFoundException: C:\Users\jsous\OneDrive\Área de Trabalho\Top_Redes\Trabalho 4\src\tests\validation\loadbalancer2.properties (O sistema não pode encontrar o caminho especificado)
	at java.base/java.io.FileInputStream.open0(Native Method)
	at java.base/java.io.FileInputStream.open(FileInputStream.java:219)
	at java.base/java.io.FileInputStream.<init>(FileInputStream.java:157)
	at java.base/java.io.FileInputStream.<init>(FileInputStream.java:112)
	at domain.LoadBalancerProxy.<init>(LoadBalancerProxy.java:58)
	... 2 more

Process finished with exit code 1

ta, me ajude aqui

C:\Users\jsous\.jdks\ms-11.0.31\bin\java.exe "-javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2026.1\lib\idea_rt.jar=64802" -Dfile.encoding=UTF-8 -classpath "C:\Users\jsous\OneDrive\Área de Trabalho\Top_Redes\Trabalho 4\out\production\Trabalho 4;C:\Users\jsous\OneDrive\Área de Trabalho\Top_Redes\Trabalho 4\pasid-validator-main\lib\mercuryauto.jar" tests.validation.LocalTest_Services
Exception in thread "main" java.lang.RuntimeException: Error reading properties file
	at domain.LoadBalancerProxy.<init>(LoadBalancerProxy.java:61)
	at tests.validation.LocalTest_Services.executeStage(LocalTest_Services.java:25)
	at tests.validation.LocalTest_Services.main(LocalTest_Services.java:16)
Caused by: java.io.FileNotFoundException: C:\Users\jsous\OneDrive\Área de Trabalho\Top_Redes\Trabalho 4\src\tests\validation\loadbalancer2.properties (O sistema não pode encontrar o caminho especificado)
	at java.base/java.io.FileInputStream.open0(Native Method)
	at java.base/java.io.FileInputStream.open(FileInputStream.java:219)
	at java.base/java.io.FileInputStream.<init>(FileInputStream.java:157)
	at java.base/java.io.FileInputStream.<init>(FileInputStream.java:112)
	at domain.LoadBalancerProxy.<init>(LoadBalancerProxy.java:58)
	... 2 more

Process finished with exit code 1


me ajude aqui

---

**Cursor**

O erro ocorre porque `user.dir` é `Trabalho 4`, mas os `.properties` estão em `pasid-validator-main\src\tests\validation\`. Corrigindo o código para procurar nesses dois locais, funciona independentemente do diretório de trabalho.



Ajustando `LocalTest_Services` para localizar automaticamente a pasta `validation` (funciona com `user.dir` = `Trabalho 4` ou `pasid-validator-main`).



O problema era só o **diretório atual**: o IntelliJ usa `Trabalho 4` como raiz, mas os `.properties` ficam em `Trabalho 4\pasid-validator-main\src\tests\validation\`.

Atualizei o `LocalTest_Services` para tentar, nesta ordem:

1. `user.dir\src\tests\validation\`  
2. `user.dir\pasid-validator-main\src\tests\validation\`

Assim roda **sem precisar mudar** o *Working directory* da run configuration.

**O que você faz agora**

1. Salve o arquivo (se o IntelliJ não tiver puxado a alteração, copie a lógica ou atualize o projeto).
2. **Build → Rebuild Project** (ou rode de novo; o IDE costuma recompilar).
3. Execute de novo **`LocalTest_Services`**.

Se ainda der erro do tipo `Could not find ...`, diga se a pasta do código no disco é mesmo `...\Trabalho 4\pasid-validator-main\...` (nome da pasta tem que bater com `pasid-validator-main` no código).

---

**Alternativa só no IntelliJ (sem mudar código):**  
*Run → Edit Configurations…* → **Working directory** =  
`C:\Users\jsous\OneDrive\Área de Trabalho\Top_Redes\Trabalho 4\pasid-validator-main`  

Com o patch no código, os dois jeitos funcionam.

---

**User**

C:\Users\jsous\.jdks\ms-11.0.31\bin\java.exe "-javaagent:C:\Program Files\JetBrains\IntelliJ IDEA 2026.1\lib\idea_rt.jar=51437" -Dfile.encoding=UTF-8 -classpath "C:\Users\jsous\OneDrive\Área de Trabalho\Top_Redes\Trabalho 4\out\production\Trabalho 4;C:\Users\jsous\OneDrive\Área de Trabalho\Top_Redes\Trabalho 4\pasid-validator-main\lib\mercuryauto.jar" tests.validation.LocalTest_Services
======================================
Load Balancer Parameters:
Load Balancer Name: Server2
Local Port: 3000
Queue Load Balancer Max Size: 100
Qtd Services List: [4]
======================================
Starting service3001
Starting service3003
Starting service3002
Starting service3004
Starting Server2
======================================
Load Balancer Parameters:
Load Balancer Name: Server1
Local Port: 2000
Queue Load Balancer Max Size: 100
Qtd Services List: [4]
======================================
Starting service2001
Starting service2003
Starting service2004
Starting service2002
Starting Server1
Server2 enabled to receive messages.
service2003 enabled to receive messages.
service2002 enabled to receive messages.
service2001 enabled to receive messages.
service2004 enabled to receive messages.

======================================
Source Parameters:
jsonPath: C:/Users/jsous/OneDrive/Área de Trabalho/Top_Redes/Trabalho 4/pasid-validator-main/src/tests/validation/
maxConsideredMessagesExpected: 500
mrtsFromModel: [405597.23, 203892.96, 136603.74, 102902.92]
sdvsFromModel: [1245.97, 613.95, 400.11, 313.47]
arrivalDelay: 100
qtdServices: [1, 2, 3, 4]
======================================
service3004 enabled to receive messages.
service3003 enabled to receive messages.
service3002 enabled to receive messages.
service3001 enabled to receive messages.
Server2 enabled to receive messages.
Server2 enabled to receive messages.
Server2 enabled to receive messages.
source enabled to receive messages.
Server1 enabled to receive messages.
source enabled to receive messages.
source enabled to receive messages.
source enabled to receive messages.
Starting source
ATTENTION: Guarantee that arrival delay is a higher value then the sum of all service times.
##############################
Model Feeding Stage Started
##############################
Only 10 requests will be generated with AD = 2000ms
1;0;1778354891224;1778354891316;92;1778354891374;1778354891442;68;1778354891448;1778354891567;119;1778354891567;1778354891570;3;1778354891586;1778354893602;2016;RESPONSE TIME:;2378;
1;1;1778354895334;1778354895335;1;1778354895335;1778354895359;24;1778354895359;1778354895467;108;1778354895467;1778354895470;3;1778354895470;1778354897525;2055;RESPONSE TIME:;2191;
1;2;1778354899368;1778354899370;2;1778354899370;1778354899375;5;1778354899375;1778354899523;148;1778354899523;1778354899578;55;1778354899580;1778354901621;2041;RESPONSE TIME:;2253;
The times to feed the models transitions are the following:
T1 = 31.666666666666668
T2 = 32.333333333333336
T3 = 125.0
T4 = 20.333333333333332
T5 = 2037.3333333333333

Process finished with exit code 0


ta, agora deu isso

---

**Cursor**

Isso é **sucesso**: a **etapa 1 (feeding)** rodou até o fim e o processo terminou com **exit code 0**.

### O que significa a saída

- **`Model Feeding Stage Started`** com **`AD = 2000ms`**: o `Source` enviou **10** requisições espaçadas para medir tempos intermediários.
- As linhas longas com muitos `;` são as mensagens com **timestamps** em cada hop (load balancers, serviços, volta ao source).
- No final:

  - **T1 = 31.67…**  
  - **T2 = 32.33…**  
  - **T3 = 125.0**  
  - **T4 = 20.33…**  
  - **T5 = 2037.33…**

  São as **médias dos tempos intermediários** que o manual chama de valores para **alimentar as transições** do seu `model.xml` no Mercury/MercuryAuto (cada **T** corresponde a uma transição/etapa do modelo, conforme o professor mapeou no manual).

### Próximos passos (ordem do manual)

1. **Abrir o modelo** (`model.xml` no Mercury/MercuryAuto) e **colocar esses tempos** nas transições certas (T1…T5), como na disciplina costuma ser feito.
2. **Rodar** `tests.model.MercuryCall_Services` para gerar de novo **MRT + desvio** do modelo para cada valor de **C** (quantidade de serviços).  
   - Se você mudar tempos no modelo, os números vão mudar em relação aos que já estão hoje no `source.properties`.
3. **Copiar** do console (ou do `MRT.csv`) para o `source.properties`:
   - `variatingServices.qtdServices=...`
   - `mrtsFromModel=...`
   - `sdvsFromModel=...`
4. No `source.properties`, colocar **`modelFeedingStage=false`**.
5. **Rodar de novo** `LocalTest_Services` → aí entra a **validação** (experimentos × modelo, gráfico, teste t).

### Observação

No log ainda aparecem `mrtsFromModel` / `sdvsFromModel` antigos — isso é normal na etapa de feeding; eles só precisam estar **consistentes com o modelo depois** que você atualizar o `model.xml` com T1…T5.

Se quiser, no próximo passo você pode colar um print ou trecho do `MercuryCall_Services` / parâmetros **C** e eu te digo exatamente o que conferir antes de rodar o modelo.

---

**User**

ta, então o que eu preciso fazer agora para deixar que nem meu trabalho pede@TRABALHO 04 - VALIDAÇÃO (1).pdf ?

---

**Cursor**

Segue um roteiro **objetivo** alinhado ao que o **TRABALHO 04 - VALIDAÇÃO** pede (métrica MRT, artigo IEEE, tabelas, gráfico com **5 pontos**, teste t, vídeo distribuído) e ao que você já fez (feeding com T1…T5).

---

### 1) Modelo e parâmetros (SPN + Mercury)

- Pegue os tempos que saíram no feeding (**T1…T5**) e **atualize o `model.xml`** (transições correspondentes no Mercury/MercuryAuto), como no manual.
- No código **`MercuryCall_Services.java`**, o eixo que varia é **`C`** (quantidade de serviços no 2º balanceador). Hoje está com **4 pontos** (`1,2,3,4`). O trabalho pede **5 pontos no eixo x** → use **cinco valores**, por exemplo **`1,2,3,4,5`** (ou o conjunto que o professor aceitar), **no modelo e na avaliação** (`new Double[]{1.0,2.0,3.0,4.0,5.0}` ou similar).
- Rode **`MercuryCall_Services`**, gere de novo **MRT** (e desvios) e **atualize** o `source.properties` com **três listas do mesmo tamanho (5 itens)**:
  - `variatingServices.qtdServices=...`
  - `mrtsFromModel=...`
  - `sdvsFromModel=...`

---

### 2) Experimento (PASID Validator)

- Em **`source.properties`**:
  - **`modelFeedingStage=false`**
  - Confirme **`arrivalDelay`**, IPs/portas e **`maxConsideredMessagesExpected`** coerentes com o cenário (e com o **AD** usado no modelo, ex. 100 ms como no exemplo).
- Rode **`LocalTest_Services`** de novo → isso gera **MRT experimental**, **gráfico** e saída do **teste t** (no console / LaTeX).

---

### 3) Artigo (o que o PDF lista)

Inclua na seção de validação:

- **Algoritmo em pseudo-código** (ou link de repositório) do pipeline de **processamento de imagem** que justifica **média e desvio** do tempo de serviço do componente variado (tema: normalização/nitidez no servidor 1; busca por similares no 2).
- **Tabela de parâmetros** (AD, tempos de serviço, `C`, filas, etc. — espelhando `source.properties` + modelo).
- **Tabela hardware/software** (PCs ou containers, SO, Java 11, rede).
- **Tabela modelo × experimento** com **teste t de duas amostras** (use os números que o validador/Mercury gerarem; cite α = 0,05 se for o caso).
- **Gráfico de linhas**: eixo **x** = quantidade de **services** (**5 pontos**), eixo **y** = **MRT** (curva do modelo e do experimento, como o `LinePlot` faz).

---

### 4) Entrega com vídeo

- O manual diz que o teste local é ilustrativo; o trabalho pede **vídeo do sistema rodando distribuído**.
- Suba **Source**, **LoadBalancer1+serviços** e **LoadBalancer2+serviços** em **máquinas/VMs/containers** diferentes e troque **`localhost`** nos `.properties` pelos **IPs reais** (mesma topologia, só distribuída).
- Repita um ciclo de validação (ou mostre o fluxo completo) e grave a tela/celular.

---

### Ordem prática “agora”

1. Atualizar **`model.xml`** com **T1…T5**.  
2. Ajustar **`MercuryCall_Services`** para **5 valores de C** → rodar Mercury → atualizar **`source.properties`**.  
3. **`modelFeedingStage=false`** → rodar **`LocalTest_Services`**.  
4. Usar **gráfico + tabela t + números** no artigo e gravar o **vídeo distribuído**.

Se quiser, no próximo passo você cola o trecho atual do **`MercuryCall_Services`** (o `EssentialParametersGroup` com `C`) e eu te digo exatamente a linha que deve ficar com **5 pontos** sem conflitar com o resto do projeto.

---

**User**

ta, mais o trabalho fala em dois servidores, isso já esta ok? não teria que rodar como se fosse em duas maquinas diferentes de algum jeito (me responda no chat)

---

**Cursor**

Em termos de **lógica do sistema**, já está “dois servidores”: no projeto isso é exatamente **dois load balancers**, cada um com **seu pool de `ServiceProxy`** — o `loadbalancer1` (porta 2000) e o `loadbalancer2` (porta 3000), encadeados como no desenho do manual. Ou seja, a **arquitetura de dois servidores** já está representada no código e nos `.properties`, mesmo rodando tudo no mesmo PC.

O que o trabalho pede **além** disso é o **vídeo mostrando rodando de modo distribuído**. Aí não basta só `localhost` no mesmo processo: você precisa **subir cada bloco em um host diferente** (dois PCs, duas VMs, contêineres em máquinas diferentes, etc.) e trocar nos `.properties` os **`localhost`** pelos **IPs reais** de cada máquina, mantendo a mesma topologia (Source → LB1 → serviços → LB2 → serviços → volta ao Source).

**Resumo:** para o **modelo e a validação numérica**, rodar local já reproduz **dois servidores** na arquitetura. Para **bater com o enunciado do vídeo**, você precisa **executar fisicamente distribuído**, não só “como se fosse” no mesmo IntelliJ.

---

**User**

e como eu faço isso?

---

**Cursor**

Você faz isso **subindo três processos Java em máquinas (ou VMs) diferentes**, cada um com **um único `main`**, e **trocando `localhost` pelos IPs da rede**. O `LocalTest_Services` é só atalho para tudo na mesma máquina; distribuído você **não** usa ele — roda cada peça separada.

---

### Ideia da topologia

- **Máquina do Server 2:** só o **2º load balancer** (e os *services* que ele sozinho já cria na mesma JVM — isso é o “servidor 2”).
- **Máquina do Server 1:** só o **1º load balancer** (servidor 1).
- **Máquina do Source:** só o **Source** (pode ser uma terceira máquina ou a mesma do Server 1; o importante é os **IPs nos `.properties** baterem com a realidade).

Ordem de subida (igual ao teste local): **Server 2 → Server 1 → Source**.

---

### 1) Ajustar os `.properties` (IPs reais)

Use os IPs **da LAN** (ex.: `192.168.0.10`), não `localhost`, entre máquinas diferentes.

**`loadbalancer2.properties` (na máquina do Server 2)**  
- `server.loadBalancerPort=3000` (ou o que você usar).  
- `service.serviceTargetIp=` **IP da máquina onde roda o Source** (onde a porta `sourcePort` escuta).  
- `service.serviceTargetPort=` porta do Source (ex.: `1000`).

**`loadbalancer1.properties` (na máquina do Server 1)**  
- `service.serviceTargetIp=` **IP da máquina do Server 2**.  
- `service.serviceTargetPort=3000` (porta do LB2).

**`source.properties` (na máquina do Source)**  
- `targetIp=` **IP do Server 1**.  
- `targetPort=2000`.  
- `variatingServices.variatedServerLoadBalancerIp=` **IP do Server 2**.  
- `variatingServices.variatedServerLoadBalancerPort=3000`.  
- `sourcePort=1000` (e no LB2, `service.serviceTargetPort` tem que ser esse valor).

Em todas as máquinas, **copie também os JARs/libs** (ou o projeto compilado) e mantenha **Java 11**.

---

### 2) Como **rodar** cada processo no IntelliJ (ou terminal)

O `LoadBalancerProxy` no `main` lê um arquivo chamado **`loadbalancer.properties`** no **diretório de trabalho** atual:

- Na máquina do **Server 2:** copie `loadbalancer2.properties` para **`loadbalancer.properties`** (já com IPs corretos).  
  *Working directory* da run configuration = pasta onde está esse `loadbalancer.properties`.  
  Execute **`domain.LoadBalancerProxy`**.

- Na máquina do **Server 1:** copie `loadbalancer1.properties` para **`loadbalancer.properties`**.  
  Mesma ideia de working directory.  
  Execute **`domain.LoadBalancerProxy`**.

O **Source** no `main` usa `user.dir` e espera **`source.properties` direto dentro do working directory** no construtor padrão… No código, `Source()` usa `user.dir` e carrega `user.dir + "/source.properties"` — confira no seu `Source.java`: se for assim, o *working directory* deve ser a pasta que **contém** `source.properties` (por exemplo a pasta `validation` com o arquivo dentro).  
Execute **`domain.Source`**.

Se no seu projeto o Source for sempre chamado com o caminho da pasta `validation` (como no `LocalTest_Services`), no modo distribuído o mais simples é: **working directory = pasta `src/tests/validation` (ou cópia dela)** com `source.properties` lá dentro, e usar uma run configuration que aponte para isso — ou um `main` mínimo que chame `new Source("C:\\caminho\\para\\validation").start()` (só se precisar).

---

### 3) Rede e firewall

- PCs na **mesma rede**, sem isolamento de “Wi‑Fi de convidado”.  
- Liberar **entrada** no firewall do Windows (ou Linux) para as portas usadas pelo Java: pelo menos **1000, 2000, 3000** (e confira se não mudou nada nos `.properties`).

---

### 4) Vídeo

Grave: uma tela mostrando **Server 2** rodando, outra **Server 1**, outra **Source** (ou duas telas se Source estiver no mesmo PC que um servidor), e o tráfego / logs mostrando que não é tudo `localhost` entre máquinas.

---

### Resumo

| Onde roda | Classe | Arquivo principal | O que editar |
|-----------|--------|-------------------|--------------|
| PC Server 2 | `LoadBalancerProxy` | `loadbalancer.properties` (cópia do LB2) | `service.serviceTargetIp` = IP do Source |
| PC Server 1 | `LoadBalancerProxy` | `loadbalancer.properties` (cópia do LB1) | `service.serviceTargetIp` = IP do Server 2 |
| PC Source | `Source` | `source.properties` | `targetIp` = Server 1; `variatedServer…` = Server 2 |

Se você me disser **quantas máquinas** tem (2 ou 3) e quem vai rodar o Source, monto a tabela “IP A / IP B / IP C” com os valores exatos linha a linha nos três arquivos.

---

**User**

ta, qual o jeito mais facil de deixar isso distribuido?

---

**Cursor**

O caminho **mais fácil** na prática costuma ser um destes dois:

---

### 1) **Dois computadores na mesma rede** (menos dor de cabeça de rede)

- PC + notebook (ou dois PCs) no **mesmo Wi‑Fi / cabo**.
- Em cada um: instalar **Java 11**, copiar a pasta do projeto (ou só `out` + `lib` + `.properties`).
- No **cmd**, `ipconfig` em cada um e usar os IPv4 (ex.: `192.168.1.10` e `192.168.1.20`).
- Ajustar só os **3 arquivos** de properties com esses IPs (como na mensagem anterior) e rodar:
  - máquina A: `LoadBalancerProxy` com `loadbalancer.properties` = cópia do **LB2**
  - máquina B: `LoadBalancerProxy` com **LB1**
  - máquina C (pode ser a A ou B): `Source`

Não precisa Docker nem nuvem: é só **TCP entre IPs da LAN** e liberar firewall nas portas **3000, 2000, 1000**.

---

### 2) **Só um PC físico: duas VMs com rede “bridged”**

- Instalar **VirtualBox** (ou similar), criar **2 VMs** (Linux leve ou Windows).
- Placa de rede em modo **Bridge** → cada VM ganha um IP **na mesma rede** que o host (ex.: `192.168.1.21`, `192.168.1.22`).
- O fluxo é **idêntico** ao item 1: três processos, três IPs, mesmos `.properties`.

Para o **vídeo do trabalho**, isso costuma ser aceito como “distribuído”, porque o tráfego **não é localhost**: são processos em **máquinas (virtuais) diferentes**.

---

### O que **não** é o mais fácil

- **WSL2 + Windows** como “segunda máquina”: IP e firewall costumam confundir mais.
- **Docker** desde zero: dá, mas é mais passo para quem só quer gravar o vídeo.

---

**Resumo:** o jeito mais simples é **dois IPs reais na LAN** — seja **dois aparelhos** ou **duas VMs em bridge**. O trabalho de verdade é só **copiar o projeto/JAR, editar IPs nos properties, subir LB2 → LB1 → Source** e abrir as portas no firewall.

---

**User**

eu so tenho um pc fisico

---

**Cursor**

Com **só um PC físico**, o jeito mais simples de ficar “distribuído” de verdade (TCP entre máquinas diferentes) é usar **máquinas virtuais** na mesma rede que o seu Windows.

### Opção mais fácil: **2 VMs + rede em Bridge**

1. Instale **VirtualBox** (grátis) ou use **Hyper-V** se já tiver no Windows Pro.
2. Crie **duas VMs** (pode ser **Ubuntu Server** leve em cada uma, ou Windows se preferir).
3. Em **cada VM**, na configuração de rede, use **Bridged Adapter / Ponte** (não NAT sozinho).
4. Ligue as duas VMs: cada uma ganha um **IP na sua rede** (ex.: `192.168.1.101` e `192.168.1.102`), **diferente** do IP do seu PC.
5. No **seu PC (host)** você pode rodar o **Source** (ou uma das peças); nas **duas VMs** você roda **LB2** e **LB1** (ou distribua como preferir), desde que nos `.properties` você use **esses IPs**, nunca `localhost` entre host e VM.
6. **Firewall**: nas VMs e no Windows, libere as portas que o trabalho usa (**1000, 2000, 3000** e o que estiver nos `.properties`).

Assim no vídeo aparecem **três “máquinas”** (host + 2 VMs) com comunicação **entre IPs**, o que atende bem o espírito do enunciado.

### Se 2 VMs pesarem no PC

- Use **1 VM + host**: VM roda **Server 2**, host roda **Server 1** e **Source** (ou outra combinação). Ainda assim há **dois sistemas** e tráfego **host ↔ VM** por IP da bridge — melhor que tudo em `localhost` num único processo.

### O que evitar como “solução fácil”

- **Só WSL2** como segunda máquina: dá, mas rede e firewall costumam dar mais trabalho que VirtualBox em bridge.

**Resumo:** com um PC só, o caminho mais direto é **VirtualBox, 2 VMs, rede bridge, três processos (LB2, LB1, Source) com IPs reais nos `.properties`**.

---

**User**

esse aqui?

---

**Cursor**

Sim, **é esse mesmo**: o **Oracle VM VirtualBox** do site oficial.

No seu caso (PC com Windows):

1. Baixe **“Windows hosts”** (instalador `.exe`).
2. Instale com as opções padrão (pode aceitar os drivers de rede quando pedir).
3. O **Extension Pack** só é necessário se for usar USB 2.0/3.0, discos compartilhados avançados, etc. Para rodar **duas VMs em rede bridge** com o seu trabalho, **não é obrigatório** começar por ele.

Depois da instalação: criar as duas VMs, em cada uma colocar rede **Bridged Adapter** e seguir o plano (LB2 em uma VM, LB1 na outra, Source no host ou em uma VM, IPs nos `.properties`).

---

**User**

instalado, e agora?

ei

ei

