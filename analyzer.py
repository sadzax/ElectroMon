import datetime

import numpy as np
import pandas as pd

import columns
import devices
import prints
import sadzax


#  1.0. Importing data
def get_data(device_type: str = 'kiv',
             file: str = None,
             sep: str = None,
             encoding: str = None,
             parse_dates: list = None,
             raw_param: bool = False):
    """
    For a custom file usage you need to set all additional params
    Need to switch to classes of devices
    """
    data = pd.DataFrame.empty
    device_type = device_type.lower()
    if file is None:
        file, sep, encoding, parse_dates = devices.links(device_type)[1:5]
    if device_type == 'nkvv':
        data = pd.read_csv(file,
                           sep=sep,
                           encoding=encoding,
                           parse_dates=parse_dates,
                           dayfirst=True)
    elif device_type == 'kiv':
        data_raw = pd.read_excel(file)
        if data_raw.columns[0] == ' № ' or raw_param is True:
            data = data_raw
        else:
            for i in range(data_raw.shape[0]):
                if data_raw.iloc[i, 0] != ' № ':
                    pass
                else:
                    data = data_raw.iloc[i+1:].copy()
                    data.columns = list(data_raw.iloc[i])
                    del data_raw
                    # noinspection PyUnreachableCode
                    break
        for an_element_of_parse_dates in parse_dates:
            for a_column in list(data.columns):
                if a_column.startswith(an_element_of_parse_dates):
                    # 'SettingWithCopyWarning' - A value is trying to be set on a copy of a slice from a DataFrame
                    pd.options.mode.chained_assignment = 'raise'
                    # Check mask @ https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
                    # data[a_column] = pd.to_datetime(data[a_column], format='%Y/%m/%d %H:%M:%S')
                    data[a_column] = pd.to_datetime(data[a_column])
                    data = data.sort_values(by=a_column)
                else:
                    try:
                        data[a_column] = data[a_column].astype(float)
                    except ValueError:
                        pass
    elif device_type == 'mon':
        data = pd.read_csv(file,
                           low_memory=False,
                           delimiter=sep,
                           encoding=encoding)
        conc = devices.links(device_type)[7]
        data[parse_dates[0]] = (data[conc[0]] + ' ' + data[conc[1]])
        for an_element_of_parse_dates in parse_dates:
            for a_column in list(data.columns):
                if a_column.startswith(an_element_of_parse_dates):
                    # 'SettingWithCopyWarning' - A value is trying to be set on a copy of a slice from a DataFrame
                    pd.options.mode.chained_assignment = 'raise'
                    # Check mask @ https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
                    # data[a_column] = pd.to_datetime(data[a_column], format='%Y/%m/%d %H:%M:%S')
                    data[a_column] = pd.to_datetime(data[a_column], format='%d.%m.%Y %H:%M:%S')
                    data = data.sort_values(by=a_column)
    return data


def stack_data(device_type: str = 'mon', method: str = 'all'):  # !!! DBGING
    error = 'Пожалуйста, введите корректное значение: цифру, соответствующую пункту из списка'
    files_list = devices.links(device_type)[5]
    if method == "all":
        devices.file_pick(device_type, 0)
        data = analyzer.get_data(device_type=device_type)
        for i in range(len(files_list)):
            devices.file_pick(device_type, i)
            iterated_data = analyzer.get_data(device_type=device_type)
            data = pd.concat([data, iterated_data])


#  2.0. Count the strings
def total_log_counter(device_type: str = 'nkvv',
                      data: pd.core = None):
    if data is None:
        data = get_data(device_type=device_type.lower())
    return data.shape[0]


#  2.1. Analysis of time of measurements
def values_time_analyzer(device_type: str = 'nkvv',
                         data: pd.core = None,
                         time_sequence_min: int = 1,
                         inaccuracy_sec: int = 3,
                         gap_const_day: int = 1440,
                         gap_const_hour: int = 60,
                         exact_gap: bool = True):
    device_type = device_type.lower()
    if data is None:
        data = get_data(device_type=device_type)
    parse_dates = devices.links(device_type)[4]
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
def values_time_analyzer_df(source_dict: dict = None,
                            orient='index',
                            cols: dict = None):
    if source_dict is None:
        source_dict = values_time_analyzer()
    if cols is None:
        cols = ["Строка в БД", "Дата", "Время", "Дата след.", "Время след.", "Разница"]
    return pd.DataFrame.from_dict(source_dict, orient=orient, columns=cols)


#  2.1.2. Slice time of measurements for big differences
def values_time_slicer(device_type: str = 'nkvv',
                       data: pd.core = None,
                       minutes_slice_mode: int = 1439,
                       min_values_required: int = 300,
                       full_param: bool = False):
    device_type = device_type.lower()
    if data is None:
        data = get_data(device_type=device_type)
    data_result = {}
    time_column = columns.time_column(device_type=device_type, data=data)
    time_analyzer_df = values_time_analyzer_df(source_dict=values_time_analyzer(device_type=device_type, data=data))
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
    if full_param is False:
        for i in data_slices.keys():
            if data_slices[i][3] >= min_values_required:
                data_result[i] = data_slices[i]
    else:
        data_result = data_slices
    return data_result


