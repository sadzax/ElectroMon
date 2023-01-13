import warnings

import pandas as pd

import analyzer
import columns
import plots

warnings.simplefilter(action='ignore', category=FutureWarning)

cols = columns.columns_analyzer()
print('Чтение и обработка файла...')
# database = analyzer.pass_the_nan(None, cols)  # it's faster to use pickle below
# database.to_pickle('main_dataframe.pkl')
database = pd.read_pickle('main_dataframe.pkl')
data = database


def info_print(the_string):
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


def saving_pkl(dataframe: pd.core, name_file):
    save_path = '/save/' + name_file + '.pkl'
    dataframe.to_pickle(save_path)
    

def average_printer(ex, abs_parameter=True):
    print(f'Среднее значение по {ex}: \r')
    df_average = analyzer.data_average_finder(filter_list=[ex], abs_parameter=abs_parameter)
    if abs_parameter is True:
        str_adder = 'по модулю '
    else:
        str_adder = ''
    for every_value in df_average:
        print(f'Среднее {str_adder}по {every_value} составило {df_average[every_value]}')
    print(f'Распределение значений {ex} (гистограмма): \r')
    plots.histogram([ex], data=database, title=f'Распределение значений {ex} (гистограмма):')


def warning_printer(filter_list_append, warning_param1=1.0, warning_param2=1.5, warn_type='accident',
                    abs_parameter=True, data=database):
    filter_list = ['time']
    for x in filter_list_append:
        filter_list.append(x)
    if warn_type == 'accident':
        warning_param = warning_param2
        warn_str = 'аварийной'
    elif warn_type == 'warning':
        warning_param = warning_param1
        warn_str = 'предупредительной'
    log_warn = analyzer.warning_finder(filter_list=filter_list, abs_parameter=abs_parameter, data=data,
                                       warning_amount=warning_param)
    for every_df in log_warn:
        if every_df.empty is True:
            print(f'Превышение уровней {every_df.axes[1].values[1]} '
                  f'для срабатывания {warn_str} (±{warning_param}) сигнализации не выявлено')
        else:
            print(f'Выявлено превышений (±{warning_param}): {every_df.shape[0]} '
                  f'уровней {every_df.axes[1].values[1]} для срабатывания {warn_str} сигнализации. '
                  f'\n Процент срабатывания {round((every_df.shape[0] / log_total) * 100, 3)}%')
            print(answering('Вывести список?', every_df))


def print_flat_graph(title, input_y, data):
    info_print(title)
    plots.flat_graph(title=title, input_y=input_y, data=data)


#  ______________________________________ COMMON ______________________________________

info_print('Подсчёт общего количества записей')
log_total = analyzer.total_log_counter(data=database)
print(f'Общее число записей в журнале измерений составило {log_total}')

info_print('Анализ периодичности и неразрывности измерений')
log_time = analyzer.values_time_analyzer(data=database)
log_time_df = analyzer.values_time_analyzer_df(source_dict=log_time, orient='index')
if len(log_time) == 0:
    print(f'Периоды измерений НКВВ не нарушены')
else:
    print(f'Выявлено {len(log_time)} нарушений периодов измерений НКВВ')
    print(answering('Хотите вывести подробные данные?', yes=log_time_df, no=''))

info_print('Анализ периодов массовой некорректности измерений')
log_nans = analyzer.total_nan_counter(data=database, cols=cols)
log_nans_df = analyzer.total_nan_counter_df(source_dict=log_nans, orient='index')
if len(log_nans) == 0:
    print(f"\n Периоды некорректных измерений не выявлены")
else:
    print(f"\n Выявлено {len(log_nans)} замеров с некорректными данными НКВВ")
    print(answering('Хотите вывести примеры некорректных данных?', yes=log_nans_df, no=''))


#  ______________________________________ HIGH VOLTAGE ______________________________________

info_print('Анализ трендов стороны ВН')

ex1 = '∆tg_HV'
ex2 = '∆C_HV'
print(f'Анализ корреляции данных {ex1}, {ex2} от температуры воздуха (при корреляции изменения на графике синхронны)')
plots.correlation_plot(filter_list1=[ex1, ex2], filter_list2=['tair'])

average_printer(ex1)

average_printer(ex2)

info_print('Анализ сигнализации со стороны ВН')
w1 = 1.0
w2 = 1.5
print(f'\nПревышение уровней {ex1} для срабатывания предупредительной (±{w1}) или аварийной (±{w2}) сигнализации: \r')
status = answering('Вывести только срабатывания аварийной сигнализации?', yes='y', no='n')
if status == 'y':
    warning_printer([ex1], w1, w2, 'accident')
elif status == 'n':
    warning_printer([ex1], w1, w2, 'warning')
    warning_printer([ex1], w1, w2, 'accident')

w1 = 3.0
w2 = 4.5
print(f'\nПревышение уровней {ex2} для срабатывания предупредительной (±{w1}) или аварийной (±{w2}) сигнализации: \r')
status = answering('Вывести только срабатывания аварийной сигнализации?', yes='y', no='n')
if status == 'y':
    warning_printer([ex2], w1, w2, 'accident', abs_parameter=True)
