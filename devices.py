import csv
import datetime
import os


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

    def return_attributes(self):  # Work on
        return [self.name, self.work_file, self.work_file_sep, self.work_file_default_encoding]


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
                                           'tg': -10.0,
                                           '∆tg': -10.0,
                                           'c_delta': -10.0,
                                           'c_deviation': 0.0,
                                           'voltage_difference': 0.0}
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
                        '∆tg': ['∆tg', 'tangent_delta']}


# russian_date_parser = lambda x: datetime.strptime(x, "DD.MM.YYY HH:MM:SS")
nkvv.paste_values_rus = ["Дата создания записи",
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
                         ""]
nkvv.paste_values_utf8 = ['\u0414\u0430\u0442\u0430 \u0441\u043e\u0437\u0434\u0430\u043d\u0438\u044f \u0437\u0430\u043f\u0438\u0441\u0438',
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
                          'Unnamed: 48']
nkvv.paste_values_rus_dict = {0: ['Дата создания записи', 'datetime', 'overall', 'no_voltage', 'time', 'time_of_measure', 'time_no_voltage'],
                              1: ['Дата сохранения в БД', 'datetime', 'overall', 'no_voltage', 'save', 'time_of_saving', 'save_no_voltage'],
                              2: ['U_A1,кВ', 'voltage', 'A1', 'HV', 'U', 'voltage_difference', 'U_HV'],
                              3: ['Ia_A1,мА', 'power', 'A1', 'HV', 'Ia', 'power_active', 'Ia_HV'],
                              4: ['Ir_A1,мА', 'power', 'A1', 'HV', 'Ir', 'power_reactive', 'Ir_HV'],
                              5: ['Tg_A1,%', 'percentage', 'A1', 'HV', 'tg', 'tangent', 'tg_HV'],
                              6: ['C_A1,пФ', 'other', 'A1', 'HV', 'C', 'c_deviation', 'C_HV'],
                              7: ['DeltaTg_A1,%', 'percentage', 'A1', 'HV', '∆tg', 'tangent_delta', '∆tg_HV'],
                              8: ['DeltaC_A1,%', 'percentage', 'A1', 'HV', '∆C', 'c_delta', '∆C_HV'],
                              9: ['U_B1,кВ', 'voltage', 'B1', 'HV', 'U', 'voltage_difference', 'U_HV'],
                              10: ['Ia_B1,мА', 'power', 'B1', 'HV', 'Ia', 'power_active', 'Ia_HV'],
                              11: ['Ir_B1,мА', 'power', 'B1', 'HV', 'Ir', 'power_reactive', 'Ir_HV'],
                              12: ['Tg_B1,%', 'percentage', 'B1', 'HV', 'tg', 'tangent', 'tg_HV'],
                              13: ['C_B1,пФ', 'other', 'B1', 'HV', 'C', 'c_deviation', 'C_HV'],
                              14: ['DeltaTg_B1,%', 'percentage', 'B1', 'HV', '∆tg', 'tangent_delta', '∆tg_HV'],
                              15: ['DeltaC_B1,%', 'percentage', 'B1', 'HV', '∆C', 'c_delta', '∆C_HV'],
                              16: ['U_C1,кВ', 'voltage', 'C1', 'HV', 'U', 'voltage_difference', 'U_HV'],
                              17: ['Ia_C1,мА', 'power', 'C1', 'HV', 'Ia', 'power_active', 'Ia_HV'],
                              18: ['Ir_C1,мА', 'power', 'C1', 'HV', 'Ir', 'power_reactive', 'Ir_HV'],
                              19: ['Tg_C1,%', 'percentage', 'C1', 'HV', 'tg', 'tangent', 'tg_HV'],
                              20: ['C_C1,пФ', 'other', 'C1', 'HV', 'C', 'c_deviation', 'C_HV'],
                              21: ['DeltaTg_C1,%', 'percentage', 'C1', 'HV', '∆tg', 'tangent_delta', '∆tg_HV'],
                              22: ['DeltaC_C1,%', 'percentage', 'C1', 'HV', '∆C', 'c_delta', '∆C_HV'],
                              23: ['U_A2,кВ', 'voltage', 'A2', 'MV', 'U', 'voltage_difference', 'U_MV'],
                              24: ['Ia_A2,мА', 'power', 'A2', 'MV', 'Ia', 'power_active', 'Ia_MV'],
                              25: ['Ir_A2,мА', 'power', 'A2', 'MV', 'Ir', 'power_reactive', 'Ir_MV'],
                              26: ['Tg_A2,%', 'percentage', 'A2', 'MV', 'tg', 'tangent', 'tg_MV'],
                              27: ['C_A2,пФ', 'other', 'A2', 'MV', 'C', 'c_deviation', 'C_MV'],
                              28: ['DeltaTg_A2,%', 'percentage', 'A2', 'MV', '∆tg', 'tangent_delta', '∆tg_MV'],
                              29: ['DeltaC_A2,%', 'percentage', 'A2', 'MV', '∆C', 'c_delta', '∆C_MV'],
                              30: ['U_B2,кВ', 'voltage', 'B2', 'MV', 'U', 'voltage_difference', 'U_MV'],
                              31: ['Ia_B2,мА', 'power', 'B2', 'MV', 'Ia', 'power_active', 'Ia_MV'],
                              32: ['Ir_B2,мА', 'power', 'B2', 'MV', 'Ir', 'power_reactive', 'Ir_MV'],
                              33: ['Tg_B2,%', 'percentage', 'B2', 'MV', 'tg', 'tangent', 'tg_MV'],
                              34: ['C_B2,пФ', 'other', 'B2', 'MV', 'C', 'c_deviation', 'C_MV'],
                              35: ['DeltaTg_B2,%', 'percentage', 'B2', 'MV', '∆tg', 'tangent_delta', '∆tg_MV'],
                              36: ['DeltaC_B2,%', 'percentage', 'B2', 'MV', '∆C', 'c_delta', '∆C_MV'],
                              37: ['U_C2,кВ', 'voltage', 'C2', 'MV', 'U', 'voltage_difference', 'U_MV'],
                              38: ['Ia_C2,мА', 'power', 'C2', 'MV', 'Ia', 'power_active', 'Ia_MV'],
                              39: ['Ir_C2,мА', 'power', 'C2', 'MV', 'Ir', 'power_reactive', 'Ir_MV'],
                              40: ['Tg_C2,%', 'percentage', 'C2', 'MV', 'tg', 'tangent', 'tg_MV'],
                              41: ['C_C2,пФ', 'other', 'C2', 'MV', 'C', 'c_deviation', 'C_MV'],
                              42: ['DeltaTg_C2,%', 'percentage', 'C2', 'MV', '∆tg', 'tangent_delta', '∆tg_MV'],
                              43: ['DeltaC_C2,%', 'percentage', 'C2', 'MV', '∆C', 'c_delta', '∆C_MV'],
                              44: ['Tair,°С', 'temperature', 'overall', 'no_voltage', 'tair', 'temperature_of_air', 'tair_no_voltage'],
                              45: ['Tdevice,°С', 'temperature', 'overall', 'no_voltage', 'tdev', 'temperature_of_device', 'tdev_no_voltage'],
                              46: ['Tcpu,°С', 'temperature', 'overall', 'no_voltage', 'tcpu', 'temperature_of_cpu', 'tcpu_no_voltage'],
                              47: ['Freq,Гц', 'frequency', 'overall', 'no_voltage', 'freq', 'frequency', 'freq_no_voltage'],
                              48: ['Unnamed: 48', 'other', 'overall', 'no_voltage', 'no_name', 'no_name', 'no_name_no_voltage']}
