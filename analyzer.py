import itertools
import datetime

import numpy as np
import pandas as pd


import columns
import devices


#  1.0. Importing data
def get_data(device_type='nkvv',
             file=None,
             sep=None,
             encoding=None,
             parse_dates=None,
             raw_param=False):
    """
    For a custom file usage you need to set all additional params
    """
    data = pd.DataFrame.empty
    if file is None:
        file, sep, encoding, parse_dates = devices.links(device_type.lower())[1:]
    if device_type.lower() == 'nkvv':
        data = pd.read_csv(file,
                           sep=sep,
                           encoding=encoding,
                           parse_dates=parse_dates,
                           dayfirst=True)
    if device_type.lower() == 'kiv':
        data_raw = pd.read_excel(file)
        if data_raw.columns[0] == ' № ' or raw_param is True:
            data = data_raw
        else:
            for i in range(data_raw.shape[0]):
                if data_raw.iloc[i, 0] != ' № ':
                    pass
                else:
                    data = data_raw.iloc[i+1:]
                    data.columns = list(data_raw.iloc[i])
                    # noinspection PyUnreachableCode
                    break
        for an_element_of_parse_dates in parse_dates:
            for a_column in list(data.columns):
                if a_column.startswith(an_element_of_parse_dates):
                    # 'SettingWithCopyWarning' - A value is trying to be set on a copy of a slice from a DataFrame
                    pd.options.mode.chained_assignment = None
                    # Check mask @ https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
                    # data[a_column] = pd.to_datetime(data[a_column], format='%Y/%m/%d %H:%M:%S')
                    data[a_column] = pd.to_datetime(data[a_column])
                    data = data.sort_values(by=a_column)
    return data


#  2.0. Count the strings
def total_log_counter(device_type='nkvv',
                      data: pd.core = None):
    if data is None:
        data = get_data(device_type=device_type.lower())
    return data.shape[0]


#  2.1. Analysis of time of measurements
def values_time_analyzer(device_type='nkvv',
                         time_sequence_min=1,
                         inaccuracy_sec=3,
                         data: pd.core = None,
                         gap_const_day=1440,
                         gap_const_hour=60,
                         exact_gap=True):
    if data is None:
        data = get_data(device_type=device_type.lower())
    parse_dates = devices.links(device_type.lower())[4]
    time_column = list(data.columns)[0]
    for an_element_of_parse_dates in parse_dates:
        for a_column in list(data.columns):
            if a_column.startswith(an_element_of_parse_dates):
                time_column = a_column
        break
    df = data[time_column].values
    error_dict = {}
    for a_row in range(df.shape[0] - 1):
        delta_time = (df[a_row + 1] - df[a_row]).astype('timedelta64[s]')
        if delta_time > (time_sequence_min*60 + inaccuracy_sec) \
                or delta_time < (time_sequence_min*60 - inaccuracy_sec):
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
            error_dict[a_row + 1] = [a_row,
                                     pd.to_datetime(str(df[a_row])).strftime('%d.%m.%y'),
                                     pd.to_datetime(str(df[a_row])).strftime('%H.%M'),
                                     pd.to_datetime(str(df[a_row + 1])).strftime('%d.%m.%y'),
                                     pd.to_datetime(str(df[a_row + 1])).strftime('%H.%M'),
                                     err]
    return error_dict


#  2.1.1. Analysis time of measurements to dataframe
def values_time_analyzer_df(source_dict=None,
                            orient='index',
                            cols=None):
    if source_dict is None:
        source_dict = values_time_analyzer()
    if cols is None:
        cols = ["Строка в БД", "Дата", "Время", "Дата след.", "Время след.", "Разница"]
    return pd.DataFrame.from_dict(source_dict, orient=orient, columns=cols)


#  2.1.2. Slice time of measurements for big differences
def values_time_slicer(data=None,
                       minutes_slice_mode=1439,
                       min_values_required=300,
                       device_type='nkvv'):
    if data is None:
        data = get_data(device_type=device_type.lower())
    parse_dates = devices.links(device_type.lower())[4]
    time_column = list(data.columns)[0]
    for an_element_of_parse_dates in parse_dates:
        for a_column in list(data.columns):
            if a_column.startswith(an_element_of_parse_dates):
                time_column = a_column
        break
    time_analyzer_df = values_time_analyzer_df(source_dict=values_time_analyzer(device_type=device_type.lower(),
                                                                                data=data))
    indexes_for_slicing = [-1]
    for i in range(time_analyzer_df.shape[0]):
        if time_analyzer_df.iloc[i, len(time_analyzer_df.columns)-1] > datetime.timedelta(minutes=minutes_slice_mode):
            indexes_for_slicing.append(time_analyzer_df.iloc[i, 0])
    indexes_for_slicing.append(int(data.shape[0]))
    data_slices_list = []
    for k in range(len(indexes_for_slicing)-1):
        data_slices_list.append(data.iloc[indexes_for_slicing[k]+1:indexes_for_slicing[k+1]])
    data_slices = {k: [v] for k, v in enumerate(data_slices_list)}
    for i in range(len(data_slices)):
        time_array = data_slices[i][0][time_column].values
        if data_slices[i][0].shape[0] > 0:
            data_slices[i].append(min(time_array))
            data_slices[i].append(max(time_array))
        else:
            data_slices[i].append(np.datetime64('NaT'))
            data_slices[i].append(np.datetime64('NaT'))
        data_slices[i].append(data_slices[i][0].shape[0])
    #  Questioning about necessity of cycle-end to save appended elements in dictionary list
    for i in range(len(data_slices)):
        if data_slices[i][0].shape[0] > min_values_required:
            str_min = pd.to_datetime(str(data_slices[i][1])).strftime('%d.%m.%y %H:%M')
            str_max = pd.to_datetime(str(data_slices[i][2])).strftime('%d.%m.%y %H:%M')
            str_quantity = data_slices[i][3]
            data_slices[i].append(f'Всего {str_quantity} записей с {str_min} по {str_max}')
        else:
            data_slices[i].append(f'Не включается в анализ')


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
def data_filter(filter_list: list,
                cols: dict = None,
                data: pd.core = None,
                device_type='nkvv',  # Work on
                file=devices.nkvv.work_file,
                sep=devices.nkvv.work_file_sep,
                encoding=devices.nkvv.work_file_default_encoding):
    if data is None:
        data = get_data(file=file, sep=sep, encoding=encoding)
    if cols is None:
        cols = columns.columns_analyzer(file=file, sep=sep, encoding=encoding)
    else:
        cols_by_data = {k: [v] for v, k in enumerate(data.columns)}
        if len(cols_by_data) > len(cols):
            # Allows to filter already trimmed data
            cols = {k: [v] for k, v in cols.items() if cols[k][0] in list(cols_by_data.values())}
    filter_list_keys = []
    for a_column in list(cols.keys()):
        for a_param in range(len(cols[0])):
            if cols[a_column][a_param] in filter_list:
                filter_list_keys.append(a_column)
    filter_list_names = [cols[i][0] for i in filter_list_keys]
    # Prevent trying to add new columns to already trimmed data:
    filter_list_names = [name for name in filter_list_names if name in list(data.columns)]
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

