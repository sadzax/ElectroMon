import os
import pandas as pd
import pathlib


class Device:
    def __init__(self, name):
        self.name = name
        self.full_name = name
        self.monitoring_params = None
        self.log_types = None
        self.work_file_name_starts = None
        self.work_file_name_ends = None
        self.work_file = None
        self.work_file_folder = 'upload/' + name + '/'
        self.work_file_sep = None
        self.work_file_default_encoding = None
        self.work_file_parse_dates = None
        self.default_dict_for_replacement_to_nan = None
        self.data_types = None
        self.data_search_name = None

    @property
    def work_file_list(self):
        return [filename for filename in os.listdir(self.work_file_folder)
                if filename.startswith(self.work_file_name_starts['measure'])]

    @property
    def work_file_picking(self, num=0):
        return self.work_file_folder + self.work_file_list(self)[num]

    def links(self):  # Work on
        return [self.name, self.work_file, self.work_file_sep, self.work_file_default_encoding,
                self.work_file_parse_dates]

    def links_replacement(self):
        return self.default_dict_for_replacement_to_nan


mon = Device('mon')

mon.full_name = 'Мониторинг устройств непрерывного контроля и защиты высоковольтных вводов'
mon.monitoring_params = {}
mon.log_types = {'measure': '.I', 'event': '.A'}
mon.work_file_folder = 'upload/mon/'
mon.work_file_name_ends = {'measure': '.I'}  # Here we take 'end', not 'start' position
mon.work_file_list = Device.work_file_listing(mon)  # Need to put a self.name in here
mon.work_file = Device.work_file_picking(mon)  # Need to put a self.name in here
mon.work_file_sep = r"\s+"
mon.work_file_default_encoding = 'WINDOWS-1251'
mon.work_file_parse_dates = ['дата', 'время', 'Дата и время']
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
                  'Дата': 'datetime', }
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
