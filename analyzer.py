import datetime
from typing import Union

import numpy as np
import pandas as pd

import columns
import devices
import sadzax


#  ____________ 1. DATA PROCESSING ________________________________________________
#  1.0.0. Importing data
def get_data(device_type: str = 'mon',
             file: str = None,
             sep: str = None,
             encoding: str = None,
             parse_dates: list = None,
             raw_param: bool = False):
    """
    Returns data from work files. 
    There should be at least one suitable uploaded file in the upload directory of the device.
    The selected files are then concatenated to form a single dataframe. 
    The data won't be sorted by the time of measurement.

        Parameters:
        -----------
    :param device_type (str): Type of device for which data is being analyzed.
    :param file (str): Name of the file to be analyzed. If not specified, a suitable file is chosen from the device's upload directory.
    :param sep (str): Delimiter to be used for parsing the file. If not specified, the default delimiter for the device is used.
    :param encoding (str): Encoding to be used for reading the file. If not specified, the default encoding for the device is used.
    :param parse_dates (list): List of column names to be parsed as dates. If not specified, no columns are parsed as dates.
    :param raw_param (bool): Whether to return raw data without any pre-processing. Default is False.

        Returns:
        -----------
    :return pd.DataFrame: A consolidated dataframe containing data from all the selected files.
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
    Stacks data in case of using multiple files for creating an uninterrupted dataflow.

    This function can be used instead of `get_data()` function. There should be at least one suitable uploaded file in the upload directory of the device.
    If only one file is available, that file is picked for analysis.
    If multiple files are available, the function prompts the user to choose the files to be consolidated.
    The selected files are then concatenated to form a single dataframe. The data is sorted by the time of measurement.

        Parameters:
        -----------
    :param device_type (str): Type of device for which data is being analyzed.
    :param file (str): Name of the file to be analyzed. If not specified, a suitable file is chosen from the device's upload directory.
    :param sep (str): Delimiter to be used for parsing the file. If not specified, the default delimiter for the device is used.
    :param encoding (str): Encoding to be used for reading the file. If not specified, the default encoding for the device is used.
    :param parse_dates (list): List of column names to be parsed as dates. If not specified, no columns are parsed as dates.
    :param raw_param (bool): Whether to return raw data without any pre-processing. Default is False.

        Returns:
        -----------
    :return pd.DataFrame: A consolidated dataframe containing data from all the selected files.
    """
    device_type = device_type.lower()
    files_list = devices.links(device_type)[5]
    #  Exclusion for a single work-file
    if len(files_list) == 1:
        print(f"Доступен всего 1 файл для анализа")
        devices.file_pick(device_type, 0)
        data = get_data(device_type, file, sep, encoding, parse_dates, raw_param)
    else:
        data = pd.DataFrame.empty
        w1 = sadzax.Rus.cases(len(files_list), "Доступен", "Доступно", "Доступно")
        w2 = sadzax.Rus.cases(len(files_list), 'файл', 'файла', 'файлов')
        print(f"{w1} {len(files_list)} {w2} для соединения данных: ")
        for i in files_list:
            print(f"Файл № {files_list.index(i) + 1}. {i}")
        try:
            #  Create a list of files for picking a specific file(s)
            inputs = list(map(int, input(f'Введите номера файлов через пробел, которые нужно соединить для общего'
                                         f' анализа (либо введите любой текст для соединения всех): ').split()))
            if len(inputs) == 0:
                inputs = list(range(len(files_list)))  # all
            #  Need to subtract 1 for bringing the 'choice'-ints to indexes
            indexes = [x-1 for x in inputs if x in list(range(len(files_list)))]
        except ValueError:
            indexes = list(range(len(files_list)))  # all files
        for i in indexes:
            devices.file_pick(device_type, i)
            if data is pd.DataFrame.empty:
                #  Exclusion for a first iteration
                data = get_data(device_type, file, sep, encoding, parse_dates, raw_param)
            else:
                #  Store a new iterated data in a temp. variable
                iterated_data = get_data(device_type, file, sep, encoding, parse_dates, raw_param)
                data = pd.concat([data, iterated_data])
    the_time_column = columns.time_column(device_type=device_type, data=data)
    #  Sort data by time of meausure
    data = data.sort_values(by=the_time_column)
    print('Консолидация данных завершена')
    return data


#  1.1. Exclude false measures
def pass_the_nan(device_type: str = 'mon',
                 data: pd.core = None,
                 cols: dict = None,
                 default_dict_for_replacement: dict = None):
    """
    Replaces specified values in a DataFrame with NaN values.

        Parameters:
        -----------
    :param device_type (str): The type of device being analyzed.
    :param data (pd.core): The DataFrame to be processed. If None, it will be obtained using get_data() with the specified device_type.
    :param cols (dict): The dictionary of columns to be analyzed. If None, it will be obtained using columns.columns_analyzer() with the specified device_type.
    :param default_dict_for_replacement (dict): The dictionary containing the values to be replaced with NaN values.
                                                If None, the default value will be obtained using devices.links() with the specified device_type.

        Returns:
        -----------
    :return pd.core: The processed DataFrame with specified values replaced by NaN.
    """
    device_type = device_type.lower()
    if data is None:
        data = get_data(device_type=device_type)
    if cols is None:
        cols = columns.columns_analyzer(device_type=device_type)
    if default_dict_for_replacement is None:
        default_dict_for_replacement = devices.links(device_type)[6]
    for i in range(len(default_dict_for_replacement)):
        #  Seeking_param is an any type string that could be found in cols-dict
        seeking_param = [x for x in default_dict_for_replacement.keys()][i]
        replacing_values = [x for x in default_dict_for_replacement.values()][i]
        for a_column_index in range(len(cols)):
            for a_param_index in range(len(cols[0])):
                #  Conversion of the seeking_param to the original column name
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


