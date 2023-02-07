import analyzer
import columns
import devices
import plots
import prints
prints.clearing_script()


#  ______________________________________ OBTAINING DATA ___________________________________________

device_type: str = 'kiv'
devices.kiv.work_file = prints.work_file_picking(device_type)

print('Чтение и обработка файла...')
# __ Correct method
data = analyzer.get_data(device_type=device_type)
cols_list = columns.columns_list_maker(device_type=device_type, data=data)
cols = columns.columns_analyzer(device_type=device_type, list_for_columns=cols_list)
data = analyzer.pass_the_nan(device_type=device_type, data=data, cols=cols)
# __ Quick method for debugging
# noinspection PyTypeChecker
# devices.Pkl.save(device_type=device_type, data=data)
# noinspection PyTypeChecker
# data = devices.Pkl.load(device_type=device_type)
# cols_list = columns.columns_list_maker(device_type=device_type, data=data)
# cols = columns.columns_analyzer(device_type=device_type, list_for_columns=cols_list)
del cols_list
print('Обработка файла завершена')

data_slices = analyzer.values_time_slicer(device_type=device_type, data=data)
data = analyzer.values_time_slicer_choose(sliced_dict=data_slices)


#  ______________________________________ COUNTERS AND TIME ANALYZERS ______________________________

prints.total_log_counter(device_type=device_type, data=data)
prints.values_time_analyzer_df(device_type=device_type, data=data)
prints.total_nan_counter_df(device_type=device_type, data=data, cols=cols)  # optimize


#  ______________________________________ MIDDLE VOLTAGE ___________________________________________

ex1 = '∆C_MV'
ex2 = '∆tg_MV'
prints.info('Анализ трендов стороны СН')

print(f'Анализ корреляции данных {ex1}, {ex2} от температуры воздуха (при корреляции изменения на графике синхронны)')
plots.correlation_plot(filter_list1=[ex1, ex2], filter_list2=['tair'], device_type=device_type, data=data, cols=cols,
                       title=f"Анализ корреляции данных {ex1}, {ex2} от температуры воздуха")

prints.average_printer(ex=ex1, data=data, cols=cols, abs_parameter=True)
prints.average_printer(ex=ex2, data=data, cols=cols, abs_parameter=True)


#  ______________________________________ MIDDLE VOLTAGE WARNINGS __________________________________

prints.info('Анализ аварийной сигнализации')

ex = '∆tg_MV'
filter_list = ['time', '∆tg']
prints.info('Анализ сигнализации со стороны ВН')
w1 = 0.35
w2 = 0.5
print(f'\nПревышение уровней {ex} для срабатывания предупредительной (±{w1}) или аварийной (±{w2}) сигнализации: \r')
status = prints.answering('\n Вывести в кратком виде? Краткий вид - это только срабатывания аварийной сигнализации'
                          ' (без предупредительной)', yes='y', no='n')
if status == 'y':
    prints.warning_printer(filter_list, device_type, data, cols, w1, w2, 'accident')
elif status == 'n':
    prints.warning_printer(filter_list, device_type, data, cols, w1, w2, 'warning')
    prints.warning_printer(filter_list, device_type, data, cols, w1, w2, 'accident')

ex = '∆C_MV'
filter_list = ['time', '∆C']
prints.info('Анализ сигнализации со стороны ВН')
w1 = 0.35
w2 = 0.5
print(f'\nПревышение уровней {ex} для срабатывания предупредительной (±{w1}) или аварийной (±{w2}) сигнализации: \r')
status = prints.answering('\n Вывести в кратком виде? Краткий вид - это только срабатывания аварийной сигнализации'
                          ' (без предупредительной)', yes='y', no='n')
if status == 'y':
    prints.warning_printer(filter_list, device_type, data, cols, w1, w2, 'accident')
elif status == 'n':
    prints.warning_printer(filter_list, device_type, data, cols, w1, w2, 'warning')
    prints.warning_printer(filter_list, device_type, data, cols, w1, w2, 'accident')


#  ______________________________________ MIDDLE VOLTAGE GRAPHS ____________________________________

mv1 = 'Графики изменения значений напряжений в фазах А, В и С стороны СН-110кВ'
prints.print_flat_graph(input_y=['U_MV'], device_type=device_type, data=data, cols=cols, title=mv1)

mv2 = 'Графики изменения активной составляющей токов утечек высоковольтных вводов фаз А, В и С стороны СН-110кВ'
prints.print_flat_graph(input_y=['Ia_MV'], device_type=device_type, data=data, cols=cols, title=mv2)

mv4 = 'Графики изменения значений tgδ высоковольтных вводов фаз А, В и С стороны СН-110кВ'
prints.print_flat_graph(input_y=['tg'], device_type=device_type, data=data, cols=cols, title=mv4)

mv5 = 'Графики изменения значений емкостей С1 высоковольтных вводов фаз А, В и С стороны СН-110кВ'
prints.print_flat_graph(input_y=['C_MV'], device_type=device_type, data=data, cols=cols, title=mv5)

mv6 = 'Графики изменения значений ∆tgδ (изменение tgδ относительно начальных значений) высоковольтных вводов' \
      ' фаз А, В и С стороны СН-110кВ'
prints.print_flat_graph(input_y=['∆tg_MV'], device_type=device_type, data=data, cols=cols, title=mv6)

mv7 = 'Графики изменения значений ∆C/C1 (изменение емкостей С1 относительно начальных значений) высоковольтных вводов' \
      ' фаз А, В и С стороны СН-110кВ'
prints.print_flat_graph(input_y=['∆C_MV'], device_type=device_type, data=data, cols=cols, title=mv7)

import pandas as pd
a = pd.read_sql_table('./db/22_06/21217004.I', con='')