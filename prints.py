import pandas as pd
import io
import sys
import analyzer
import devices
import plots
import sadzax
import frontend


def info(the_string):
    print(f'\n          {the_string}\r')


def device_picking():
    error = 'Пожалуйста, введите корректное значение: цифру, соответствующую пункту из списка'
    print('\nДоступны следующие устройства для анализа: \n')
    for obj in devices.objs:
        print(f"{devices.objs.index(obj) + 1}. {obj.full_name} ({obj.name})")
    while True:
        try:
            choice = int(input('\nВыберите № устройства: '))
            if choice <= 0 or choice > len(devices.objs):
                print(error)
                continue
            print(f'\nВыбрано устройство: \n"{devices.objs[choice - 1].full_name}"\n'
                  f'Системный код устройства - "{devices.objs[choice - 1].name}"')
            return devices.objs[choice - 1].name
        except:
            print(error)
            continue


def file_picking(device_type='kiv'):
    error = 'Пожалуйста, введите корректное значение: цифру, соответствующую пункту из списка'
    files_list = devices.links(device_type)[5]
    w1 = sadzax.Rus.cases(len(files_list), "Доступен", "Доступно", "Доступно")
    w2 = sadzax.Rus.cases(len(files_list), 'файл', 'файла', 'файлов')
    print(f"{w1} {len(files_list)} {w2} для анализа: ")
    for i in files_list:
        print(f"Файл № {files_list.index(i) + 1}. {i}")
    if len(files_list) == 1:
        print(f"Данный файл выбран для анализа")
        return devices.file_pick(device_type, 0)
    elif len(files_list) > 1:
        while True:
            try:
                choice = int(input('Выберите № файла: '))
                if choice <= 0 or choice > len(files_list):
                    print(error)
                    continue
                print(f"Выбран файл № {choice} - {files_list[choice - 1]}")
                return devices.file_pick(device_type, choice - 1)
            except:
                print(error)
                continue


def total_log_counter(device_type, data):
    info('Подсчёт общего количества записей')
    log_total = analyzer.total_log_counter(device_type=device_type, data=data)
    print(f'Общее число записей в журнале измерений составило {log_total}')


def values_time_analyzer(device_type, data, log: pd.core = None):
    info('Анализ периодичности и неразрывности измерений')
    if log is None:
        log = analyzer.values_time_analyzer(device_type=device_type, data=data)
    if log.shape[0] == 0:
        print(f'Периоды измерений не нарушены')
    else:
        print(f'Выявлено {log.shape[0]} нарушений периодов измерений')
        print(sadzax.question('Хотите вывести подробные данные?', yes=log, no=''))


def values_time_slicer(device_type, data, log: dict = None):
    info('Выбор неразрывного периода для анализа')
    if log is None:
        log = analyzer.values_time_slicer(device_type=device_type, data=data)
    error = 'Пожалуйста, введите корректное значение: цифру, соответствующую пункту из списка срезов'
    w1 = sadzax.Rus.cases(len(log), 'найден', 'найдены', 'найдены')
    w2 = sadzax.Rus.cases(len(log), 'срез', 'среза', 'срезов')
    print(f"По заданным параметрам {w1} {len(log)} {w2} данных")
    k = [i for i in log.keys()]
    for i in log:
        print(f"Срез данных № {k.index(i)+1}. " + log[i][4])
    if len(log) < 1:
        print(f"Ошибка источника периодов")
        return data
    elif len(log) == 1:
        print(f"Срез данных принят к анализу")
        return log[0][0]
    elif len(log) > 1:
        try:
            inputs = sadzax.Enter.mapped_ints('Введите срезы для анализа'
                                              ' (либо введите любой текст для анализа всех срезов): ')
            outputs = [x for x in k if k.index(x) in inputs]
        except:
            outputs = k
        if len(outputs) < 1:
            outputs = k
        print(f"\nВыбранные срезы данных:")
        df = pd.DataFrame.empty
        for choice in outputs:
            print(f"№ {k.index(choice)+1}. " + log[choice][4])
            iterated_data = log[choice][0]
            if df is pd.DataFrame.empty:
                df = iterated_data
            else:
                df = pd.concat([df, iterated_data])
            del iterated_data
        return df


