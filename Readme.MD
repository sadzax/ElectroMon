# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Description

ElectroMon is the app that monitors high-voltage parameters. 
It uses data uploaded from devices that make minute-by-minute measurements 
in power plants, transformers and other electrical appliances.

&nbsp;

# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Implementation
## Tech-stack
Backend is written in 
**Python**,
graphs and plots are provided by **Jupyter Notebook** 

&nbsp;

## Requirements and peculiarities
Requires some Python additional classic libs, all of which can be downloaded via `pip install`:

Check [requirements.txt](requirements.txt) in root directory

The actual devices are applied with usage of cyrillic characters. 
Encoding and translational features should be considered.

Data source located in `upload/`

&nbsp;

## App Structure
### &nbsp;&nbsp; Device initialisation ([devices.py](devices.py))
ElectroMon bases on actual physical devices-measurers, described in file 
[devices.py](devices.py)

It also able to content

&nbsp;&nbsp; There is a list of them:
- ``nkvv`` - Device for continuous monitoring and protection of high-voltage inputs<details><summary>cyrillic</summary>Устройство непрерывного контроля и защиты высоковольтных вводов</details>
- ``kiv`` - Input isolation monitoring device <details><summary>cyrillic</summary>Устройство контроля изоляции вводов</details>
- ``monitoring`` - Monitoring of devices for continuous monitoring and protection of high-voltage inputs <details><summary>cyrillic</summary>Мониторинг устройств непрерывного контроля и защиты высоковольтных вводов</details>

[Devices](devices.py) 
mostly store and return attributes for further processing.
Module consist of methods setting properties and statuses of device, such as:
- name of the device
- default folder and files for uploads of data
- type of data source, used delimiters, splitters etc.
- columns used for setting values of measurements and their decoding map 
- typical errors of the devices measurements
- misc. info
<details><summary>Example of device initialisation</summary>

    nkvv.name = 'nkvv'
    nkvv.full_name = 'Устройство непрерывного контроля и защиты высоковольтных вводов'
    nkvv.monitoring_params = {'input': 220000, 'output': 110000}
    nkvv.log_types = {'measure': 'csv', 'event': 'csv'}
    self.file_folder = 'upload/' + name + '/'
    nkvv.file_name_starts = {'measure': 'DB_i'}
    nkvv.file_sep = ';'
    nkvv.file_default_encoding = 'WINDOWS-1251'
    nkvv.file_parse_dates = ['Дата создания записи', 'Дата сохранения в БД']
    nkvv.default_dict_for_replacement_to_nan = {'power': [-300.0, 0.0],
                                                'tg': -10.0,
                                                '∆tg': -10.0,
                                                'c_delta': -10.0,
                                                'c_deviation': 0.0,
                                                'voltage_difference': 0.0}
</details>

### &nbsp;&nbsp; Columns processing ([columns.py](columns.py)) 
Based on [devices](devices) attributes
[сolumns](columns.py)
processes data columns into Python dictionary with enumerated keys (can be used as indexes too) 
and values as list of parameters:
1. Original name of the column passed as string
2. Measurement used
3. Code of sensor and a phase 
4. Voltage parameter 
5. Short search name
6. Full search name
7. Concatenation of short search name and voltage parameter

[Columns](columns.py) are set to cover column's parameters across as many viewpoints as possible

