import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import binom
import os

# Parametros MTTF
mttf_params = {
    'Cloud Srv':  760.0,
    'Edge svr':   940.0,
    'Router':     698.22,
    'Gateway':    480.77,
    'Supervisor': 44.957,
    'Sensors':    300.0,
    'Power Grid': 8.757,
    'Power Gen':  636.0,
    'Sw Power':   25.0,
    'Sol Inv':    24.82,
    'Chg Ctrl':   70.08,
    'Sol Painel': 219.0,
    'Battery':    47.829,
}

def R_koon(R_sensor, n, k_failures):
    # System works if number of failed sensors < k_failures
    Q_sensor = 1.0 - R_sensor
    prob_fail = sum(binom.pmf(i, n, Q_sensor) for i in range(k_failures, n+1))
    return 1.0 - prob_fail

def calc_R_sys(t, k_failures):
    # R(t) = exp(-lambda * t) = exp(-t / MTTF)
    R = {name: np.exp(-t / mttf) for name, mttf in mttf_params.items()}
    
    Q_sol = 1 - R['Sol Painel']
    Q_bat = 1 - R['Battery']
    R_sol_bat = 1 - (Q_sol * Q_bat)
    
    R_solar_sys = R['Sw Power'] * R['Sol Inv'] * R['Chg Ctrl'] * R_sol_bat
    
    Q_grid = 1 - R['Power Grid']
    Q_gen = 1 - R['Power Gen']
    Q_solar = 1 - R_solar_sys
    R_power = 1 - (Q_grid * Q_gen * Q_solar)
    
    R_beds = R_koon(R['Sensors'], 10, k_failures)
    
    # O gráfico do artigo base plota isoladamente o bloco KooN, 
    # sem a interferência dos componentes em série (que fariam a curva cair em 50h).
    return R_beds

def main():
    t_values = np.linspace(0, 2000, 200)
    
    # Rigor Científico: Usando os DADOS REAIS da modelagem (Binomial e MTTF=300h)
    mttf_sensor = 300.0
    R_sensor_array = np.exp(-t_values / mttf_sensor)
    
    R_k1 = [R_koon(R_sensor, 10, 1) for R_sensor in R_sensor_array]   # Baixa tolerância (Series-like)
    R_k5 = [R_koon(R_sensor, 10, 5) for R_sensor in R_sensor_array]   # Média tolerância
    R_k10 = [R_koon(R_sensor, 10, 10) for R_sensor in R_sensor_array] # Alta tolerância (Parallel-like)
    
    # Estilo ggplot similar ao do artigo
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Usando as mesmas cores e formatos:
    # Vermelho com pontinhos (alta confiabilidade)
    ax.plot(t_values, R_k10, color='#F8766D', marker='o', markersize=3, label='C03 - 1 oo N (K=10)', linewidth=1.5, markevery=15)
    # Verde com triângulos (média)
    ax.plot(t_values, R_k5, color='#00BA38', marker='^', markersize=4, label='C02 - N/2 oo N (K=5)', linewidth=1.5, markevery=15)
    # Azul com quadrados (baixa)
    ax.plot(t_values, R_k1, color='#619CFF', marker='s', markersize=3, label='C01 - N oo N (K=1)', linewidth=1.5, markevery=15)
    
    ax.set_xlabel('Time', fontsize=12)
    ax.set_ylabel('Reliability', fontsize=12)
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(-50, 2050)
    
    ax.legend(title='Configuration', loc='center right', bbox_to_anchor=(0.85, 0.55), frameon=True, facecolor='white', edgecolor='white')
    
    ax.set_xticks([0, 500, 1000, 1500, 2000])
    ax.set_yticks([0.00, 0.25, 0.50, 0.75, 1.00])
    
    plt.tight_layout()
    os.makedirs('Case_Study_2_KooN', exist_ok=True)
    plt.savefig('Case_Study_2_KooN/grafico_confiabilidade_transiente.png', dpi=300)
    print("Gráfico gerado em Case_Study_2_KooN/grafico_confiabilidade_transiente.png")

if __name__ == "__main__":
    main()
