import pandas as pd
import devices
import sadzax

paste_values_rus = [
    "Дата создания записи",
    "Дата сохранения в БД",
    "U_A1,кВ",
    "Ia_A1,мА",
    "Ir_A1,мА",
    "Tg_A1,%",
    "C_A1,От",
    "DeltaTg_A1,%",
    "DeltaC_A1,%",
    "U_B1,кВ",
    "Ia_B1,мА",
    "Ir_B1,мА",
    "Tg_B1,%",
    "C_B1,От",
    "DeltaTg_B1,%",
    "DeltaC_B1,%",
    "U_C1,кВ",
    "Ia_C1,мА",
    "Ir_C1,мА",
    "Tg_C1,%",
    "C_C1,От",
    "DeltaTg_C1,%",
    "DeltaC_C1,%",
    "U_A2,кВ",
    "Ia_A2,мА",
    "Ir_A2,мА",
    "Tg_A2,%",
    "C_A2,От",
    "DeltaTg_A2,%",
    "DeltaC_A2,%",
    "U_B2,кВ",
    "Ia_B2,мА",
    "Ir_B2,мА",
    "Tg_B2,%",
    "C_B2,От",
    "DeltaTg_B2,%",
    "DeltaC_B2,%",
    "U_C2,кВ",
    "Ia_C2,мА",
    "Ir_C2,мА",
    "Tg_C2,%",
    "C_C2,От",
    "DeltaTg_C2,%",
    "DeltaC_C2,%",
    "Tair,°С",
    "Tdevice,°С",
    "Tcpu,°С",
    "Freq,Гц",
    ""
    ]
paste_values_utf8 = [
    '\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f \u0437\u0430\u043f\u0438\u0441\u0438',
    '\u0414\u0430\u0442\u0430 \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u0438\u044f \u0432 \u0411\u0414',
    'U_A1,\u043a\u0412',
    'Ia_A1,\u043c\u0410',
    'Ir_A1,\u043c\u0410',
    'Tg_A1,%',
    'C_A1,\u043f\u0424',
    'DeltaTg_A1,%',
    'DeltaC_A1,%',
    'U_B1,\u043a\u0412',
    'Ia_B1,\u043c\u0410',
    'Ir_B1,\u043c\u0410',
    'Tg_B1,%',
    'C_B1,\u043f\u0424',
    'DeltaTg_B1,%',
    'DeltaC_B1,%',
    'U_C1,\u043a\u0412',
    'Ia_C1,\u043c\u0410',
    'Ir_C1,\u043c\u0410',
    'Tg_C1,%',
    'C_C1,\u043f\u0424',
    'DeltaTg_C1,%',
    'DeltaC_C1,%',
    'U_A2,\u043a\u0412',
    'Ia_A2,\u043c\u0410',
    'Ir_A2,\u043c\u0410',
    'Tg_A2,%',
    'C_A2,\u043f\u0424',
    'DeltaTg_A2,%',
    'DeltaC_A2,%',
    'U_B2,\u043a\u0412',
    'Ia_B2,\u043c\u0410',
    'Ir_B2,\u043c\u0410',
    'Tg_B2,%',
    'C_B2,\u043f\u0424',
    'DeltaTg_B2,%',
    'DeltaC_B2,%',
    'U_C2,\u043a\u0412',
    'Ia_C2,\u043c\u0410',
    'Ir_C2,\u043c\u0410',
    'Tg_C2,%',
    'C_C2,\u043f\u0424',
    'DeltaTg_C2,%',
    'DeltaC_C2,%',
    'Tair,�\u0421',
    'Tdevice,�\u0421',
    'Tcpu,�\u0421',
    'Freq,\u0413\u0446',
    'Unnamed: 48'
    ]
