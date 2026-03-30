"""
Script para plotar gráficos dos resultados de simulação JMT (.jsimg)
Processa automaticamente todos os arquivos .jsimg na pasta Resultados.
Estilo: acadêmico com fundo branco, sem barras de erro.
"""

import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import os
import glob

# --- Configuração ---
PASTA_RESULTADOS = os.path.dirname(os.path.abspath(__file__))
PASTA_GRAFICOS = os.path.join(PASTA_RESULTADOS, "Graficos")
os.makedirs(PASTA_GRAFICOS, exist_ok=True)

# --- Estilo acadêmico (fundo branco, sem barras de erro) ---
matplotlib.rcdefaults()
plt.rcParams.update({
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": "black",
    "axes.labelcolor": "black",
    "axes.linewidth": 0.8,
    "axes.labelsize": 13,
    "text.color": "black",
    "xtick.color": "black",
    "ytick.color": "black",
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.size": 4,
    "ytick.major.size": 4,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "grid.alpha": 0.0,
    "font.size": 11,
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "legend.frameon": True,
    "legend.edgecolor": "black",
    "legend.fancybox": False,
    "legend.fontsize": 9,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.facecolor": "white",
})

CORES = ["blue", "red", "black"]
MARCADORES = ["s", "o", "^", "D", "v"]


