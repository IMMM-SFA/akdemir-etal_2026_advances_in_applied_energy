import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches

##########################################
years = [2025, 2030, 2035]
t_scenario = 'hotter'
original_run_name = 'run_110824'
data_center_run_name = 'run_022725'
IM3_scenarios = [f'rcp45{t_scenario}_ssp3', f'rcp85{t_scenario}_ssp3', f'rcp45{t_scenario}_ssp5', f'rcp85{t_scenario}_ssp5']
data_center_demand_scenarios = ['low_growth','moderate_growth','high_growth','higher_growth']
data_center_specific_scenarios = ['flat']
##########################################

#Reading nodal topology
all_nodes = pd.read_csv('../../../../../Exp_B_Grid_Stress/Analysis/Supplementary_Data/BA_Topology_Files/selected_nodes_125.csv', header=0)
all_node_numbers = [*all_nodes['SelectedNodes']]
all_node_strings = [f'bus_{i}' for i in all_node_numbers]

hourly_timestamp = pd.date_range(start='2015-01-01 00:00:00', end='2015-12-31 23:00:00', freq='h')
daily_timestamp = pd.date_range(start='2015-01-01', end='2015-12-31', freq='d')

nodes_to_BA = pd.read_csv('../../../../../Exp_B_Grid_Stress/Analysis/Supplementary_Data/BA_Topology_Files/nodes_to_BA_state.csv', header=0)
nodes_to_BA_filt = nodes_to_BA.loc[nodes_to_BA['Number'].isin(all_node_numbers)].copy()
BAs_df = pd.read_csv('../../../../../Exp_B_Grid_Stress/Analysis/Supplementary_Data/BA_Topology_Files/BAs.csv', header=0)
BAs_df.loc[5, 'Abbreviation'] = 'CAISO'

#Reading LMP and demand and calculating demand weighted average LMP for WECC
for sc in IM3_scenarios:
    for dc_d in data_center_demand_scenarios:
        for dc_s in data_center_specific_scenarios:
            for yy in years:

                GO_Before_LMP = pd.read_parquet(glob.glob(f'Z:/im3/exp_b/exp_b_multi_model_coupling_west/experiment_runs/{original_run_name}/{sc}/go/output/native_output/{yy}/duals/duals_{yy}PI*.parquet')[0])
                GO_After_LMP = pd.read_parquet(glob.glob(f'Z:/im3/exp_b/exp_b_data_centers/task_1/experiment_runs/{data_center_run_name}/{sc}/{dc_d}/{dc_s}/go/output/native_output/{yy}/duals/duals_{yy}PI*.parquet')[0])

                GO_Before_Demand = pd.read_csv(glob.glob(f'Z:/im3/exp_b/exp_b_multi_model_coupling_west/experiment_runs/{original_run_name}/{sc}/go/input/nodal_load_csv/{yy}/nodal_load_*.csv')[0], header=0)
                GO_Before_Demand.index = hourly_timestamp
                GO_After_Demand = pd.read_csv(glob.glob(f'Z:/im3/exp_b/exp_b_data_centers/task_1/experiment_runs/{data_center_run_name}/{sc}/{dc_d}/{dc_s}/go/input/nodal_load_csv/{yy}/nodal_load_*.csv')[0], header=0)
                GO_After_Demand.index = hourly_timestamp

                GO_Before_LOL = pd.read_parquet(glob.glob(f'Z:/im3/exp_b/exp_b_multi_model_coupling_west/experiment_runs/{original_run_name}/{sc}/go/output/native_output/{yy}/slack/slack_{yy}PI*.parquet')[0])
                GO_After_LOL = pd.read_parquet(glob.glob(f'Z:/im3/exp_b/exp_b_data_centers/task_1/experiment_runs/{data_center_run_name}/{sc}/{dc_d}/{dc_s}/go/output/native_output/{yy}/slack/slack_{yy}PI*.parquet')[0])

                #Calculating and saving WECC LMP metrics
                Nodal_Demand_Weights_Before = GO_Before_Demand.sum()/GO_Before_Demand.sum().sum()
                WECC_GO_LMP_Before = np.zeros(len(hourly_timestamp))
                for bus in all_node_strings:
                    WECC_GO_LMP_Before = WECC_GO_LMP_Before + (GO_Before_LMP.loc[GO_Before_LMP['Bus']==bus]['Value'].values*Nodal_Demand_Weights_Before[bus])

                Nodal_Demand_Weights_After = GO_After_Demand.sum()/GO_After_Demand.sum().sum()
                WECC_GO_LMP_After = np.zeros(len(hourly_timestamp))
                for bus in all_node_strings:
                    WECC_GO_LMP_After = WECC_GO_LMP_After + (GO_After_LMP.loc[GO_After_LMP['Bus']==bus]['Value'].values*Nodal_Demand_Weights_After[bus])

                globals()[f'WECC_LMP_{sc}_{yy}_Before'] = WECC_GO_LMP_Before
                globals()[f'WECC_LMP_{sc}_{yy}_{dc_d}_{dc_s}_After'] = WECC_GO_LMP_After

                globals()[f'WECC_Load_LOL_{sc}_{yy}_Before'] = pd.DataFrame(GO_Before_Demand.sum(axis=1).values, columns=['Load'])
                globals()[f'WECC_Load_LOL_{sc}_{yy}_Before']['LOL_Graph_Loc'] = [np.nan if i==0 else globals()[f'WECC_Load_LOL_{sc}_{yy}_Before'].loc[idx,'Load'] for idx, i in enumerate([*GO_Before_LOL.groupby('Time').sum(numeric_only=True)['Value']])]
                globals()[f'WECC_Load_LOL_{sc}_{yy}_Before']['LOL_Actual'] = [*GO_Before_LOL.groupby('Time').sum(numeric_only=True)['Value']]

                globals()[f'WECC_Load_LOL_{sc}_{yy}_{dc_d}_{dc_s}_After'] = pd.DataFrame(GO_After_Demand.sum(axis=1).values, columns=['Load'])
                globals()[f'WECC_Load_LOL_{sc}_{yy}_{dc_d}_{dc_s}_After']['LOL_Graph_Loc'] = [np.nan if i==0 else globals()[f'WECC_Load_LOL_{sc}_{yy}_{dc_d}_{dc_s}_After'].loc[idx,'Load'] for idx, i in enumerate([*GO_After_LOL.groupby('Time').sum(numeric_only=True)['Value']])]
                globals()[f'WECC_Load_LOL_{sc}_{yy}_{dc_d}_{dc_s}_After']['LOL_Actual'] = [*GO_After_LOL.groupby('Time').sum(numeric_only=True)['Value']]