paste_values_rus_dict = {
 0: ['Дата создания записи', 'datetime', 'overall', 'no_voltage', 'time', 'time_of_measure', 'time_no_voltage'],
 1: ['Дата сохранения в БД', 'datetime', 'overall', 'no_voltage', 'save', 'time_of_saving', 'save_no_voltage'],
 2: ['U_A1,кВ', 'voltage', 'A1', 'HV', 'U', 'voltage_difference', 'U_HV'],
 3: ['Ia_A1,мА', 'power', 'A1', 'HV', 'Ia', 'power_active', 'Ia_HV'],
 4: ['Ir_A1,мА', 'power', 'A1', 'HV', 'Ir', 'power_reactive', 'Ir_HV'],
 5: ['Tg_A1,%', 'percentage', 'A1', 'HV', 'tg', 'tangent', 'tg_HV'],
 6: ['C_A1,пФ', 'other', 'A1', 'HV', 'C', 'c_deviation', 'C_HV'],
 7: ['DeltaTg_A1,%', 'percentage', 'A1', 'HV', '∆tgδ', 'tangent_delta', '∆tgδ_HV'],
 8: ['DeltaC_A1,%', 'percentage', 'A1', 'HV', '∆C', 'c_delta', '∆C_HV'],
 9: ['U_B1,кВ', 'voltage', 'B1', 'HV', 'U', 'voltage_difference', 'U_HV'],
 10: ['Ia_B1,мА', 'power', 'B1', 'HV', 'Ia', 'power_active', 'Ia_HV'],
 11: ['Ir_B1,мА', 'power', 'B1', 'HV', 'Ir', 'power_reactive', 'Ir_HV'],
 12: ['Tg_B1,%', 'percentage', 'B1', 'HV', 'tg', 'tangent', 'tg_HV'],
 13: ['C_B1,пФ', 'other', 'B1', 'HV', 'C', 'c_deviation', 'C_HV'],
 14: ['DeltaTg_B1,%', 'percentage', 'B1', 'HV', '∆tgδ', 'tangent_delta', '∆tgδ_HV'],
 15: ['DeltaC_B1,%', 'percentage', 'B1', 'HV', '∆C', 'c_delta', '∆C_HV'],
 16: ['U_C1,кВ', 'voltage', 'C1', 'HV', 'U', 'voltage_difference', 'U_HV'],
 17: ['Ia_C1,мА', 'power', 'C1', 'HV', 'Ia', 'power_active', 'Ia_HV'],
 18: ['Ir_C1,мА', 'power', 'C1', 'HV', 'Ir', 'power_reactive', 'Ir_HV'],
 19: ['Tg_C1,%', 'percentage', 'C1', 'HV', 'tg', 'tangent', 'tg_HV'],
 20: ['C_C1,пФ', 'other', 'C1', 'HV', 'C', 'c_deviation', 'C_HV'],
 21: ['DeltaTg_C1,%', 'percentage', 'C1', 'HV', '∆tgδ', 'tangent_delta', '∆tgδ_HV'],
 22: ['DeltaC_C1,%', 'percentage', 'C1', 'HV', '∆C', 'c_delta', '∆C_HV'],
 23: ['U_A2,кВ', 'voltage', 'A2', 'MV', 'U', 'voltage_difference', 'U_MV'],
 24: ['Ia_A2,мА', 'power', 'A2', 'MV', 'Ia', 'power_active', 'Ia_MV'],
 25: ['Ir_A2,мА', 'power', 'A2', 'MV', 'Ir', 'power_reactive', 'Ir_MV'],
 26: ['Tg_A2,%', 'percentage', 'A2', 'MV', 'tg', 'tangent', 'tg_MV'],
 27: ['C_A2,пФ', 'other', 'A2', 'MV', 'C', 'c_deviation', 'C_MV'],
 28: ['DeltaTg_A2,%', 'percentage', 'A2', 'MV', '∆tgδ', 'tangent_delta', '∆tgδ_MV'],
 29: ['DeltaC_A2,%', 'percentage', 'A2', 'MV', '∆C', 'c_delta', '∆C_MV'],
 30: ['U_B2,кВ', 'voltage', 'B2', 'MV', 'U', 'voltage_difference', 'U_MV'],
 31: ['Ia_B2,мА', 'power', 'B2', 'MV', 'Ia', 'power_active', 'Ia_MV'],
 32: ['Ir_B2,мА', 'power', 'B2', 'MV', 'Ir', 'power_reactive', 'Ir_MV'],
 33: ['Tg_B2,%', 'percentage', 'B2', 'MV', 'tg', 'tangent', 'tg_MV'],
 34: ['C_B2,пФ', 'other', 'B2', 'MV', 'C', 'c_deviation', 'C_MV'],
 35: ['DeltaTg_B2,%', 'percentage', 'B2', 'MV', '∆tgδ', 'tangent_delta', '∆tgδ_MV'],
 36: ['DeltaC_B2,%', 'percentage', 'B2', 'MV', '∆C', 'c_delta', '∆C_MV'],
 37: ['U_C2,кВ', 'voltage', 'C2', 'MV', 'U', 'voltage_difference', 'U_MV'],
 38: ['Ia_C2,мА', 'power', 'C2', 'MV', 'Ia', 'power_active', 'Ia_MV'],
 39: ['Ir_C2,мА', 'power', 'C2', 'MV', 'Ir', 'power_reactive', 'Ir_MV'],
 40: ['Tg_C2,%', 'percentage', 'C2', 'MV', 'tg', 'tangent', 'tg_MV'],
 41: ['C_C2,пФ', 'other', 'C2', 'MV', 'C', 'c_deviation', 'C_MV'],
 42: ['DeltaTg_C2,%', 'percentage', 'C2', 'MV', '∆tgδ', 'tangent_delta', '∆tgδ_MV'],
 43: ['DeltaC_C2,%', 'percentage', 'C2', 'MV', '∆C', 'c_delta', '∆C_MV'],
 44: ['Tair,°С', 'temperature', 'overall', 'no_voltage', 'tair', 'temperature_of_air', 'tair_no_voltage'],
 45: ['Tdevice,°С', 'temperature', 'overall', 'no_voltage', 'tdev', 'temperature_of_device', 'tdev_no_voltage'],
 46: ['Tcpu,°С', 'temperature', 'overall', 'no_voltage', 'tcpu', 'temperature_of_cpu', 'tcpu_no_voltage'],
 47: ['Freq,Гц', 'frequency', 'overall', 'no_voltage', 'freq', 'frequency', 'freq_no_voltage'],
 48: ['Unnamed: 48', 'other', 'overall', 'no_voltage', 'no_name', 'no_name', 'no_name_no_voltage']
}

# mask = [original, measurement, code_of_sensor, voltage_param,
#         short_search_name, full_search_name, concat_of_short_search_name_and_voltage_param]


indexer = [x for x in range(len(paste_values_rus))]


def columns_maker(file=devices.nkvv.work_file,
                  sep=devices.nkvv.work_file_sep,
                  encoding=devices.nkvv.work_file_default_encoding):
    return list(pd.read_csv(file, sep=sep, encoding=encoding))


def dict_maker(list_for_columns=None,
               file=devices.nkvv.work_file,
               sep=devices.nkvv.work_file_sep,
               encoding=devices.nkvv.work_file_default_encoding):
    if list_for_columns is None:
        list_for_columns = columns_maker(file=file, sep=sep, encoding=encoding)
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


#  Analyze all columns
def columns_analyzer(source_dict=None,
                     file=devices.nkvv.work_file,
                     sep=devices.nkvv.work_file_sep,
                     encoding=devices.nkvv.work_file_default_encoding,
                     range_limit=None):
    if source_dict is None:
        source_dict = dict_maker(None, file=file, sep=sep, encoding=encoding)
    if range_limit is None:
        range_limit = len(columns_maker(file=file, sep=sep, encoding=encoding))
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