def processar_arquivo(caminho_jsimg):
    """Processa um arquivo .jsimg e gera os gráficos."""
    nome_arquivo = os.path.splitext(os.path.basename(caminho_jsimg))[0]
    # Preservar estrutura de subpastas (ex: Cenario 1/Teste_2Q_2N)
    caminho_relativo = os.path.relpath(caminho_jsimg, PASTA_RESULTADOS)
    pasta_relativa = os.path.join(os.path.dirname(caminho_relativo), nome_arquivo)
    pasta_saida = os.path.join(PASTA_GRAFICOS, pasta_relativa)
    os.makedirs(pasta_saida, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"Processando: {nome_arquivo}")
    print(f"{'='*60}")

    # --- Parsing do XML ---
    tree = ET.parse(caminho_jsimg)
    root = tree.getroot()

    # Extrair parâmetros da análise paramétrica
    jmodel = root.find("jmodel")
    parametric = jmodel.find("parametric")
    taxa_inicio = float(parametric.find("field[@name='From']").get("value"))
    taxa_fim = float(parametric.find("field[@name='To']").get("value"))
    num_passos = int(parametric.find("field[@name='Steps']").get("value"))

    # Gerar valores da taxa de chegada (eixo X)
    taxas_chegada = np.linspace(taxa_inicio, taxa_fim, num_passos)

    # --- Extrair número de servidores de cada fila ---
    sim = root.find("sim")
    servidores = {}
    for node in sim.findall("node"):
        node_name = node.get("name")
        for section in node.findall("section"):
            if section.get("className") == "Server":
                max_jobs = section.find("parameter[@name='maxJobs']/value")
                if max_jobs is not None:
                    servidores[node_name] = int(max_jobs.text)

    # --- Extrair resultados ---
    results = root.find("results")
    metricas = {}

    for measure in results.findall("measure"):
        nome = measure.get("name")
        medias = []
        lower_bounds = []
        upper_bounds = []
        for sample in measure.findall("sample"):
            medias.append(float(sample.get("meanValue")))
            lower_bounds.append(float(sample.get("lowerBound")))
            upper_bounds.append(float(sample.get("upperBound")))
        metricas[nome] = {
            "media": np.array(medias),
            "lower": np.array(lower_bounds),
            "upper": np.array(upper_bounds),
            "ref_class": measure.get("referenceClass"),
            "ref_station": measure.get("referenceStation"),
        }

    # Detectar automaticamente métricas de utilização (ex: Queue 1_Class1_Utilization, Maquina 1_Class1_Utilization)
    util_keys = [k for k in metricas if k.endswith("_Utilization")]
    util_labels = []
    for uk in util_keys:
        station = metricas[uk]["ref_station"]
        n_servers = servidores.get(station, "?")
        util_labels.append(f"{station} ({n_servers} servers)")

    # --- Gráfico 1: Tempo de Resposta do Sistema ---
    fig1, ax1 = plt.subplots(figsize=(7, 5))
    m = metricas["Network_Class1_System Response Time"]
    yerr = [np.abs(m["media"] - m["lower"]), np.abs(m["upper"] - m["media"])]
    ax1.errorbar(taxas_chegada, m["media"], yerr=yerr, color=CORES[0], 
                 marker=MARCADORES[0], markersize=5, linewidth=1.2, 
                 capsize=3, capthick=1, label="Class1")
    ax1.set_xlabel("Arrival Rate (data/s)")
    ax1.set_ylabel("System Response Time (s)")
    ax1.legend(loc="best")
    fig1.tight_layout()
    fig1.savefig(os.path.join(pasta_saida, "tempo_resposta.png"))
    plt.close(fig1)
    print("  Salvo: tempo_resposta.png")

    # --- Gráfico 2: Throughput do Sistema ---
    fig2, ax2 = plt.subplots(figsize=(7, 5))
    m = metricas["Network_Class1_System Throughput"]
    yerr = [np.abs(m["media"] - m["lower"]), np.abs(m["upper"] - m["media"])]
    ax2.errorbar(taxas_chegada, m["media"], yerr=yerr, color=CORES[0], 
                 marker=MARCADORES[0], markersize=5, linewidth=1.2, 
                 capsize=3, capthick=1, label="Class1")
    ax2.set_xlabel("Arrival Rate (data/s)")
    ax2.set_ylabel("System Throughput (jobs/s)")
    ax2.legend(loc="best")
    fig2.tight_layout()
    fig2.savefig(os.path.join(pasta_saida, "throughput.png"))
    plt.close(fig2)
    print("  Salvo: throughput.png")

    # --- Gráfico 3: Taxa de Drop do Sistema ---
    fig3, ax3 = plt.subplots(figsize=(7, 5))
    m = metricas["Network_Class1_System Drop Rate"]
    yerr = [np.abs(m["media"] - m["lower"]), np.abs(m["upper"] - m["media"])]
    ax3.errorbar(taxas_chegada, m["media"], yerr=yerr, color=CORES[0], 
                 marker=MARCADORES[0], markersize=5, linewidth=1.2, 
                 capsize=3, capthick=1, label="Class1")
    ax3.set_xlabel("Arrival Rate (data/s)")
    ax3.set_ylabel("Drop Rate (data/s)")
    ax3.legend(loc="best")
    fig3.tight_layout()
    fig3.savefig(os.path.join(pasta_saida, "drop_rate.png"))
    plt.close(fig3)
    print("  Salvo: drop_rate.png")

    # --- Gráfico 4: Utilização das Estações ---
    fig4, ax4 = plt.subplots(figsize=(7, 5))
    for i, (uk, label) in enumerate(zip(util_keys, util_labels)):
        m = metricas[uk]
        yerr = [np.abs(m["media"] - m["lower"]), np.abs(m["upper"] - m["media"])]
        ax4.errorbar(taxas_chegada, m["media"], yerr=yerr, color=CORES[i % len(CORES)],
                     marker=MARCADORES[i % len(MARCADORES)], markersize=5, linewidth=1.2, 
                     capsize=3, capthick=1, label=label)
    ax4.set_xlabel("Arrival Rate (data/s)")
    ax4.set_ylabel("Utilization (%)")
    ax4.legend(loc="best")
    fig4.tight_layout()
    fig4.savefig(os.path.join(pasta_saida, "utilizacao.png"))
    plt.close(fig4)
    print("  Salvo: utilizacao.png")

    # --- Gráfico 5: Painel Completo 2x2 ---
    fig5, axes = plt.subplots(2, 2, figsize=(12, 9))

    # (a) Response Time
    ax = axes[0, 0]
    m = metricas["Network_Class1_System Response Time"]
    yerr = [np.abs(m["media"] - m["lower"]), np.abs(m["upper"] - m["media"])]
    ax.errorbar(taxas_chegada, m["media"], yerr=yerr, color=CORES[0], 
                marker=MARCADORES[0], markersize=4, linewidth=1.0, 
                capsize=2.5, capthick=0.8, label="Class1")
    ax.set_xlabel("Arrival Rate (data/s)")
    ax.set_ylabel("System Response Time (s)")
    ax.legend(loc="best", fontsize=8)

    # (b) Throughput
    ax = axes[0, 1]
    m = metricas["Network_Class1_System Throughput"]
    yerr = [np.abs(m["media"] - m["lower"]), np.abs(m["upper"] - m["media"])]
    ax.errorbar(taxas_chegada, m["media"], yerr=yerr, color=CORES[0], 
                marker=MARCADORES[0], markersize=4, linewidth=1.0, 
                capsize=2.5, capthick=0.8, label="Class1")
    ax.set_xlabel("Arrival Rate (data/s)")
    ax.set_ylabel("Throughput (jobs/s)")
    ax.legend(loc="best", fontsize=8)

    # (c) Drop Rate
    ax = axes[1, 0]
    m = metricas["Network_Class1_System Drop Rate"]
    yerr = [np.abs(m["media"] - m["lower"]), np.abs(m["upper"] - m["media"])]
    ax.errorbar(taxas_chegada, m["media"], yerr=yerr, color=CORES[0], 
                marker=MARCADORES[0], markersize=4, linewidth=1.0, 
                capsize=2.5, capthick=0.8, label="Class1")
    ax.set_xlabel("Arrival Rate (data/s)")
    ax.set_ylabel("Drop Rate (data/s)")
    ax.legend(loc="best", fontsize=8)

    # (d) Utilização
    ax = axes[1, 1]
    for i, (uk, label) in enumerate(zip(util_keys, util_labels)):
        m = metricas[uk]
        yerr = [np.abs(m["media"] - m["lower"]), np.abs(m["upper"] - m["media"])]
        ax.errorbar(taxas_chegada, m["media"], yerr=yerr, color=CORES[i % len(CORES)],
                    marker=MARCADORES[i % len(MARCADORES)], markersize=4, linewidth=1.0, 
                    capsize=2.5, capthick=0.8, label=label)
    ax.set_xlabel("Arrival Rate (data/s)")
    ax.set_ylabel("Utilization (%)")
    ax.legend(loc="best", fontsize=8)

    fig5.tight_layout()
    fig5.savefig(os.path.join(pasta_saida, "painel_completo.png"))
    plt.close(fig5)
    print("  Salvo: painel_completo.png")

    print(f"  Gráficos salvos em: {pasta_saida}")