#  1.2. Set data types
def set_dtypes(device_type: str = 'mon',
               data: pd.core = None,
               cols: dict = None,
               default_dict_for_dtypes: dict = None):
    """
    Sets the data types for specified columns in a DataFrame.

        Parameters:
        -----------
    :param device_type (str): The type of device being analyzed.
    :param data (pd.core): The DataFrame to be processed. If None, it will be obtained using get_data() with the specified device_type.
    :param cols (dict): The dictionary of columns to be analyzed. If None, it will be obtained using columns.columns_analyzer() with the specified device_type.
    :param default_dict_for_dtypes (dict): The dictionary containing the data types for each column.
                                           If None, the default value will be obtained using devices.links() with the specified device_type.

        Returns:
        -----------
    :return pd.core: The processed DataFrame with specified data types for columns.
    """
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
            #  Seeking_param is an any type string that could be found in cols-dict
            seeking_param = [x for x in default_dict_for_dtypes.keys()][i]
            for a_column_index in range(len(cols)):
                for a_param_index in range(len(cols[0])):
                    #  Conversion of the seeking_param to the original column name
                    if cols[a_column_index][a_param_index] == seeking_param:
                        try:
                            data[cols[a_column_index][0]] = data[cols[a_column_index][0]]\
                                .astype(default_dict_for_dtypes[seeking_param])
                        except Union[ValueError, TypeError]:
                            pass
    return data


#  ____________ 2. BASIC TIME ANALYZING AND SLICING _______________________________
#  2.0.0. Count the strings
def total_counter(device_type: str = 'mon',
                  data: pd.core = None):
    """
    The total_counter function takes a device type and a pandas DataFrame as input
    and returns the total number of logs in the DataFrame. If no DataFrame is provided,
    the function calls the get_data function to obtain one.

        Parameters:
        -----------
    :param device_type (str): a string indicating the type of device from which the logs were obtained.
    :param data (pd.core): a pandas DataFrame containing the logs. Default is None.

        Returns:
        -----------
    :return An integer representing the total number of logs in the DataFrame.
    """
    if data is None:
        data = get_data(device_type=device_type.lower())
    return data.shape[0]


#  2.0.1. Count the periods
def total_periods(device_type: str = 'mon',
                  data: pd.core = None):
    """
    Compute the start and end dates of a time series data, given a device type and a data set.

        Parameters:
        -----------
    :param device_type (str): A string that represents the type of device, by default 'mon'.
    :param data (pandas.core.frame.DataFrame): A pandas DataFrame that contains the time series data, by default None.

        Returns:
        --------
    :return a list containing two pandas Timestamp objects, representing the start and end dates of the time series.
    """
    if data is None:
        data = get_data(device_type=device_type.lower())
    the_time_column = columns.time_column(device_type=device_type, data=data)
    data = data.sort_values(by=the_time_column)
    data = data.reset_index(drop=True)
    data_date_start = pd.to_datetime(data[the_time_column][0])
    data_date_end = pd.to_datetime(data[the_time_column][data.shape[0] - 1])
    return [data_date_start, data_date_end]


#  2.1.0. Analysis of time of measurements
def values_time_analyzer(device_type: str = 'mon',
                         data: pd.core = None,
                         time_sequence_min: int = 1,
                         inaccuracy_sec: int = 3,
                         gap_const_day: int = 1440,
                         gap_const_hour: int = 60,
                         time_column: str = None,
                         exact_gap: bool = True):
    """
    Analyzes the time gaps between consecutive rows in a given time column of a Pandas DataFrame and returns a DataFrame
    with information about any gaps that exceed a specified duration or fall outside a certain range of durations.

        Parameters:
        -----------
    :param device_type : str, default 'mon'
        The type of device for which to retrieve the data.
    :param data : pandas.core.frame.DataFrame, optional
        The DataFrame containing the data to analyze. If None, the data will be retrieved using the `get_data()` function.
    :param time_sequence_min : int, default 1
        The minimum duration (in minutes) that a time sequence should last.
    :param inaccuracy_sec : int, default 3
        The maximum allowed deviation (in seconds) from the expected time sequence duration.
    :param gap_const_day : int, default 1440
        The minimum duration (in minutes) for which to report gaps in the DataFrame, if `exact_gap` is False.
    :param gap_const_hour : int, default 60
        The minimum duration (in minutes) for which to report gaps in the DataFrame, if `exact_gap` is False.
    :param time_column : str, optional
        The name of the time column to analyze. If None, the column will be determined automatically based on the device type and the available columns in the DataFrame.
    :param exact_gap : bool, default True
        Whether to report gaps in the DataFrame with the exact duration or with a duration rounded to the nearest day, hour, or minute, depending on their size.

        Returns:
        --------
    :return pandas.core.frame.DataFrame or None
        A DataFrame with information about any gaps that exceed a specified duration or fall outside a certain range
        of durations, or None if no such gaps were found. The DataFrame contains the following columns:
        - "Строка в БД" (Database row): the index of the row in the DataFrame where the gap starts.
        - "Дата" (Date): the date of the row where the gap starts, in the format 'dd.mm.yy'.
        - "Время" (Time): the time of the row where the gap starts, in the format 'hh.mm'.
        - "Дата след." (Next date): the date of the row where the gap ends, in the format 'dd.mm.yy'.
        - "Время след." (Next time): the time of the row where the gap ends, in the format 'hh.mm'.
        - "Разница" (Duration): the duration of the gap, in minutes or days, depending on its size and the value of
          `exact_gap`.
    """
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
    if len(error_dict) > 0:
        cols_t = ["Строка в БД", "Дата", "Время", "Дата след.", "Время след.", "Разница"]
        return pd.DataFrame.from_dict(error_dict, orient='index', columns=cols_t)
    else:
        return None


