import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import seaborn as sns
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

##########################################
years = [2025, 2030, 2035]
t_scenario = 'hotter'
original_run_name = 'run_110824'
data_center_run_name = 'run_022725'
IM3_scenarios = [f'rcp45{t_scenario}_ssp3']
data_center_demand_scenarios = ['low_growth','moderate_growth','high_growth','higher_growth']
data_center_specific_scenarios_1 = ['no_gen_retire_0_gas','no_gen_retire_25_gas','no_gen_retire_50_gas_only','no_gen_retire_50_gas','no_gen_retire_75_gas','no_gen_retire_100_gas']
data_center_specific_scenarios_2 = ['cost_750_drup_0_drdown_5','cost_500_drup_0_drdown_5', 'cost_250_drup_0_drdown_5' ,'cost_750_drup_0_drdown_15','cost_500_drup_0_drdown_15', 'cost_250_drup_0_drdown_15']
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

#Creating LMP and LOL scenario datasets for plotting
All_areas = []
All_DC_demands = []
All_DC_scenarios = []
All_years = []
All_Metrics = []
All_Values = []

#Firstly, populating base IM3 and flat metrics
for sc in IM3_scenarios:
    for dc_d in data_center_demand_scenarios:
        
        Stats_case = pd.read_excel(f'../../Base_runs/Table_Stats/LMP_LOL_Demand_Statistics_{sc}.xlsx', header=0, sheet_name=f'{dc_d}_flat', index_col=0)

        for dc_s in ['Before','After']:
            for yy in years:
                for my_BA in [*Stats_case.index]:
                    for my_m in ['LMP_$/MWh','LOL_to_Demand_%','LOL_Hours']:

                        if dc_d == 'low_growth':
                            dc_d_name = 'Low growth (3.71% Annually)'
                        elif dc_d == 'moderate_growth':
                            dc_d_name = 'Moderate growth (5% Annually)'
                        elif dc_d == 'high_growth':
                            dc_d_name = 'High growth (10% Annually)'
                        elif dc_d == 'higher_growth':
                            dc_d_name = 'Higher growth (15% Annually)'

                        if dc_s == 'Before':
                            dc_s_name = 'Base'
                        elif dc_s == 'After':
                            dc_s_name = 'Flat'

                        All_areas.append(my_BA)
                        All_DC_demands.append(dc_d_name)
                        All_DC_scenarios.append(dc_s_name)
                        All_years.append(yy)
                        All_Metrics.append(my_m)
                        All_Values.append(Stats_case.loc[my_BA,f'{yy}_{my_m}_{dc_s}'])


#Secondly, populating generator retirement delay scenario metrics
for sc in IM3_scenarios:
    for dc_d in data_center_demand_scenarios:
        for dc_s in data_center_specific_scenarios_1:
        
            Stats_case = pd.read_excel(f'../../No_retire/Table_Stats/LMP_LOL_Demand_Statistics_{sc}_{dc_d}.xlsx', header=0, sheet_name=f'{dc_s}', index_col=0)
            
            for yy in years:
                for my_BA in [*Stats_case.index]:
                    for my_m in ['LMP_$/MWh','LOL_to_Demand_%','LOL_Hours']:

                        if dc_d == 'low_growth':
                            dc_d_name = 'Low growth (3.71% Annually)'
                        elif dc_d == 'moderate_growth':
                            dc_d_name = 'Moderate growth (5% Annually)'
                        elif dc_d == 'high_growth':
                            dc_d_name = 'High growth (10% Annually)'
                        elif dc_d == 'higher_growth':
                            dc_d_name = 'Higher growth (15% Annually)'

                        All_areas.append(my_BA)
                        All_DC_demands.append(dc_d_name)
                        All_DC_scenarios.append(dc_s)
                        All_years.append(yy)
                        All_Metrics.append(my_m)
                        All_Values.append(Stats_case.loc[my_BA,f'{yy}_{my_m}_After'])



#Thirdly, populating demand curtailment scenario metrics
for sc in IM3_scenarios:
    for dc_d in data_center_demand_scenarios:
        for dc_s in data_center_specific_scenarios_2:
        
            Stats_case = pd.read_excel(f'../Table_Stats/LMP_LOL_Demand_Statistics_{sc}_{dc_d}.xlsx', header=0, sheet_name=f'{dc_s}', index_col=0)
            
            for yy in years:
                for my_BA in [*Stats_case.index]:
                    for my_m in ['LMP_$/MWh','LOL_to_Demand_%','LOL_Hours']:

                        if dc_d == 'low_growth':
                            dc_d_name = 'Low growth (3.71% Annually)'
                        elif dc_d == 'moderate_growth':
                            dc_d_name = 'Moderate growth (5% Annually)'
                        elif dc_d == 'high_growth':
                            dc_d_name = 'High growth (10% Annually)'
                        elif dc_d == 'higher_growth':
                            dc_d_name = 'Higher growth (15% Annually)'

                        All_areas.append(my_BA)
                        All_DC_demands.append(dc_d_name)
                        All_DC_scenarios.append(dc_s)
                        All_years.append(yy)
                        All_Metrics.append(my_m)
                        All_Values.append(Stats_case.loc[my_BA,f'{yy}_{my_m}_After'])



