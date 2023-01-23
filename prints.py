import pandas as pd
import analyzer
import columns
import devices
import plots
import sadzax


def clearing_script():
    import sys
    import warnings
    warnings.simplefilter(action='ignore', category=FutureWarning)
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')


clearing_script()


def info(the_string):
    print(f'\n\n          {the_string}...\r')


def answering(question, yes='', no='', answer_list=None):
    answer = input(f'  {question}  ')
    if answer_list is None:
        answer_list = {'yes': ['yes', 'ye', 'yeah', 'ok', 'y', 'да', 'ага', 'ок', 'хорошо', 'давай', 'го', 'д', 'lf'],
                       'no': ['no', 'nope', 'nah', 'n', 'нет', 'не', 'не надо', 'н', 'не-а', 'yt', 'ytn']}
    for answer_example in answer_list['yes']:
        if answer == answer_example:
            return yes
    for answer_example in answer_list['no']:
        if answer == answer_example:
            return no


def work_file_picking(device_type='kiv'):
    error = 'Пожалуйста, введите корректное значение: цифру, соответствующую пункту из списка'
    files_list = devices.work_file_listing(device_type)
    l = len(files_list)
    w1 = sadzax.Rus.cases(l, "Доступен", "Доступно", "Доступно")
    w2 = sadzax.Rus.cases(l, 'файл', 'файла', 'файлов')
    print(f"{w1} {l} {w2} для анализа: ")
    for i in files_list:
        print(f"Файл № {files_list.index(i) + 1}. {i}")
    if l == 1:
        print(f"Данный файл выбран для анализа")
        return devices.work_file_picking(device_type)
    elif l > 1:
        while True:
            try:
                choice = int(input('Выберите № файла: '))
                if choice <= 0 or choice > l:
                    print(error)
                    continue
                print(f"Выбран файл {files_list[choice-1]}")
                return devices.work_file_picking(device_type, choice-1)
            except:
                print(error)
                continue


def total_log_counter(device_type, data):
    info('Подсчёт общего количества записей')
    log_total = analyzer.total_log_counter(device_type=device_type, data=data)
    print(f'Общее число записей в журнале измерений составило {log_total}')


def values_time_analyzer_df(data, device_type):
    info('Анализ периодичности и неразрывности измерений')
    log_time = analyzer.values_time_analyzer(data=data, device_type=device_type)
    log_time_df = analyzer.values_time_analyzer_df(source_dict=log_time, orient='index')
    if len(log_time) == 0:
        print(f'Периоды измерений не нарушены')
    else:
        print(f'Выявлено {len(log_time)} нарушений периодов измерений')
        print(answering('Хотите вывести подробные данные?', yes=log_time_df, no=''))
