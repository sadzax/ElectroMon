import itertools

import numpy as np
import pandas as pd

import columns
import devices


#  1.0. Importing CSV
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


#  2.0. Count the strings
def total_log_counter(data: pd.core = None,
                      file=devices.nkvv.work_file,
                      sep=devices.nkvv.work_file_sep,
                      encoding=devices.nkvv.work_file_default_encoding):
    if data is None:
        data = get_data(file=file, sep=sep, encoding=encoding)
    return data.shape[0]


#  2.1. Analysis of time of measurements
def values_time_analyzer(col_number=0,
                         time_sequence_min=1,
                         cols=None,
                         data: pd.core = None,
                         file=devices.nkvv.work_file,
                         sep=devices.nkvv.work_file_sep,
                         encoding=devices.nkvv.work_file_default_encoding,
                         gap_const_day=1440,
                         gap_const_hour=60,
                         exact_gap=True):
    if data is None:
        data = get_data(file=file, sep=sep, encoding=encoding)
    if cols is None:
        cols = columns.columns_analyzer(file=file, sep=sep, encoding=encoding)
    df = data[cols[col_number][0]].values
    error_dict = {}
    for a_row in range(df.shape[0] - 1):
        if (df[a_row + 1] - df[a_row]).astype('timedelta64[m]') == time_sequence_min:
            pass
        else:
            if exact_gap is False:  # for console use
                gap = (df[a_row + 1] - df[a_row]).astype('timedelta64[m]')
                if gap > gap_const_day:
                    err = (df[a_row + 1] - df[a_row]).astype('timedelta64[D]')
                elif gap > gap_const_hour:
                    err = (df[a_row + 1] - df[a_row]).astype('timedelta64[h]')
                elif gap < time_sequence_min:
                    err = (df[a_row + 1] - df[a_row]).astype('timedelta64[s]')
                else:
                    err = gap
            else:
                err = df[a_row + 1] - df[a_row]
            error_dict[a_row + 1] = [pd.to_datetime(str(df[a_row])).strftime('%d.%m.%y'),
                                     pd.to_datetime(str(df[a_row])).strftime('%H.%M'),
                                     pd.to_datetime(str(df[a_row + 1])).strftime('%d.%m.%y'),
                                     pd.to_datetime(str(df[a_row + 1])).strftime('%H.%M'),
                                     err]
    return error_dict


#  2.1.1. Analysis of time of measurements to dataframe
def values_time_analyzer_df(source_dict=None,
                            orient='index',
                            cols=None):
    if source_dict is None:
        source_dict = values_time_analyzer()
    if cols is None:
        cols = ["Дата", "Время", "Дата след.", "Время след.", "Разница"]
    return pd.DataFrame.from_dict(source_dict, orient=orient, columns=cols)


#  2.2. Exclude (Ia(r) = -300, Tg = -10) to NaN  ______ ADD EXCLUSIONS LISTS!
def pass_the_nan(default_dict_for_replacement=None,
                 cols=None,
                 data: pd.core = None,
                 file=devices.nkvv.work_file,
                 sep=devices.nkvv.work_file_sep,
                 encoding=devices.nkvv.work_file_default_encoding):
    if data is None:
        data = get_data(file=file, sep=sep, encoding=encoding)
    if cols is None:
        cols = columns.columns_analyzer(file=file, sep=sep, encoding=encoding)
    if default_dict_for_replacement is None:
        default_dict_for_replacement = devices.nkvv.default_dict_for_replacement_to_nan
    for i in range(len(default_dict_for_replacement)):
        seeking_param = [x for x in default_dict_for_replacement.keys()][i]
        replacing_value = [x for x in default_dict_for_replacement.values()][i]
        for a_column in range(len(cols)):
            for a_param in range(len(cols[0])):
                if cols[a_column][a_param] == seeking_param:
                    for a_row in range(data.shape[0]):  # Need to optimize memory usage
                        if isinstance(replacing_value, list) is False:
                            if data.iloc[a_row, a_column] == replacing_value:
                                data.iloc[a_row, a_column] = np.NaN
                        else:
                            for every_replacing_value in replacing_value:
                                if data.iloc[a_row, a_column] == every_replacing_value:
                                    data.iloc[a_row, a_column] = np.NaN
    return data


#  2.3. Counting the nan_strings:
def total_nan_counter(data=None,
                      cols=None,
                      file=devices.nkvv.work_file,
                      sep=devices.nkvv.work_file_sep,
                      encoding=devices.nkvv.work_file_default_encoding):
    if data is None:
        data = get_data(file=file, sep=sep, encoding=encoding)
    if cols is None:
        cols = columns.columns_analyzer(file=file, sep=sep, encoding=encoding)
    nans_dict = {}
    for a_row in range(data.shape[0]):
        nan_counter = 0
        for a_column in range(len(cols)):
            if pd.isna(data.iloc[a_row, a_column]) is True:
                nan_counter += 1
        if nan_counter > (len(cols)/3):
            nans_dict[a_row] = [pd.to_datetime(str(data.iloc[a_row, 0])).strftime('%d.%m.%y'),
                                pd.to_datetime(str(data.iloc[a_row, 0])).strftime('%H.%M'),
                                round((nan_counter/len(cols))*100, 0)]  # correct percentage
    return nans_dict