#  2.1.1. Slice time of measurements for big gaps
def values_time_slicer(device_type: str = 'mon',
                       data: pd.core = None,
                       time_analyzer: pd.core = None,
                       minutes_slice_mode: int = 1440,
                       min_values_required: int = 300,
                       time_column: str = None,
                       full_param: bool = False):
    """
    Slices the data based on time intervals, and returns a dictionary containing information about sliced data.

        Parameters:
        -----------
    :param device_type (str): A string representing the type of device. Default is 'mon'.
    :param data (pd.core): A Pandas DataFrame containing the data. Default is None.
    :param time_analyzer (pd.core): A Pandas DataFrame containing the analyzed data. Default is None.
    :param minutes_slice_mode (int): An integer representing the number of minutes to slice the data by. Default is 1439.
    :param min_values_required (int): An integer representing the minimum number of values required for the slice to be included in the analysis. Default is 300.
    :param time_column (str): A string representing the name of the column containing the time data. Default is None.
    :param full_param (bool): A boolean representing whether to return the full parameter set. Default is False.

        Returns:
        --------
    :return data_result (dict): A dictionary containing information about the sliced data.
    """
    #  Convert device_type to lowercase
    device_type = device_type.lower()
    if data is None:
        data = get_data(device_type=device_type)
    if time_column is None:
        time_column = columns.time_column(device_type=device_type, data=data)
    #  Initialize empty dictionary to store sliced data
    data_result = {}
    try:
        if time_analyzer is None:
            time_analyzer = values_time_analyzer(device_type=device_type, data=data)
        indexes_for_slicing = [-1]
        for i in range(time_analyzer.shape[0]):
            if time_analyzer.iloc[i, len(time_analyzer.columns) - 1] > datetime.timedelta(minutes=minutes_slice_mode):
                indexes_for_slicing.append(time_analyzer.iloc[i, 0])
        #  Initialize list to store indexes for slicing
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
                str_min = pd.to_datetime(str(data_slices[i][1])).strftime('%d.%m.%Y %H:%M')
                str_max = pd.to_datetime(str(data_slices[i][2])).strftime('%d.%m.%Y %H:%M')
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
    #  In case of not-founding any gaps in measurements
    except AttributeError:
        pass
    return data_result


