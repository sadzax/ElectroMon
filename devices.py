import os
import pandas as pd
import pathlib


class Device:
    def __init__(self, name):
        """
        Инициализация устройства, поля:
        1. Краткое имя
        """
        self.name = name
        self.full_name = name
        self.monitoring_params = None
        self.log_types = None
        self.work_file_list_choice = 0  # default
        self.work_file_name_starts = None
        self.work_file_name_ends = None
        self.work_file_folder = 'upload/' + name + '/'
        self.work_file_sep = None
        self.work_file_default_encoding = None
        self.work_file_parse_dates = None
        self.default_dict_for_replacement_to_nan = None
        self.data_types = None
        self.data_search_name = None

    @property
    def work_file_list(self):  # Прописать для окончания
        return [filename for filename in os.listdir(self.work_file_folder)
                if filename.startswith(self.work_file_name_starts['measure'])]

    @property
    def work_file(self):
        return self.work_file_folder + self.work_file_list[self.work_file_list_choice]

    def work_file_pick(self, num=0):  # Отдаёт значения в ./prints
        work_file = self.work_file_folder + self.work_file_list[num]
        self.work_file_list_choice = num
        return work_file

    def links(self):  # Можно добавлять значения
        return [
            self.name, self.work_file, self.work_file_sep, self.work_file_default_encoding,  # 0-3
            self.work_file_parse_dates, self.work_file_list,  # 4-5
            self.default_dict_for_replacement_to_nan  # 6
                ]


nkvv = Device('nkvv')
nkvv.full_name = 'Устройство непрерывного контроля и защиты высоковольтных вводов'
nkvv.monitoring_params = {'input': 220000, 'output': 110000}
nkvv.log_types = {'measure': 'csv', 'event': 'csv'}
nkvv.work_file_folder = 'upload/nkvv/'
nkvv.work_file_name_starts = {'measure': 'DB_i'}
nkvv.work_file_sep = ';'
nkvv.work_file_default_encoding = 'WINDOWS-1251'
nkvv.work_file_parse_dates = ['Дата создания записи', 'Дата сохранения в БД']
nkvv.default_dict_for_replacement_to_nan = {'power': [-300.0, 0.0],
                                            'tg': -10.0,
                                            '∆tg': -10.0,
                                            'c_delta': -10.0,
                                            'c_deviation': 0.0,
                                            'voltage_difference': 0.0}
nkvv.data_types = {'кВ': 'voltage',
                   'мА': 'power',
                   ',%': 'percentage',
                   'От': 'deviation',
                   '°С': 'temperature',
                   'Гц': 'frequency',
                   'Дата': 'datetime',}
nkvv.data_search_name = {'DeltaTg': ['∆tg', 'tangent_delta'],
                         'DeltaC_': ['∆C', 'c_delta'],
                         'Tg_': ['tg', 'tangent'],
                         'C_': ['C', 'c_deviation'],
                         'Дата создания записи': ['time', 'time_of_measure'],
                         'Дата сохранения в БД': ['save', 'time_of_saving'],
                         'U_': ['U', 'voltage_difference'],
                         'Ia_': ['Ia', 'power_active'],
                         'Ir_': ['Ir', 'power_reactive'],
                         'Freq': ['freq', 'frequency'],
                         'Tair': ['tair', 'temperature_of_air'],
                         'Tdev': ['tdev', 'temperature_of_device'],
                         'Tcpu': ['tcpu', 'temperature_of_cpu']}


kiv = Device('kiv')
kiv.full_name = 'Устройство контроля изоляции вводов'
kiv.log_types = {'measure': 'xlsx', 'event': 'xlsx'}
kiv.work_file_folder = 'upload/kiv/'
kiv.work_file_name_starts = {'measure': 'MeasJ', 'event': 'WorkJ'}
kiv.work_file_parse_dates = ['Дата/Время']  # Starts with
kiv.default_dict_for_replacement_to_nan = {'power': [-300.0, 0.0],
                                           'tg': [-10.0, 0.0],
                                           '∆tg': [-10.0, 0.0],
                                           'c_delta': [-10.0, 0.0],
                                           'c_deviation': [0.0, 0.0],
                                           'voltage_difference': [0.0]}