elif status == 'n':
    warning_printer([ex2], w1, w2, 'warning', abs_parameter=True)
    warning_printer([ex2], w1, w2, 'accident', abs_parameter=True)

hv1 = 'Графики изменения значений напряжений в фазах А, В и С стороны ВН-220кВ'
print_flat_graph(input_y=['U_HV'], data=database, title=hv1)

hv2 = 'Графики изменения активной составляющей токов утечек высоковольтных вводов фаз А, В и С стороны ВН-220кВ'
print_flat_graph(input_y=['Ia_HV'], data=database, title=hv2)

hv3 = 'Графики изменения реактивной составляющей токов утечек высоковольтных вводов фаз А, В и С стороны ВН-220кВ'
print_flat_graph(input_y=['Ir_HV'], data=database, title=hv3)

hv4 = 'Графики изменения значений tgδ высоковольтных вводов фаз А, В и С стороны ВН-220кВ'
print_flat_graph(input_y=['tg_HV'], data=database, title=hv4)

hv5 = 'Графики изменения значений емкостей С1 высоковольтных вводов фаз А, В и С стороны ВН-220кВ'
print_flat_graph(input_y=['C_HV'], data=database, title=hv5)

hv6 = 'Графики изменения значений ∆tgδ (изменение tgδ относительно начальных значений) высоковольтных вводов' \
      ' фаз А, В и С стороны ВН-220кВ'
print_flat_graph(input_y=['∆tg_HV'], data=database, title=hv6)

hv7 = 'Графики изменения значений ∆C/C1 (изменение емкостей С1 относительно начальных значений) высоковольтных вводов' \
      ' фаз А, В и С стороны ВН-220кВ'
print_flat_graph(input_y=['∆C_HV'], data=database, title=hv7)


#  ______________________________________ MIDDLE VOLTAGE ___________________________________________

info_print('Анализ трендов стороны СН')

ex3 = '∆tg_MV'
ex4 = '∆C_MV'
print(f'Анализ корреляции данных {ex3}, {ex4} от температуры воздуха (при корреляции изменения на графике синхронны)')
plots.correlation_plot(filter_list1=[ex3, ex4], filter_list2=['tair'])

average_printer(ex3)

average_printer(ex4)

info_print('Анализ сигнализации со стороны ВН')
w1 = 1.0
w2 = 1.5
print(f'\nПревышение уровней {ex3} для срабатывания предупредительной (±{w1}) или аварийной (±{w2}) сигнализации: \r')
status = answering('Вывести только срабатывания аварийной сигнализации?', yes='y', no='n')
if status == 'y':
    warning_printer([ex3], w1, w2, 'accident')
elif status == 'n':
    warning_printer([ex3], w1, w2, 'warning')
    warning_printer([ex3], w1, w2, 'accident')

w1 = 3.0
w2 = 4.5
print(f'\nПревышение уровней {ex4} для срабатывания предупредительной (±{w1}) или аварийной (±{w2}) сигнализации: \r')
status = answering('Вывести только срабатывания аварийной сигнализации?', yes='y', no='n')
if status == 'y':
    warning_printer([ex4], w1, w2, 'accident', abs_parameter=True)
elif status == 'n':
    warning_printer([ex4], w1, w2, 'warning', abs_parameter=True)
    warning_printer([ex4], w1, w2, 'accident', abs_parameter=True)

mv1 = 'Графики изменения значений напряжений в фазах А, В и С стороны СН-110кВ'
print_flat_graph(input_y=['U_MV'], data=database, title=mv1)

mv2 = 'Графики изменения активной составляющей токов утечек высоковольтных вводов фаз А, В и С стороны СН-110кВ'
print_flat_graph(input_y=['Ia_MV'], data=database, title=mv2)

mv3 = 'Графики изменения реактивной составляющей токов утечек высоковольтных вводов фаз А, В и С стороны СН-110кВ'
print_flat_graph(input_y=['Ir_MV'], data=database, title=mv3)

mv4 = 'Графики изменения значений tgδ высоковольтных вводов фаз А, В и С стороны СН-110кВ'
print_flat_graph(input_y=['tg_MV'], data=database, title=mv4)

mv5 = 'Графики изменения значений емкостей С1 высоковольтных вводов фаз А, В и С стороны СН-110кВ'
print_flat_graph(input_y=['C_MV'], data=database, title=mv5)

mv6 = 'Графики изменения значений ∆tgδ (изменение tgδ относительно начальных значений) высоковольтных вводов' \
      ' фаз А, В и С стороны СН-110кВ'
print_flat_graph(input_y=['∆tg_MV'], data=database, title=mv6)

mv7 = 'Графики изменения значений ∆C/C1 (изменение емкостей С1 относительно начальных значений) высоковольтных вводов' \
      ' фаз А, В и С стороны СН-110кВ'
print_flat_graph(input_y=['∆C_MV'], data=database, title=mv7)