#Plotting the LMP duration curve for each scenario
for sc in IM3_scenarios:
    for dc_s in data_center_specific_scenarios: 
    
        plt.rcParams.update({'font.size': 12})
        plt.rcParams['font.sans-serif'] = "Arial"
        plt.style.use('seaborn-v0_8-whitegrid') 
        fig,ax = plt.subplots(2,3, figsize=(15,8))

        scenario_colors = ['#0173B2','#ECE133','#DE8F05','#D55E00', '#000000']
        scenario_names = ['Low Demand Growth (3.71% Annually)','Moderate Demand Growth (5% Annually)','High Demand Growth (10% Annually)','Higher Demand Growth (15% Annually)', 'Reference']

        ax[0,0].tick_params(axis='both', which='both', length=10, color='#CCCCCC')
        ax[0,1].tick_params(axis='both', which='both', length=10, color='#CCCCCC')
        ax[0,2].tick_params(axis='both', which='both', length=10, color='#CCCCCC')
        ax[1,0].tick_params(axis='both', which='both', length=10, color='#CCCCCC')
        ax[1,1].tick_params(axis='both', which='both', length=10, color='#CCCCCC')
        ax[1,2].tick_params(axis='both', which='both', length=10, color='#CCCCCC')

        for yy_idx, yy in enumerate(years):

            ax[0,yy_idx].plot(range(len(hourly_timestamp)), np.sort(globals()[f'WECC_LMP_{sc}_{yy}_Before'])[::-1],
                                    color=scenario_colors[-1], label=scenario_names[-1])
            
            ax[1,yy_idx].plot(range(len(hourly_timestamp)), np.sort(globals()[f'WECC_LMP_{sc}_{yy}_Before'])[::-1],
                                    color=scenario_colors[-1], label=scenario_names[-1])

            for dc_d_idx, dc_d in enumerate(data_center_demand_scenarios):
                ax[0,yy_idx].plot(range(len(hourly_timestamp)), np.sort(globals()[f'WECC_LMP_{sc}_{yy}_{dc_d}_{dc_s}_After'])[::-1], 
                                color=scenario_colors[dc_d_idx], label=scenario_names[dc_d_idx])
                
                ax[1,yy_idx].plot(range(len(hourly_timestamp)), np.sort(globals()[f'WECC_LMP_{sc}_{yy}_{dc_d}_{dc_s}_After'])[::-1], 
                                color=scenario_colors[dc_d_idx], label=scenario_names[dc_d_idx])

            ax[0,yy_idx].set_title(f'{yy}', weight='bold', fontsize=16) 
            ax[1,yy_idx].set_xlabel(f'Cumulative Hours', weight='bold', fontsize=15)

            ax[0,yy_idx].set_xlim([0,8760])
            ax[0,yy_idx].set_ylim([0,100])
            ax[1,yy_idx].set_xlim([0,240])
            ax[1,yy_idx].set_ylim([0,2000])

            ax[0,yy_idx].set_xticks([0,1500,3000,4500,6000,7500,8760])
            ax[1,yy_idx].set_xticks([0,40,80,120,160,200,240])
        
        
        handles = []
        line1 = Line2D([0], [0], label=scenario_names[-1], color=scenario_colors[-1])
        line2 = Line2D([0], [0], label=scenario_names[0], color=scenario_colors[0])
        line3 = Line2D([0], [0], label=scenario_names[1], color=scenario_colors[1])
        line4 = Line2D([0], [0], label=scenario_names[2], color=scenario_colors[2])
        line5 = Line2D([0], [0], label=scenario_names[3], color=scenario_colors[3])
        
        handles.extend([line1,line2,line3,line4,line5])
        fig.legend(handles=handles,loc='center', bbox_to_anchor=(0.5, -0.025), ncol=3, fontsize=12, frameon=True)

        ax[0,0].set_ylabel(f'LMP ($/MWh)', weight='bold', fontsize=15)
        ax[1,0].set_ylabel(f'LMP ($/MWh)', weight='bold', fontsize=15)

        fig.tight_layout()
        plt.savefig(f'LMP_duration_curve_{sc}_{dc_s}.png', dpi=500, bbox_inches='tight')
        plt.show()
        plt.clf()

    

