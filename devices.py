import os
import pandas as pd
import pathlib
import glob


class Device:
    def __init__(self, name):
        """
        Devices mostly store and return attributes for further processing
        Module consist of methods setting properties and statuses of device, such as:
        """
        self.name = name
        self.full_name = name
        self.monitoring_params = None
        self.log_types = None
        self.file_list_choice = 0  # default
        self.file_name_starts = None
        self.file_name_ends = None
        self.file_folder = 'upload/' + name + '/'
        self.file_sep = None
        self.file_default_encoding = None
        self.file_parse_dates_basis = None
        self.file_parse_dates = None
        self.default_dict_for_replacement_to_nan = None
        self.default_dict_for_dtypes = None
        self.data_types = None
        self.data_search_name = None
        self.warning_map = {'∆tg': [1.0, 1.5], '∆C': [3.0, 5.0]}

    @property
    def file_list(self):
        """
        Sets the list of files based on 'file_name_starts' and/or 'file_name_ends' properties
        :returns: list of files as filepath form root directory
        """
        error = f'У устройства "{self.full_name}" в папке {self.file_folder} нет подходящих файлов.' \
                f' Загрузите их, пожалуйста'
        all_files = ['/'.join([i for i in filepath.parts]) for filepath
                     in pathlib.Path(self.file_folder).glob('**/*')]
        if self.file_name_starts is None and self.file_name_ends is None:
            if not all_files:
                print(error)
            else:
                return all_files
        elif self.file_name_starts is None:
            endswith = self.file_name_ends['measure']
            return [filepath for filepath in all_files
                    if str(filepath)[-len(endswith):] == endswith]
        elif self.file_name_ends is None:
            startswith = self.file_name_starts['measure']
            return [filepath for filepath in all_files
                    if filepath[filepath.find('/', 7) + 1:].startswith(startswith)]
        else:
            endswith = self.file_name_ends['measure']
            startswith = self.file_name_starts['measure']
            return [filepath for filepath in all_files
                    if str(filepath)[-len(endswith):] == endswith
                    and filepath[filepath.find('/', 7) + 1:].startswith(startswith)]

    @property
    def file(self):
        return self.file_list[self.file_list_choice]

    def file_pick(self, num=0):  # Returns values to ./prints
        """
        Picks a file out of file list, should take a number/index of a file
        """
        file = self.file_list[num]
        self.file_list_choice = num
        return file

    def links(self):  # Можно добавлять значения
        """
        Method contains main properties of a devices returned as a list
        The method can be enlarged with new properties, but the order of the list must never be rearranged
            because its indexes are used in analytical functions
        """
        return [
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
        ]


# Can I reorganize this module?
nkvv = Device('nkvv')
nkvv.full_name = 'Устройство непрерывного контроля и защиты высоковольтных вводов'
nkvv.monitoring_params = {'input': 220000, 'output': 110000}
nkvv.log_types = {'measure': 'csv', 'event': 'csv'}
nkvv.file_folder = 'upload/nkvv/'
nkvv.file_name_starts = {'measure': 'DB_i'}
nkvv.file_sep = ';'
nkvv.file_default_encoding = 'WINDOWS-1251'
nkvv.file_parse_dates = ['Дата создания записи', 'Дата сохранения в БД']
nkvv.default_dict_for_replacement_to_nan = {'power': [-300.0, 0.0],
                                            'tg': [-10.0],
                                            '∆tg': [-10.0],
                                            'c_delta': [-10.0],
                                            'c_deviation': [0.0],
                                            'voltage_difference': [0.0]}
nkvv.data_types = {'кВ': 'voltage',
                   'мА': 'power',
                   ',%': 'percentage',
                   'От': 'deviation',
                   '°С': 'temperature',
                   'Гц': 'frequency',
                   'Дата': 'datetime', }
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
nkvv.default_dict_for_dtypes = {'∆tg': float,
                                '∆C': float,
                                'tg': float,
                                'C': float,
                                'U': float,
                                'Ia': float,
                                'Ir': float,
                                'freq': float,
                                'tair': float,
                                'tdev': float,
                                'tcpu': float}

