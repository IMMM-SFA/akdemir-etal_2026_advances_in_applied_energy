import pandas as pd
import numpy as np
import geopandas as gpd
import yaml
from shapely.geometry import Point
from matplotlib.patches import Patch
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import glob
import seaborn as sns
from matplotlib.ticker import MultipleLocator  
import matplotlib as mpl
import matplotlib.ticker as mticker

##########################################
# years = [2025, 2030, 2035]
years = [2035]
t_scenario = 'hotter'
original_run_name = 'run_110824'
data_center_run_name = 'run_022725'
IM3_scenarios = [f'rcp45{t_scenario}_ssp3']
data_center_demand_scenarios = ['low_growth','moderate_growth','high_growth','higher_growth']
data_center_specific_scenarios = ['no_gen_retire_0_gas','no_gen_retire_25_gas','no_gen_retire_50_gas_only','no_gen_retire_50_gas','no_gen_retire_75_gas','no_gen_retire_100_gas']
##########################################

#Reading nodal topology
all_nodes = pd.read_csv('../../../../../Exp_B_Grid_Stress/Analysis/Supplementary_Data/BA_Topology_Files/selected_nodes_125.csv', header=0)
all_node_numbers = [*all_nodes['SelectedNodes']]
all_node_strings = [f'bus_{i}' for i in all_node_numbers]

nodes_to_BA = pd.read_csv('../../../../../Exp_B_Grid_Stress/Analysis/Supplementary_Data/BA_Topology_Files/nodes_to_BA_state.csv', header=0)
nodes_to_BA_filt = nodes_to_BA.loc[nodes_to_BA['Number'].isin(all_node_numbers)].copy()
BAs_df = pd.read_csv('../../../../../Exp_B_Grid_Stress/Analysis/Supplementary_Data/BA_Topology_Files/BAs.csv', header=0)
BAs_df.loc[5, 'Abbreviation'] = 'CAISO'

#Reading BAs and states shapefiles
states_gdf = gpd.read_file('../../../../../Coop_Transmission/Analysis/Data/Supplementary_Data/Shapefiles/US_States/dtl_st.shp')
states_gdf = states_gdf.loc[states_gdf['STATE_ABBR'].isin(['WA','OR','CA','AZ','NM','CO','UT','NV','ID','WY','MT'])].copy()
states_gdf = states_gdf.to_crs("EPSG:9311")

BAs_gdf = gpd.read_file('../../../Supplementary_Data/WECC_IM3_BAs_Shapefile/wecc_ba_shp_10k.shp')
BAs_gdf = BAs_gdf.to_crs("EPSG:9311")
BAs_gdf['ba_abb'] = ['NaN' for i in range(len(BAs_df))]
for my_BA in range(len(BAs_df)):
    BA_abb = BAs_df.loc[BAs_df['Name']==BAs_gdf.loc[my_BA,'ba_name']]['Abbreviation'].values[0]
    BAs_gdf.loc[my_BA,'ba_abb'] = BA_abb

BAs_gdf.sort_values(by='ba_abb', ascending=True, inplace=True)
BAs_gdf.reset_index(inplace=True,drop=True)

#Creating datasets with LMP and LOL change information
for sc in IM3_scenarios:
    for dc_d in data_center_demand_scenarios:
        for dc_s in data_center_specific_scenarios:
            globals()[f'LMP_LOL_Data_{sc}_{dc_d}_{dc_s}'] = pd.read_excel(f'../Table_Stats/LMP_LOL_Demand_Statistics_{sc}_{dc_d}.xlsx', header=0, sheet_name=f'{dc_s}', index_col=0)
            globals()[f'LMP_LOL_Data_{sc}_{dc_d}_{dc_s}'] = globals()[f'LMP_LOL_Data_{sc}_{dc_d}_{dc_s}'].loc[BAs_gdf['ba_abb'].values,:]
            globals()[f'LMP_LOL_Data_{sc}_{dc_d}_{dc_s}'].sort_index(axis='index', ascending=True, inplace=True)
            globals()[f'LMP_LOL_Data_{sc}_{dc_d}_{dc_s}'].reset_index(inplace=True,drop=True)
            
            globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_{dc_s}'] = BAs_gdf.copy()
            globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_{dc_s}'] = pd.concat([globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_{dc_s}'], globals()[f'LMP_LOL_Data_{sc}_{dc_d}_{dc_s}']], axis=1)


