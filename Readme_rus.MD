# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Contents
- [Описание](#-описание)


- [Реализация](#-реализация)


- [Требования](#-требования)


- [Установка](#-установка)


- [Структура](#-структура)


- - [Инициализатор устройств](#-инициализатор-устройств-devicespy)
- - - [Замеры](#замеры)
- - - [Свойства](#свойства)
- - - [Источники](#источники)
- - - [Ссылки](#ссылки)
- - - [Быстрое сохранение и загрузка](#быстрое-сохранение-и-загрузка)


- - [Обработка столбцов](#-обработка-столбцов-columnspy)
- - - [Анализатор столбцов](#анализатор-столбцов)
- - - [Defining the time column](#defining-the-time-column)


- - [Analyzers and processors](#-analyzers-and-processors-analyzerpy)
- - - [Data import](#data-import)
- - - [Replace data](#replace-data)
- - - [Counter](#counter)
- - - [Timestamp analyzing](#timestamp-analyzing)
- - - [Periods](#periods)
- - - [Nans](#nans)
- - - [Filtering](#filtering)
- - - [Averages](#averages)
- - - [Distributions](#distributions)
- - - [Correlations](#correlations)
- - - [Warnings](#warnings)

- - [Other modules](#-other-modules)

- [Runner](#-runner)

&nbsp;

# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Описание

**ElectroMon**  - это приложение для мониторинга параметров высокого напряжения.
Оно использует данные, загруженные с устройств, которые производят поминутные замеры на электростанциях, трансформаторах и других электрических устройствах.

&nbsp;

# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Реализация
Backend написан на языке 
**Python** 
с использованием библиотек **pandas** и **numpy**.
Графики, диаграммы и выводы в печатный вид создаются с помощью 
**Jupyter Notebook** 
с использованием библиотек **matplotlib** и **reportlab**.

&nbsp;

# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Требования
Требуются дополнительные "классические" библиотеки для Python, все из которых можно загрузить с помощью `pip install`:

Требования по библиотекам перечислены в 
[requirements.txt](requirements.txt) 
в корневой директории.

Фактические устройства используются с использованием кириллических символов. 
Необходимо учитывать особенности кодирования и перевода в программном коде.

&nbsp;

# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Установка



&nbsp;

# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Структура
## &nbsp;&nbsp; Инициализатор устройств ([devices.py](devices.py))

### Замеры
ElectroMon получает данные от фактических физических устройств, снимающих показания.

&nbsp;&nbsp; Список доступных устройств и их короткие коды, используемые в программе:
- ``nkvv`` - **Устройство непрерывного контроля и защиты высоковольтных вводов**
- ``kiv`` - **Устройство контроля изоляции вводов**
- ``monitoring`` - **Мониторинг устройств непрерывного контроля и защиты высоковольтных вводов**

### Свойства 

Файл
[Devices](devices.py) 
хранит и возвращает атрибуты для последующей обработки.
Модуль содержит методы установки свойств и статусов устройства, таких как:

- имя устройства
- папка и файлы по умолчанию для загрузки данных
- тип источника данных, используемые разделители
- столбцы, используемые для установки значений измерений и их карты декодирования
- прописанные типичные ошибки измерений устройств
- значения предупредительных и аварийных сигналов для определённых типов измерений
- и т.д.
<details><summary>Пример инициализатора</summary>

    self.name = 'nkvv'
    self.full_name = 'Устройство непрерывного контроля и защиты высоковольтных вводов'
    self.monitoring_params = {'input': 220000, 'output': 110000}
    self.log_types = {'measure': 'csv', 'event': 'csv'}
    self.file_folder = 'upload/' + name + '/'
    self.file_name_starts = {'measure': 'DB_i'}
    self.file_sep = ';'
    self.file_default_encoding = 'WINDOWS-1251'
    self.file_parse_dates = ['Дата создания записи', 'Дата сохранения в БД']
    self.default_dict_for_replacement_to_nan = {'power': [-300.0, 0.0],
                                                'tg': -10.0,
                                                '∆tg': -10.0,
                                                'c_delta': -10.0,
                                                'c_deviation': 0.0,
                                                'voltage_difference': 0.0}
</details>

### Источники

Исходные данные располагаются в папке `upload/` и должны соответствовать требованиям, описанным в файле 
[devices.py](devices.py) в классе `Device`, 
включая инициализирующие свойства, такие как `self.file_name_starts` или `self.file_name_ends` объектов-устройств. 
При добавлении нового типа файлов/шаблонов эти свойства следует обновлять.

<details><summary>Пример выгруженных с устройств файлов</summary>

    'upload/kiv/MeasJ a284 #572665920 30-12-2022.xlsx' 
    'upload/mon/22_06/21217004.I' 
    'upload/mon/22_07/21217004.I' 
    'upload/mon/22_08/21217004.I' 
    'upload/mon/22_09/21217004.I' 
    'upload/mon/22_10/21217004.I' 
    'upload/mon/22_11/21217004.I' 
    'upload/mon/22_12/21217004.I' 
    'upload/mon/23_01/21217004.I' 
    'upload/nkvv/DB_i.csv;  
</details>

### Ссылки

Функция `links()` содержит основные свойства устройств, возвращаемые в виде списка. 
Метод можно расширить новыми свойствами, но порядок списка не должен изменяться, так как его индексы используются в аналитических функциях.

<details><summary>Текущий список ссылок для получения данных по устройству через функцию</summary>

            self.name,  # 0
            self.file,  # 1
            self.file_sep,  # 2
            self.file_default_encoding,  # 3
            self.file_parse_dates,  # 4
            self.file_list,  # 5
            self.default_dict_for_replacement_to_nan,  # 6
            self.file_parse_dates_basis,  # 7
            self.default_dict_for_dtypes,  # 8
            self.full_name,  # 9
            self.warning_map  # 10
</details>

### Быстрое сохранение и загрузка

Сохраненный кэш данных для устройства может быть сохранен в формате `.pkl` в директории `save/` для дальнейшей быстрой загрузки.

Используйте класс `Pkl` и методы `save()` или `load()` в [devices](devices.py)

<details><summary>Пример быстрого сохранения и загрузки данных </summary>
Сохранение оперируемых данных устройства контроля и изоляции вводов:

    data = devices.Pkl.save(device_type='kiv', data=data)

Загрузка этих данных:

    data = devices.Pkl.load(device_type='kiv')
</details>

## &nbsp;&nbsp; Обработка столбцов ([columns.py](columns.py)) 

### Анализатор столбцов

Based on [devices](devices.py) attributes
`columns_analyzer()`
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
in order to increase efficiency of analytical functions.

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

### Defining the time column

`time_column()` returns full name of a timestamp-column in dats based on `device` property 
`self.file_parse_dates`. This property stores a list of columns which contain time-type data
and the main time column (with the fixed time of the measurement) must be first in this list.

## &nbsp;&nbsp; Analyzers and processors ([analyzer.py](analyzer.py))

### Data import
The import is based on work-files (described in [Sources](#Sources)).
In case of using a multiple files for creating an uninterrupted dataflow `stack_data()` function should be used.
Stacking data from different files also automatically sorted by ascending timestamps of the measurement.
Data import functions returns pandas DataFrame. It is recommended to set a `data` as a variable to store this result.

### Replace data
There are some measurements that actually mean "NaN" but 
due to the technical issues of the devices 
are actually written as values in upload-files.
`pass_the_nan()` 
replaces specified values in a DataFrame with NaN values.

<details><summary>Example of NaN-measures</summary>

    {
        'power': [-300.0, 0.0],
        'tg': [-10.0],
        '∆tg': [-10.0],
        'c_delta': [-10.0],
        'c_deviation': [0.0],
        'voltage_difference': [0.0]
    }
</details>

`set_dtypes` 
sets the data types for specified columns in a DataFrame.

The dictionaries are stored in [device](devices.py):
- the values to be replaced with NaN values 
is a dictionary
`self.default_dict_for_replacement_to_nan` 
property
- the data types for each column 
is a dictionary
`self.default_dict_for_dtypes` 
property

It's recommended to pass variable `data` and return it as a `data` variable as well for these functions 

### Counter

`total_counter()` is a simple function that takes a device type and a pandas DataFrame as input 
and returns the total number of logs in the DataFrame. 
If no DataFrame is provided, the function calls `get_data()` to obtain one.

`total_periods()` check for received data to return the start and the end of the measures. 
You can pass format of the data by `format=` argument. 

### Timestamp analyzing

`values_time_analyzer()` analyzes the time gaps between consecutive rows in a given time column of a 
Pandas DataFrame and returns a DataFrame with information about any gaps that exceed a specified duration 
or fall outside a certain range of durations.

`values_time_slicer()` slices the data based on time intervals. 
Returns a dictionary containing information about sliced data, every dictionary value contains 
separate pandas DataFrame. Data is separated by the big time gaps, f.e. if there are measures 
in quite different periods of time. DefauSlt time-gap parameter for slicing is 1439 minutes (a day).

### Periods
`time_period_choose()` is designed to enable a user to select a time period of interest within a given dataset.
It then calculates the start and end dates of the dataset, prints them, and prompts the user to enter a specific time period of interest.
The function sorts the dataset by the time of measurement and resets the indexes.

### Nans
`total_nan_counter()` analyzes the percentage of NaN values in each row of the input data and returns 
a pandas DataFrame that shows the time periods where the percentage of NaN values exceeds a specified threshold.
Default 
`false_data_percentage` 
set to 33.0 means that measurements in the particular moment is too uncertain if more than 1/3 of measures are errors
Map of the typical errors of the devices measurements can be found in 
[devices.py](devices.py) 
as a `self.default_dict_for_replacement_to_nan` property. They are slightly described in
[Attributes](#attributes)

If there are too many NaN values in each row in a database 
`total_nan_counter_ease()` 
can be used to stack continuous periods of NaN values in measure database.

### Filtering
`data_filter()` returns a new DataFrame that only contains the columns that match the filter list.
Filter a Pandas DataFrame by a list of column names but also can be given codes of measurers or shortnames
and practically anything from [columns.py](columns.py) / [Main columns analyzer](#main-columns-analyzer)

### Averages
`data_average_finder()` filters and calculates the average value of a specified list of columns in a given dataset.
It returns a dictionary with column names as keys and their corresponding average value as values.

### Distributions
`data_distribution_finder()` analyzes the distribution of values in the specified columns of the data.

### Correlations
`data_correlation()` calculates the correlation between columns of two filtered dataframes. 
Returns a dictionary with the correlation parameters as keys and the corresponding sequence of correlation values.
If you plot this data, f.e. 100% strict correlation would like "x=y" type of graph with a 45° angle.

### Warnings
`warning_finder()` is the basic function for analyzing warnings. 
It finds time intervals when certain parameters exceed specified warning or accident threshold values.
Default warning or accident threshold values set in 
[devices.py](devices.py) 
for each device in a `self.warning_map` property. They are slightly described in
[Attributes](#attributes)

The next step for analyzing of warnings would be using 
`warning_finder_merge()` 
that merges the dataframes in the input dictionary 
`log` 
and adds columns for warning parameters based on the given 
`warn_type` 
and threshold values. 
It returns the resulting merged dataframe. 

If there are too many warnings 
`warning_finder_ease()` 
can be used to stack continuous periods of warnings in database. 
It takes in a dictionary log and several optional arguments to filter and process the data in order to identify 
warning or accident events. 

## &nbsp;&nbsp; Other Modules

([prints.py](prints.py))

([plots.py](plots.py))

([frontend.py](frontend.py))

([sadzax.py](sadzax.py))

# &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Runner

([run.py](run.py))

([output.py](output.py))