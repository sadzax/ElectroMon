import csv
import pandas as pd
import matplotlib.pyplot as plt


class Device:
    pass


main_device = Device()
main_device.name = 'NKVV'
main_device.full_name = 'Устройство непрерывного контроля и защиты высоковольтных вводов'
main_device.monitoring_params = {'input': 220000, 'output': 110000}
main_device.log_types = {'measure': 'CSV', 'event': 'CSV'}

#  russian_date_parser = lambda x: datetime.strptime(x, "DD.MM.YYY HH:MM:SS")


def preview(file, limit):
    with open(file) as r_file:
        file_reader = csv.DictReader(r_file, delimiter=";")
        count = 0
        while count < limit:
            for every_row in file_reader:
                print(every_row)
                count += 1


work_file = 'DB_i.csv'


def get_data(file):
    data = pd.read_csv(file,
                       sep=';',
                       encoding='WINDOWS-1251',
                       parse_dates=['Дата создания записи', 'Дата сохранения в БД'],
                       dayfirst=True)
    return data


a = get_data(work_file)
print(a)
