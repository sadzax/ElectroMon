import numpy as np
import pandas as pd
import columns
import devices
import itertools

#  Get variable for data
cols = columns.columns_analyzer()
cols_len = len(columns.columns_maker())


#  Importing CSV
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


#  Get variable for data
database = get_data()


#  Count the strings
def total_log_counter(data: pd.core = database):
    return data.shape[0]


#  Analysis of time of measurements
def values_time_analyzer(col_number=0,
                         time_sequence_min=1,
                         cl=cols,
                         data: pd.core = database):
    df = data[cl[col_number][0]].values
    for a_row in range(df.shape[0] - 1):
        if (df[a_row + 1] - df[a_row]).astype('timedelta64[m]') == time_sequence_min:
            pass
        else:
            gap = (df[a_row + 1] - df[a_row]).astype('timedelta64[m]')
            if gap > 1440:
                err = (df[a_row + 1] - df[a_row]).astype('timedelta64[D]')
            elif gap > 60:
                err = (df[a_row + 1] - df[a_row]).astype('timedelta64[h]')
            elif gap < 1:
                err = (df[a_row + 1] - df[a_row]).astype('timedelta64[s]')
            else:
                err = gap
            print(f"Ошибка измерения времени в данных! Строка № {a_row}:\n"
                  f"В строке № {a_row}"
                  f" дата {pd.to_datetime(str(df[a_row])).strftime('%d.%m.%y')}"
                  f" время {pd.to_datetime(str(df[a_row])).strftime('%H.%M')}"
                  f", в следующей строке № {a_row + 1}"
                  f" дата {pd.to_datetime(str(df[a_row + 1])).strftime('%d.%m.%y')}"
                  f" время {pd.to_datetime(str(df[a_row + 1])).strftime('%H.%M')}"
                  f", т.е. через {err}\n")


#  Exclude (Ia(r) = -300, Tg = -10) to NaN
def pass_the_nan(seeking_param='power',  # Need to optimize memory usage
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


database = pass_the_nan('power', -300.0)
database = pass_the_nan('tg', -10.0)  # ?? Need to optimize
database = pass_the_nan('∆tgδ', -10.0)


#  ______ Correlation with environment temperature (p.3.1. of the report)
def correlation_temp():
    pass


#  Filtering
def data_filter(filter_list,
                data=database,
                cl=cols):
    filter_list_indexes = []
    for a_column in range(cols_len):
        for a_param in range(len(cols[0])):
            if cl[a_column][a_param] in filter_list:
                filter_list_indexes.append(a_column)
    filter_list_names = [cl[i][0] for i in filter_list_indexes]
    return data[filter_list_names]


# Main averager
def data_average_finder(filter_list=None,
                        abs_parameter=True,
                        unite_parameter=False,
                        list_of_non_math=None,
                        data=database,
                        cl=cols):
    if filter_list is None:
        filter_list = ['time', '∆tgδ_HV']
    if list_of_non_math is None:
        list_of_non_math = ['Дата создания записи',
                            'Дата сохранения в БД']
    df = data_filter(filter_list, data, cl)
    func_columns_list = list(df.columns)
    func_result_prev = []
    func_result = {}
    for i in range(df.shape[1]):
        for k in list_of_non_math:
            if k == func_columns_list[i]:
                break
        else:
            columns_list_of_values = df[func_columns_list[i]].tolist()
            # okay
            if unite_parameter is False:
                if abs_parameter is True:
                    values_without_nan = [abs(x) for x in columns_list_of_values if not np.isnan(x)]
                else:
                    values_without_nan = [x for x in columns_list_of_values if not np.isnan(x)]
                func_result[func_columns_list[i]] = sum(values_without_nan)/len(values_without_nan)
            else:
                if abs_parameter is True:
                    dump = [abs(x) for x in columns_list_of_values if not np.isnan(x)]
                else:
                    dump = [x for x in columns_list_of_values if not np.isnan(x)]
                func_result_prev = func_result_prev + dump
                func_result = {'Среднее по всем: ': sum(func_result_prev) / len(func_result_prev)}
    return func_result


#  ______ Search for deviations
def data_deviation_finder(filter_list, data=database, cl=cols):
    df = data_filter(filter_list, data, cols)
    func_columns_list = list(df.columns)
    for i in range(df.shape[1] - 1):
        if func_columns_list[i] == "Дата создания записи" or "Дата сохранения в БД":
            pass
        else:
            return data[func_columns_list[i]].value_counts(normalize=False, sort=False)


print(data_average_finder(['time', '∆tgδ_HV']))


#  ______ Проверка параметра ∆tgδ для технических целей
def delta_tg_checker(cl=cols,
                     data: pd.core = database,
                     exclude_values=(-10.0, -300.0)):
    df = []
    for column_index in range(cols_len):
        if cl[column_index][4] == '∆tgδ' and cl[column_index][3] == 'HV':
            df.append(data[cl[column_index][0]].tolist())
    list_of_all_values = list(itertools.chain.from_iterable(df))
    list_of_filtered_values = []
    for value in list_of_all_values:
        if value not in exclude_values:
            list_of_filtered_values.append(value)
    list_of_filtered_abs_values = [abs(x) for x in list_of_filtered_values]  # уточнить по модулю отклонения
    return list_of_filtered_abs_values


#  ______ Проверка срабатывания сигнализации срабатывания предупредительной сигнализации (1%)
def delta_tg_checker_warning(operating_data=None, warning=1):
    if operating_data is None:
        operating_data = delta_tg_HV_check
    warning_list = []
    for a_value in operating_data:
        if abs(a_value) >= warning:
            warning_list.append(a_value)
    if not warning_list:
        print(f"Превышение уровня ∆tgδ для срабатывания сигнализации не выявлено")  # убрать
        return warning_list
    else:
        return warning_list


delta_tg_HV_check = delta_tg_checker()


print(values_time_analyzer())
print(f"\nОбщее число записей в журнале измерений составило {total_log_counter()}")

delta_tg_check = delta_tg_checker()

print(f"\nСреднее отклонение ∆tgδ стороны ВН составляет"
      f" по модулю {round(sum(delta_tg_HV_check) / len(delta_tg_HV_check), 3)}%"
      f" при общем количестве {len(delta_tg_HV_check)} показателей (исключены значения '∆tgδ = -10')")
print(f"\nПревышение уровня ∆tgδ ±1% для срабатывания"
      f" предупредительной сигнализации: {len(delta_tg_checker_warning())}"
      f" случая(-ев) \n {delta_tg_checker_warning()}")
