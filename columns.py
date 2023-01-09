import pandas as pd
import devices
import sadzax
import os

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


types_of_data = {
        'кВ': 'voltage',
        'мА': 'power',
        ',%': 'percentage',
        'От': 'deviation',
        '°С': 'temperature',
        'Гц': 'frequency',
        'Дата': 'datetime',
}

#  rebuild with classes!
kiv_types_of_data = {
        '°С': 'temperature',
        'Дата': 'datetime',
        'U': 'voltage',
        'C1': 'power',
        'tg': 'percentage',
        '∆C': 'deviation'
}


def kiv_xlsx_columns_analyzer(source_dict=None,
                              range_limit=None):
    if source_dict is None:
        source_dict = dict_maker(list(pd.read_excel(devices.kiv.work_file_folder + kiv_xlsx_files_form()[0]).iloc[3]))
    if range_limit is None:
        range_limit = len(source_dict)
    for i in range(range_limit):
        tail = sadzax.Trimmer.right(source_dict[i][0], 2)
        head = sadzax.Trimmer.left(source_dict[i][0], 4)
        for key in kiv_types_of_data:
            if key == tail:
                source_dict[i].append(kiv_types_of_data[key])
            elif key == head:
                source_dict[i].append(kiv_types_of_data[key])
            elif 'ф.' in source_dict[i]:
                source_dict[i].append(kiv_types_of_data[key])
    return source_dict


#  Analyze all columns
def columns_analyzer(source_dict=None,
                     file=devices.nkvv.work_file,
                     sep=devices.nkvv.work_file_sep,
                     encoding=devices.nkvv.work_file_default_encoding,
                     range_limit=None):
    if source_dict is None:
        source_dict = dict_maker(None, file=file, sep=sep, encoding=encoding)
    if range_limit is None:
        range_limit = len(columns_list_maker(file=file, sep=sep, encoding=encoding))
    for i in range(range_limit):
        tail = sadzax.Trimmer.right(source_dict[i][0], 2)
        head = sadzax.Trimmer.left(source_dict[i][0], 4)
        for key in types_of_data:
            if key == tail:
                source_dict[i].append(types_of_data[tail])
            elif key == head:
                source_dict[i].append(types_of_data[head])
        if len(source_dict[i]) < 2:
            source_dict[i].append('other')
    for i in range(range_limit):
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
    for i in range(range_limit):
        if sadzax.Trimmer.left(source_dict[i][0], 7) == "DeltaTg":
            source_dict[i].append('∆tgδ')
            source_dict[i].append('tangent_delta')
        elif sadzax.Trimmer.left(source_dict[i][0], 7) == "DeltaC_":
            source_dict[i].append('∆C')
            source_dict[i].append('c_delta')
        elif sadzax.Trimmer.left(source_dict[i][0], 3) == "Tg_":
            source_dict[i].append('tg')
            source_dict[i].append('tangent')
        elif sadzax.Trimmer.left(source_dict[i][0], 2) == "C_":
            source_dict[i].append('C')
            source_dict[i].append('c_deviation')
        elif sadzax.Trimmer.left(source_dict[i][0], 20) == "Дата создания записи":
            source_dict[i].append('time')
            source_dict[i].append('time_of_measure')
        elif sadzax.Trimmer.left(source_dict[i][0], 20) == "Дата сохранения в БД":
            source_dict[i].append('save')
            source_dict[i].append('time_of_saving')
        elif sadzax.Trimmer.left(source_dict[i][0], 2) == "U_":
            source_dict[i].append('U')
            source_dict[i].append('voltage_difference')
        elif sadzax.Trimmer.left(source_dict[i][0], 3) == "Ia_":
            source_dict[i].append('Ia')
            source_dict[i].append('power_active')
        elif sadzax.Trimmer.left(source_dict[i][0], 3) == "Ir_":
            source_dict[i].append('Ir')
            source_dict[i].append('power_reactive')
        elif sadzax.Trimmer.left(source_dict[i][0], 4) == "Freq":
            source_dict[i].append('freq')
            source_dict[i].append('frequency')
        elif sadzax.Trimmer.left(source_dict[i][0], 4) == "Tair":
            source_dict[i].append('tair')
            source_dict[i].append('temperature_of_air')
        elif sadzax.Trimmer.left(source_dict[i][0], 4) == "Tdev":
            source_dict[i].append('tdev')
            source_dict[i].append('temperature_of_device')
        elif sadzax.Trimmer.left(source_dict[i][0], 4) == "Tcpu":
            source_dict[i].append('tcpu')
            source_dict[i].append('temperature_of_cpu')
        else:
            source_dict[i].append('no_name')
            source_dict[i].append('no_name')
    for i in range(range_limit):
        source_dict[i].append(source_dict[i][4] + '_' + source_dict[i][3])
    return source_dict



