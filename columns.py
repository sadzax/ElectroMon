import os

import pandas as pd

import devices
import sadzax

# mask = [original, measurement, code_of_sensor, voltage_param,
#         short_search_name, full_search_name, concat_of_short_search_name_and_voltage_param]


indexer = [x for x in range(len(devices.nkvv.paste_values_rus))]


#  Need to organize "file=devices.nkvv.work_file" etc..... ->  to func.
def columns_list_maker(device_type='nkvv',
                       file=devices.nkvv.work_file,
                       sep=devices.nkvv.work_file_sep,
                       encoding=devices.nkvv.work_file_default_encoding,
                       data: pd.core = None):
    """
    Need to take it to the class of Devices
    """
    if device_type == 'nkvv':
        return list(pd.read_csv(file, sep=sep, encoding=encoding))
    elif device_type == 'kiv':
        return list(data.iloc[3])


def dict_maker(list_for_columns=None,
               file=devices.nkvv.work_file,
               sep=devices.nkvv.work_file_sep,
               encoding=devices.nkvv.work_file_default_encoding):
    if list_for_columns is None:
        list_for_columns = columns_list_maker(file=file, sep=sep, encoding=encoding)
    return {v: [k] for v, k in enumerate(list_for_columns)}


#  Analyze all columns
def columns_analyzer(source_dict=None,
                     file=devices.nkvv.work_file,
                     sep=devices.nkvv.work_file_sep,
                     encoding=devices.nkvv.work_file_default_encoding):
    """
    Need to take it to the class of Devices
    """
    if source_dict is None:
        source_dict = dict_maker(None, file=file, sep=sep, encoding=encoding)
    for i in range(len(source_dict)):
        tail = sadzax.Trimmer.right(source_dict[i][0], 2)
        head = sadzax.Trimmer.left(source_dict[i][0], 4)
        for key in devices.nkvv.data_types:
            if key == tail:
                source_dict[i].append(devices.nkvv.data_types[tail])
            elif key == head:
                source_dict[i].append(devices.nkvv.data_types[head])
        if len(source_dict[i]) < 2:
            source_dict[i].append('other')
    for i in range(len(source_dict)):
        if source_dict[i][0].find("_") == -1:
            source_dict[i].append('overall')
        else:
            codename = sadzax.Trimmer.right((sadzax.Trimmer.left(source_dict[i][0],
                                                                 source_dict[i][0].find("_") + 3)), 2)
            source_dict[i].append(codename)
        if sadzax.Trimmer.right(source_dict[i][2], 1) == '1':
            source_dict[i].append('HV')
        elif sadzax.Trimmer.right(source_dict[i][2], 1) == '2':
            source_dict[i].append('MV')
        else:
            source_dict[i].append('no_voltage')
    for i in range(len(source_dict)):
        for a_key in devices.nkvv.data_search_name:
            if sadzax.Trimmer.left(source_dict[i][0], len(a_key)) == a_key:
                source_dict[i].append(devices.nkvv.data_search_name[a_key][0])
                source_dict[i].append(devices.nkvv.data_search_name[a_key][1])
        if len(source_dict[i]) < 5:
            source_dict[i].append('no_name')
            source_dict[i].append('no_name')
    for i in range(len(source_dict)):
        source_dict[i].append(source_dict[i][4] + '_' + source_dict[i][3])
    return source_dict