#  2.1.2.1. Choose one of the slices of time of measurements
def values_time_slicer_choose(sliced_dict=None, device_type: str = 'kiv'):
    if sliced_dict is None:
        sliced_dict = values_time_slicer(device_type=device_type)
    error = 'Пожалуйста, введите корректное значение: цифру, соответствующую пункту из списка срезов'
    l = len(sliced_dict)
    w = sadzax.Rus.cases(l, 'срез', 'среза', 'срезов')
    print(f"По заданным параметрам найдено {l} {w} данных")
    k = [i for i in sliced_dict.keys()]
    for i in sliced_dict:
        print(f"Срез данных № {k.index(i)+1}. " + sliced_dict[i][4])
    while True:
        try:
            choice = int(input('Введите срез для анализа: '))
            if choice <= 0 or choice > len(k):
                print(error)
                continue
            print(f"Вы выбрали срез данных № {choice}. " + sliced_dict[k[choice - 1]][4])
            return sliced_dict[k[choice - 1]][0]
        except:
            print(error)
            continue


#  2.2. Exclude (Ia(r) = -300, Tg = -10) to NaN  ______ ADD EXCLUSIONS LISTS!
def pass_the_nan(device_type: str = 'nkvv',
                 data: pd.core = None,
                 cols: dict = None,
                 default_dict_for_replacement: dict = None):
    device_type = device_type.lower()
    if data is None:
        data = get_data(device_type=device_type)
    if cols is None:
        cols = columns.columns_analyzer(device_type=device_type)
    if default_dict_for_replacement is None:
        default_dict_for_replacement = devices.links(device_type)[6]
    for i in range(len(default_dict_for_replacement)):
        seeking_param = [x for x in default_dict_for_replacement.keys()][i]
        replacing_values = [x for x in default_dict_for_replacement.values()][i]
        for a_column_index in range(len(cols)):
            for a_param_index in range(len(cols[0])):
                if cols[a_column_index][a_param_index] == seeking_param:
                    arr = data[cols[a_column_index][0]]
                    arr = np.array(arr)
                    if isinstance(replacing_values, list) is False:
                        replacing_values = list(replacing_values)
                    for every_replacing_value in replacing_values:
                        arr[arr == every_replacing_value] = np.NaN
                    data[cols[a_column_index][0]] = arr
    return data


#  2.3. Counting the nan_strings:
def total_nan_counter(device_type='nkvv',
                      data: pd.core = None,
                      cols: dict = None,
                      false_data_percentage: float = 30.0):
    device_type = device_type.lower()
    if data is None:
        data = get_data(device_type=device_type)
    if cols is None:
        cols = columns.columns_analyzer(device_type=device_type)
    nans_dict = {}
    time_column = columns.time_column(device_type=device_type, data=data)
    time_index = 0
    for i in range(len(cols)):
        if cols[i][0] == time_column:
            time_index = i
    for a_row in range(data.shape[0]):
        nan_counter = 0
        for a_column in range(len(cols)):
            if pd.isna(data.iloc[a_row, a_column]) is True:
                nan_counter += 1
        if nan_counter > (len(cols)*(false_data_percentage/100)):
            nans_dict[a_row] = [pd.to_datetime(str(data.iloc[a_row, time_index])).strftime('%d.%m.%y'),
                                pd.to_datetime(str(data.iloc[a_row, time_index])).strftime('%H.%M'),
                                round((nan_counter/len(cols))*100, 0)]  # correct percentage
    return nans_dict


#  2.3.1.  Counting the nan_strings to dataframe:
def total_nan_counter_df(source_dict: dict = None,
                         cols: list = None,
                         orient: str = 'index'):
    if source_dict is None:
        source_dict = total_nan_counter()
    if cols is None:
        cols = ['Дата', 'Время', '% некорректных данных (из общего числа считываемых) в момент замера']
    return pd.DataFrame.from_dict(source_dict, orient=orient, columns=cols)


