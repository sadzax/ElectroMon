import numpy as np
import pandas as pd
import columns
import devices
import plots
import temp_exec
import sadzax
import run
import analyzer


def get_data(usecols: list = None,
             file=devices.nkvv.work_file,
             sep=devices.nkvv.work_file_sep,
             encoding=devices.nkvv.work_file_default_encoding):
    if usecols is None:
        parse_dates = devices.nkvv.work_file_parse_dates
    else:
        parse_date_columns = []
        for k in usecols:
            if k in devices.nkvv.work_file_parse_dates:
                parse_date_columns.append(k)
        parse_dates = parse_date_columns
    data = pd.read_csv(file,
                       sep=sep,
                       encoding=encoding,
                       parse_dates=parse_dates,
                       usecols=usecols,
                       dayfirst=True)
    return data


#  Однократное получение данных в переменную
database = get_data()


#  Подсчёт общего количества строк
def total_log_counter(data: pd.core = database):
    return data.shape[0]


#  Перевести исключения (Ia(r) = -300, Tg = -10) в NaN
def pass_the_nan(seeking_param='power',
                 replacing_value=-300.0,
                 cl=cols,
                 data: pd.core = database):
    for a_column in range(cols_len):
        for a_param in range(len(cols[0])):
            if cl[a_column][a_param] == seeking_param:
                for a_row in range(data.shape[0]):
                    if data.iloc[a_row, a_column] == replacing_value:
                        data.iloc[a_row, a_column] = np.NaN
    return data


def data_filter(filter_list, data=database, cl=cols):
    filter_list_indexes = []
    for a_column in range(cols_len):
        for a_param in range(len(cols[0])):
            if cl[a_column][a_param] in filter_list:
                filter_list_indexes.append(a_column)
    filter_list_names = [cl[i][0] for i in filter_list_indexes]
    return data[filter_list_names]

filter_list=['time', '∆tgδ_HV']
abs_parameter=True
unite_parameter=False
list_of_non_math=None
data=database
cl=cols
# list_of_non_math = ['Дата создания записи','Дата сохранения в БД']

database = pass_the_nan('power', -300.)
database = pass_the_nan('tg', -10.0)
database = pass_the_nan('∆tgδ', -10.0)
