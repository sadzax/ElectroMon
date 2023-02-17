# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Description

ElectroMon is the app that monitors high-voltage parameters. 
It uses data uploaded from devices that make minute-by-minute measurements 
in power plants, transformers and other electrical appliances.

# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Implementation
## Stack
Backend is written in 
**Python**,
graphs and plots are provided by **Jupyter Notebook** 

## Requirements amd peculiarities
Requires some Python additional classic libs, all can be downloaded via `pip install` 

Check [requirements txt file](requirements.txt)

The actual devices are applied with usage of cyrillic characters.
Encoding and translational features should be considered.

## App Structure
ElectroMon bases on actual devices-measurers, described in file 
[devices](devices.py)

&nbsp;&nbsp; There is a list of them:
- ``nkvv`` - Устройство непрерывного контроля и защиты высоковольтных вводов
- ``kiv`` - Устройство контроля изоляции вводов
- ``monitoring`` - Мониторинг устройств непрерывного контроля и защиты высоковольтных вводов

[devices](devices.py) contains of 