#Creating a final dataset including all necessary data
LMP_LOL_data = pd.DataFrame(zip(All_areas,All_DC_demands,All_DC_scenarios,All_years,All_Metrics,All_Values), columns=['Region','Demand Scenario','Simulation Scenario','Year','Metric','Value'])  
        


#Plotting LMP and LOL metrics for each scenario
# for my_area in ['WECC','AZPS','BPAT','CAISO','NEVP']:
for my_area in ['WECC']:
    for yy in years:

        plt.rcParams.update({'font.size': 9})
        plt.rcParams['font.sans-serif'] = "Arial"
        fig,ax = plt.subplots(1,3, figsize=(12,8),sharey=True)

        scenario_colors = ['#0173B2','#ECE133','#DE8F05','#D55E00']
        scenario_names = ['Low growth (3.71% Annually)','Moderate growth (5% Annually)','High growth (10% Annually)','Higher growth (15% Annually)']
        
        data_BA_filt = LMP_LOL_data.loc[LMP_LOL_data['Region']==my_area].copy()
        data_BA_base_filt = data_BA_filt.loc[(data_BA_filt['Simulation Scenario']=='Base') & (data_BA_filt['Demand Scenario']=='Low growth (3.71% Annually)')].copy()
        data_BA_scenario_filt = data_BA_filt.loc[data_BA_filt['Simulation Scenario']!='Base'].copy()

        for my_m_idx, my_m in enumerate(['LMP_$/MWh','LOL_to_Demand_%','LOL_Hours']):
            
            data_BA_base_filt_further = data_BA_base_filt.loc[(data_BA_base_filt['Year']==yy) & (data_BA_base_filt['Metric']==my_m)].copy()
            data_BA_scenario_filt_further = data_BA_scenario_filt.loc[(data_BA_scenario_filt['Year']==yy) & (data_BA_scenario_filt['Metric']==my_m)].copy()

            ax[my_m_idx].axvline(data_BA_base_filt_further['Value'].values[0], color='#000000', alpha=0.5)
            ax_s = sns.barplot(ax=ax[my_m_idx], data=data_BA_scenario_filt_further, x='Value', y='Simulation Scenario', hue='Demand Scenario', errorbar=None, orient='h', palette=scenario_colors, hue_order=scenario_names, saturation=1, legend=False)
            
            if my_m == 'LOL_to_Demand_%':
                ax_s.bar_label(container = ax_s.containers[0], labels=[f'{int(bar.get_width())}' if bar.get_width() < 0.001 else f'{round(bar.get_width(),3)}' for bar in ax_s.containers[0]], fontsize=6, padding=1)
                ax_s.bar_label(container = ax_s.containers[1], labels=[f'{int(bar.get_width())}' if bar.get_width() < 0.001 else f'{round(bar.get_width(),3)}' for bar in ax_s.containers[1]], fontsize=6, padding=1)
                ax_s.bar_label(container = ax_s.containers[2], labels=[f'{int(bar.get_width())}' if bar.get_width() < 0.001 else f'{round(bar.get_width(),3)}' for bar in ax_s.containers[2]], fontsize=6, padding=1)
                ax_s.bar_label(container = ax_s.containers[3], labels=[f'{int(bar.get_width())}' if bar.get_width() < 0.001 else f'{round(bar.get_width(),3)}' for bar in ax_s.containers[3]], fontsize=6, padding=1)

            elif my_m == 'LOL_Hours':
                ax_s.bar_label(container = ax_s.containers[0], labels=[f'{int(bar.get_width())}' if bar.get_width() < 0.001 else f'{round(bar.get_width())}' for bar in ax_s.containers[0]], fontsize=6, padding=1)
                ax_s.bar_label(container = ax_s.containers[1], labels=[f'{int(bar.get_width())}' if bar.get_width() < 0.001 else f'{round(bar.get_width())}' for bar in ax_s.containers[1]], fontsize=6, padding=1)
                ax_s.bar_label(container = ax_s.containers[2], labels=[f'{int(bar.get_width())}' if bar.get_width() < 0.001 else f'{round(bar.get_width())}' for bar in ax_s.containers[2]], fontsize=6, padding=1)
                ax_s.bar_label(container = ax_s.containers[3], labels=[f'{int(bar.get_width())}' if bar.get_width() < 0.001 else f'{round(bar.get_width())}' for bar in ax_s.containers[3]], fontsize=6, padding=1)

            else:
                ax_s.bar_label(container = ax_s.containers[0], labels=[f'{int(bar.get_width())}' if bar.get_width() < 0.001 else f'{round(bar.get_width(),1)}' for bar in ax_s.containers[0]], fontsize=6, padding=1)
                ax_s.bar_label(container = ax_s.containers[1], labels=[f'{int(bar.get_width())}' if bar.get_width() < 0.001 else f'{round(bar.get_width(),1)}' for bar in ax_s.containers[1]], fontsize=6, padding=1)
                ax_s.bar_label(container = ax_s.containers[2], labels=[f'{int(bar.get_width())}' if bar.get_width() < 0.001 else f'{round(bar.get_width(),1)}' for bar in ax_s.containers[2]], fontsize=6, padding=1)
                ax_s.bar_label(container = ax_s.containers[3], labels=[f'{int(bar.get_width())}' if bar.get_width() < 0.001 else f'{round(bar.get_width(),1)}' for bar in ax_s.containers[3]], fontsize=6, padding=1)
            
            sns.despine()

        ax[0].set_xlabel('Yearly Average LMP ($/MWh)', weight='bold', fontsize=12) 
        ax[1].set_xlabel('Proportion of Yearly Unserved\nEnergy to Demand (%)', weight='bold', fontsize=12) 
        ax[2].set_xlabel('Number of Yearly Unserved\nEnergy Hours', weight='bold', fontsize=12) 

        ax[0].set(ylabel='')

        ax[0].set_yticks(['Flat']+data_center_specific_scenarios_1+data_center_specific_scenarios_2) 
        ax[1].set_yticks(['Flat']+data_center_specific_scenarios_1+data_center_specific_scenarios_2) 
        ax[2].set_yticks(['Flat']+data_center_specific_scenarios_1+data_center_specific_scenarios_2) 

        ax[0].set_xlim([0,200])
        ax[0].set_xticks([0,50,100,150,200])
        ax[0].set_xticklabels(['0','50','100','150','200'])

        ax[1].set_xlim([0,0.5])
        ax[1].set_xticks([0,0.1,0.2,0.3,0.4,0.5])
        ax[1].set_xticklabels(['0','0.1','0.2','0.3','0.4','0.5'])

        ax[2].set_xlim([0,600])
        ax[2].set_xticks([0,100,200,300,400,500,600])
        ax[2].set_xticklabels(['0','100','200','300','400','500','600'])

        ax[0].set_yticklabels([f'Data Center Scenario',f'Postponing {100}%\nNuclear Retirements',
                                f'Postponing {100}%\nNuclear and {25}%\nNatural Gas Retirements',f'Postponing Only {50}%\nNatural Gas Retirements',
                                f'Postponing {100}%\nNuclear and {50}%\nNatural Gas Retirements',f'Postponing {100}%\nNuclear and {75}%\nNatural Gas Retirements',
                                f'Postponing {100}%\nNuclear and {100}%\nNatural Gas Retirements',f'5% Demand Available\nfor Curtailment with\n750 $/MWh Compensation',
                                f'5% Demand Available\nfor Curtailment with\n500 $/MWh Compensation', f'5% Demand Available\nfor Curtailment with\n250 $/MWh Compensation',
                                f'15% Demand Available\nfor Curtailment with\n750 $/MWh Compensation', f'15% Demand Available\nfor Curtailment with\n500 $/MWh Compensation',
                                f'15% Demand Available\nfor Curtailment with\n250 $/MWh Compensation']) 

        
        handles = []
        patch1 = Patch(facecolor='#0173B2', edgecolor=None,label='Low Demand Growth\n(3.71% Annually)',linewidth=0.5)
        patch2 = Patch(facecolor='#ECE133', edgecolor=None,label='Moderate Demand Growth\n(5% Annually)',linewidth=0.5)
        patch3 = Patch(facecolor='#DE8F05', edgecolor=None,label='High Demand Growth\n(10% Annually)',linewidth=0.5)
        patch4 = Patch(facecolor='#D55E00', edgecolor=None,label='Higher Demand Growth\n(15% Annually)',linewidth=0.5)
        line1 = Line2D([0], [0], label='Reference', color='#000000', alpha=0.5)
        handles.extend([line1,patch1,patch2,patch3,patch4])

        fig.legend(handles=handles,loc='center', bbox_to_anchor=(0.58, -0.018), ncol=5, fontsize=8, frameon=True, framealpha=1)
        
        fig.tight_layout()

        plt.savefig(f'LMP_LOL_case_comparison_{my_area}_{yy}.png', dpi=500, bbox_inches='tight')
        plt.show()
        plt.clf()