def total_nan_counter(device_type, data, false_data_percentage: float = 33.0, log: pd.core = None):
    info('Анализ периодов массовой некорректности измерений')
    if log is None:
        log = analyzer.total_nan_counter(device_type=device_type, data=data,
                                         false_data_percentage=false_data_percentage)
    w1 = sadzax.Rus.cases(log.shape[0], "Выявлен", "Выявлено", "Выявлено")
    w2 = sadzax.Rus.cases(log.shape[0], "замер", "замера", "замеров")
    if log.shape[0] == 0:
        print(f"\n Периоды некорректных измерений не выявлены")
    else:
        print(f"\n {w1} {log.shape[0]} {w2} с некорректными данными (там, где"
              f" за один замер зафиксировано более {false_data_percentage}% некорректных данных)")
        print(f"Замеры с некорректными данными составили {round((log.shape[0] / data.shape[0]) * 100, 1)}%"
              f" от общего числа произведённых замеров")
        print(sadzax.question('Хотите вывести примеры некорректных данных?', yes=log, no=''))


def average_printer(ex, data, cols, abs_parameter=True):
    print(f'Средние значения по {ex}: \r')
    df_average = analyzer.data_average_finder(filter_list=[ex], data=data, cols=cols, abs_parameter=abs_parameter)
    if abs_parameter is True:
        str_adder = 'по модулю '
    else:
        str_adder = ''
    for every_value in df_average:
        print(f'Среднее {str_adder}по {every_value} составило {df_average[every_value]}')


def warning_printer(device_type: str = 'mon',
                    log: dict = None,
                    warn_type: str = 'accident',
                    filter_list=None,
                    data: pd.core = None,
                    cols: dict = None,
                    warning_param_war: float = None,
                    warning_param_acc: float = None,
                    abs_parameter: bool = True):
    log_list_i = 0
    if warn_type == 'warning' or warn_type == 'war':
        warning_param = warning_param_war
        warn_str = 'предупредительной'
    elif warn_type == 'accident' or warn_type == 'acc':
        warning_param = warning_param_acc
        warn_str = 'аварийной'
        log_list_i = 1
    if log is None:
        log = analyzer.warning_finder(filter_list=filter_list,
                                      device_type=device_type,
                                      data=data,
                                      cols=cols,
                                      warning_param_war=warning_param_war,
                                      warning_param_acc=warning_param_acc,
                                      abs_parameter=abs_parameter)
    for key in log:
        if key == 'datetime':
            pass
        else:
            num = log[key][log_list_i].shape[0]
            if num == 0:
                print(f"По {key}: срабатывания {warn_str} (±{warning_param}%) сигнализации не выявлены\n")
            else:
                print(
                    f"По {key}: выявлено {num} {sadzax.Rus.cases(num, 'срабатывание', 'срабатывания', 'срабатываний')} "
                    f"{warn_str} (±{warning_param}%) сигнализации."
                    f"\n Процент срабатывания {round((num / log['datetime'][log_list_i].shape[0]) * 100, 3)}%"
                    f" (от общего числа замеров)\n"
                )


def print_flat_graph(input_x=None, input_y=None, device_type='kiv', data=None, cols=None, title=None):
    info(title)
    plots.flat_graph(input_x=input_x, input_y=input_y, device_type=device_type, data=data, cols=cols, title=title)


def print_scatter(input_x=None, input_y=None, device_type='mon', data=None, cols=None, title=None):
    info(title)
    plots.scatter(input_x=input_x, input_y=input_y, device_type=device_type, data=data, cols=cols, title=title)
