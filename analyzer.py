import datetime

import numpy as np
import pandas as pd

import columns
import devices
import sadzax


#  ____________ 1. DATA PROCESSING ________________________________________________

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
    print(f'Начало обработки файла "{file}"')
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
                    data[a_column] = pd.to_datetime(data[a_column], format='%d.%m.%Y %H:%M:%S')
                    data = data.sort_values(by=a_column)
    print('Обработка файла окончена')
    return data


#  1.0.1. Importing Data with stacking
def stack_data(device_type: str = 'mon',
               file: str = None,
               sep: str = None,
               encoding: str = None,
               parse_dates: list = None,
               raw_param: bool = False):
    """
    For a custom file usage you need to set all additional params
    """
    device_type = device_type.lower()
    files_list = devices.links(device_type)[5]
    if len(files_list) == 1:
        print(f"Доступен всего 1 файл для анализа")
        devices.file_pick(device_type, 0)
        data = get_data(device_type=device_type)
    else:
        data = pd.DataFrame.empty
        w1 = sadzax.Rus.cases(len(files_list), "Доступен", "Доступно", "Доступно")
        w2 = sadzax.Rus.cases(len(files_list), 'файл', 'файла', 'файлов')
        print(f"{w1} {len(files_list)} {w2} для соединения данных: ")
        for i in files_list:
            print(f"Файл № {files_list.index(i) + 1}. {i}")
        try:
            inputs = list(map(int, input(f'Введите номера файлов через пробел, которые нужно соединить для общего'
                                         f' анализа (либо введите любой текст для соединения всех): ').split()))
            if len(inputs) == 0:
                inputs = list(range(len(files_list)))  # all
            indexes = [x-1 for x in inputs if x in list(range(len(files_list)))]
        except ValueError:
            indexes = list(range(len(files_list)))  # all files
        for i in indexes:
            devices.file_pick(device_type, i)
            if data is pd.DataFrame.empty:
                data = get_data(device_type, file, sep, encoding, parse_dates, raw_param)
            else:
                iterated_data = get_data(device_type, file, sep, encoding, parse_dates, raw_param)
                data = pd.concat([data, iterated_data])
    the_time_column = columns.time_column(device_type)
    data = data.sort_values(by=the_time_column)
    print('Консолидация данных завершена')
    return data


#  1.1. Exclude false measures
def pass_the_nan(device_type: str = 'nkvv',
                 data: pd.core = None,
                 cols: dict = None,
                 default_dict_for_replacement: dict = None,
                 default_dict_for_dtypes: dict = None):
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
                        try:
                            arr[arr == every_replacing_value] = np.NaN
                        except ValueError:
                            pass
                    data[cols[a_column_index][0]] = arr
    return data


def set_dtypes(device_type: str = 'mon',
               data: pd.core = None,
               cols: dict = None,
               default_dict_for_dtypes: dict = None):
    device_type = device_type.lower()
    if data is None:
        data = get_data(device_type=device_type)
    if cols is None:
        cols = columns.columns_analyzer(device_type=device_type)
    if default_dict_for_dtypes is None:
        default_dict_for_dtypes = devices.links(device_type)[8]
    if default_dict_for_dtypes is None:
        pass
    else:
        for i in range(len(default_dict_for_dtypes)):
            seeking_param = [x for x in default_dict_for_dtypes.keys()][i]
            for a_column_index in range(len(cols)):
                for a_param_index in range(len(cols[0])):
                    if cols[a_column_index][a_param_index] == seeking_param:
                        try:
                            data[cols[a_column_index][0]] = data[cols[a_column_index][0]]\
                                .astype(default_dict_for_dtypes[seeking_param])
                        except ValueError | TypeError:
                            pass
    return data


#  ____________ 1. BASIC TIME ANALYZING AND SLICING _______________________________

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
                         time_column: str = None,
                         exact_gap: bool = True):
    device_type = device_type.lower()
    if data is None:
        data = get_data(device_type=device_type)
    if time_column is None:
        time_column = columns.time_column(device_type=device_type, data=data)
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
    cols_t = ["Строка в БД", "Дата", "Время", "Дата след.", "Время след.", "Разница"]
    return pd.DataFrame.from_dict(error_dict, orient='index', columns=cols_t)


#  2.2.1. Slice time of measurements for big gaps
def values_time_slicer(device_type: str = 'kiv',
                       data: pd.core = None,
                       time_analyzer: pd.core = None,
                       minutes_slice_mode: int = 1439,
                       min_values_required: int = 300,
                       time_column: str = None,
                       full_param: bool = False):
    device_type = device_type.lower()
    if data is None:
        data = get_data(device_type=device_type)
    if time_column is None:
        time_column = columns.time_column(device_type=device_type, data=data)
    data_result = {}
    if time_analyzer is None:
        time_analyzer = values_time_analyzer(device_type=device_type, data=data)
    indexes_for_slicing = [-1]
    for i in range(time_analyzer.shape[0]):
        if time_analyzer.iloc[i, len(time_analyzer.columns) - 1] > datetime.timedelta(minutes=minutes_slice_mode):
            indexes_for_slicing.append(time_analyzer.iloc[i, 0])
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


#  2.3. Counting the nan_strings:
def total_nan_counter(device_type='nkvv',
                      data: pd.core = None,
                      false_data_percentage: float = 33.0):
    device_type = device_type.lower()
    if data is None:
        data = get_data(device_type=device_type)
    time_column = columns.time_column(device_type=device_type, data=data)
    data['% сбоя данных в момент замера'] = round((data.isna().sum(axis=1) / data.shape[1]) * 100, 0)
    df = data[[time_column, '% сбоя данных в момент замера']]
    df.insert(1, 'alarm', df['% сбоя данных в момент замера'] > false_data_percentage, True)
    for k, v in {'Дата': '%d.%m.%y', 'Время': '%H.%M'}.items():
        df.insert(df.shape[1], k, pd.to_datetime(df['Дата и время']).apply(lambda x: x.strftime(v)), True)
    return df[df['alarm'] == True].iloc[:, 2:5]
    # time_index = 0
    # for i in range(len(cols)):
    #     if cols[i][0] == time_column:
    #         time_index = i
    # for a_row in range(data.shape[0]):
    #     nan_counter = 0
    #     for a_column in range(len(cols)):
    #         if pd.isna(data.iloc[a_row, a_column]) is True:
    #             nan_counter += 1
    #     if nan_counter > (len(cols)*(false_data_percentage/100)):
    #         nans_dict[a_row] = [pd.to_datetime(str(data.iloc[a_row, time_index])).strftime('%d.%m.%y'),
    #                             pd.to_datetime(str(data.iloc[a_row, time_index])).strftime('%H.%M'),
    #                             round((nan_counter/len(cols))*100, 0)]  # correct percentage
    # cols_out = ['Дата', 'Время', '% сбоя данных в момент замера']
    # return pd.DataFrame.from_dict(nans_dict, orient='index', columns=cols_out)


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