for sc in IM3_scenarios:
    for dc_d in data_center_demand_scenarios:
        globals()[f'LMP_LOL_Data_{sc}_{dc_d}_flat'] = pd.read_excel(f'../../Base_runs/Table_Stats/LMP_LOL_Demand_Statistics_{sc}.xlsx', header=0, sheet_name=f'{dc_d}_flat', index_col=0)
        globals()[f'LMP_LOL_Data_{sc}_{dc_d}_flat'] = globals()[f'LMP_LOL_Data_{sc}_{dc_d}_flat'].loc[BAs_gdf['ba_abb'].values,:]
        globals()[f'LMP_LOL_Data_{sc}_{dc_d}_flat'].sort_index(axis='index', ascending=True, inplace=True)
        globals()[f'LMP_LOL_Data_{sc}_{dc_d}_flat'].reset_index(inplace=True,drop=True)
        
        globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_flat'] = BAs_gdf.copy()
        globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_flat'] = pd.concat([globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_flat'], globals()[f'LMP_LOL_Data_{sc}_{dc_d}_flat']], axis=1)


#Creating a figure of BA percent LMP change maps with diverging palette for each IM3 scenario
for sc in IM3_scenarios:
    for yy in years:
    
        plt.rcParams.update({'font.size': 10})
        plt.rcParams['font.sans-serif'] = "Arial"
        plt.rcParams['axes.edgecolor'] = '#FFFFFF'
        fig,ax = plt.subplots(len(data_center_demand_scenarios),len(data_center_specific_scenarios)+1, figsize=(21,12))

        LMP_norm = mpl.colors.BoundaryNorm(boundaries=[-35,-30,-25,-20,-15,-10,-5,0,5,10,15,25,50,75,100], ncolors=256, extend='both')
        LMP_cmap = 'coolwarm'
        
        for dc_d_idx, dc_d in enumerate(data_center_demand_scenarios):
        

            globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_flat'].plot(column=f'{yy}_LMP_Diff_%', cmap=LMP_cmap, norm=LMP_norm, 
                                                                         legend=False, ax=ax[dc_d_idx, 0], linewidth=0.5)
                
            states_gdf.plot(ax=ax[dc_d_idx, 0], color='None', edgecolor='gray', linewidth=0.5, alpha=0.7)
            
            ax[dc_d_idx, 0].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
            ax[dc_d_idx, 0].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

            for dc_s_idx, dc_s in enumerate(data_center_specific_scenarios):

                globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_{dc_s}'].plot(column=f'{yy}_LMP_Diff_%', cmap=LMP_cmap, norm=LMP_norm, 
                                                                         legend=False, ax=ax[dc_d_idx, dc_s_idx+1], linewidth=0.5)
                
                states_gdf.plot(ax=ax[dc_d_idx, dc_s_idx+1], color='None', edgecolor='gray', linewidth=0.5, alpha=0.7)
                

                ax[0, 0].set_title(f'Data Center\nScenario (Generator\nRetirements\nas Planned)', weight='bold', fontsize=16)
                ax[0, 1].set_title(f'Postponing\n{100}% Nuclear\nRetirements', weight='bold', fontsize=16)
                ax[0, 2].set_title(f'Postponing {100}%\nNuclear and {25}%\nNatural Gas\nRetirements', weight='bold', fontsize=16)
                ax[0, 3].set_title(f'Postponing Only\n{50}% Natural Gas\nRetirements', weight='bold', fontsize=16)
                ax[0, 4].set_title(f'Postponing {100}%\nNuclear and {50}%\nNatural Gas\nRetirements', weight='bold', fontsize=16)
                ax[0, 5].set_title(f'Postponing {100}%\nNuclear and {75}%\nNatural Gas\nRetirements', weight='bold', fontsize=16)
                ax[0, 6].set_title(f'Postponing {100}%\nNuclear and {100}%\nNatural Gas\nRetirements', weight='bold', fontsize=16)

                ax[0, 0].set_ylabel('Low Demand Growth\n(3.71% Annually)', weight='bold', fontsize=16)
                ax[1, 0].set_ylabel('Moderate Demand\nGrowth (5% Annually)', weight='bold', fontsize=16)
                ax[2, 0].set_ylabel('High Demand Growth\n(10% Annually)', weight='bold', fontsize=16)
                ax[3, 0].set_ylabel('Higher Demand\nGrowth (15% Annually)', weight='bold', fontsize=16)

                ax[dc_d_idx, dc_s_idx+1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
                ax[dc_d_idx, dc_s_idx+1].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

        fig.tight_layout(h_pad=0.1,w_pad=0.3)
        
        # Create a ScalarMappable for the colorbar
        sm = mpl.cm.ScalarMappable(norm=LMP_norm, cmap=LMP_cmap)
        
        # Add single colorbar to the figure
        cbar = fig.colorbar(sm, ax=ax, shrink=0.45, pad=0.01, anchor=(0.02, 0.5), ticks=[-35,-30,-25,-20,-15,-10,-5,0,5,10,15,25,50,75,100], format=mticker.FixedFormatter(['-35','-30','-25','-20','-15','-10','-5','0','5','10','15','25','50','75','100']))
        cbar.set_label(f'Yearly Average LMP Change in {yy} Compared to Reference Scenario (%)', rotation=90, labelpad=10)

        plt.savefig(f'LMP_percent_maps_diverging_{sc}_{yy}.png', dpi=300, bbox_inches='tight')
        plt.show()
        plt.clf()



#Creating a figure of BA LOL to demand ratio change maps for each IM3 scenario
for sc in IM3_scenarios:
    for yy in years:
    
        plt.rcParams.update({'font.size': 10})
        plt.rcParams['font.sans-serif'] = "Arial"
        plt.rcParams['axes.edgecolor'] = '#FFFFFF'
        fig,ax = plt.subplots(len(data_center_demand_scenarios),len(data_center_specific_scenarios)+1, figsize=(21,12))

        LOL_norm = mpl.colors.BoundaryNorm(boundaries=[0.00000001, 0.2, 0.4, 0.6, 0.8, 1], ncolors=256, extend='both')
        LOL_cmap = 'Greys'
        
        for dc_d_idx, dc_d in enumerate(data_center_demand_scenarios):
        

            globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_flat'].plot(column=f'{yy}_LOL_to_Demand_%_After', cmap=LOL_cmap, norm=LOL_norm, 
                                                                         legend=False, ax=ax[dc_d_idx, 0], linewidth=0.5)
                
            states_gdf.plot(ax=ax[dc_d_idx, 0], color='None', edgecolor='gray', linewidth=0.5, alpha=0.7)
            
            ax[dc_d_idx, 0].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
            ax[dc_d_idx, 0].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

            for dc_s_idx, dc_s in enumerate(data_center_specific_scenarios):

                globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_{dc_s}'].plot(column=f'{yy}_LOL_to_Demand_%_After', cmap=LOL_cmap, norm=LOL_norm, 
                                                                         legend=False, ax=ax[dc_d_idx, dc_s_idx+1], linewidth=0.5)
                
                states_gdf.plot(ax=ax[dc_d_idx, dc_s_idx+1], color='None', edgecolor='gray', linewidth=0.5, alpha=0.7)
                

                ax[0, 0].set_title(f'Data Center\nScenario (Generator\nRetirements\nas Planned)', weight='bold', fontsize=16)
                ax[0, 1].set_title(f'Postponing\n{100}% Nuclear\nRetirements', weight='bold', fontsize=16)
                ax[0, 2].set_title(f'Postponing {100}%\nNuclear and {25}%\nNatural Gas\nRetirements', weight='bold', fontsize=16)
                ax[0, 3].set_title(f'Postponing Only\n{50}% Natural Gas\nRetirements', weight='bold', fontsize=16)
                ax[0, 4].set_title(f'Postponing {100}%\nNuclear and {50}%\nNatural Gas\nRetirements', weight='bold', fontsize=16)
                ax[0, 5].set_title(f'Postponing {100}%\nNuclear and {75}%\nNatural Gas\nRetirements', weight='bold', fontsize=16)
                ax[0, 6].set_title(f'Postponing {100}%\nNuclear and {100}%\nNatural Gas\nRetirements', weight='bold', fontsize=16)

                ax[0, 0].set_ylabel('Low Demand Growth\n(3.71% Annually)', weight='bold', fontsize=16)
                ax[1, 0].set_ylabel('Moderate Demand\nGrowth (5% Annually)', weight='bold', fontsize=16)
                ax[2, 0].set_ylabel('High Demand Growth\n(10% Annually)', weight='bold', fontsize=16)
                ax[3, 0].set_ylabel('Higher Demand\nGrowth (15% Annually)', weight='bold', fontsize=16)

                ax[dc_d_idx, dc_s_idx+1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
                ax[dc_d_idx, dc_s_idx+1].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

        fig.tight_layout(h_pad=0.1,w_pad=0.3)
        
        # Create a ScalarMappable for the colorbar
        sm = mpl.cm.ScalarMappable(norm=LOL_norm, cmap=LOL_cmap)
        
        # Add single colorbar to the figure
        cbar = fig.colorbar(sm, ax=ax, shrink=0.45, pad=0.01, anchor=(0.02, 0.5), ticks=[0.00000001, 0.2, 0.4, 0.6, 0.8, 1], format=mticker.FixedFormatter(['0', '0.2', '0.4', '0.6', '0.8', '1']))
        cbar.set_label(f'Proportion of Yearly Unserved Energy to Demand in {yy} (%)', rotation=90, labelpad=10)

        plt.savefig(f'LOL_ratio_maps_{sc}_{yy}.png', dpi=300, bbox_inches='tight')
        plt.show()
        plt.clf()



#Creating a figure of BA LOL hour change maps for each IM3 scenario
for sc in IM3_scenarios:
    for yy in years:
    
        plt.rcParams.update({'font.size': 10})
        plt.rcParams['font.sans-serif'] = "Arial"
        plt.rcParams['axes.edgecolor'] = '#FFFFFF'
        fig,ax = plt.subplots(len(data_center_demand_scenarios),len(data_center_specific_scenarios)+1, figsize=(21,12))

        LOL_norm = mpl.colors.BoundaryNorm(boundaries=[0.00000001, 10, 20, 30, 40, 50, 60, 70], ncolors=256, extend='both')
        LOL_cmap = 'Greys'
        
        for dc_d_idx, dc_d in enumerate(data_center_demand_scenarios):
        

            globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_flat'].plot(column=f'{yy}_LOL_Hours_After', cmap=LOL_cmap, norm=LOL_norm, 
                                                                         legend=False, ax=ax[dc_d_idx, 0], linewidth=0.5, 
                                                                         legend_kwds={'shrink':0.75,'label':f'Number of Yearly Unserved\nEnergy Hours in {yy}','anchor':(0, 0.4), 'ticks':[0.00000001, 10, 20, 30, 40, 50, 60, 70],
                                                                                      'format':mticker.FixedFormatter(['0', '10', '20', '30', '40', '50', '60', '70'])})
                
            states_gdf.plot(ax=ax[dc_d_idx, 0], color='None', edgecolor='gray', linewidth=0.5, alpha=0.7)
            
            ax[dc_d_idx, 0].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
            ax[dc_d_idx, 0].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

            for dc_s_idx, dc_s in enumerate(data_center_specific_scenarios):

                globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_{dc_s}'].plot(column=f'{yy}_LOL_Hours_After', cmap=LOL_cmap, norm=LOL_norm, 
                                                                         legend=False, ax=ax[dc_d_idx, dc_s_idx+1], linewidth=0.5, 
                                                                         legend_kwds={'shrink':0.75,'label':f'Number of Yearly Unserved\nEnergy Hours in {yy}','anchor':(0, 0.4), 'ticks':[0.00000001, 10, 20, 30, 40, 50, 60, 70],
                                                                                      'format':mticker.FixedFormatter(['0', '10', '20', '30', '40', '50', '60', '70'])})
                
                states_gdf.plot(ax=ax[dc_d_idx, dc_s_idx+1], color='None', edgecolor='gray', linewidth=0.5, alpha=0.7)
                

                ax[0, 0].set_title(f'Data Center\nScenario (Generator\nRetirements\nas Planned)', weight='bold', fontsize=16)
                ax[0, 1].set_title(f'Postponing\n{100}% Nuclear\nRetirements', weight='bold', fontsize=16)
                ax[0, 2].set_title(f'Postponing {100}%\nNuclear and {25}%\nNatural Gas\nRetirements', weight='bold', fontsize=16)
                ax[0, 3].set_title(f'Postponing Only\n{50}% Natural Gas\nRetirements', weight='bold', fontsize=16)
                ax[0, 4].set_title(f'Postponing {100}%\nNuclear and {50}%\nNatural Gas\nRetirements', weight='bold', fontsize=16)
                ax[0, 5].set_title(f'Postponing {100}%\nNuclear and {75}%\nNatural Gas\nRetirements', weight='bold', fontsize=16)
                ax[0, 6].set_title(f'Postponing {100}%\nNuclear and {100}%\nNatural Gas\nRetirements', weight='bold', fontsize=16)

                ax[0, 0].set_ylabel('Low Demand Growth\n(3.71% Annually)', weight='bold', fontsize=16)
                ax[1, 0].set_ylabel('Moderate Demand\nGrowth (5% Annually)', weight='bold', fontsize=16)
                ax[2, 0].set_ylabel('High Demand Growth\n(10% Annually)', weight='bold', fontsize=16)
                ax[3, 0].set_ylabel('Higher Demand\nGrowth (15% Annually)', weight='bold', fontsize=16)

                ax[dc_d_idx, dc_s_idx+1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
                ax[dc_d_idx, dc_s_idx+1].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

        fig.tight_layout(h_pad=0.1,w_pad=0.3)
        
        # Create a ScalarMappable for the colorbar
        sm = mpl.cm.ScalarMappable(norm=LOL_norm, cmap=LOL_cmap)
        
        # Add single colorbar to the figure
        cbar = fig.colorbar(sm, ax=ax, shrink=0.45, pad=0.01, anchor=(0.02, 0.5), ticks=[0.00000001, 10, 20, 30, 40, 50, 60, 70], format=mticker.FixedFormatter(['0', '10', '20', '30', '40', '50', '60', '70']))
        cbar.set_label(f'Number of Yearly Unserved Energy Hours in {yy}', rotation=90, labelpad=10)

        plt.savefig(f'LOL_hour_maps_{sc}_{yy}.png', dpi=300, bbox_inches='tight')
        plt.show()
        plt.clf()