#  2.3.1.  Counting the nan_strings to dataframe:
def total_nan_counter_df(source_dict=None,
                         orient='index',
                         cols=None):
    if source_dict is None:
        source_dict = total_nan_counter()
    if cols is None:
        cols = ['Дата', 'Время', '% некорректных замеров']
    return pd.DataFrame.from_dict(source_dict, orient=orient, columns=cols)


#  3.1. Filtering
def data_filter(filter_list,
                cols=None,
                data: pd.core = None,
                file=devices.nkvv.work_file,
                sep=devices.nkvv.work_file_sep,
                encoding=devices.nkvv.work_file_default_encoding):
    if data is None:
        data = get_data(file=file, sep=sep, encoding=encoding)
    if cols is None:
        cols = columns.columns_analyzer(file=file, sep=sep, encoding=encoding)
    filter_list_indexes = []
    for a_column in range(len(cols)):
        for a_param in range(len(cols[0])):
            if cols[a_column][a_param] in filter_list:
                filter_list_indexes.append(a_column)
    filter_list_names = [cols[i][0] for i in filter_list_indexes]
    return data[filter_list_names]


# 4.1. Main averager
def data_average_finder(filter_list=None,
                        abs_parameter=True,
                        unite_parameter=False,
                        round_parameter=3,
                        list_of_non_math=None,
                        cols=None,
                        data: pd.core = None,
                        file=devices.nkvv.work_file,
                        sep=devices.nkvv.work_file_sep,
                        encoding=devices.nkvv.work_file_default_encoding):
    if filter_list is None:
        filter_list = ['time', '∆tg_HV']
    if list_of_non_math is None:
        list_of_non_math = ['Дата создания записи',
                            'Дата сохранения в БД']
    if data is None:
        data = get_data(file=file, sep=sep, encoding=encoding)
    if cols is None:
        cols = columns.columns_analyzer(file=file, sep=sep, encoding=encoding)
    df = data_filter(filter_list, cols=cols, data=data)
    func_columns_list = list(df.columns)
    func_result_prev = []
    func_result = {}
    for i in range(df.shape[1]):
        for k in list_of_non_math:
            if k == func_columns_list[i]:
                break
        else:
            columns_list_of_values = df[func_columns_list[i]].tolist()
            if unite_parameter is False:
                if abs_parameter is True:
                    values_without_nan = [abs(x) for x in columns_list_of_values if not np.isnan(x)]
                else:
                    values_without_nan = [x for x in columns_list_of_values if not np.isnan(x)]
                func_result[func_columns_list[i]] = round(sum(values_without_nan)
                                                          / len(values_without_nan), round_parameter)
            else:
                if abs_parameter is True:
                    dump = [abs(x) for x in columns_list_of_values if not np.isnan(x)]
                else:
                    dump = [x for x in columns_list_of_values if not np.isnan(x)]
                func_result_prev = func_result_prev + dump
                func_result = {'Average: ': round(sum(func_result_prev)
                                                  / len(func_result_prev), round_parameter)}
    return func_result


#  4.2. Search for distributions
def data_distribution_finder(filter_list,
                             unite_parameter=False,
                             cols=None,
                             data: pd.core = None,
                             list_of_non_math=None,
                             file=devices.nkvv.work_file,
                             sep=devices.nkvv.work_file_sep,
                             encoding=devices.nkvv.work_file_default_encoding):
    if data is None:
        data = get_data(file=file, sep=sep, encoding=encoding)
    if cols is None:
        cols = columns.columns_analyzer(file=file, sep=sep, encoding=encoding)
    if list_of_non_math is None:
        list_of_non_math = ['Дата создания записи',
                            'Дата сохранения в БД']
    df = data_filter(filter_list, cols=cols, data=data)
    func_columns_list = list(df.columns)
    func_result_prev = pd.Series([], dtype=pd.StringDtype())
    func_result = {}
    for i in range(df.shape[1]):
        for k in list_of_non_math:
            if k == func_columns_list[i]:
                break
        else:
            if unite_parameter is False:
                func_result[func_columns_list[i]] = data[func_columns_list[i]].value_counts(normalize=True,
                                                                                            sort=True)
            else:  # doesn't work with different amount of indexes*
                dump = data[func_columns_list[i]].value_counts(normalize=True, sort=True)
                func_result_prev = np.c_[func_result_prev, dump]
                func_result['Overall distribution: '] = func_result_prev
    return func_result


