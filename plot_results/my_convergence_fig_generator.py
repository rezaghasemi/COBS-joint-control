import glob
import numpy as np
from tqdm import tqdm
import os
import pandas as pd
import matplotlib.pyplot as plt


row = 0

colors = {"PPO": 'r', "SAC": 'g', "Branching Dueling DQN": 'b'}
all_result = {"PPO": [], "SAC": [], "Branching Dueling DQN": []}
all_energy_result = {"PPO": [], "SAC": [], "Branching Dueling DQN": []}
all_pmv_result = {"PPO": [], "SAC": [], "Branching Dueling DQN": []}
all_pmv_vio_result = {"PPO": [], "SAC": [], "Branching Dueling DQN": []}
folder_counter = 0

folders = list()

for count, folder in enumerate(glob.glob("/media/reza/Tempo/github/COBS-joint-control/Results/rl_results/**")):
    folder_counter += 1
    folders.append(folder)
## original code is:
   
#    if "cooling" in folder and "seed19" in folder:
#        folder_counter += 1
#        folders.append(folder)

print(folder_counter)

### why 400? is that the number of runs??

results_ = np.zeros((folder_counter, 400))



for folder in tqdm(folders):
    result = list()
    energy_result = list()
    pmv_result = list()
    pmv_vio_result = list()
    current = 0

### why range 4??? it seems 4 represents the number of the run files? I changed it to num_run
    # for j in range(4):
    for j in range(4):
        if not os.path.isfile(f"{folder}/run_{j}.csv"):
            continue
        cols = ['HVAC Power', 'run', 'total reward']
        
### posibly number of the zones
        for i in range(1, 6):

            cols.append(f'Lights Zone {i}')
            cols.append(f'PMV Zone {i}')
            cols.append(f'Occu Zone {i}')
        df = pd.read_csv(f"{folder}/run_{j}.csv", usecols=cols)
        print(df.head())
        df['pmv'] = 0
        df['pmv count'] = 0
        df['pmv violate'] = 0
        for i in range(1, 6):
            df['pmv'] += abs(df[f'PMV Zone {i}']) * (df[f'Occu Zone {i}'] != 0)
            df['pmv count'] += (df[f'Occu Zone {i}'] != 0)
        df['pmv count'][df['pmv count'] == 0] = 99999
        df['pmv'] = df['pmv'] / df['pmv count']
        df['pmv violate'][abs(df['pmv']) > 0.7] = 1
        print(df.head())
        df = df.groupby(['run']).sum().sort_values(by=['run'])
        print(df.head())
        df['light'] = 0
        for i in range(1, 6):
            df['light'] += df[f'Lights Zone {i}']
        result.append(df['total reward'].values)
        energy_result.append(df['HVAC Power'].values + df['light'].values)
        pmv_result.append(df['pmv'].values)
        pmv_vio_result.append(df['pmv violate'].values)

    result = np.concatenate(result)
    energy_result = np.concatenate(energy_result)
    pmv_result = np.concatenate(pmv_result)
    pmv_vio_result = np.concatenate(pmv_vio_result)

    if "PPO" in folder:
        name = "PPO"
    elif "SAC" in folder:
        name = "SAC"
    else:
        name = "Branching Dueling DQN"
    
    all_result[name].append(result)
    all_energy_result[name].append(energy_result)
    all_pmv_result[name].append(pmv_result)
    all_pmv_vio_result[name].append(pmv_vio_result)
        
    row += 1
    print(folder, result.min())
    print(all_result)




## Reza Hand made 





## Complete visualization by Zhang

# all_color = ["blue", "red", 'green']
# hatch = ['/', '\\', '|']
# line_style = ['-', ':', '--']
# agent_name = ["PPO", "SAC", "BDQN"]

# # How it has been calculated
# confidence = 0.95

# for title_name, data_source in (("Reward", all_result), ("Energy Cost", all_energy_result), ("PMV", all_pmv_result), ("PMV violation", all_pmv_vio_result)):
#     plt.figure(figsize=(8, 4))
#     confidence = 0.95
#     algo_id = 0
#     for name in data_source:
#         min_len = min([temp_result.size for temp_result in data_source[name]])
#         matrix = np.zeros((len(data_source[name]), min_len))
#         for i, temp_result in enumerate(data_source[name]):
#             matrix[i, :] = temp_result[:min_len]
        
#         if name == "PPO":
#             matrix = np.concatenate([matrix[2:6, :], matrix[7:9, :]], axis=0)
#         if title_name in ("PMV violation", "PMV"):
#             matrix = matrix / 3071
#         plt.plot(matrix.mean(axis=0), label=agent_name[algo_id], color=all_color[algo_id], linestyle=line_style[algo_id])
#         se = scipy.stats.sem(matrix, axis=0)
#         m = matrix.mean(axis=0)
#         h = se * scipy.stats.t.ppf((1 + confidence) / 2., 8)
# #         h = se * 1.96 / (10 ** 0/5)
#         plt.fill_between(np.arange(min_len), m + h, m - h, alpha=0.4, hatch=hatch[algo_id], edgecolor=all_color[algo_id], label=agent_name[algo_id] + " 95% Confidence Interval")
#         algo_id += 1
    
#     plt.xlabel(r"$\bf{Episode}$")
#     plt.xlim([0, 400])
#     if title_name == "Reward":
#         plt.ylabel(r"$\bf{Reward}$")

#     plt.legend(loc="lower right")
#     plt.savefig("temp.png")
#     plt.show()
