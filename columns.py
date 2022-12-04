import devices
import pandas as pd
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
    0: ['Дата создания записи', 'datetime', 'no_codename', 'no_voltage_param', 'no_indicator'],
    1: ['Дата сохранения в БД', 'datetime', 'no_codename', 'no_voltage_param', 'no_indicator'],
    2: ['U_A1,кВ', 'voltage', 'A1', 'HV', 'no_indicator'],
    3: ['Ia_A1,мА', 'power', 'A1', 'HV', 'no_indicator'],
    4: ['Ir_A1,мА', 'power', 'A1', 'HV', 'no_indicator'],
    5: ['Tg_A1,%', 'percentage', 'A1', 'HV', 'tg'],
    6: ['C_A1,пФ', 'other', 'A1', 'HV', 'C_dev'],
    7: ['DeltaTg_A1,%', 'percentage', 'A1', 'HV', '∆tgδ'],
    8: ['DeltaC_A1,%', 'percentage', 'A1', 'HV', '∆C'],
    9: ['U_B1,кВ', 'voltage', 'B1', 'HV', 'no_indicator'],
    10: ['Ia_B1,мА', 'power', 'B1', 'HV', 'no_indicator'],
    11: ['Ir_B1,мА', 'power', 'B1', 'HV', 'no_indicator'],
    12: ['Tg_B1,%', 'percentage', 'B1', 'HV', 'tg'],
    13: ['C_B1,пФ', 'other', 'B1', 'HV', 'C_dev'],
    14: ['DeltaTg_B1,%', 'percentage', 'B1', 'HV', '∆tgδ'],
    15: ['DeltaC_B1,%', 'percentage', 'B1', 'HV', '∆C'],
    16: ['U_C1,кВ', 'voltage', 'C1', 'HV', 'no_indicator'],
    17: ['Ia_C1,мА', 'power', 'C1', 'HV', 'no_indicator'],
    18: ['Ir_C1,мА', 'power', 'C1', 'HV', 'no_indicator'],
    19: ['Tg_C1,%', 'percentage', 'C1', 'HV', 'tg'],
    20: ['C_C1,пФ', 'other', 'C1', 'HV', 'C_dev'],
    21: ['DeltaTg_C1,%', 'percentage', 'C1', 'HV', '∆tgδ'],
    22: ['DeltaC_C1,%', 'percentage', 'C1', 'HV', '∆C'],
    23: ['U_A2,кВ', 'voltage', 'A2', 'MV', 'no_indicator'],
    24: ['Ia_A2,мА', 'power', 'A2', 'MV', 'no_indicator'],
    25: ['Ir_A2,мА', 'power', 'A2', 'MV', 'no_indicator'],
    26: ['Tg_A2,%', 'percentage', 'A2', 'MV', 'tg'],
    27: ['C_A2,пФ', 'other', 'A2', 'MV', 'C_dev'],
    28: ['DeltaTg_A2,%', 'percentage', 'A2', 'MV', '∆tgδ'],
    29: ['DeltaC_A2,%', 'percentage', 'A2', 'MV', '∆C'],
    30: ['U_B2,кВ', 'voltage', 'B2', 'MV', 'no_indicator'],
    31: ['Ia_B2,мА', 'power', 'B2', 'MV', 'no_indicator'],
    32: ['Ir_B2,мА', 'power', 'B2', 'MV', 'no_indicator'],
    33: ['Tg_B2,%', 'percentage', 'B2', 'MV', 'tg'],
    34: ['C_B2,пФ', 'other', 'B2', 'MV', 'C_dev'],
    35: ['DeltaTg_B2,%', 'percentage', 'B2', 'MV', '∆tgδ'],
    36: ['DeltaC_B2,%', 'percentage', 'B2', 'MV', '∆C'],
    37: ['U_C2,кВ', 'voltage', 'C2', 'MV', 'no_indicator'],
    38: ['Ia_C2,мА', 'power', 'C2', 'MV', 'no_indicator'],
    39: ['Ir_C2,мА', 'power', 'C2', 'MV', 'no_indicator'],
    40: ['Tg_C2,%', 'percentage', 'C2', 'MV', 'tg'],
    41: ['C_C2,пФ', 'other', 'C2', 'MV', 'C_dev'],
    42: ['DeltaTg_C2,%', 'percentage', 'C2', 'MV', '∆tgδ'],
    43: ['DeltaC_C2,%', 'percentage', 'C2', 'MV', '∆C'],
    44: ['Tair,°С', 'temperature', 'no_codename', 'no_voltage_param', 'no_indicator'],
    45: ['Tdevice,°С', 'temperature', 'no_codename', 'no_voltage_param', 'no_indicator'],
    46: ['Tcpu,°С', 'temperature', 'no_codename', 'no_voltage_param', 'no_indicator'],
    47: ['Freq,Гц', 'frequency', 'no_codename', 'no_voltage_param', 'no_indicator'],
    48: ['Unnamed: 48', 'other', 'no_codename', 'no_voltage_param', 'no_indicator']
}


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
            source_dict[i].append('no_codename')
        else:
            codename = sadzax.Trimmer.right((sadzax.Trimmer.left(source_dict[i][0],
                                                                 source_dict[i][0].find("_") + 3)), 2)
            source_dict[i].append(codename)
        if sadzax.Trimmer.right(source_dict[i][2], 1) == '1':
            source_dict[i].append('HV')
        elif sadzax.Trimmer.right(source_dict[i][2], 1) == '2':
            source_dict[i].append('MV')
        else:
            source_dict[i].append('no_voltage_param')
    for i in range(range_limit):
        if sadzax.Trimmer.left(source_dict[i][0], 7) == "DeltaTg":
            source_dict[i].append('∆tgδ')
        elif sadzax.Trimmer.left(source_dict[i][0], 7) == "DeltaC_":
            source_dict[i].append('∆C')
        elif sadzax.Trimmer.left(source_dict[i][0], 3) == "Tg_":
            source_dict[i].append('tg')
        elif sadzax.Trimmer.left(source_dict[i][0], 2) == "C_":
            source_dict[i].append('C_dev')
        elif sadzax.Trimmer.left(source_dict[i][0], 20) == "Дата создания записи":
            source_dict[i].append('time')
        else:
            source_dict[i].append('no_indicator')
    for i in range(range_limit):
        source_dict[i].append(source_dict[i][4] + '_' + source_dict[i][3])
    return source_dict