kiv.data_types = {'°С': 'temperature',
                  'Дата': 'datetime',
                  'U': 'voltage',
                  'I': 'power',
                  'tg': 'percentage',
                  '∆tg': 'percentage',
                  '∆C': 'deviation',
                  'C1': 'deviation'}
kiv.data_search_name = {'Дата': ['time', 'time_of_measure'],
                        'U': ['U', 'voltage_difference'],
                        'I': ['Ia', 'power_active'],  # Ask question
                        'C1': ['C', 'c_deviation'],
                        'tg': ['tg', 'tangent'],
                        '∆C': ['∆C', 'c_delta'],
                        '∆tg': ['∆tg', 'tangent_delta'],
                        'Iunb': ['Ia', 'power_unbalanced'],
                        'Phy_unb': ['phy', 'angle_unbalanced'],
                        'Tmk': ['tcpu', 'temperature_of_cpu'],
                        'Tamb': ['tair', 'temperature_of_air']}


mon = Device('mon')
mon.full_name = 'Мониторинг устройств непрерывного контроля и защиты высоковольтных вводов'
mon.monitoring_params = {'input': 220000, 'output': 110000}
mon.log_types = {'measure': 'csv', 'event': 'csv'}
mon.work_file_folder = 'upload/mon/'
mon.work_file_name_ends = {'measure': '.I'}
mon.work_file_sep = r"\s+"
mon.work_file_default_encoding = 'WINDOWS-1251'
mon.work_file_parse_dates = ['Дата и время']
mon.default_dict_for_replacement_to_nan = {'power': [-300.0, 0.0],
                                            'tg': -10.0,
                                            '∆tg': -10.0,
                                            'c_delta': -10.0,
                                            'c_deviation': 0.0,
                                            'voltage_difference': 0.0}
mon.data_types = {'кВ': 'voltage',
                   'мА': 'power',
                   ',%': 'percentage',
                   'От': 'deviation',
                   '°С': 'temperature',
                   'Гц': 'frequency',
                   'Дата': 'datetime',}
mon.data_search_name = {'DeltaTg': ['∆tg', 'tangent_delta'],
                         'DeltaC_': ['∆C', 'c_delta'],
                         'Tg_': ['tg', 'tangent'],
                         'C_': ['C', 'c_deviation'],
                         'Дата создания записи': ['time', 'time_of_measure'],
                         'Дата сохранения в БД': ['save', 'time_of_saving'],
                         'U_': ['U', 'voltage_difference'],
                         'Ia_': ['Ia', 'power_active'],
                         'Ir_': ['Ir', 'power_reactive'],
                         'Freq': ['freq', 'frequency'],
                         'Tair': ['tair', 'temperature_of_air'],
                         'Tdev': ['tdev', 'temperature_of_device'],
                         'Tcpu': ['tcpu', 'temperature_of_cpu']}


# Avoid error of func inside class and/or before obj.init.
def work_file_pick(device_type, num=0):
    return Device.work_file_pick(eval(device_type), num)


# Avoid error of func inside class and/or before obj.init.
def links(device_type):
    return Device.links(eval(device_type))


class Pkl:
    def save(device_type, data):
        path = './save/' + device_type + '/'
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        name_file = eval(device_type).work_file[eval(device_type).work_file.find('/', 7) + 1:]
        total_path = path + name_file + '.pkl'
        data.to_pickle(total_path)

    def load(device_type):
        name_file = eval(device_type).work_file[eval(device_type).work_file.find('/', 7) + 1:]
        path = './save/' + device_type + '/'
        total_path = path + name_file + '.pkl'
        return pd.read_pickle(total_path)
