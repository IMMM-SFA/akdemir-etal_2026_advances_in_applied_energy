

# akdemir-etal_2026_advances_in_applied_energy

**Economic and reliability impacts of data centers on future electricity grids and potential mitigation strategies**

Kerem Ziya Akdemir<sup>1\*</sup>, Casey D. Burleyson<sup>1</sup>, Kendall Mongird<sup>1</sup>, Konstantinos Oikonomou<sup>1</sup>, Travis B. Thurber<sup>1</sup>, Chris R. Vernon<sup>1</sup>, and Jennie S. Rice<sup>1</sup>

<sup>1 </sup> Pacific Northwest National Laboratory, Richland, WA, USA

\* corresponding author: keremziya.akdemir@pnnl.gov

## Abstract
Recent advancements in artificial intelligence have created an unprecedented demand for data centers. However, increasing data center electricity demand can strain electricity grids without careful resource planning and operational practices. This study investigates the grid stress and reliability impacts of projected future data centers in the United States (U.S.) Western Interconnection between 2025 and 2035 without compensating power system upgrades. Moreover, we explore the potential benefits of two impact mitigation strategies: delaying scheduled generator retirements and data center demand response through curtailment. We analyze benefits in terms of wholesale electricity prices and unserved energy events across four data center demand growth rates: 3.71%, 5%, 10%, and 15% annually. The results indicate that data centers can cause substantial grid stress and outages in the U.S. Western Interconnection by 2035 if future generation and transmission plans do not consider these large loads. Without mitigation, increases in annual average wholesale electricity prices range from 43% to 203%, and increases in the number of annual unserved energy hours vary between 159 and 507 hours in 2035. Our findings show that postponing scheduled retirements of natural gas and nuclear generators (20.3 GW to 32.7 GW) can eliminate grid stress and reliability impacts in most regions by 2035. Despite having value during grid stress periods, curtailment of data center demands is insufficient to eliminate all data center driven grid stress and reliability issues in 2035. More efficient utilization of data center demand response can be achieved if it is combined with new generation and transmission capacity.

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
| TELL Outputs (Data center scenarios) | https://data.msdlive.org/records/93tcr-68y86 | https://doi.org/10.57931/3007669 |

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

| Script/File Name | Description |
| --- | --- |
| `GO_config.yml` | Configuration file containing paths to the input/output files of GO |
| `GO_simulation.py` | Script that creates GO model input database and starts GO model simulation |

### Steps of running GO
1. Example `GO_config.yml` file includes paths to the inputs/outputs for `rcp45hotter_ssp3`/`low_growth`/`dr_cost_500_drup_0_drdown_15` scenario combination and the year `2035`. Determine which scenario/year you would like to run and alter the paths in `GO_config.yml` so that they point to the specific [input](#input-data)/[output](#output-data)/[supplementary](#supplementary-data) datasets.
2. Make sure `my_config_file_path` parameter in `GO_simulation.py` script points to the path of `GO_config.yml` file.
3. `my_simulation_days` parameter in `GO_simulation.py` script defaults to a full-year. If you need to simulate only a certain part of the year, adjust `my_simulation_days` accordingly.
4. Change `my_solver_name` parameter in `GO_simulation.py` script so that it matches the solver you would like to use. Make sure that the solver you would like to use can be accessed via [pyomo](https://github.com/Pyomo/pyomo) package.
5. `my_dr_cost` parameter in `GO_simulation.py` script defaults to 250 $/MWh demand response compensation cost. Adjust `my_dr_cost` according to the specific scenario you would like to simulate.
6. Run `GO_simulation.py` and analyze/compare the outputs.
7. Restart from step 1 for every different scenario/year you would like to simulate. 

## Reproduce my figures
Use the scripts found in the `figures` directory to reproduce the figures used in this publication. 
- Please check and make sure that all the necessary packages listed in `requirements.txt` are installed in your local Python environment.
- Please download [input](#input-data)/[output](#output-data)/[supplementary](#supplementary-data) datasets.
- Please update all the paths in the scripts so that they point to the local paths of the downloaded [input](#input-data)/[output](#output-data)/[supplementary](#supplementary-data) datasets. 

| Figure Number | Script/File Name | Description |
| --- | --- | --- |
| 1 | `Flowchart.drawio` | Shows the flowchart with all scenario and sensitivity experiment combinations (use https://app.diagrams.net to open the file) |
| 2 | `LMP_Load_LOL_Duration_Curve.py` | Plots the LMP duration curves for all days and for the 10 worst (i.e., highest LMP) days of 2025, 2030, and 2035 |
| 3 | `LMP_Load_LOL_Duration_Curve.py` | Plots the load duration curves for all days and for the 10 worst (i.e., highest load) days of 2025, 2030, and 2035 |
| 4 | `Before_After_LMP_LOL_Map.py` | Plots the spatial distribution of yearly average LMPs in the U.S. Western Interconnection |
| 5 | `Before_After_LMP_LOL_Map.py` | Plots the spatial distribution of the proportion of yearly unserved energy to demand in the U.S. Western Interconnection |
| 6 | `LMP_LOL_Change_Colored_Maps.py` | Plots the spatial distribution of yearly average LMP change compared to the reference scenario |
| 7 | `LMP_LOL_sc_bars_nums.py` | Plots the yearly average LMP, proportion of yearly unserved energy to demand, and number of yearly unserved energy hours in 2035 |