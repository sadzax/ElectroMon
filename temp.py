import warnings
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import os
import columns
import devices
import plots
import prints
import sadzax
import analyzer
warnings.simplefilter(action='ignore', category=FutureWarning)
prints.clearing_script()

device_type = 'mon'
data = analyzer.stack_data(device_type=device_type)
cols_list = columns.columns_list_maker(device_type=device_type, data=data)

# columns_analyzer

list_for_columns = cols_list
source_dict = {k: [v] for k, v in enumerate(list_for_columns)}
result_dict = source_dict.copy()

for i in range(len(result_dict)):
    tail = sadzax.Trimmer.right(result_dict[3][0], 2)
    head = sadzax.Trimmer.left(result_dict[3][0], 4)
    for key in devices.mon.data_types:
        if key == tail:
            result_dict[i].append(devices.mon.data_types[tail])
        elif key == head:
            result_dict[i].append(devices.mon.data_types[head])
    if len(result_dict[i]) < 2:
        result_dict[i].append('other')
    if result_dict[i][0].find("_") == -1:
        result_dict[i].append('overall')
    else:
        codename = sadzax.Trimmer.right((sadzax.Trimmer.left(result_dict[i][0],
                                                             result_dict[i][0].find("_") + 3)), 2)
        result_dict[i].append(codename)
    if sadzax.Trimmer.right(result_dict[i][2], 1) == '1':
        result_dict[i].append('HV')
    elif sadzax.Trimmer.right(result_dict[i][2], 1) == '2':
        result_dict[i].append('MV')
    else:
        result_dict[i].append('no_voltage')
    for a_key in devices.mon.data_search_name:
        if sadzax.Trimmer.left(result_dict[i][0], len(a_key)) == a_key:
            result_dict[i].append(devices.mon.data_search_name[a_key][0])
            result_dict[i].append(devices.mon.data_search_name[a_key][1])