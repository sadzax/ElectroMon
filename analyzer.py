import datetime
import pandas as pd
import matplotlib.pyplot as plt
import columns
import devices

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


def total_log_counter(data: pd.core.frame.DataFrame = get_data()):
    return data.shape[0]


def values_counter(col_number=2,
                   row_numer=None,
                   cl=cols,
                   data: pd.core.frame.DataFrame = get_data()):
    return data[cl[col_number][0]].value_counts[row_numer](normalize=False, sort=False)


def values_time_analyzer(col_number=0,
                         time_sequence_min=1,
                         cl=cols,
                         data: pd.core.frame.DataFrame = get_data()):
    df = data[cl[col_number][0]].values
    for i in range(df.shape[0]-1):
        if (df[i+1]-df[i]).astype('timedelta64[m]') == time_sequence_min:
            pass
        else:
            gap = (df[i + 1] - df[i]).astype('timedelta64[m]')
            if gap > 1440:
                err = (df[i + 1] - df[i]).astype('timedelta64[D]')
            elif gap > 60:
                err = (df[i + 1] - df[i]).astype('timedelta64[h]')
            elif gap < 1:
                err = (df[i + 1] - df[i]).astype('timedelta64[s]')
            else:
                err = gap
            print(f"Ошибка измерения времени в данных! Строка № {i}:\n"
                  f"В строке № {i}"
                  f" дата {pd.to_datetime(str(df[i])).strftime('%d.%m.%y')}"
                  f" время {pd.to_datetime(str(df[i])).strftime('%H.%M')}"
                  f", в следующей строке № {i+1}"
                  f" дата {pd.to_datetime(str(df[i+1])).strftime('%d.%m.%y')}"
                  f" время {pd.to_datetime(str(df[i+1])).strftime('%H.%M')}"
                  f", т.е. через {err}\n")


def delta_tg_checker(cl=cols,
                     data: pd.core.frame.DataFrame = get_data()):
    for i in range(48):
        if cl[i][3] == '∆tgδ':
            return data[cl[i][0]].value_counts()


print(values_time_analyzer())
print(f"\nОбщее число записей в журнале измерений составило {total_log_counter()}")

print(delta_tg_checker())