#  3.1. Filtering
def data_filter(filter_list: list,
                device_type: str = 'nkvv',
                data: pd.core = None,
                cols: dict = None):
    device_type = device_type.lower()
    if data is None:
        data = get_data(device_type=device_type)
    if cols is None:
        cols = columns.columns_analyzer(device_type=device_type)
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
def data_average_finder(filter_list: list = None,
                        device_type: str = 'nkvv',
                        data: pd.core = None,
                        cols: dict = None,
                        abs_parameter: bool = True,
                        unite_parameter: bool = False,
                        round_parameter: int = 3,
                        list_of_non_math: list = None):
    device_type = device_type.lower()
    if data is None:
        data = get_data(device_type=device_type)
    if cols is None:
        cols = columns.columns_analyzer(device_type=device_type)
    if list_of_non_math is None:
        list_of_non_math = devices.links(device_type)[4]
    if filter_list is None:
        filter_list = ['∆tg_MV']
    # else:
    #     df = data_filter(filter_list, cols=cols, data=data)
    #     func_columns_list = list(df.columns)
    #     for k in list_of_non_math:
    #         for i in range(df.shape[1]):
    #             if func_columns_list[i].startswith(k) is True:
    #                 break
    #     else:
    #         filter_list.append('time')
    df = data_filter(filter_list, cols=cols, data=data)
    func_columns_list = list(df.columns)
    func_result_prev = []
    func_result = {}
    for i in range(df.shape[1]):
        for k in list_of_non_math:
            if func_columns_list[i].startswith(k) is True:
                break
        else:  # For-Else - ?
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
def data_distribution_finder(filter_list: list,
                             device_type: str = 'nkvv',
                             data: pd.core = None,
                             cols: dict = None,
                             unite_parameter: bool = False,
                             list_of_non_math: list = None):
    device_type = device_type.lower()
    if data is None:
        data = get_data(device_type=device_type)
    if cols is None:
        cols = columns.columns_analyzer(device_type=device_type)
    if list_of_non_math is None:
        list_of_non_math = devices.links(device_type)[4]
    df = data_filter(filter_list, cols=cols, data=data)
    func_columns_list = list(df.columns)
    func_result_prev = pd.Series([], dtype=pd.StringDtype())
    func_result = {}
    for i in range(df.shape[1]):
        for k in list_of_non_math:
            if func_columns_list[i].startswith(k) is True:
                break
        else:  # For-Else - ?
            if unite_parameter is False:
                func_result[func_columns_list[i]] = data[func_columns_list[i]].value_counts(normalize=True,
                                                                                            sort=True)
            else:  # doesn't work with different amount of indexes*
                dump = data[func_columns_list[i]].value_counts(normalize=True, sort=True)
                func_result_prev = np.c_[func_result_prev, dump]
                func_result['Overall distribution: '] = func_result_prev
    return func_result


#  4.3. Correlations
def data_correlation(filter_list1: list = None,
                     filter_list2: list = None,
                     device_type: str = 'nkvv',
                     data: pd.core = None,
                     cols: dict = None):
    """
    Returns dictionary of { Corr.Params : [ Sequence of correlation]  }
    100% strict correlation is a x=y type of a graph
    """
    device_type = device_type.lower()
    if data is None:
        data = get_data(device_type=device_type)
    if cols is None:
        cols = columns.columns_analyzer(device_type=device_type)
    if filter_list1 is None:
        filter_list1 = ['∆tg_HV']
    if filter_list2 is None:
        filter_list2 = ['∆tg_MV']
    func_result = {}
    df1 = data_filter(filter_list1, cols=cols, data=data)
    df2 = data_filter(filter_list2, cols=cols, data=data)
    df = pd.concat([df1, df2], axis=1)
    for h in range(df1.shape[1]):
        for g in range(df2.shape[1]):
            a_values = df[df.columns.values[h]].tolist()
            b_values = df[df.columns.values[g + df1.shape[1]]].tolist()
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
            func_result[str(df.columns[h] + ' correlation with ' + df.columns[g + df1.shape[1]])] = correlation_sequence
    return func_result


#  4.4. Warning Notes
def warning_finder(filter_list: list = None,
                   device_type: str = 'nkvv',
                   data: pd.core = None,
                   cols: dict = None,
                   warning_amount: float = 1.0,
                   abs_parameter: bool = True,
                   list_of_non_math: list = None):
    """
    Need to put a 'time' in filter_list
    """
    device_type = device_type.lower()
    if data is None:
        data = get_data(device_type=device_type)
    if cols is None:
        cols = columns.columns_analyzer(device_type=device_type)
    if filter_list is None:
        filter_list = ['time', '∆tgδ_MV']
    if list_of_non_math is None:
        list_of_non_math = devices.links(device_type)[4]
    df = data_filter(filter_list=filter_list, cols=cols, data=data)
    cols_list = list(df.columns)
    date_index = 0
    for i in range(df.shape[1]):
        for k in list_of_non_math:
            if cols_list[i].startswith(k) is True:
                date_index = i
    func_result = []
    for i in range(df.shape[1]):
        if i == date_index:
            pass
        else:
            df_temp = data_filter(filter_list=[cols_list[date_index], cols_list[i]], data=df, cols=cols)
            # arr = df_temp[cols_list[i]]
            # arr = np.array(arr)
            # arr[arr >= warning_amount]
            if abs_parameter is True:
                df_temp_result = df_temp.loc[(df_temp[cols_list[i]] >= warning_amount) |
                                             (df_temp[cols_list[i]] <= warning_amount * -1)]
            else:
                df_temp_result = df_temp.loc[(df_temp[cols_list[i]] >= warning_amount)]
            func_result.append(df_temp_result)
    return func_result
