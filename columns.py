import os

import pandas as pd

import analyzer
import devices
import sadzax

# mask = [original, measurement, code_of_sensor, voltage_param,
#         short_search_name, full_search_name, concat_of_short_search_name_and_voltage_param]


#  Need to organize "file=devices.nkvv.work_file" etc... ->  to func.
def columns_list_maker(device_type: str = 'nkvv',
                       data: pd.core = None,
                       file: str = None,
                       sep: str = None,
                       encoding: str = None):
    """
    Need to take it to the class of Devices
    """
    if file is None:
        file, sep, encoding, parse_dates = devices.links(device_type)[1:5]
    if device_type == 'nkvv':
        return list(pd.read_csv(file, sep=sep, encoding=encoding))
    elif device_type == 'kiv':
        if data is None:
            data = analyzer.get_data(device_type=device_type)
        if data.columns[0] == ' № ':
            return list(data.columns)
        else:
            for i in range(data.shape[0]):
                if data.iloc[i, 0] != ' № ':
                    pass
                else:
                    return list(data.iloc[i+1])
                    # noinspection PyUnreachableCode
                    break
    elif device_type == 'mon':
        if data is None:
            data = analyzer.get_data(device_type=device_type)
        return list(data.columns)


#  Analyze all columns
def columns_analyzer(device_type: str ='nkvv',
                     list_for_columns: list = None):
    """
    Need to take it to the class of Devices
    """
    if list_for_columns is None:
        list_for_columns = columns_list_maker(device_type=device_type)
    source_dict = {k: [v] for k, v in enumerate(list_for_columns)}
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
            elif 'unb' in str(result_dict[i][0]):  # Works with kiv.xlsx for a phase-parameters
                result_dict[i].append("unb")
            else:
                result_dict[i].append('no_voltage')
            for a_key in devices.kiv.data_search_name:
                # if sadzax.Trimmer.left(source_dict[i][0], len(a_key)) == a_key and 'ф.' or 'Дата' in str(result_dict[i][0]):  #
                if sadzax.Trimmer.left(source_dict[i][0], len(a_key)) == a_key:
                    try:
                        source_dict[i][4] = devices.kiv.data_search_name[a_key][0]
                        source_dict[i][5] = devices.kiv.data_search_name[a_key][1]
                    except:
                        source_dict[i].append('no_name')
                        source_dict[i].append('no_name')
                        source_dict[i][4] = devices.kiv.data_search_name[a_key][0]
                        source_dict[i][5] = devices.kiv.data_search_name[a_key][1]
            if len(source_dict[i]) < 5:
                source_dict[i].append('no_name')
                source_dict[i].append('no_name')
            source_dict[i].append(source_dict[i][4] + '_' + source_dict[i][3])
    return result_dict


def time_column(device_type='nkvv',
                data: pd.core = None):
    device_type = device_type.lower()
    if data is None:
        data = analyzer.get_data(device_type=device_type)
    parse_dates = devices.links(device_type)[4]
    the_time_column = list(data.columns)[0]
    for an_element_of_parse_dates in parse_dates:
        for a_column in list(data.columns):
            if a_column.startswith(an_element_of_parse_dates):
                the_time_column = a_column
        break
    return the_time_column
