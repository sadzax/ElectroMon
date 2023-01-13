import os

import pandas as pd

import devices
import sadzax

# mask = [original, measurement, code_of_sensor, voltage_param,
#         short_search_name, full_search_name, concat_of_short_search_name_and_voltage_param]


#  Need to organize "file=devices.nkvv.work_file" etc... ->  to func.
def columns_list_maker(device_type='nkvv',
                       file=devices.nkvv.work_file,
                       sep=devices.nkvv.work_file_sep,
                       encoding=devices.nkvv.work_file_default_encoding,
                       data: pd.core = pd.read_excel(devices.kiv.work_file)):
    """
    Need to take it to the class of Devices
    """
    # attr = devices.Device.return_attributes(device_type)  # Why doesn't it work?
    if device_type == 'nkvv':
        # return list(pd.read_csv(attr[1], sep=attr[2], encoding=attr[3]))
        return list(pd.read_csv(file, sep=sep, encoding=encoding))
    elif device_type == 'kiv':
        if data.columns[0] == ' № ':
            return list(data.columns)
        else:
            for i in range(data.shape[0]):
                if data.iloc[i, 0] != ' № ':
                    pass
                else:
                    return list(data.iloc[i])
                    # noinspection PyUnreachableCode
                    break


#  Analyze all columns
def columns_analyzer(device_type='nkvv',
                     list_for_columns=None):
    """
    Need to take it to the class of Devices
    """
    if list_for_columns is None:
        list_for_columns = columns_list_maker(device_type=device_type)
    source_dict = {v: [k] for v, k in enumerate(list_for_columns)}
    result_dict = source_dict.copy()
    if device_type == "nkvv":
        for i in range(len(result_dict)):
            tail = sadzax.Trimmer.right(result_dict[i][0], 2)
            head = sadzax.Trimmer.left(result_dict[i][0], 4)
            for key in devices.nkvv.data_types:
                if key == tail:
                    result_dict[i].append(devices.nkvv.data_types[tail])
                elif key == head:
                    result_dict[i].append(devices.nkvv.data_types[head])
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
            for a_key in devices.nkvv.data_search_name:
                if sadzax.Trimmer.left(result_dict[i][0], len(a_key)) == a_key:
                    result_dict[i].append(devices.nkvv.data_search_name[a_key][0])
                    result_dict[i].append(devices.nkvv.data_search_name[a_key][1])
            if len(result_dict[i]) < 5:
                result_dict[i].append('no_name')
                result_dict[i].append('no_name')
            result_dict[i].append(result_dict[i][4] + '_' + result_dict[i][3])
    elif device_type == 'kiv':
        for i in range(len(result_dict)):
            tail = sadzax.Trimmer.right(result_dict[i][0], 2)
            head = sadzax.Trimmer.left(result_dict[i][0], 4)
            for key in devices.kiv.data_types:
                if key == tail:
                    result_dict[i].append(devices.kiv.data_types[key])
                elif key == head:
                    result_dict[i].append(devices.kiv.data_types[key])
                elif 'ф.' in str(result_dict[i][0]):  # Works with kiv.xlsx for a phase-parameters
                    if str(result_dict[i][0]).startswith(key):
                        result_dict[i].append(devices.kiv.data_types[key])
            if len(result_dict[i]) < 2:
                result_dict[i].append("other")
            if result_dict[i][0].find("ф.") == -1:
                result_dict[i].append('overall')
            else:
                codename = sadzax.Trimmer.right((sadzax.Trimmer.left(source_dict[i][0],
                                                                    source_dict[i][0].find("ф.") + 3)), 1) + '0'
                source_dict[i].append(codename)
            if 'ф.' in str(result_dict[i][0]):  # Works with kiv.xlsx for a phase-parameters
                result_dict[i].append("MV")
            else:
                result_dict[i].append('no_voltage')
            for a_key in devices.kiv.data_search_name:
                if sadzax.Trimmer.left(source_dict[i][0], len(a_key)) == a_key and 'ф.' in str(result_dict[i][0]):
                    source_dict[i].append(devices.kiv.data_search_name[a_key][0])
                    source_dict[i].append(devices.kiv.data_search_name[a_key][1])
            if len(source_dict[i]) < 5:
                source_dict[i].append('no_name')
                source_dict[i].append('no_name')
            source_dict[i].append(source_dict[i][4] + '_' + source_dict[i][3])
    return result_dict