#  4.3. Correlations
def data_correlation(filter_list1=None,
                     filter_list2=None,
                     cols=None,
                     data: pd.core = None,  # Unite similar functions
                     file=devices.nkvv.work_file,
                     sep=devices.nkvv.work_file_sep,
                     encoding=devices.nkvv.work_file_default_encoding):
    if data is None:
        data = get_data(file=file, sep=sep, encoding=encoding)
    if cols is None:
        cols = columns.columns_analyzer(file=file, sep=sep, encoding=encoding)
    if filter_list1 is None:
        filter_list1 = ['∆tg_HV']
    if filter_list2 is None:
        filter_list2 = ['∆tg_MV']
    func_result = {}
    df1 = data_filter(filter_list1, cols=cols, data=data)
    df2 = data_filter(filter_list2, cols=cols, data=data)
    shape1 = data_filter(filter_list1, cols=cols, data=data).shape[1]
    shape2 = data_filter(filter_list2, cols=cols, data=data).shape[1]
    df = pd.concat([df1, df2], axis=1)
    for h in range(shape1):
        for g in range(shape2):
            a_values = df[df.columns.values[h]].tolist()
            b_values = df[df.columns.values[g + shape1]].tolist()
            # a_values_without_nan = [x for x in a_values if not np.isnan(x)]
            # NaNs can cause different amount of indexes
            # b_values_without_nan = [x for x in b_values if not np.isnan(x)]
            correlation_integer = 0
            correlation_sequence = []
            for j in range(len(a_values) - 1):
                if np.isnan(a_values[j]) is True or np.isnan(b_values[j]) is True:  # == / is
                    correlation_integer = np.NaN
                elif a_values[j + 1] >= a_values[j] and b_values[j + 1] >= b_values[j]:
                    correlation_integer = correlation_integer + 1
                elif a_values[j + 1] <= a_values[j] and b_values[j + 1] <= b_values[j]:
                    correlation_integer = correlation_integer + 1
                else:
                    correlation_integer = correlation_integer - 1
                correlation_sequence.append(correlation_integer)
            func_result[str(df.columns[h] + ' correlation with ' + df.columns[g + shape1])] = correlation_sequence
    return func_result


#  4.4. Warning Notes
def warning_finder(filter_list=None,
                   warning_amount=1,
                   abs_parameter=True,
                   cols=None,
                   data: pd.core = None,
                   list_of_non_math=None,
                   file=devices.nkvv.work_file,
                   sep=devices.nkvv.work_file_sep,
                   encoding=devices.nkvv.work_file_default_encoding):
    if filter_list is None:
        filter_list = ['time', '∆tgδ_MV']
    if list_of_non_math is None:
        list_of_non_math = ['Дата создания записи', 'Дата сохранения в БД']
    if data is None:
        data = get_data(file=file, sep=sep, encoding=encoding)
    if cols is None:
        cols = columns.columns_analyzer(file=file, sep=sep, encoding=encoding)
    df = data_filter(filter_list, cols=cols, data=data)
    cols_list = list(df.columns)
    date_index = 0
    for k in list_of_non_math:
        for i in range(df.shape[1]):
            if k == cols_list[i]:
                date_index = i
    func_result = []
    for i in range(df.shape[1]):
        for k in list_of_non_math:
            if k == cols_list[i]:
                break
        else:
            df_temp = data_filter(filter_list=[cols_list[date_index], cols_list[i]], data=df)
            if abs_parameter is True:
                df_temp_result = df_temp.loc[(df_temp[cols_list[i]] >= warning_amount) |
                                             (df_temp[cols_list[i]] <= warning_amount * -1)]
            else:
                df_temp_result = df_temp.loc[(df_temp[cols_list[i]] >= warning_amount)]
            func_result.append(df_temp_result)
    return func_result


#  ______ Archive _ Проверка параметра ∆tgδ для технических целей
def delta_tg_checker(cols=None,
                     data: pd.core = None,
                     exclude_values=(-10.0, -300.0),
                     file=devices.nkvv.work_file,
                     sep=devices.nkvv.work_file_sep,
                     encoding=devices.nkvv.work_file_default_encoding):
    if data is None:
        data = get_data(file=file, sep=sep, encoding=encoding)
    if cols is None:
        cols = columns.columns_analyzer(file=file, sep=sep, encoding=encoding)
    df = []
    for column_index in range(len(columns.columns_list_maker(file=file, sep=sep, encoding=encoding))):
        if cols[column_index][4] == '∆tg' and cols[column_index][3] == 'HV':
            df.append(data[cols[column_index][0]].tolist())
    list_of_all_values = list(itertools.chain.from_iterable(df))
    list_of_filtered_values = []
    for value in list_of_all_values:
        if value not in exclude_values:
            list_of_filtered_values.append(value)
    list_of_filtered_abs_values = [abs(x) for x in list_of_filtered_values]  # уточнить по модулю отклонения
    return list_of_filtered_abs_values


#  ______ Archive _ Проверка срабатывания сигнализации срабатывания предупредительной сигнализации (1%)
def delta_tg_checker_warning(operating_data=None,
                             warning=1):
    if operating_data is None:
        operating_data = delta_tg_checker()
    warning_list = []
    for a_value in operating_data:
        if abs(a_value) >= warning:
            warning_list.append(a_value)
    if not warning_list:
        print(f"Превышение уровня ∆tgδ для срабатывания сигнализации не выявлено")  # убрать
        return warning_list
    else:
        return warning_list