#Plotting the load duration curve with unserved energy for each scenario
for sc in IM3_scenarios:
    for dc_s in data_center_specific_scenarios: 
    
        plt.rcParams.update({'font.size': 12})
        plt.rcParams['font.sans-serif'] = "Arial"
        plt.style.use('seaborn-v0_8-whitegrid') 
        fig,ax = plt.subplots(2,3, figsize=(15,8))

        scenario_colors = ['#0173B2','#ECE133','#DE8F05','#D55E00', '#000000']
        scenario_names = ['Low Demand Growth (3.71% Annually)','Moderate Demand Growth (5% Annually)','High Demand Growth (10% Annually)','Higher Demand Growth (15% Annually)', 'Reference']

        my_scale = 4

        ax[0,0].tick_params(axis='both', which='both', length=10, color='#CCCCCC')
        ax[0,1].tick_params(axis='both', which='both', length=10, color='#CCCCCC')
        ax[0,2].tick_params(axis='both', which='both', length=10, color='#CCCCCC')
        ax[1,0].tick_params(axis='both', which='both', length=10, color='#CCCCCC')
        ax[1,1].tick_params(axis='both', which='both', length=10, color='#CCCCCC')
        ax[1,2].tick_params(axis='both', which='both', length=10, color='#CCCCCC')

        for yy_idx, yy in enumerate(years):

            if np.max(globals()[f'WECC_Load_LOL_{sc}_{yy}_Before'].sort_values(by='Load', ascending=False)['LOL_Actual'].values) == 0:
                size_original = 0
            else:
                size_original = globals()[f'WECC_Load_LOL_{sc}_{yy}_Before'].sort_values(by='Load', ascending=False)['LOL_Actual'].values/globals()[f'WECC_Load_LOL_{sc}_{yy}_Before'].sort_values(by='Load', ascending=False)['Load'].values*100*my_scale

            ax[0,yy_idx].plot(range(len(hourly_timestamp)), globals()[f'WECC_Load_LOL_{sc}_{yy}_Before'].sort_values(by='Load', ascending=False)['Load'].values/1000,
                                    color=scenario_colors[-1], label=scenario_names[-1] if yy_idx == 0 else "")
            
            ax[1,yy_idx].plot(range(len(hourly_timestamp)), globals()[f'WECC_Load_LOL_{sc}_{yy}_Before'].sort_values(by='Load', ascending=False)['Load'].values/1000,
                                    color=scenario_colors[-1], label="")
            
            ax[0,yy_idx].scatter(range(len(hourly_timestamp)), globals()[f'WECC_Load_LOL_{sc}_{yy}_Before'].sort_values(by='Load', ascending=False)['LOL_Graph_Loc'].values/1000,
                                    edgecolors=scenario_colors[-1], s=size_original, facecolors='none', linewidths=0.5)
            
            ax[1,yy_idx].scatter(range(len(hourly_timestamp)), globals()[f'WECC_Load_LOL_{sc}_{yy}_Before'].sort_values(by='Load', ascending=False)['LOL_Graph_Loc'].values/1000,
                                    edgecolors=scenario_colors[-1], s=size_original, facecolors='none', linewidths=0.5)
            
            for dc_d_idx, dc_d in enumerate(data_center_demand_scenarios):

                if np.max(globals()[f'WECC_Load_LOL_{sc}_{yy}_{dc_d}_{dc_s}_After'].sort_values(by='Load', ascending=False)['LOL_Actual'].values) == 0:
                    size_scenario = 0
                else:
                    size_scenario = globals()[f'WECC_Load_LOL_{sc}_{yy}_{dc_d}_{dc_s}_After'].sort_values(by='Load', ascending=False)['LOL_Actual'].values/globals()[f'WECC_Load_LOL_{sc}_{yy}_{dc_d}_{dc_s}_After'].sort_values(by='Load', ascending=False)['Load'].values*100*my_scale

                ax[0,yy_idx].plot(range(len(hourly_timestamp)), globals()[f'WECC_Load_LOL_{sc}_{yy}_{dc_d}_{dc_s}_After'].sort_values(by='Load', ascending=False)['Load'].values/1000, 
                                color=scenario_colors[dc_d_idx], label=scenario_names[dc_d_idx] if yy_idx == 0 else "")
                
                ax[1,yy_idx].plot(range(len(hourly_timestamp)), globals()[f'WECC_Load_LOL_{sc}_{yy}_{dc_d}_{dc_s}_After'].sort_values(by='Load', ascending=False)['Load'].values/1000, 
                                color=scenario_colors[dc_d_idx], label="")
                
                ax[0,yy_idx].scatter(range(len(hourly_timestamp)), globals()[f'WECC_Load_LOL_{sc}_{yy}_{dc_d}_{dc_s}_After'].sort_values(by='Load', ascending=False)['LOL_Graph_Loc'].values/1000, 
                                edgecolors=scenario_colors[dc_d_idx], s=size_scenario, facecolors='none', linewidths=0.5)
                
                ax[1,yy_idx].scatter(range(len(hourly_timestamp)), globals()[f'WECC_Load_LOL_{sc}_{yy}_{dc_d}_{dc_s}_After'].sort_values(by='Load', ascending=False)['LOL_Graph_Loc'].values/1000, 
                                edgecolors=scenario_colors[dc_d_idx], s=size_scenario, facecolors='none', linewidths=0.5)
                
            for area in [0.5*my_scale, 1*my_scale, 2*my_scale, 4*my_scale, 8*my_scale]:
                ax[0,yy_idx].scatter([], [], c='white', s=area, label=f'{area/my_scale}% Unserved Energy' if yy_idx == 0 else "",edgecolors='#000000', linewidths=0.5)
                ax[1,yy_idx].scatter([], [], c='white', s=area, label="",edgecolors='#000000', linewidths=0.5)
            
            ax[0,yy_idx].set_title(f'{yy}', weight='bold', fontsize=16) 
            ax[1,yy_idx].set_xlabel(f'Cumulative Hours', weight='bold', fontsize=15)

            ax[0,yy_idx].set_xlim([0,8760])
            ax[1,yy_idx].set_xlim([0,240])

            if (sc == f'rcp45{t_scenario}_ssp3') or (sc == f'rcp85{t_scenario}_ssp3'):
                ax[0,yy_idx].set_ylim([60,200])
                ax[1,yy_idx].set_ylim([120,200])
            else:
                ax[0,yy_idx].set_ylim([60,220])
                ax[1,yy_idx].set_ylim([120,220])
                ax[1,yy_idx].set_yticks([120,130,140,150,160,170,180,190,200,210,220])


            ax[0,yy_idx].set_xticks([0,1500,3000,4500,6000,7500,8760])
            ax[1,yy_idx].set_xticks([0,40,80,120,160,200,240])

        ax[0,0].set_ylabel(f'Electricity Demand (GWh)', weight='bold', fontsize=15)
        ax[1,0].set_ylabel(f'Electricity Demand (GWh)', weight='bold', fontsize=15)
        fig.legend(loc='center', frameon=True, framealpha=1, ncols=5, fontsize=10, bbox_to_anchor=(0.5, -0.025))

        fig.tight_layout()
        plt.savefig(f'Load_duration_curve_{sc}_{dc_s}.png', dpi=500, bbox_inches='tight')
        plt.show()
        plt.clf()
