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
            globals()[f'LMP_LOL_Data_{sc}_{dc_d}_{dc_s}'] = pd.read_excel(f'../Table_Stats/LMP_LOL_Demand_Statistics_{sc}.xlsx', header=0, sheet_name=f'{dc_d}_{dc_s}', index_col=0)
            globals()[f'LMP_LOL_Data_{sc}_{dc_d}_{dc_s}'] = globals()[f'LMP_LOL_Data_{sc}_{dc_d}_{dc_s}'].loc[BAs_gdf['ba_abb'].values,:]
            globals()[f'LMP_LOL_Data_{sc}_{dc_d}_{dc_s}'].sort_index(axis='index', ascending=True, inplace=True)
            globals()[f'LMP_LOL_Data_{sc}_{dc_d}_{dc_s}'].reset_index(inplace=True,drop=True)
            
            globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_{dc_s}'] = BAs_gdf.copy()
            globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_{dc_s}'] = pd.concat([globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_{dc_s}'], globals()[f'LMP_LOL_Data_{sc}_{dc_d}_{dc_s}']], axis=1)



#Creating a figure of BA LMP change maps (before and after data centers) for each IM3 scenario
for sc in IM3_scenarios:
    for dc_s in data_center_specific_scenarios:

        plt.rcParams.update({'font.size': 12})
        plt.rcParams['font.sans-serif'] = "Arial"
        plt.rcParams['axes.edgecolor'] = '#FFFFFF'
        fig,ax = plt.subplots(3,5, figsize=(16,9))

        LMP_norm = mpl.colors.BoundaryNorm(boundaries=[0, 25, 50, 75, 100, 125, 150], ncolors=256, extend='both')
        LMP_cmap = 'YlOrRd'

        for yy_idx, yy in enumerate(years):

            globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_{dc_s}'].plot(column=f'{yy}_LMP_$/MWh_Before', cmap=LMP_cmap, norm=LMP_norm, 
                                                                        legend=False, ax=ax[yy_idx,0], linewidth=0.5)
            
            states_gdf.plot(ax=ax[yy_idx,0], color='None', edgecolor='gray', linewidth=0.5, alpha=0.7)

            ax[yy_idx,0].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
            ax[yy_idx,0].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

            for dc_d_idx, dc_d in enumerate(data_center_demand_scenarios):
                
                    globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_{dc_s}'].plot(column=f'{yy}_LMP_$/MWh_After', cmap=LMP_cmap, norm=LMP_norm, 
                                                                            legend=False, ax=ax[yy_idx,dc_d_idx+1], linewidth=0.5)
                    
                    states_gdf.plot(ax=ax[yy_idx,dc_d_idx+1], color='None', edgecolor='gray', linewidth=0.5, alpha=0.7)
                    
                    ax[yy_idx,dc_d_idx+1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
                    ax[yy_idx,dc_d_idx+1].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

        ax[0,0].set_title('Reference', weight='bold', fontsize=15)
        ax[0,1].set_title('Low Demand Growth\n(3.71% Annually)', weight='bold', fontsize=15)
        ax[0,2].set_title('Moderate Demand\nGrowth (5% Annually)', weight='bold', fontsize=15)
        ax[0,3].set_title('High Demand Growth\n(10% Annually)', weight='bold', fontsize=15)
        ax[0,4].set_title('Higher Demand\nGrowth (15% Annually)', weight='bold', fontsize=15)

        ax[0, 0].set_ylabel('2025', weight='bold', fontsize=15)
        ax[1, 0].set_ylabel('2030', weight='bold', fontsize=15)
        ax[2, 0].set_ylabel('2035', weight='bold', fontsize=15)

        fig.tight_layout(h_pad=0.1,w_pad=0.3)
        
        # Create a ScalarMappable for the colorbar
        sm = mpl.cm.ScalarMappable(norm=LMP_norm, cmap=LMP_cmap)
        
        # Add single colorbar to the figure
        cbar = fig.colorbar(sm, ax=ax, shrink=0.5, pad=0.01, anchor=(0.02, 0.5))
        cbar.set_label('Yearly Average LMP ($/MWh)', rotation=90, labelpad=10)
        
        plt.savefig(f'LMP_maps_{sc}_{dc_s}.png', dpi=400, bbox_inches='tight')
        plt.show()
        plt.clf()



#Creating a figure of BA LOL change maps (before and after data centers) for each IM3 scenario
for sc in IM3_scenarios:
    for dc_s in data_center_specific_scenarios:

        plt.rcParams.update({'font.size': 12})
        plt.rcParams['font.sans-serif'] = "Arial"
        plt.rcParams['axes.edgecolor'] = '#FFFFFF'
        fig,ax = plt.subplots(3,5, figsize=(16,9))

        LOL_norm = mpl.colors.BoundaryNorm(boundaries=[0.00000001, 0.2, 0.4, 0.6, 0.8, 1], ncolors=256, extend='both')
        LOL_cmap = 'Greys'

        for yy_idx, yy in enumerate(years):

            globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_{dc_s}'].plot(column=f'{yy}_LOL_to_Demand_%_Before', cmap=LOL_cmap, norm=LOL_norm, 
                                                                        legend=False, ax=ax[yy_idx,0], linewidth=0.5)
            
            states_gdf.plot(ax=ax[yy_idx,0], color='None', edgecolor='gray', linewidth=0.5, alpha=0.7)

            ax[yy_idx,0].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
            ax[yy_idx,0].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

            for dc_d_idx, dc_d in enumerate(data_center_demand_scenarios):
                
                    globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_{dc_s}'].plot(column=f'{yy}_LOL_to_Demand_%_After', cmap=LOL_cmap, norm=LOL_norm, 
                                                                            legend=False, ax=ax[yy_idx,dc_d_idx+1], linewidth=0.5)
                    
                    states_gdf.plot(ax=ax[yy_idx,dc_d_idx+1], color='None', edgecolor='gray', linewidth=0.5, alpha=0.7)
                    
                    ax[yy_idx,dc_d_idx+1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
                    ax[yy_idx,dc_d_idx+1].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

        ax[0,0].set_title('Reference', weight='bold', fontsize=15)
        ax[0,1].set_title('Low Demand Growth\n(3.71% Annually)', weight='bold', fontsize=15)
        ax[0,2].set_title('Moderate Demand\nGrowth (5% Annually)', weight='bold', fontsize=15)
        ax[0,3].set_title('High Demand Growth\n(10% Annually)', weight='bold', fontsize=15)
        ax[0,4].set_title('Higher Demand\nGrowth (15% Annually)', weight='bold', fontsize=15)

        ax[0, 0].set_ylabel('2025', weight='bold', fontsize=15)
        ax[1, 0].set_ylabel('2030', weight='bold', fontsize=15)
        ax[2, 0].set_ylabel('2035', weight='bold', fontsize=15)

        fig.tight_layout(h_pad=0.1,w_pad=0.3)
        
        # Create a ScalarMappable for the colorbar
        sm = mpl.cm.ScalarMappable(norm=LOL_norm, cmap=LOL_cmap)
        
        # Add single colorbar to the figure
        cbar = fig.colorbar(sm, ax=ax, shrink=0.5, pad=0.01, anchor=(0.02, 0.5), ticks=[0.00000001, 0.2, 0.4, 0.6, 0.8, 1], format=mticker.FixedFormatter(['0', '0.2', '0.4', '0.6', '0.8', '1']))
        cbar.set_label('Proportion of Yearly Unserved Energy to Demand (%)', rotation=90, labelpad=10)

        plt.savefig(f'LOL_ratio_maps_{sc}_{dc_s}.png', dpi=400, bbox_inches='tight')
        plt.show()
        plt.clf()


                                
#Creating a figure of BA LOL hour change maps (before and after data centers) for each IM3 scenario
for sc in IM3_scenarios:
    for dc_s in data_center_specific_scenarios:

        plt.rcParams.update({'font.size': 12})
        plt.rcParams['font.sans-serif'] = "Arial"
        plt.rcParams['axes.edgecolor'] = '#FFFFFF'
        fig,ax = plt.subplots(3,5, figsize=(16,9))

        LOL_norm = mpl.colors.BoundaryNorm(boundaries=[0.00000001, 10, 20, 30, 40, 50, 60, 70], ncolors=256, extend='both')
        LOL_cmap = 'Greys'

        for yy_idx, yy in enumerate(years):

            globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_{dc_s}'].plot(column=f'{yy}_LOL_Hours_Before', cmap=LOL_cmap, norm=LOL_norm, 
                                                                        legend=False, ax=ax[yy_idx,0], linewidth=0.5)
            
            states_gdf.plot(ax=ax[yy_idx,0], color='None', edgecolor='gray', linewidth=0.5, alpha=0.7)

            ax[yy_idx,0].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
            ax[yy_idx,0].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

            for dc_d_idx, dc_d in enumerate(data_center_demand_scenarios):
                
                    globals()[f'LMP_LOL_Data_Shape_{sc}_{dc_d}_{dc_s}'].plot(column=f'{yy}_LOL_Hours_After', cmap=LOL_cmap, norm=LOL_norm, 
                                                                            legend=False, ax=ax[yy_idx,dc_d_idx+1], linewidth=0.5)
                    
                    states_gdf.plot(ax=ax[yy_idx,dc_d_idx+1], color='None', edgecolor='gray', linewidth=0.5, alpha=0.7)
                    
                    ax[yy_idx,dc_d_idx+1].tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
                    ax[yy_idx,dc_d_idx+1].tick_params(axis='y', which='both', left=False, right=False, labelleft=False)

        ax[0,0].set_title('Reference', weight='bold', fontsize=15)
        ax[0,1].set_title('Low Demand Growth\n(3.71% Annually)', weight='bold', fontsize=15)
        ax[0,2].set_title('Moderate Demand\nGrowth (5% Annually)', weight='bold', fontsize=15)
        ax[0,3].set_title('High Demand Growth\n(10% Annually)', weight='bold', fontsize=15)
        ax[0,4].set_title('Higher Demand\nGrowth (15% Annually)', weight='bold', fontsize=15)

        ax[0, 0].set_ylabel('2025', weight='bold', fontsize=15)
        ax[1, 0].set_ylabel('2030', weight='bold', fontsize=15)
        ax[2, 0].set_ylabel('2035', weight='bold', fontsize=15)

        fig.tight_layout(h_pad=0.1,w_pad=0.3)
        
        # Create a ScalarMappable for the colorbar
        sm = mpl.cm.ScalarMappable(norm=LOL_norm, cmap=LOL_cmap)
        
        # Add single colorbar to the figure
        cbar = fig.colorbar(sm, ax=ax, shrink=0.5, pad=0.01, anchor=(0.02, 0.5), ticks=[0.00000001, 10, 20, 30, 40, 50, 60, 70], format=mticker.FixedFormatter(['0', '10', '20', '30', '40', '50', '60', '70']))
        cbar.set_label('Number of Yearly Unserved Energy Hours', rotation=90, labelpad=10)
        
        plt.savefig(f'LOL_hour_maps_{sc}_{dc_s}.png', dpi=400, bbox_inches='tight')
        plt.show()
        plt.clf()
     