def extrair_dados(caminho_jsimg):
    """Extrai dados de um arquivo .jsimg para uso nos gráficos unificados."""
    tree = ET.parse(caminho_jsimg)
    root = tree.getroot()

    # Extrair parâmetros da análise paramétrica
    jmodel = root.find("jmodel")
    parametric = jmodel.find("parametric")
    taxa_inicio = float(parametric.find("field[@name='From']").get("value"))
    taxa_fim = float(parametric.find("field[@name='To']").get("value"))
    num_passos = int(parametric.find("field[@name='Steps']").get("value"))
    taxas_chegada = np.linspace(taxa_inicio, taxa_fim, num_passos)

    # Extrair número de máquinas e núcleos por máquina
    sim = root.find("sim")
    maquinas = []
    for node in sim.findall("node"):
        node_name = node.get("name")
        for section in node.findall("section"):
            if section.get("className") == "Server":
                max_jobs = section.find("parameter[@name='maxJobs']/value")
                if max_jobs is not None:
                    maquinas.append({
                        "nome": node_name,
                        "nucleos": int(max_jobs.text),
                    })

    num_maquinas = len(maquinas)
    nucleos_por_maquina = maquinas[0]["nucleos"] if maquinas else 0
    primeira_maquina = maquinas[0]["nome"] if maquinas else None

    # Extrair resultados
    results = root.find("results")
    metricas = {}
    for measure in results.findall("measure"):
        nome = measure.get("name")
        medias = [float(s.get("meanValue")) for s in measure.findall("sample")]
        lower_bounds = [float(s.get("lowerBound")) for s in measure.findall("sample")]
        upper_bounds = [float(s.get("upperBound")) for s in measure.findall("sample")]
        metricas[nome] = {
            "media": np.array(medias),
            "lower": np.array(lower_bounds),
            "upper": np.array(upper_bounds),
            "ref_class": measure.get("referenceClass"),
            "ref_station": measure.get("referenceStation"),
        }

    # Encontrar a chave de utilização da primeira máquina
    util_key_primeira = None
    if primeira_maquina:
        for k in metricas:
            if k.endswith("_Utilization") and metricas[k]["ref_station"] == primeira_maquina:
                util_key_primeira = k
                break

    return {
        "taxas_chegada": taxas_chegada,
        "metricas": metricas,
        "num_maquinas": num_maquinas,
        "nucleos_por_maquina": nucleos_por_maquina,
        "util_key_primeira": util_key_primeira,
    }


