import os
import csv
import numpy as np
from scipy.stats import binom

# Parâmetros Base
params = {
    'Cloud Srv':  {'mttf': 760.0,   'mttr': 0.74},
    'Edge svr':   {'mttf': 940.0,   'mttr': 1.37},
    'Router':     {'mttf': 698.22,  'mttr': 8.0},
    'Gateway':    {'mttf': 480.77,  'mttr': 8.0},
    'Supervisor': {'mttf': 44.957,  'mttr': 1.0},
    'Sensors':    {'mttf': 18.0,   'mttr': 2.0},
    'Power Grid': {'mttf': 8.757,   'mttr': 4.807},
    'Power Gen':  {'mttf': 636.0,   'mttr': 37.0},
    'Sw Power':   {'mttf': 25.0,    'mttr': 8.0},
    'Sol Inv':    {'mttf': 24.82,   'mttr': 8.0},
    'Chg Ctrl':   {'mttf': 70.08,   'mttr': 8.0},
    'Sol Painel': {'mttf': 219.0,   'mttr': 8.0},
    'Battery':    {'mttf': 47.829,  'mttr': 8.0},
}

def avail(mttf, mttr):
    return mttf / (mttf + mttr)

def avail_koon(a_sensor, n, k):
    q = 1 - a_sensor
    prob_fail = sum(binom.pmf(i, n, q) for i in range(k, n+1))
    return 1 - prob_fail

A = {name: avail(p['mttf'], p['mttr']) for name, p in params.items()}

def calc_system(A_dict, koon_k=5):
    n_sensors = 10
    Q_sol_bat = (1 - A_dict['Sol Painel']) * (1 - A_dict['Battery'])
    A_sol_bat = 1 - Q_sol_bat
    A_solar = A_dict['Sw Power'] * A_dict['Sol Inv'] * A_dict['Chg Ctrl'] * A_sol_bat
    Q_power = (1 - A_dict['Power Grid']) * (1 - A_dict['Power Gen']) * (1 - A_solar)
    A_power = 1 - Q_power
    A_beds = avail_koon(A_dict['Sensors'], n_sensors, koon_k)
    A_hosp = (A_dict['Cloud Srv'] * A_dict['Edge svr'] * A_dict['Router'] *
               A_dict['Gateway'] * A_dict['Supervisor'] * A_beds)
    A_sys = A_hosp * A_power
    return A_sys, A_hosp, A_power

def main():
    # Cria as pastas para organização
    folders = ['Case_Study_1_Energy', 'Case_Study_2_KooN', 'Case_Study_3_Sensitivity']
    for f in folders:
        os.makedirs(f, exist_ok=True)
        
    A_sys, A_hosp, A_power = calc_system(A)
    
    # ==========================================
    # Case Study 1: Impact of Energy Configuration
    # ==========================================
    A_pwr_A = A['Power Grid']
    Q_pwr_B = (1-A['Power Grid']) * (1-A['Power Gen'])
    A_pwr_B = 1 - Q_pwr_B
    A_pwr_C = A_power
    
    A_hosp_base = A_hosp 
    
    avail_configs = [A_hosp_base * A_pwr_A, A_hosp_base * A_pwr_B, A_sys]
    downtime_configs = [(1-a)*8760 for a in avail_configs]
    labels_configs = ['Config. A (Grid Only)', 'Config. B (Grid + Generator)', 'Config. C (Grid + Gen + Solar)']
    
    with open('Case_Study_1_Energy/data_energy.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Configuration', 'Availability', 'Downtime'])
        for l, a, d in zip(labels_configs, avail_configs, downtime_configs):
            writer.writerow([l, a, d])
            
    # ==========================================
    # Case Study 2: KooN Variation
    # ==========================================
    k_values = list(range(1, 11))
    sys_avails_koon = []
    for k in k_values:
        a, _, _ = calc_system(A, koon_k=k)
        sys_avails_koon.append(a)
        
    with open('Case_Study_2_KooN/data_koon.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['k', 'Availability'])
        for k, val in zip(k_values, sys_avails_koon):
            writer.writerow([k, val])
            
    # ==========================================
    # Case Study 3: Sensitivity Analysis
    # ==========================================
    components_sa = ['Power Grid', 'Edge svr', 'Cloud Srv', 'Gateway', 'Supervisor']
    factors = [0.5, 0.75, 1.0, 1.25, 1.5]
    
    with open('Case_Study_3_Sensitivity/data_sensitivity.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ['Component', 'Factor', 'Availability']
        writer.writerow(header)
        for comp in components_sa:
            for fac in factors:
                A_mod = dict(A)
                A_mod[comp] = avail(params[comp]['mttf'] * fac, params[comp]['mttr'])
                a_s, _, _ = calc_system(A_mod)
                writer.writerow([comp, fac, a_s])
                
    print("Cálculos concluídos com sucesso. CSVs gerados nas respectivas pastas de cada Estudo de Caso.")

if __name__ == "__main__":
    main()
