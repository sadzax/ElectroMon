import os
import pandas as pd


class Device:
    def __init__(self, name):
        self.name = name
        # self.full_name = name
        # self.monitoring_params = None
        # self.log_types = None
        # self.work_file_name_starts = None
        # self.work_file_folder = None
        # self.work_file_list = Device.work_file_listing(name)  # Why doesn't it work?
        # self.work_file = Device.work_file_picking(name, 0)  # Why doesn't it work?
        # self.work_file_sep = None
        # self.work_file_default_encoding = None
        # self.work_file_parse_dates = None
        # self.default_dict_for_replacement_to_nan = None
        # self.data_types = None
        # self.data_search_name = None

    def work_file_listing(self):
        return [filename for filename in os.listdir(self.work_file_folder)
                if filename.startswith(self.work_file_name_starts['measure'])]

    def work_file_picking(self, num=0):
        return self.work_file_folder + Device.work_file_listing(self)[num]

    def links(self):  # Work on
        return [self.name, self.work_file, self.work_file_sep, self.work_file_default_encoding,
                self.work_file_parse_dates]

    def links_replacement(self):
        return self.default_dict_for_replacement_to_nan


nkvv = Device('nkvv')
nkvv.full_name = 'Устройство непрерывного контроля и защиты высоковольтных вводов'
nkvv.monitoring_params = {'input': 220000, 'output': 110000}
nkvv.log_types = {'measure': 'csv', 'event': 'csv'}
nkvv.work_file_folder = 'upload/nkvv/'
nkvv.work_file_name_starts = {'measure': 'DB_i'}
nkvv.work_file_list = Device.work_file_listing(nkvv)  # Need to put a self.name in here
nkvv.work_file = Device.work_file_picking(nkvv, 0)  # Need to put a self.name in here
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
kiv.full_name = 'Устройство КИВ'  # Need to update
kiv.monitoring_params = {}  # Need to update
kiv.log_types = {'measure': 'xlsx', 'event': 'xlsx'}
kiv.work_file_folder = 'upload/kiv/'
kiv.work_file_name_starts = {'measure': 'MeasJ', 'event': 'WorkJ'}
kiv.work_file_list = Device.work_file_listing(kiv)  # Need to put a self.name in here
kiv.work_file = Device.work_file_picking(kiv, 0)  # Need to put a self.name in here
kiv.work_file_sep = None
kiv.work_file_default_encoding = None
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



# Avoid error of func inside class and/or before obj.init.
def work_file_listing(device_type):
    return [filename for filename in os.listdir(eval(device_type).work_file_folder)
            if filename.startswith(eval(device_type).work_file_name_starts['measure'])]


# Avoid error of func inside class and/or before obj.init.
def work_file_picking(device_type, num=0):
    return eval(device_type).work_file_folder + Device.work_file_listing(eval(device_type))[num]


# Avoid error of func inside class and/or before obj.init.
def links(device_type):
    return Device.links(eval(device_type))


# Avoid error of func inside class and/or before obj.init.
def links_replacement(device_type):
    return Device.links_replacement(eval(device_type))


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