def gerar_graficos_unificados(arquivos_cenario, nome_cenario):
    """Gera gráficos unificados (uma curva por configuração) para um cenário."""
    pasta_saida = os.path.join(PASTA_GRAFICOS, nome_cenario, "Unificados")
    os.makedirs(pasta_saida, exist_ok=True)

    # Extrair dados de todos os arquivos e ordenar por total de núcleos
    dados = []
    for arq in sorted(arquivos_cenario):
        dados.append(extrair_dados(arq))
    dados.sort(key=lambda d: (d["num_maquinas"], d["nucleos_por_maquina"]))

    # Detectar o que está variando: máquinas ou núcleos?
    num_maquinas_set = set(d["num_maquinas"] for d in dados)
    nucleos_set = set(d["nucleos_por_maquina"] for d in dados)
    
    # Gerar labels baseado no que varia
    for d in dados:
        if len(num_maquinas_set) > 1 and len(nucleos_set) == 1:
            # Varia máquinas, núcleos constante
            d["label"] = f"{d['num_maquinas']} Raspberry Pi"
        elif len(nucleos_set) > 1 and len(num_maquinas_set) == 1:
            # Varia núcleos, máquinas constante
            d["label"] = f"{d['nucleos_por_maquina']} Núcleos"
        else:
            # Variam ambos (manter o formato original)
            d["label"] = f"{d['num_maquinas']} Máq. × {d['nucleos_por_maquina']} Núcleos"

    cores_ext = ["blue", "red", "black", "green", "purple", "orange", "brown", "gray"]
    marcadores_ext = ["s", "o", "^", "D", "v", "P", "X", "h"]

    # --- (a) Tempo de Resposta Unificado ---
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, d in enumerate(dados):
        m = d["metricas"]["Network_Class1_System Response Time"]
        yerr = [np.abs(m["media"] - m["lower"]), np.abs(m["upper"] - m["media"])]
        cor = cores_ext[i % len(cores_ext)]
        ax.errorbar(d["taxas_chegada"], m["media"], yerr=yerr,
                    color=cor,
                    marker=marcadores_ext[i % len(marcadores_ext)],
                    markersize=5, linewidth=1.2, capsize=3, capthick=1, 
                    label=d["label"])
    ax.set_xlabel("Arrival Rate (data/s)")
    ax.set_ylabel("System Response Time (s)")
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(os.path.join(pasta_saida, "tempo_resposta_unificado.png"))
    plt.close(fig)
    print(f"  Salvo: {nome_cenario}/Unificados/tempo_resposta_unificado.png")

    # --- (b) Throughput Unificado ---
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, d in enumerate(dados):
        m = d["metricas"]["Network_Class1_System Throughput"]
        yerr = [np.abs(m["media"] - m["lower"]), np.abs(m["upper"] - m["media"])]
        cor = cores_ext[i % len(cores_ext)]
        ax.errorbar(d["taxas_chegada"], m["media"], yerr=yerr,
                    color=cor,
                    marker=marcadores_ext[i % len(marcadores_ext)],
                    markersize=5, linewidth=1.2, capsize=3, capthick=1, 
                    label=d["label"])
    ax.set_xlabel("Arrival Rate (data/s)")
    ax.set_ylabel("System Throughput (jobs/s)")
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(os.path.join(pasta_saida, "throughput_unificado.png"))
    plt.close(fig)
    print(f"  Salvo: {nome_cenario}/Unificados/throughput_unificado.png")

    # --- (c) Drop Rate Unificado ---
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, d in enumerate(dados):
        m = d["metricas"]["Network_Class1_System Drop Rate"]
        yerr = [np.abs(m["media"] - m["lower"]), np.abs(m["upper"] - m["media"])]
        cor = cores_ext[i % len(cores_ext)]
        ax.errorbar(d["taxas_chegada"], m["media"], yerr=yerr,
                    color=cor,
                    marker=marcadores_ext[i % len(marcadores_ext)],
                    markersize=5, linewidth=1.2, capsize=3, capthick=1, 
                    label=d["label"])
    ax.set_xlabel("Arrival Rate (data/s)")
    ax.set_ylabel("Drop Rate (data/s)")
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(os.path.join(pasta_saida, "drop_rate_unificado.png"))
    plt.close(fig)
    print(f"  Salvo: {nome_cenario}/Unificados/drop_rate_unificado.png")

    # --- (d) Utilização Unificado (primeira máquina = utilização do sistema) ---
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, d in enumerate(dados):
        uk = d["util_key_primeira"]
        if uk and uk in d["metricas"]:
            m = d["metricas"][uk]
            yerr = [np.abs(m["media"] - m["lower"]), np.abs(m["upper"] - m["media"])]
            cor = cores_ext[i % len(cores_ext)]
            ax.errorbar(d["taxas_chegada"], m["media"], yerr=yerr,
                        color=cor,
                        marker=marcadores_ext[i % len(marcadores_ext)],
                        markersize=5, linewidth=1.2, capsize=3, capthick=1, 
                        label=d["label"])
    ax.set_xlabel("Arrival Rate (data/s)")
    ax.set_ylabel("Utilization (%)")
    ax.legend(loc="best")
    fig.tight_layout()
    fig.savefig(os.path.join(pasta_saida, "utilizacao_unificado.png"))
    plt.close(fig)
    print(f"  Salvo: {nome_cenario}/Unificados/utilizacao_unificado.png")

    # --- Painel 2x2 Unificado ---
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    for i, d in enumerate(dados):
        c = cores_ext[i % len(cores_ext)]
        mk = marcadores_ext[i % len(marcadores_ext)]
        lbl = d["label"]

        m = d["metricas"]["Network_Class1_System Response Time"]
        yerr = [np.abs(m["media"] - m["lower"]), np.abs(m["upper"] - m["media"])]
        axes[0, 0].errorbar(d["taxas_chegada"], m["media"], yerr=yerr, color=c, 
                            marker=mk, markersize=4, linewidth=1.0, 
                            capsize=2.5, capthick=0.8, label=lbl)

        m = d["metricas"]["Network_Class1_System Throughput"]
        yerr = [np.abs(m["media"] - m["lower"]), np.abs(m["upper"] - m["media"])]
        axes[0, 1].errorbar(d["taxas_chegada"], m["media"], yerr=yerr, color=c, 
                            marker=mk, markersize=4, linewidth=1.0, 
                            capsize=2.5, capthick=0.8, label=lbl)

        m = d["metricas"]["Network_Class1_System Drop Rate"]
        yerr = [np.abs(m["media"] - m["lower"]), np.abs(m["upper"] - m["media"])]
        axes[1, 0].errorbar(d["taxas_chegada"], m["media"], yerr=yerr, color=c, 
                            marker=mk, markersize=4, linewidth=1.0, 
                            capsize=2.5, capthick=0.8, label=lbl)

        uk = d["util_key_primeira"]
        if uk and uk in d["metricas"]:
            m = d["metricas"][uk]
            yerr = [np.abs(m["media"] - m["lower"]), np.abs(m["upper"] - m["media"])]
            axes[1, 1].errorbar(d["taxas_chegada"], m["media"], yerr=yerr,
                                color=c, marker=mk, markersize=4, linewidth=1.0, 
                                capsize=2.5, capthick=0.8, label=lbl)

    axes[0, 0].set_xlabel("Arrival Rate (data/s)")
    axes[0, 0].set_ylabel("System Response Time (s)")
    axes[0, 0].legend(loc="best", fontsize=8)

    axes[0, 1].set_xlabel("Arrival Rate (data/s)")
    axes[0, 1].set_ylabel("Throughput (jobs/s)")
    axes[0, 1].legend(loc="best", fontsize=8)

    axes[1, 0].set_xlabel("Arrival Rate (data/s)")
    axes[1, 0].set_ylabel("Drop Rate (data/s)")
    axes[1, 0].legend(loc="best", fontsize=8)

    axes[1, 1].set_xlabel("Arrival Rate (data/s)")
    axes[1, 1].set_ylabel("Utilization (%)")
    axes[1, 1].legend(loc="best", fontsize=8)

    fig.tight_layout()
    fig.savefig(os.path.join(pasta_saida, "painel_unificado.png"))
    plt.close(fig)
    print(f"  Salvo: {nome_cenario}/Unificados/painel_unificado.png")