#  2.2. Selection of the time period
def time_period_choose(data: pd.core = None, device_type: str = 'mon', format: str = None):
    """
    The function time_period_choose is designed to enable a user to select a time period of interest within a given dataset.
    It takes three arguments, data, device_type, and format.    If no data argument is passed, the function calls the get_data function with the device_type argument, to get the dataset of interest.
    If no format argument is passed, the default format of '%d.%m.%Y' is used.
    The function sorts the dataset by the time of measurement and resets the indexes.
    It then calculates the start and end dates of the dataset, prints them, and prompts the user to enter a specific time period of interest.
    If the start and end dates are in the same year, the function prompts the user to enter a specific time period of interest, but within that year, using the "day-month" pair format.
    If the start and end dates are not in the same year, the function prompts the user to enter a time period of interest using the format argument.
    The function checks that the user's input dates are within the available range of dates in the dataset.
    If the user enters an invalid date, the function will prompt the user to enter a valid date.
    If the user enters a start date that is earlier than the first available date, the function will use the first available date as the start date.
    If the user enters an end date that is later than the last available date, the function will use the last available date as the end date.
    If the user enters an end date that is earlier than the start date, the function will switch the start and end dates and add 23 hours, 59 minutes, and 59 seconds to the end date, to ensure that the end date is inclusive.
    Finally, the function returns the start and end dates as pandas Timestamp objects.

        Parameters:
        -----------
    :param data: data is a pandas dataframe containing the dataset of interest,
    :param device_type: device_type specifies the type of device used to collect the data
    :param format: format is a string that represents the format of the date

        Returns:
        --------
    :return pandas.core.frame.DataFrame - A DataFrame as a copy (not a view) of the passed data to the function
    """
    if data is None:
        data = get_data(device_type=device_type)
    if format is None:
        format = '%d.%m.%Y'
    the_time_column = columns.time_column(device_type=device_type, data=data)
    #  Sort data by time of meausure and reset indexes
    data = data.sort_values(by=the_time_column)
    data = data.reset_index(drop=True)
    #  Get the start and the end of whole period
    data_date_start = pd.to_datetime(data[the_time_column][0])
    data_date_end = pd.to_datetime(data[the_time_column][data.shape[0] - 1])
    print(f"Доступен период данных с {data_date_start.strftime(format)} по {data_date_end.strftime(format)}")
    #  Same Year
    if data_date_start.strftime('%Y') == data_date_end.strftime('%Y'):
        print(f'Доступны данные только в рамках {data_date_end.strftime("%Y")} года,'
              f' при задании периодов использовуйте связку "день-месяц"')
        user_start = sadzax.Enter.date(format='%d.%m',
                                       input_descripton=f'Введите дату начала конкретизированного периода: ',
                                       arg_must_be=sadzax.Enter.allowed_symbs_dates,
                                       arg_max_capacity=6,
                                       arg_error=f'Некорректная дата, введите в формате "%d.%m", например, "31.03"',
                                       dayfirst=True,
                                       convert_to_pd=True,
                                       return_timestamp=True,
                                       one_year_status=True,
                                       one_year=data_date_end.strftime("%Y"))
        if user_start < data_date_start:
            print(f"Задана дата начала периода раньше первой доступной даты,"
                  f" началом периода назначена первая доступная дата {data_date_start.strftime(format)}")
            user_start = data_date_start
        user_end = sadzax.Enter.date(format='%d.%m',
                                     input_descripton=f'Введите дату конца конкретизированного периода: ',
                                     arg_must_be=sadzax.Enter.allowed_symbs_dates,
                                     arg_max_capacity=6,
                                     arg_error=f'Некорректная дата, введите в формате "%d.%m", например, "31.03"',
                                     dayfirst=True,
                                     convert_to_pd=True,
                                     return_timestamp=True,
                                     one_year_status=True,
                                     one_year=data_date_end.strftime("%Y"))
        if user_end > data_date_end:
            print(f"Задана дата конца периода позже последней доступной даты,"
                  f" концом периода назначена последня доступная дата {data_date_end.strftime(format)}")
            user_end = data_date_end
    else:
        #  Ask user to enter dates for picking a period
        user_start = sadzax.Enter.date(format=format,
                                       input_descripton=f'Введите дату начала конкретизированного периода: ',
                                       arg_must_be=sadzax.Enter.allowed_symbs_dates,
                                       arg_max_capacity=10,
                                       arg_error=f'Некорректная дата, введите в формате {format}, например, "31.03.22"',
                                       dayfirst=True,
                                       convert_to_pd=True,
                                       return_timestamp=True)
        if user_start < data_date_start:
            print(f"Задана дата начала периода раньше первой доступной даты,"
                  f" началом периода назначена первая доступная дата {data_date_start.strftime(format)}")
            user_start = data_date_start
        user_end = sadzax.Enter.date(format=format,
                                     input_descripton=f'Введите дату конца конкретизированного периода: ',
                                     arg_must_be=sadzax.Enter.allowed_symbs_dates,
                                     arg_max_capacity=10,
                                     arg_error=f'Некорректная дата, введите в формате {format}, например, "31.03.22"',
                                     dayfirst=True,
                                     convert_to_pd=True,
                                     return_timestamp=True)
        if user_end > data_date_end:
            print(f"Задана дата конца периода позже последней доступной даты,"
                  f" концом периода назначена последня доступная дата {data_date_end.strftime(format)}")
            user_end = data_date_end
    if user_end < user_start:
        print(f"Задана дата конца периода, предшествующая дате начала, произведена перемена их местами")
        #  Switch the start and the end with adding 23:59:59 to end date
        temp = user_end
        user_end = user_start + datetime.timedelta(hours=23, minutes=59, seconds=59)
        user_start = temp
    else:
        #  Adding 23:59:59 to end date because the date by default is set to 00.00 time
        user_end = user_end + datetime.timedelta(hours=23, minutes=59, seconds=59)
    data = data[data[the_time_column] >= user_start].iloc[:]
    data = data[data[the_time_column] <= user_end].iloc[:]
    data = data.reset_index(drop=True)
    return data


