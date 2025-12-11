

# akdemir-etal_2026_advances_in_applied_energy

**Economic and reliability impacts of data centers on future electricity grids and potential mitigation strategies**

Kerem Ziya Akdemir<sup>1\*</sup>, Casey D. Burleyson<sup>1</sup>, Kendall Mongird<sup>1</sup>, Konstantinos Oikonomou<sup>1</sup>, Travis B. Thurber<sup>1</sup>, Chris R. Vernon<sup>1</sup>, and Jennie S. Rice<sup>1</sup>

<sup>1 </sup> Pacific Northwest National Laboratory, Richland, WA, USA

\* corresponding author: keremziya.akdemir@pnnl.gov

## Abstract
Recent advancements in artificial intelligence have created an unprecedented demand for data centers. However, increasing data center electricity demand can strain electricity grids without careful resource planning practices. This study investigates the grid stress and reliability impacts of projected future data centers in the United States (U.S.) Western Interconnection between 2025 and 2035 without compensating power system upgrades. Moreover, we explore the potential benefits of two impact mitigation strategies: delaying scheduled generator retirements and data center demand response through curtailment. We analyze benefits in terms of wholesale electricity prices and unserved energy events across four data center demand growth rates: 3.71%, 5%, 10%, and 15% annually. The results indicate that data centers can cause substantial grid stress and outages in the U.S. Western Interconnection if future generation and transmission plans do not consider these large loads by 2035. Depending on data center demand growth levels, increases in annual average wholesale electricity prices range from 43% to 203% in 2035. Increases in the number of annual unserved energy hours vary between 159 and 507 hours in 2035. Postponing scheduled retirements of natural gas and nuclear generators (20.3 GW to 32.7 GW) can eliminate grid stress and reliability impacts in most regions. Despite having value during grid stress periods, curtailment of data center demands is insufficient to eliminate all data center driven grid stress and reliability issues in 2035. More efficient utilization of data center demand response can be achieved if it is combined with new generation and transmission capacity.

## Journal reference
To be updated with appropriate reference information once the paper is published.

## Code reference
To be updated with appropriate reference information once the paper is published.

## Data reference

### Input data
| Dataset | Repository Link | DOI |
| --- | --- | --- |
| GO Inputs (Data center scenarios) | https://data.msdlive.org/records/jcsdw-gpt30 | https://doi.org/10.57931/2589826 |
| GO Inputs (Reference scenarios) | https://data.msdlive.org/records/7art3-45280 | https://doi.org/10.57931/2497839 |

### Output data
| Dataset | Repository Link | DOI |
| --- | --- | --- |
| GO Outputs (Data center scenarios) | https://data.msdlive.org/records/jcsdw-gpt30 | https://doi.org/10.57931/2589826 |
| GO Outputs (Reference scenarios) | https://data.msdlive.org/records/7art3-45280 | https://doi.org/10.57931/2497839 |

### Supplementary data
All supplementary data can be found in the `supplementary_data` directory.

