import datetime
import pandas as pd
import matplotlib.pyplot as plt
import columns
import devices
import itertools

#  Однократное получение данных (* уточнить по оптимизации, нужно ли)
cols = columns.columns_analyzer()


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


#  Однократное получение данных (* уточнить по оптимизации, нужно ли)
database = get_data()


def total_log_counter(data: pd.core = database):
    return data.shape[0]


#  (* уточнить по использованию)
def values_counter(col_number=2,
                   row_numer=None,
                   cl=cols,
                   data: pd.core.frame.DataFrame = database):
    return data[cl[col_number][0]].value_counts[row_numer](normalize=False, sort=False)


#  Анализ времени замеров
def values_time_analyzer(col_number=0,
                         time_sequence_min=1,
                         cl=cols,
                         data: pd.core.frame.DataFrame = database):
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


#  (* описать исключения Ia(r) = -300, Tg = -10)
def pass_the_row(cl=cols,
                 data: pd.core.frame.DataFrame = database):
    for a_column in range(48):  # range(48) заменить на формулу
        #  if (Ia(r) == -300) or (Tg == -10)
        return data[cl[a_column][0]].tolist()


#  Корреляция с температурой окружающей среды (п.3.1. отчёта)


#  Проверка параметра ∆tgδ для срабатывания предупредительной сигнализации (1%)
def delta_tg_checker(cl=cols,  # Добавить индексы и оперировать словарём (с датами и временем)
                     data: pd.core.frame.DataFrame = database,
                     exclude_value=-10.0):
    df = []
    for column_name in range(48):  # range(48) заменить на формулу
        if cl[column_name][4] == '∆tgδ' and cl[column_name][3] == 'HV':  # заменить фильтры на формулы
            df.append(data[cl[column_name][0]].tolist())
    list_of_all_values = list(itertools.chain.from_iterable(df))
    list_of_filtered_values = []
    for column_name in list_of_all_values:
        if column_name != exclude_value:
            list_of_filtered_values.append(column_name)
    list_of_filtered_abs_values = [abs(x) for x in list_of_filtered_values]  # уточнить по модулю отклонения
    return list_of_filtered_abs_values


delta_tg_HV_check = delta_tg_checker()


def delta_tg_checker_counter(col_number=2,
                   row_numer=None,
                   cl=cols,
                   data: pd.core.frame.DataFrame = database):
    return data[cl[col_number][0]].value_counts[row_numer](normalize=False, sort=False)


def delta_tg_checker_warning(operating_data=delta_tg_HV_check, warning=1):
    warning_list = []
    for a_value in operating_data:
        if abs(a_value) >= warning:
            warning_list.append(a_value)
    if not warning_list:
        print(f"Превышение уровня ∆tgδ для срабатывания сигнализации не выявлено")  # убрать
        return warning_list
    else:
        return warning_list


#  prints
print(values_time_analyzer())
print(f"\nОбщее число записей в журнале измерений составило {total_log_counter()}")

delta_tg_check = delta_tg_checker()

print(f"\nСреднее отклонение ∆tgδ стороны ВН составляет"
      f" по модулю {round(sum(delta_tg_HV_check)/len(delta_tg_HV_check),3)}%"
      f" при общем количестве {len(delta_tg_HV_check)} показателей (исключены значения '∆tgδ = -10')")
print(f"\nПревышение уровня ∆tgδ ±1% для срабатывания"
      f" предупредительной сигнализации: {len(delta_tg_checker_warning())}"
      f" случая(-ев) \n {delta_tg_checker_warning()}")