#  2.3.1. Counting the nan_strings:
def total_nan_counter(device_type='nkvv',
                      data: pd.core = None,
                      false_data_percentage: float = 33.0):
    """
    Analyzes the percentage of NaN values in each row of the input data and returns a DataFrame that shows the time periods where the percentage of NaN values exceeds a specified threshold.

        Parameters:
        -----------
    :param device_type (str, optional): The type of device for which the data is collected. Defaults to 'nkvv'.
    :param data (pandas DataFrame, optional): The input data containing the measurements.
                                              If not specified, the function will use the `get_data()` function to obtain the data for the specified device.
    :param false_data_percentage (float, optional): The threshold percentage above which a row is considered
                                                    as containing false data due to excessive NaN values. Defaults to 33.0.

        Returns:
        -----------
    :return pandas DataFrame: A view of the cleaned input DataFrame that shows the time periods where the percentage of NaN values exceeds the specified threshold.
    The returned DataFrame contains the following columns:
    - 'Время замера' (time_column): The time of measurement for each row.
    - '% сбоя данных в момент замера': The percentage of NaN values in each row.
    - 'Дата': The date of each measurement in the format DD.MM.YY.
    - 'Время': The time of each measurement in the format HH.MM.
    - 'alarm': A Boolean column indicating whether the percentage of NaN values in the row exceeds the specified threshold (True) or not (False).
    """
    #  Set the device & unmutable data
    device_type = device_type.lower()
    if data is None:
        data = get_data(device_type=device_type)
    #  Take time column for analyzing of mass-nan-periods
    time_column = columns.time_column(device_type=device_type, data=data)
    #  Prevent SettingWithCopy
    data2 = data.copy()
    #  Sum of all nan-data of a row out of all columns divided by the shape of the row returns it's 'nan-percentage'
    data2['% сбоя данных в момент замера'] = round((data2.isna().sum(axis=1) / data2.shape[1]) * 100, 0)
    #  Dataframe view cleaned from all other data
    df = data2[[time_column, '% сбоя данных в момент замера']]
    #  Create a column that checks if row contains more than max allowed nans (which we set in 'false_data_percentage')
    df.insert(1, 'alarm', df['% сбоя данных в момент замера'] > false_data_percentage, True)
    #  Forms additional columns with a readable date and time formats
    for k, v in {'Дата': '%d.%m.%y', 'Время': '%H.%M'}.items():
        df.insert(df.shape[1], k, pd.to_datetime(df[df.columns[0]]).apply(lambda x: x.strftime(v)), True)
    #  Returns a view of the cleaned dataframe with only alarms
    return df[df['alarm'] == True].iloc[:, 0:5]
    #  Archive (too heavy)
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


# 2.3.2. Stacking selected false measures in continious periods
def total_nan_counter_ease(df: pd.core, time_sequence_min: int = 1, inaccuracy_sec: int = 3):
    """
    The function total_nan_counter_ease eases the result of the total_nan_counter function by returning the periods of false measurements.
    The function takes a Pandas dataframe out of the total_nan_counter function result as the first argument and returns a dataframe with 3 columns:
    Start of the period, End of the period, and Quantity of false measurements.
    The function has two optional arguments: time_sequence_min, which is the minimum time sequence in minutes, and inaccuracy_sec, which is the inaccuracy in seconds.
    These arguments are used to set the delta check column and to filter the delta check with False value as the borders of periods of false measurements.

        Parameters:
        -----------
    :param df: Pandas dataframe
    :param time_sequence_min: Minimum time sequence in minutes (default=1)
    :param inaccuracy_sec: Inaccuracy in seconds (default=3)

        Returns:
        -----------
    :return: Pandas dataframe with 3 columns: Start of the period, End of the period, and Quantity of false measurements
    """
    #  Take a total_nan_counter func result as a base
    df = df.reset_index(drop=True)
    if df.shape[0] == 0:
        pass
    else:
        #  Insert a subtraction result column and a column that checks for delta set by *args
        df.insert(5, 'delta_sec', df.iloc[:, 0].diff().astype('timedelta64[s]'))
        df.insert(6, 'delta_check', df['delta_sec'] < time_sequence_min*60 + inaccuracy_sec)
        #  Sets 'delta_check' of first row to False as a default start period of false measurements
        df.iloc[0, 6] = False
        #  Filters 'delta_check' with 'False' value as a borders of periods of false measurements
        df_with_only_breakers_ie_start = df[df['delta_check'] == False].iloc[:]
        #  Create a dict for further appending with borders
        ease_dict = {}
        #  Makes a list of indexes of left borders of periods for finding following indexes as right borders
        list_of_breakers_ie_start = [i for i in df_with_only_breakers_ie_start.alarm.index]
        #  Sets the right borders of periods depending on the left border dataframe-index
        for i in range(len(list_of_breakers_ie_start)):
            #  Exclusion for a first left border in a list
            if i == 0:
                left_border = 0
                right_border = list_of_breakers_ie_start[i+1] - 1
            else:
                left_border = list_of_breakers_ie_start[i]
                #  Exclusion for a last right border in a list
                if (i+1) == len(list_of_breakers_ie_start):
                    right_border = (df.shape[0] - 1)
                else:
                    #  Main branch for all other left borders
                    right_border = list_of_breakers_ie_start[i+1] - 1
                #  Forms a dictionary
            ease_dict[list_of_breakers_ie_start[i]] = [
                list_of_breakers_ie_start[i],
                df[df.columns[3]][df[df.columns[3]].index[left_border]],
                df[df.columns[4]][df[df.columns[4]].index[left_border]],
                df[df.columns[3]][df[df.columns[3]].index[right_border]],
                df[df.columns[4]][df[df.columns[4]].index[right_border]],
                right_border - left_border + 1
            ]
        cols_t = ["Строка в БД", "Дата начала замеров", "Время начала",
                  "Дата окончания замеров", "Время окончания", "Количество некорректных замеров"]
        #  Creates a dataframe out of the dictionary
        return pd.DataFrame.from_dict(ease_dict, orient='index', columns=cols_t)