| Dataset | Description | Reference |
| --- | --- | --- |
| BA_Topology_Files/BAs.csv | Names and abbreviations of 28 balancing authorities considered in the U.S. Western Interconnection | Created by authors |
| BA_Topology_Files/nodes_to_BA_state.csv | Nodal information including number IDs, names, area names, voltages, angles, locations, loads, geometries, balancing authority and state information within 10000-nodal topology of the U.S. Western Interconnection | [ACTIVSg10k](https://electricgrids.engr.tamu.edu/electric-grid-test-cases/activsg10k/) (Modified by authors) |
| BA_Topology_Files/selected_nodes_125.csv | Number IDs of the selected nodes within reduced 125-nodal topology of the U.S. Western Interconnection  | Created by authors |
| Shapefiles/US_states | Folder including shapefile of U.S. census states | [U.S. EIA](https://atlas.eia.gov/maps/774019f31f8549c39b5c72f149bbe74e) |
| Shapefiles/WECC_IM3_BAs | Folder including shapefile of WECC balancing authorities | Created by authors |

## Contributing modeling software
| Model | Version | Model Repository Link | DOI of Specific Version |
| --- | --- | --- | --- |
| GO | v0.1.0 | https://github.com/IMMM-SFA/go | https://doi.org/10.5281/zenodo.15399795 |
| TEP | v1.1.0 | https://github.com/keremakdemir/Transmission_Expansion_Planner | https://doi.org/10.5281/zenodo.15413081 |
| GCAM-USA | v5.3 | https://github.com/JGCRI/gcam-core | https://doi.org/10.5281/zenodo.3908600 |
| CERF | v2.4.0 | https://github.com/IMMM-SFA/cerf | https://doi.org/10.5281/zenodo.13830460 |
| TELL | v1.1.0 | https://github.com/IMMM-SFA/tell | https://doi.org/10.5281/zenodo.8264217 |
| reV | v0.7.0 | https://github.com/NREL/reV | https://doi.org/10.5281/zenodo.7301491 |

## Reproduce my experiment
Use the scripts/files found in the `workflow` directory to reproduce the experiment presented in this publication. 
- Please check and make sure that all the necessary packages listed in `requirements.txt` are installed in your local Python environment.
- Please download [input](#input-data)/[output](#output-data)/[supplementary](#supplementary-data) datasets.
- Please update all the paths in the configuration files and scripts so that they point to the local paths of the downloaded [input](#input-data)/[output](#output-data)/[supplementary](#supplementary-data) datasets.
- By default, transmission network optimization outputs from TEP is fed into GO and used as an input.

| Script/File Name | Description |
| --- | --- |
| `GO_config.yml` | Configuration file containing paths to the input/output files of GO |
| `GO_simulation.py` | Script that creates GO model input database and starts GO model simulation |

### Steps of running GO
1. Example `GO_config.yml` file includes paths to the inputs/outputs for scenario `rcp45cooler_ssp3` and year `2050`. Determine which scenario/year you would like to run and alter the paths in `GO_config.yml` so that they point to the specific [input](#input-data)/[output](#output-data)/[supplementary](#supplementary-data) datasets.
2. Make sure `my_config_file_path` parameter in `GO_simulation.py` script points to the path of `GO_config.yml` file.
3. `my_simulation_days` parameter in `GO_simulation.py` script defaults to a full-year. If you need to simulate only a certain part of the year, adjust `my_simulation_days` accordingly.
4. Change `my_solver_name` parameter in `GO_simulation.py` script so that it matches the solver you would like to use. Make sure that the solver you would like to use can be accessed via [pyomo](https://github.com/Pyomo/pyomo) package.
5. Run `GO_simulation.py` and analyze/compare the outputs.
6. Restart from step 1 for every different scenario/year you would like to simulate. 

## Reproduce my figures
Use the scripts found in the `figures` directory to reproduce the figures used in this publication. 
- Please check and make sure that all the necessary packages listed in `requirements.txt` are installed in your local Python environment.
- Please download [input](#input-data)/[output](#output-data)/[supplementary](#supplementary-data) datasets.
- Please update all the paths in the scripts so that they point to the local paths of the downloaded [input](#input-data)/[output](#output-data)/[supplementary](#supplementary-data) datasets. 
- Setting `t_scenario = cooler` would produce the figures in the main body of the manuscript, whereas setting `t_scenario = hotter` would produce the figures in the supplementary information.

| Figure Number | Script/File Name | Description |
| --- | --- | --- |
| 1 | `Experiment_flowchart.pptx` | Shows the flowchart of the modeling chain to simulate grid stress and reliability between 2020 and 2055 |
| 2 | `Nodal_topology.py` | Plots the 125-nodal topology of GO model and three transmission planning regions of the U.S. Western Interconnection |
| 3 | `Grid_futures.py` | Plots the changes in dispatchable generation capacity, renewable generation capacity, storage discharge capacity, intraregional transmission capacity, interregional transmission capacity, and average hourly demand between 2020-2055 |
| 4 | `Generation_mix.py` | Plots the annual generation mix in U.S. Western Interconnection between 2020-2055 |
| 5 | `LMP_demand_boxplots.py` | Plots the distributions of daily average LMP and daily average demand for the U.S. Western Interconnection between 2020-2055 |
| 6 | `LMP_LOL_heatmaps.py` | Plots the yearly average LMP and yearly unserved energy to demand ratio for each U.S. Western Interconnection balancing authority and for each simulation year between 2020-2055 |
| 7 | `Reasons_for_grid_stress.py` | Plots the demand, available renewable and storage capacities, intraregional and interregional transmission line usage, day of year and hour of day distributions of high LMP and unserved energy events considering all simulation years between 2020-2055 |
| 8 | `Storage_net_demand_trends.py` | Plots the average hour of day trends of storage capacity utilization and net demand for each simulation year between 2020-2055 |