kiv = Device('kiv')
kiv.full_name = 'Устройство контроля изоляции вводов'
kiv.log_types = {'measure': 'xlsx', 'event': 'xlsx'}
kiv.file_folder = 'upload/kiv/'
kiv.file_name_starts = {'measure': 'MeasJ', 'event': 'WorkJ'}
kiv.file_parse_dates = ['Дата/Время']  # Starts with
kiv.default_dict_for_replacement_to_nan = {'power': [-300.0, 0.0],
                                           'tg': [-10.0, 0.0],
                                           '∆tg': [-10.0],
                                           'c_delta': [-10.0],
                                           'c_deviation': [0.0],
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
mon.file_folder = 'upload/mon/'
mon.file_name_ends = {'measure': '.I'}
mon.file_sep = r"\s+"
mon.file_default_encoding = 'WINDOWS-1251'
mon.file_parse_dates_basis = ['дата', 'время']
mon.file_parse_dates = ['Дата и время']
mon.default_dict_for_replacement_to_nan = {'power': [-300.0],
                                           'power_active': [-300.0],
                                           'power_reactive': [-300.0],
                                           'tg': [-10.0],
                                           'tangent': [-10.0],
                                           '∆tg': [-10.0],
                                           'tangent_delta': [-10.0],
                                           'c_delta': [-10.0],
                                           'c_deviation': [0.0],
                                           'other': ['****'],
                                           'overall': ['****']}
mon.data_types = {'кВ': 'voltage',
                  'мА': 'power',
                  ',%': 'percentage',
                  'От': 'deviation',
                  '°С': 'temperature',
                  'Гц': 'frequency',
                  'Дата': 'datetime', }
mon.data_search_name = {'dtan_': ['∆tg', 'tangent_delta'],
                        'dC_': ['∆C', 'c_delta'],
                        'tan_': ['tg', 'tangent'],
                        'C_': ['C', 'c_deviation'],
                        'Дата и время': ['time', 'time_of_measure'],
                        'U_': ['U', 'voltage_difference'],
                        'Ia_': ['Ia', 'power_active'],
                        'Ip_': ['Ir', 'power_reactive'],
                        'Freq': ['freq', 'frequency'],
                        'Tair': ['tair', 'temperature_of_air'],
                        'Tdev': ['tdev', 'temperature_of_device'],
                        'Tcpu': ['tcpu', 'temperature_of_cpu']}
mon.default_dict_for_dtypes = {'∆tg': float,
                               '∆C': float,
                               'tg': float,
                               'C': float,
                               'U': float,
                               'Ia': float,
                               'Ir': float,
                               'freq': float,
                               'tair': float,
                               'tdev': float,
                               'tcpu': float}


# Devices
objs = [nkvv, kiv, mon]


# Avoid error of func inside class and/or before obj.init.
def file_pick(device_type, num=0):
    return Device.file_pick(eval(device_type), num)


# Avoid error of func inside class and/or before obj.init.
def links(device_type):
    return Device.links(eval(device_type))


class Pkl:
    """
    Saved cache of data for a device can be stored in a
    .pkl format in save/ directory for further fast upload.
    """
    def save(device_type, data: object) -> object:
        path = './save/' + device_type + '/'
        isExist = os.path.exists(path)
        if not isExist:
            os.makedirs(path)
        name_file = eval(device_type).file[eval(device_type).file.find('/', 7) + 1:]
        total_path = path + name_file + '.pkl'
        try:
            data.to_pickle(total_path)
        except OSError:
            total_path = path + name_file.replace('/', '_') + '.pkl'
            data.to_pickle(total_path)

    def load(device_type):
        name_file = eval(device_type).file[eval(device_type).file.find('/', 7) + 1:]
        path = './save/' + device_type + '/'
        total_path = path + name_file + '.pkl'
        try:
            return pd.read_pickle(total_path)
        except FileNotFoundError:
            list_of_files = glob.glob(path + '*pkl')
            latest_file = max(list_of_files, key=os.path.getctime)
            return pd.read_pickle(latest_file)
