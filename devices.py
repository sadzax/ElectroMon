import csv
import pandas as pd
import numpy as np
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


work_file = 'DB_i.csv'  # goal file
work_file_sep = ';'
work_file_default_encoding = 'WINDOWS-1251'
work_file_parse_dates = ['Дата создания записи', 'Дата сохранения в БД']


def get_cols(file=work_file, sep=work_file_sep, encoding=work_file_default_encoding, parse_dates=None):
    if parse_dates is None:
        parse_dates = work_file_parse_dates
    col_array = pd.read_csv(file,
                            sep=sep,
                            encoding=encoding,
                            parse_dates=parse_dates,
                            dayfirst=True,
                            nrows=1).columns
    return col_array


def get_data(usecols: list = None, file=work_file, sep=work_file_sep, encoding=work_file_default_encoding):
    if usecols is None:
        parse_dates = work_file_parse_dates
    else:
        cols = []
        for k in usecols:
            if k in work_file_parse_dates:
                cols.append(k)
        parse_dates = cols
    data = pd.read_csv(file,
                       sep=sep,
                       encoding=encoding,
                       parse_dates=parse_dates,
                       usecols=usecols,
                       dayfirst=True)
    return data


def plot_2d_simple(val_x: str, val_y: str, size_x: int = 14, size_y: int = 4):
    df = get_data([val_x, val_y])
    fig, axs = plt.subplots(figsize=(size_x, size_y))
    plt.xlabel(val_x)
    plt.ylabel(val_y)
    x = df[val_x].tolist()
    y = df[val_y].tolist()
    axs.plot(x, y)