<details><summary>Example of columns dictionary</summary>

    0: ['Дата создания записи', 'datetime', 'overall', 'no_voltage', 'time', 'time_of_measure', 'time_no_voltage'],
    1: ['Дата сохранения в БД', 'datetime', 'overall', 'no_voltage', 'save', 'time_of_saving', 'save_no_voltage'],
    2: ['U_A1,кВ', 'voltage', 'A1', 'HV', 'U', 'voltage_difference', 'U_HV'],
    3: ['Ia_A1,мА', 'power', 'A1', 'HV', 'Ia', 'power_active', 'Ia_HV'],
    4: ['Ir_A1,мА', 'power', 'A1', 'HV', 'Ir', 'power_reactive', 'Ir_HV'],
    5: ['Tg_A1,%', 'percentage', 'A1', 'HV', 'tg', 'tangent', 'tg_HV'],
    6: ['C_A1,пФ', 'other', 'A1', 'HV', 'C', 'c_deviation', 'C_HV'],
    7: ['DeltaTg_A1,%', 'percentage', 'A1', 'HV', '∆tg', 'tangent_delta', '∆tg_HV'],
    8: ['DeltaC_A1,%', 'percentage', 'A1', 'HV', '∆C', 'c_delta', '∆C_HV'],
    9: ['U_B1,кВ', 'voltage', 'B1', 'HV', 'U', 'voltage_difference', 'U_HV'],
    10: ['Ia_B1,мА', 'power', 'B1', 'HV', 'Ia', 'power_active', 'Ia_HV'],
    11: ['Ir_B1,мА', 'power', 'B1', 'HV', 'Ir', 'power_reactive', 'Ir_HV'],
    12: ['Tg_B1,%', 'percentage', 'B1', 'HV', 'tg', 'tangent', 'tg_HV'],
    13: ['C_B1,пФ', 'other', 'B1', 'HV', 'C', 'c_deviation', 'C_HV'],
    14: ['DeltaTg_B1,%', 'percentage', 'B1', 'HV', '∆tg', 'tangent_delta', '∆tg_HV'],
    15: ['DeltaC_B1,%', 'percentage', 'B1', 'HV', '∆C', 'c_delta', '∆C_HV'],
    16: ['U_C1,кВ', 'voltage', 'C1', 'HV', 'U', 'voltage_difference', 'U_HV'],
    17: ['Ia_C1,мА', 'power', 'C1', 'HV', 'Ia', 'power_active', 'Ia_HV'],
    18: ['Ir_C1,мА', 'power', 'C1', 'HV', 'Ir', 'power_reactive', 'Ir_HV'],
    19: ['Tg_C1,%', 'percentage', 'C1', 'HV', 'tg', 'tangent', 'tg_HV'],
    20: ['C_C1,пФ', 'other', 'C1', 'HV', 'C', 'c_deviation', 'C_HV'],
    21: ['DeltaTg_C1,%', 'percentage', 'C1', 'HV', '∆tg', 'tangent_delta', '∆tg_HV'],
    22: ['DeltaC_C1,%', 'percentage', 'C1', 'HV', '∆C', 'c_delta', '∆C_HV'],
    23: ['U_A2,кВ', 'voltage', 'A2', 'MV', 'U', 'voltage_difference', 'U_MV'],
    24: ['Ia_A2,мА', 'power', 'A2', 'MV', 'Ia', 'power_active', 'Ia_MV'],
    25: ['Ir_A2,мА', 'power', 'A2', 'MV', 'Ir', 'power_reactive', 'Ir_MV'],
    26: ['Tg_A2,%', 'percentage', 'A2', 'MV', 'tg', 'tangent', 'tg_MV'],
    27: ['C_A2,пФ', 'other', 'A2', 'MV', 'C', 'c_deviation', 'C_MV'],
    28: ['DeltaTg_A2,%', 'percentage', 'A2', 'MV', '∆tg', 'tangent_delta', '∆tg_MV'],
    29: ['DeltaC_A2,%', 'percentage', 'A2', 'MV', '∆C', 'c_delta', '∆C_MV'],
    30: ['U_B2,кВ', 'voltage', 'B2', 'MV', 'U', 'voltage_difference', 'U_MV'],
    31: ['Ia_B2,мА', 'power', 'B2', 'MV', 'Ia', 'power_active', 'Ia_MV'],
    32: ['Ir_B2,мА', 'power', 'B2', 'MV', 'Ir', 'power_reactive', 'Ir_MV'],
    33: ['Tg_B2,%', 'percentage', 'B2', 'MV', 'tg', 'tangent', 'tg_MV'],
    34: ['C_B2,пФ', 'other', 'B2', 'MV', 'C', 'c_deviation', 'C_MV'],
    35: ['DeltaTg_B2,%', 'percentage', 'B2', 'MV', '∆tg', 'tangent_delta', '∆tg_MV'],
    36: ['DeltaC_B2,%', 'percentage', 'B2', 'MV', '∆C', 'c_delta', '∆C_MV'],
    37: ['U_C2,кВ', 'voltage', 'C2', 'MV', 'U', 'voltage_difference', 'U_MV'],
    38: ['Ia_C2,мА', 'power', 'C2', 'MV', 'Ia', 'power_active', 'Ia_MV'],
    39: ['Ir_C2,мА', 'power', 'C2', 'MV', 'Ir', 'power_reactive', 'Ir_MV'],
    40: ['Tg_C2,%', 'percentage', 'C2', 'MV', 'tg', 'tangent', 'tg_MV'],
    41: ['C_C2,пФ', 'other', 'C2', 'MV', 'C', 'c_deviation', 'C_MV'],
    42: ['DeltaTg_C2,%', 'percentage', 'C2', 'MV', '∆tg', 'tangent_delta', '∆tg_MV'],
    43: ['DeltaC_C2,%', 'percentage', 'C2', 'MV', '∆C', 'c_delta', '∆C_MV'],
    44: ['Tair,°С', 'temperature', 'overall', 'no_voltage', 'tair', 'temperature_of_air', 'tair_no_voltage'],
    45: ['Tdevice,°С', 'temperature', 'overall', 'no_voltage', 'tdev', 'temperature_of_device', 'tdev_no_voltage'],
    46: ['Tcpu,°С', 'temperature', 'overall', 'no_voltage', 'tcpu', 'temperature_of_cpu', 'tcpu_no_voltage'],
    47: ['Freq,Гц', 'frequency', 'overall', 'no_voltage', 'freq', 'frequency', 'freq_no_voltage'],
    48: ['Unnamed: 48', 'other', 'overall', 'no_voltage', 'no_name', 'no_name', 'no_name_no_voltage']
</details>

### &nbsp;&nbsp; Analyzers and processors ([analyzer.py](analyzer.py))

*to be updated...*
