"""
Script para gerar CSVs com os dados de simulação de cada cenário.
Gera um CSV para o Cenário 1 e outro para o Cenário 2.
"""

import xml.etree.ElementTree as ET
import numpy as np
import os
import glob
import csv

PASTA_RESULTADOS = os.path.dirname(os.path.abspath(__file__))


def extrair_dados_csv(caminho_jsimg):
    """Extrai todos os dados relevantes de um arquivo .jsimg."""
    tree = ET.parse(caminho_jsimg)
    root = tree.getroot()

    nome_arquivo = os.path.splitext(os.path.basename(caminho_jsimg))[0]

    # Parâmetros da análise paramétrica
    jmodel = root.find("jmodel")
    parametric = jmodel.find("parametric")
    taxa_inicio = float(parametric.find("field[@name='From']").get("value"))
    taxa_fim = float(parametric.find("field[@name='To']").get("value"))
    num_passos = int(parametric.find("field[@name='Steps']").get("value"))
    taxas_chegada = np.linspace(taxa_inicio, taxa_fim, num_passos)

    # Extrair info das máquinas (número de máquinas e núcleos)
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

    # Extrair resultados
    results = root.find("results")
    metricas = {}
    for measure in results.findall("measure"):
        nome = measure.get("name")
        medias = [float(s.get("meanValue")) for s in measure.findall("sample")]
        metricas[nome] = {
            "media": medias,
            "ref_station": measure.get("referenceStation"),
        }

    # Pegar métricas principais
    response_time = metricas.get("Network_Class1_System Response Time", {}).get("media", [])
    throughput = metricas.get("Network_Class1_System Throughput", {}).get("media", [])
    drop_rate = metricas.get("Network_Class1_System Drop Rate", {}).get("media", [])

    # Utilização da primeira máquina (utilização do sistema)
    util_primeira = []
    if maquinas:
        primeira = maquinas[0]["nome"]
        for k, v in metricas.items():
            if k.endswith("_Utilization") and v["ref_station"] == primeira:
                util_primeira = v["media"]
                break

    # Utilização de todas as máquinas
    utils_todas = {}
    for maq in maquinas:
        for k, v in metricas.items():
            if k.endswith("_Utilization") and v["ref_station"] == maq["nome"]:
                utils_todas[maq["nome"]] = v["media"]
                break

    return {
        "nome_arquivo": nome_arquivo,
        "num_maquinas": num_maquinas,
        "nucleos_por_maquina": nucleos_por_maquina,
        "taxas_chegada": taxas_chegada.tolist(),
        "response_time": response_time,
        "throughput": throughput,
        "drop_rate": drop_rate,
        "util_sistema": util_primeira,
        "utils_maquinas": utils_todas,
        "maquinas": maquinas,
    }


def gerar_csv_cenario(arquivos, nome_cenario, pasta_saida):
    """Gera um CSV com os dados de um cenário."""
    todos_dados = []
    for arq in sorted(arquivos):
        todos_dados.append(extrair_dados_csv(arq))

    # Ordenar por (num_maquinas, nucleos)
    todos_dados.sort(key=lambda d: (d["num_maquinas"], d["nucleos_por_maquina"]))

    caminho_csv = os.path.join(pasta_saida, f"{nome_cenario}.csv")

    with open(caminho_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")

        # Cabeçalho
        header = [
            "Configuração",
            "Num Máquinas",
            "Núcleos por Máquina",
            "Taxa de Chegada (data/s)",
            "Tempo de Resposta (s)",
            "Throughput (jobs/s)",
            "Taxa de Drop (data/s)",
            "Utilização do Sistema (%)",
        ]

        # Adicionar colunas de utilização por máquina
        # Pegar o máximo de máquinas para definir as colunas
        max_maquinas = max(d["num_maquinas"] for d in todos_dados)
        for i in range(1, max_maquinas + 1):
            header.append(f"Utilização Máquina {i} (%)")

        writer.writerow(header)

        # Dados
        for d in todos_dados:
            config = f"{d['num_maquinas']} Máq. × {d['nucleos_por_maquina']} Núcleos"
            n_pontos = len(d["taxas_chegada"])

            for j in range(n_pontos):
                row = [
                    config,
                    d["num_maquinas"],
                    d["nucleos_por_maquina"],
                    f"{d['taxas_chegada'][j]:.4f}",
                    f"{d['response_time'][j]:.6f}" if j < len(d["response_time"]) else "",
                    f"{d['throughput'][j]:.6f}" if j < len(d["throughput"]) else "",
                    f"{d['drop_rate'][j]:.6f}" if j < len(d["drop_rate"]) else "",
                    f"{d['util_sistema'][j]:.6f}" if j < len(d["util_sistema"]) else "",
                ]

                # Utilização por máquina
                for i in range(1, max_maquinas + 1):
                    nome_maq = f"Maquina {i}"
                    if nome_maq in d["utils_maquinas"] and j < len(d["utils_maquinas"][nome_maq]):
                        row.append(f"{d['utils_maquinas'][nome_maq][j]:.6f}")
                    else:
                        row.append("")

                writer.writerow(row)

    print(f"  CSV salvo: {caminho_csv}")
    return caminho_csv


# --- Main ---
print("=" * 60)
print("Gerando CSVs dos dados de simulação")
print("=" * 60)

# Encontrar todos os .jsimg
arquivos = sorted(glob.glob(os.path.join(PASTA_RESULTADOS, "**", "*.jsimg"), recursive=True))

if not arquivos:
    print("Nenhum arquivo .jsimg encontrado!")
else:
    # Agrupar por cenário (subpasta)
    cenarios = {}
    for arq in arquivos:
        pasta_rel = os.path.relpath(os.path.dirname(arq), PASTA_RESULTADOS)
        if pasta_rel == ".":
            pasta_rel = "Raiz"
        cenarios.setdefault(pasta_rel, []).append(arq)

    for nome_cenario, arqs in sorted(cenarios.items()):
        print(f"\n  Processando: {nome_cenario} ({len(arqs)} arquivos)")
        gerar_csv_cenario(arqs, nome_cenario.replace(" ", "_"), PASTA_RESULTADOS)

    print(f"\nConcluído! CSVs salvos em: {PASTA_RESULTADOS}")
