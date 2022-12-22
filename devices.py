import csv


class Device:
    pass


nkvv = Device()
nkvv.name = 'NKVV'
nkvv.full_name = 'Устройство непрерывного контроля и защиты высоковольтных вводов'
nkvv.monitoring_params = {'input': 220000, 'output': 110000}
nkvv.log_types = {'measure': 'CSV', 'event': 'CSV'}
nkvv.work_file = 'DB_i.csv'
nkvv.work_file_sep = ';'
nkvv.work_file_default_encoding = 'WINDOWS-1251'
nkvv.work_file_parse_dates = ['Дата создания записи', 'Дата сохранения в БД']
nkvv.default_dict_for_replacement_to_nan = {'power': [-300.0, 0.0],
                                            'tg': -10.0,
                                            '∆tgδ': -10.0,
                                            'c_delta': -10.0,
                                            'c_deviation': 0.0,
                                            'voltage_difference': 0.0}


#  russian_date_parser = lambda x: datetime.strptime(x, "DD.MM.YYY HH:MM:SS")


def preview(file, limit):
    with open(file) as r_file:
        file_reader = csv.DictReader(r_file, delimiter=";")
        count = 0
        while count < limit:
            for every_row in file_reader:
                print(every_row)
                count += 1
