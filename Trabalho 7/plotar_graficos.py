import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

def configure_axis_style(ax, xlabel, ylabel):
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.tick_params(which='both', direction='in', top=True, right=True)
    ax.xaxis.set_minor_locator(AutoMinorLocator())
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    # Fundo branco, bordas pretas
    ax.set_facecolor('white')
    for spine in ax.spines.values():
        spine.set_color('black')
        spine.set_linewidth(0.8)

def main():
    if not os.path.exists('Case_Study_1_Energy/data_energy.csv'):
        print("Erro: rode 'calcular_dados.py' primeiro.")
        return

    # Base MTTFs for Sensitivity X-axis
    base_mttf = {
        'Power Grid': 8.757,
        'Edge svr': 940.0,
        'Cloud Srv': 760.0,
        'Gateway': 480.77,
        'Supervisor': 44.957
    }

    df1 = pd.read_csv('Case_Study_1_Energy/data_energy.csv')
    baseline_sys_avail = df1[df1['Configuration'].str.contains('Config. C')]['Availability'].values[0] * 100

    # ==========================================
    # Case Study 3: Sensitivity Analysis (Estilo Artigo)
    # ==========================================
    df3 = pd.read_csv('Case_Study_3_Sensitivity/data_sensitivity.csv')
    components_sa = df3['Component'].unique()
    
    # Criar imagens isoladas para cada componente
    colors = ['black', 'black', 'green', 'green', 'blue']
    letters = ['a', 'b', 'c', 'd', 'e']
    
    for i, comp in enumerate(components_sa):
        fig, ax = plt.subplots(figsize=(6, 5))
        comp_data = df3[df3['Component'] == comp]
        
        factors = comp_data['Factor'].values
        x_values = factors * base_mttf[comp]
        y_values = comp_data['Availability'].values * 100
        
        ax.plot(x_values, y_values, marker='o', markersize=4, color=colors[i], 
                linewidth=0.8, label='Parameter')
        
        ax.axhline(y=baseline_sys_avail, color='red', linestyle='--', linewidth=0.8, label='Baseline')
        
        xlabel = f"{comp.upper().replace(' ', '_')}_MTTF (h)"
        configure_axis_style(ax, xlabel, "Availability")
        
        ax.legend(loc='lower right', fontsize=9, framealpha=1, edgecolor='black', 
                  borderpad=0.6, handlelength=2.0)
        
        
        plt.tight_layout()
        safe_comp_name = comp.replace(' ', '_').lower()
        plt.savefig(f'Case_Study_3_Sensitivity/case_study_3_sensitivity_{safe_comp_name}_artigo.png', dpi=300, bbox_inches='tight')
        plt.close()

    # ==========================================
    # Case Study 2: KooN (Estilo Artigo)
    # ==========================================
    df2 = pd.read_csv('Case_Study_2_KooN/data_koon.csv')
    k_values = df2['k'].values
    sys_avails_koon = df2['Availability'].values * 100
    
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.plot(k_values, sys_avails_koon, marker='o', markersize=4, color='black', linewidth=0.8, label='Parameter')
    
    # Baseline
    baseline_val = sys_avails_koon[list(k_values).index(5)]
    ax.axhline(y=baseline_val, color='red', linestyle='--', linewidth=0.8, label='Baseline')
    
    configure_axis_style(ax, "SENSORS_KooN (k)", "Availability")
    ax.legend(loc='lower right', fontsize=9, framealpha=1, edgecolor='black', borderpad=0.6)
    
    
    plt.tight_layout()
    plt.savefig('Case_Study_2_KooN/case_study_2_koon_artigo.png', dpi=300, bbox_inches='tight')
    plt.close()

    # ==========================================
    # Case Study 1: Energia (Como não é de linha, vamos fazer um bar plot minimalista)
    # ==========================================
    # O artigo de espelhamento usa gráficos de barras simples
    labels_configs = ['Config. A\
(Grid Only)', 'Config. B\
(Grid + Gen)', 'Config. C\
(Grid+Gen+Solar)']
    avail_configs = df1['Availability'].values * 100
    downtime_configs = df1['Downtime'].values
    
    fig, ax1 = plt.subplots(figsize=(6, 5))
    # Gráfico de Disponibilidade apenas para ficar parecido com os resultados unificados
    ax1.bar(labels_configs, avail_configs, color='gray', edgecolor='black', width=0.4)
    ax1.set_ylim([min(avail_configs)-2, 100])
    
    configure_axis_style(ax1, "Configuration", "Availability (%)")
            
    plt.tight_layout()
    plt.savefig('Case_Study_1_Energy/case_study_1_energy_availability_artigo.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Gráfico de Downtime Anual
    fig, ax2 = plt.subplots(figsize=(6, 5))
    ax2.bar(labels_configs, downtime_configs, color='darkred', edgecolor='black', width=0.4)
    
    configure_axis_style(ax2, "Configuration", "Annual Downtime (h)")
            
    plt.tight_layout()
    plt.savefig('Case_Study_1_Energy/case_study_1_energy_downtime_artigo.png', dpi=300, bbox_inches='tight')
    plt.close()

    print("Novos gráficos estilo artigo acadêmico gerados!")

if __name__ == "__main__":
    main()