#  3.1. Filtering
def data_filter(filter_list: list,
                device_type: str = 'nkvv',
                data: pd.core = None,
                cols: dict = None):
    """
    Filter a Pandas DataFrame by a list of column names.

        Parameters:
        -----------
    :param filter_list (list): A list of strings representing the names of the columns to filter.
    :param device_type (str): A string representing the device type to fetch data from (default 'nkvv').
    :param data (pd.core.frame.DataFrame): A Pandas DataFrame to filter (default None).
    :param cols (dict): A dictionary of column names and their positions (default None).

        Returns:
        -----------
    :return pd.core.frame.DataFrame: A new Pandas DataFrame that only contains the columns that match the filter list.
    """
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
                        device_type: str = 'mon',
                        data: pd.core = None,
                        cols: dict = None,
                        abs_parameter: bool = True,
                        unite_parameter: bool = False,
                        round_parameter: int = 3,
                        list_of_non_math: list = None):
    """
    This function filters and calculates the average value of a specified list of columns in a given dataset.
    It returns a dictionary with column names as keys and their corresponding average value as values.

        Parameters:
        -----------
    :param filter_list (list): A list of column names to filter and calculate average values from (default ['∆tg_MV'])
    :param device_type (str): A string representing the device type to get data for (default 'mon')
    :param data (pd.core): A pandas dataframe containing the data to filter and calculate averages from (default None)
    :param cols (dict): A dictionary containing information about the columns of the dataset (default None)
    :param abs_parameter (bool): A boolean indicating whether or not to calculate averages using absolute values (default True)
    :param unite_parameter (bool): A boolean indicating whether or not to unite all filtered columns and calculate average value for them together (default False)
    :param round_parameter (int): An integer representing the number of decimal places to round the calculated average values (default 3)
    :param list_of_non_math (list): A list of strings representing prefixes of column names to exclude from calculations (default None)

        Returns:
        -----------
    :return dict: A dictionary with column names as keys and their corresponding average value as values
    """
    device_type = device_type.lower()
    if data is None:
        data = get_data(device_type=device_type)
    if cols is None:
        cols = columns.columns_analyzer(device_type=device_type)
    if list_of_non_math is None:
        list_of_non_math = devices.links(device_type)[4]
    if filter_list is None:
        filter_list = ['∆tg_MV']
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
                             device_type: str = 'mon',
                             data: pd.core = None,
                             cols: dict = None,
                             unite_parameter: bool = False,
                             list_of_non_math: list = None):
    """
    Analyzes the distribution of values in the specified columns of the data.

        Parameters:
        -----------
    :param filter_list (list): A list of column names to be analyzed.
    :param device_type (str): The device type of the data. Defaults to 'mon'.
    :param data (pandas.core.frame.DataFrame): The data to be analyzed. If None, the data will be obtained with the 'get_data' function using the specified device_type.
    :param cols (dict): A dictionary with information about the columns of the data.
                        If None, the information will be obtained with the 'columns_analyzer' function using the specified device_type.
    :param unite_parameter (bool): A flag indicating whether the distribution of all specified columns should be combined into one result. Defaults to False.
                                   If True, the result will be a DataFrame with the combined distributions.
                                   If False, the result will be a dictionary with a distribution for each column.
    :param list_of_non_math (list): A list of strings that are prefixes of column names that should be excluded from the analysis. Defaults to None.

        Returns:
        -----------
    :return A dictionary with the distribution of values in the specified columns of the data.
            If unite_parameter is False, the dictionary will have a distribution for each specified column.
            If unite_parameter is True, the dictionary will have a single key 'Overall distribution: ' and the value will be a DataFrame with the combined distribution.
    """
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
def data_correlation(filter_list1: list = None,
                     filter_list2: list = None,
                     device_type: str = 'nkvv',
                     data: pd.core = None,
                     cols: dict = None):
    """
    Calculates the correlation between columns of two filtered dataframes and returns a dictionary
    with the correlation parameters as keys and the corresponding sequence of correlation values as values.

        Parameters:
        -----------
    :param filter_list1 : list, optional
        A list of filters to be applied to the data columns for the first dataframe.
    :param filter_list2 : list, optional
        A list of filters to be applied to the data columns for the second dataframe.
    :param device_type : str, optional
        A string specifying the device type. Default is 'nkvv'.
    :param data : pandas.core.frame.DataFrame, optional
        A pandas dataframe. Default is None.
    :param cols : dict, optional
        A dictionary of the device's column names. Default is None.

        Returns:
        --------
    :return A dictionary containing the correlation parameters as keys and the corresponding sequence of correlation values as values.

        Notes:
        ------
    100% strict correlation is a "x=y"-type of graph with ~45 dgrs. angle.
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


#  4.4.0. Warning Notes
def warning_finder(filter_list: list = None,
                   device_type: str = 'nkvv',
                   data: pd.core = None,
                   cols: dict = None,
                   warning_param_war: float = 1.0,
                   warning_param_acc: float = 1.5,
                   abs_parameter: bool = True,
                   list_of_non_math: list = None):
    """
    Finds time intervals when certain parameters exceed specified warning or accident threshold values.

        Parameters:
        -----------
    :param filter_list (list, optional): List of column names to filter data by. If None, defaults to ['time', '∆tg_HV'].
    :param device_type (str, optional): Type of device to get data for. Defaults to 'nkvv'.
    :param data (pd.core, optional): Dataframe to use for analysis. If None, loads data using get_data() function.
    :param cols (dict, optional): Dictionary of column names to use for filtering data. If None, analyzes column names using columns_analyzer() function.
    :param warning_param_war (float, optional): Warning parameter value for warning type events. Defaults to 1.0.
    :param warning_param_acc (float, optional): Warning parameter value for accident type events. Defaults to 1.5.
    :param abs_parameter (bool, optional): If True, uses absolute value of warning parameter to detect events. Defaults to True.
    :param list_of_non_math (list, optional): List of non-mathematical column names. If None, loads from devices.links() function for the specified device type.

    Returns:
    -----------
    :return dict: Dictionary of dataframes, where keys are column names and values are lists of two dataframes. 
                  The first dataframe contains time intervals when the parameter exceeds the warning threshold, 
                  and the second dataframe contains time intervals when the parameter exceeds the accident threshold. 
                  The time intervals are stored in the 'time' column of the dataframes.
    """
    device_type = device_type.lower()
    if list_of_non_math is None:
        list_of_non_math = devices.links(device_type)[4]
    if data is None:
        data = get_data(device_type=device_type)
    if cols is None:
        cols = columns.columns_analyzer(device_type=device_type)
    if filter_list is None:
        filter_list = ['time', '∆tg_HV']
    else:
        if isinstance(filter_list, list) is False:
            filter_list = [filter_list]
        if 'time' in filter_list:
            pass
        else:
            filter_list.append('time')
    #  Form main DataFrame for work: warning params + time column
    df = data_filter(filter_list=filter_list, cols=cols, data=data)
    df = df.reset_index(drop=True)
    cols_list = list(df.columns)
    #  Default datetime column
    datetime_index = 0
    for i in range(df.shape[1]):
        if cols_list[i].startswith(list_of_non_math[0]) is True:
            datetime_index = i
    func_result = {}
    #  Iterating columns
    for a_column_index in range(df.shape[1]):
        if a_column_index == datetime_index:
            func_result['datetime'] = []
            df_temp_result = data_filter(filter_list=[cols_list[datetime_index]], data=df, cols=cols)
            func_result['datetime'].append(df_temp_result)
            func_result['datetime'].append(df_temp_result)
            del df_temp_result
        else:
            #  Temporal dataframe for a warnings/accidents storage
            df_t = data_filter(filter_list=[cols_list[datetime_index], cols_list[a_column_index]], data=df, cols=cols)
            func_result[cols_list[a_column_index]] = []
            for warning_amount in [warning_param_war, warning_param_acc]:
                if abs_parameter is True:
                    df_temp_result = df_t.loc[(df_t[cols_list[a_column_index]] >= warning_amount) |
                                              (df_t[cols_list[a_column_index]] <= warning_amount * -1)]
                else:
                    df_temp_result = df_t.loc[(df_t[cols_list[a_column_index]] >= warning_amount)]
                func_result[cols_list[a_column_index]].append(df_temp_result)
                del df_temp_result
            del df_t
    return func_result


#  4.4.1. Warning Notes - Merging
def warning_finder_merge(log: dict,
                         device_type: str = 'mon',
                         data: pd.core = None,
                         warn_type: str = 'acc',
                         warning_param_war: float = 1.0,
                         warning_param_acc: float = 1.5):
    """
    Merges the dataframes in the input dictionary `log` and adds columns for warning parameters based on the given `warn_type` and threshold values.
    Returns the resulting merged dataframe.

        Parameters:
        -----------
    :param log : dict
        A dictionary containing a set of dataframes.
    :param device_type : str, optional
        A string indicating the type of device used for measurements. Default is 'mon'.
    :param data : pd.core, optional
        A pandas dataframe of data. Default is None.
    :param warn_type : str, optional
        A string indicating the type of warning, either 'warning' or 'war' for a warning signal or 'accident' or 'acc' for an accident signal. Default is 'acc'.
    :param warning_param_war : float, optional
        A float value indicating the warning threshold for a warning signal. Default is 1.0.
    :param warning_param_acc : float, optional
        A float value indicating the warning threshold for an accident signal. Default is 1.5.

        Returns:
        --------
    :return df : pd.core
        A pandas dataframe of merged dataframes with added columns for warning parameters based on the given `warn_type` and threshold values.
    """
    if data is None:
        data = get_data(device_type=device_type)
    datetime_name = columns.time_column(device_type=device_type, data=data)
    #  Create main dataframe for merging
    df = log['datetime'][0]
    log_list_i = 0
    warn_str = 'предупредительный'
    warning_param = warning_param_war
    if warn_type == 'warning' or warn_type == 'war':
        log_list_i = 0
        warn_str = 'предупредительный'
        warning_param = warning_param_war
    elif warn_type == 'accident' or warn_type == 'acc':
        warning_param = warning_param_acc
        warn_str = 'аварийный'
        log_list_i = 1
    for key in log:
        #  dict-Key 'datetime' is for uninterrupted whole-time measurer for plotting and should be passed here
        if key == 'datetime':
            pass
        else:
            if log[key][0].shape[0] == 0:
                pass
            else:
                df_temp = log[key][log_list_i]
                df = pd.merge(df, df_temp, how='left', on=datetime_name)
    df.insert(df.shape[1], str(warn_str + ' отриц.'), warning_param)
    df.insert(df.shape[1], str(warn_str + ' полож.'), warning_param * -1)
    return df


#  4.4.2. Warning Notes - Merge - Ease
def warning_finder_ease(log: dict,
                        device_type: str = 'mon',
                        warn_type: str = 'accident',
                        warning_param_war: float = 1.0,
                        warning_param_acc: float = 1.5,
                        min_values_for_print: int = 5,
                        time_sequence_min: int = 1,
                        inaccuracy_sec: int = 3):
    """
    The warning_finder_ease function takes in a dictionary log and several optional arguments to filter and process
    the data in log in order to identify warning or accident events (in a row)
    It returns a Pandas DataFrame summarizing the identified events.

        Parameters:
        -----------
    :param log (dict): A dictionary containing measurements of different parameters, including a datetime column. The data is expected to be in the form of a Pandas DataFrame.
    :param device_type (str, default='mon'): A string indicating the type of device used to make the measurements.
    :param warn_type (str, default='accident'): A string indicating the type of warning to be identified.
                                                Possible values are 'accident' or 'acc' for accident warnings, and 'warning' or 'war' for warning alerts.
    :param warning_param_war (float, default=1.0): A float representing the warning threshold for the specified warning type, as a percentage of the maximum value for the relevant parameter.
    :param warning_param_acc (float, default=1.5): A float representing the accident threshold for the specified warning type, as a percentage of the maximum value for the relevant parameter.
    :param min_values_for_print (int, default=5): An integer representing the minimum number of consecutive warning measurements required to be included in the output DataFrame.
    :param time_sequence_min (int, default=1): An integer representing the minimum time in minutes between consecutive measurements for them to be considered as part of the same warning event.
    :param inaccuracy_sec (int, default=3): An integer representing the maximum difference in seconds allowed between
                                            consecutive measurements for them to be considered as part of the same warning event.

        Returns:
        -----------
    :return A Pandas DataFrame summarizing the identified warning or accident events, including the parameter name,
            start and end times, and the number of consecutive measurements that were part of the same event.
            If no events were identified, a string is returned instead.
    """
    #  warning_finder func. returns two dataframes for every key-measurer, ind.0 = warnings, ind.1 = accident
    log_list_i = 0
    warn_str = 'предупредительная'
    warning_param = warning_param_war
    if warn_type == 'warning' or warn_type == 'war':
        log_list_i = 0
        warn_str = 'предупредительная'
        warning_param = warning_param_war
    elif warn_type == 'accident' or warn_type == 'acc':
        warning_param = warning_param_acc
        warn_str = 'аварийная'
        log_list_i = 1
    #  Create a dict for further appending with border
    ease_dict = {}
    for key in log:
        #  dict-Key 'datetime' is for uninterrupted whole-time measurer for plotting and should be passed here
        if key == 'datetime':
            pass
        else:
            if log[key][int(log_list_i)].shape[0] == 0:
                pass
            else:
                df = log[key][int(log_list_i)]
                df = df.reset_index(drop=True)
                datetime_index = 0
                for i in range(df.shape[1]):
                    if list(df.columns)[i].startswith(devices.links(device_type)[4][0]) is True:
                        datetime_index = i
                if df.shape[0] == 0:
                    pass
                else:
                    #  Insert a subtraction result column and a column that checks for delta set by *args
                    df.insert(2, 'delta_sec', df.iloc[:, datetime_index].diff().astype('timedelta64[s]'))
                    df.insert(3, 'delta_check', df['delta_sec'].dt.seconds < time_sequence_min * 60 + inaccuracy_sec)
                    #  Sets 'delta_check' of first row to False as a default start period of false measurements
                    df.iloc[0, 3] = False
                    #  Filters 'delta_check' with 'False' value as a borders of periods of false measurements
                    df_with_only_breakers_ie_start = df[df['delta_check'] == False].iloc[:]
                    #  Makes a list of indexes of left borders of periods for finding following indexes as right borders
                    list_of_breakers_ie_start = [i for i in df_with_only_breakers_ie_start.delta_check.index]
                    #  Sets the right borders of periods depending on the left border dataframe-index
                    for i in range(len(list_of_breakers_ie_start)):
                        #  Exclusion for a first left border in a list
                        if i == 0:
                            left_border = 0
                            #  Exclusion for a single-period
                            if len(list_of_breakers_ie_start) == 1:
                                right_border = (df.shape[0] - 1)
                            else:
                                right_border = list_of_breakers_ie_start[i + 1] - 1
                        else:
                            left_border = list_of_breakers_ie_start[i]
                            #  Exclusion for a last right border in a list
                            if (i + 1) == len(list_of_breakers_ie_start):
                                right_border = (df.shape[0] - 1)
                            else:
                                #  Main branch for all other left borders
                                right_border = list_of_breakers_ie_start[i + 1] - 1
                            #  Forms a dictionary
                        ease_dict[key + ' _ ' + str(list_of_breakers_ie_start[i])] = [
                            key + ' ' + warn_str + ' (' + str(warning_param) + '%)',
                            df[df.columns[datetime_index]][df[df.columns[datetime_index]].index[left_border]],
                            df[df.columns[datetime_index]][df[df.columns[datetime_index]].index[right_border]],
                            right_border - left_border + 1
                        ]
    ease_dict_trimmed = {k: v for k, v in ease_dict.items() if v[3] >= min_values_for_print}
    cols_t = ["Показатель", "Начало", "Окончание", "Количество непрерывных сигнальных замеров"]
    #  Creates a dataframe out of the dictionary
    if len(ease_dict_trimmed) > 0:
        return pd.DataFrame.from_dict(ease_dict_trimmed, orient='index', columns=cols_t)
    else:
        return str(f'Периоды непрерывной сигнализации (минимум {min_values_for_print} подряд) не выявлены')
