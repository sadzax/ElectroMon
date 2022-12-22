import pandas as pd
import analyzer
import columns
import plots
import devices
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

cols = columns.columns_analyzer()
# database = analyzer.pass_the_nan(None, cols)  # it's faster to use pickle below
# database.to_pickle('main_dataframe.pkl')
database = pd.read_pickle('main_dataframe.pkl')
data = database


def info_print(the_string):
    print(f"\n\n          {the_string}...\r")


def answering(question, yes='', no='', answer_list=None):
    answer = input(f"  {question}  ")
    if answer_list is None:
        answer_list = {'yes': ['yes', 'ye', 'yeah', 'ok', 'y', 'да', 'ага', 'ок', 'хорошо', 'давай', 'го', 'д', 'lf'],
                       'no': ['no', 'nope', 'nah', 'n', 'нет', 'не', 'не надо', 'н', 'не-а', 'yt', 'ytn']}
    for answer_example in answer_list['yes']:
        if answer == answer_example:
            print(yes)
    for answer_example in answer_list['no']:
        if answer == answer_example:
            print(no)


info_print('Подсчёт общего количества записей')
log_total = analyzer.total_log_counter(data=database)
print(f"Общее число записей в журнале измерений составило {log_total}")


info_print('Анализ периодичности и неразрывности измерений')
log_time = analyzer.values_time_analyzer(data=database)
log_time_df = analyzer.values_time_analyzer_df(source_dict=log_time, orient='index')
if len(log_time) == 0:
    print(f"Периоды измерений НКВВ не нарушены")
else:
    print(f"Выявлено {len(log_time)} нарушений периодов измерений НКВВ")
    answering('Хотите вывести подробные данные?', yes=log_time_df, no='')


# info_print('Анализ периодов массовой некорректности измерений')
# log_nans = analyzer.total_nan_counter(data=database, cols=cols)
# log_nans_df = analyzer.total_nan_counter_df(source_dict=log_nans, orient='index')
# if len(log_nans) == 0:
#     print(f"\n Периоды некорректных измерений не выявлены")
# else:
#     print(f"\n Выявлено {len(log_nans)} замеров с некорректными данными НКВВ")
#     answering('Хотите вывести примеры некорректных данных?', yes=log_nans_df, no='')


info_print('Анализ трендов стороны ВН')
ex1 = '∆tgδ_HV'
ex2 = '∆C_HV'
print(f'Анализ корреляции данных {ex1}, {ex2} от температуры воздуха (при корреляции изменения на графике синхронны)')
log_trends_HV_3_1 = plots.correlation_plot(filter_list1=[ex1, ex2], filter_list2=['tair'])
print(f"Среднее значение по {ex1}: \r")
log_trends_HV_3_2 = analyzer.data_average_finder(filter_list=[ex1], abs_parameter=True)
for i in log_trends_HV_3_2:
    print(f"Среднее по {i} составило {log_trends_HV_3_2[i]}")
print(f"Распределение значений {ex1} (гистограмма): \r")
plots.histogram([ex1], data=database, data_distribution_parameter=False)


info_print('Анализ сигнализации со стороны ВН')
w1 = 1.0
w2 = 1.5
print(f"Превышение уровней {ex1} для срабатывания предупредительной (±{w1}) или аварийной (±{w2}) сигнализации: \r")


def warning_printer(filter_list_append, warning_param1=w1, warning_param2=w2, warn_type='accident',
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
            print(f"Превышение уровней {every_df.axes[1].values[1]} "
                  f"для срабатывания {warn_str} (±{warning_param}) сигнализации не выявлено")
        else:
            print(f"Выявлено {log_warn[every_df].shape[0]} превышения(-ий) (±{warning_param}) "
                  f"уровней {every_df.axes[1].values[1]}"
                  f"для срабатывания {warn_str} сигнализации")


warning_printer([ex1], w1, w2, 'warning')
warning_printer([ex1], w1, w2, 'accident')

w1 = 3.0
w2 = 4.5
print(f"Превышение уровней {ex2} для срабатывания предупредительной (±{w1}) или аварийной (±{w2}) сигнализации: \r")
warning_printer([ex2], w1, w2, 'warning')
warning_printer([ex2], w1, w2, 'accident')



print(f"\n")

print(f"\nСреднее отклонение ∆tgδ стороны ВН составляет"
      # f" по модулю {round(sum(delta_tg_HV_check) / len(delta_tg_HV_check), 3)}%"
      # f" при общем количестве {len(delta_tg_HV_check)} "
      f"показателей (исключены значения '∆tgδ = -10')")
print(f"\nПревышение уровня ∆tgδ ±1% для срабатывания"
      # f" предупредительной сигнализации: {len(analyzer.delta_tg_checker_warning())}"
      # f" случая(-ев) \n {analyzer.delta_tg_checker_warning()}' - "
      f"")