# --- Processar todos os .jsimg na pasta e subpastas ---
arquivos = sorted(glob.glob(os.path.join(PASTA_RESULTADOS, "**", "*.jsimg"), recursive=True))

if not arquivos:
    print("Nenhum arquivo .jsimg encontrado na pasta Resultados (incluindo subpastas)!")
else:
    print(f"Encontrados {len(arquivos)} arquivo(s) .jsimg")
    for arq in arquivos:
        processar_arquivo(arq)

    # --- Gráficos Unificados por cenário ---
    print(f"\n{'='*60}")
    print("Gerando gráficos unificados por cenário...")
    print(f"{'='*60}")

    # Agrupar arquivos por subpasta (cenário)
    cenarios = {}
    for arq in arquivos:
        pasta_rel = os.path.relpath(os.path.dirname(arq), PASTA_RESULTADOS)
        if pasta_rel == ".":
            pasta_rel = "Raiz"
        cenarios.setdefault(pasta_rel, []).append(arq)

    for nome_cenario, arqs in sorted(cenarios.items()):
        if len(arqs) >= 2:  # só faz sentido unificar se houver >= 2 configs
            print(f"\n  Cenário: {nome_cenario} ({len(arqs)} configurações)")
            gerar_graficos_unificados(arqs, nome_cenario)

    print(f"\nTodos os gráficos salvos em: {PASTA_GRAFICOS}")
