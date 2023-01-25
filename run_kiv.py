import analyzer
import columns
import devices
import plots
import prints
prints.clearing_script()


device_type: str = 'kiv'
devices.kiv.work_file = prints.work_file_picking(device_type)

print('Чтение и обработка файла...')
database = analyzer.get_data(device_type=device_type)
data = database.copy()
data = analyzer.pass_the_nan(device_type=device_type, data=data, cols=cols)
# # noinspection PyTypeChecker
# devices.Pkl.save(device_type=device_type, data=data)
# # noinspection PyTypeChecker
# data = devices.Pkl.load(device_type=device_type)
cols_list = columns.columns_list_maker(device_type=device_type, data=data)
cols = columns.columns_analyzer(device_type=device_type, list_for_columns=cols_list)
del cols_list
print('Обработка файла завершена')

data_slices = analyzer.values_time_slicer(device_type=device_type, data=data)
data = analyzer.values_time_slicer_choose(sliced_dict=data_slices)


prints.total_log_counter(device_type=device_type, data=data)
prints.values_time_analyzer_df(device_type=device_type, data=data)
prints.total_nan_counter_df(device_type=device_type, data=data, cols=cols)


#  ______________________________________ MIDDLE VOLTAGE ___________________________________________

ex1 = '∆C_MV'
ex2 = '∆tg_MV'

prints.info('Анализ трендов стороны СН')

print(f'Анализ корреляции данных {ex1}, {ex2} от температуры воздуха (при корреляции изменения на графике синхронны)')
plots.correlation_plot(filter_list1=[ex1, ex2], filter_list2=['tair'], device_type=device_type, data=data, cols=cols,
                       title=f"Анализ корреляции данных {ex1}, {ex2} от температуры воздуха")

prints.average_printer(ex=ex1, data=data, cols=cols)

# Averages
zzz = analyzer.data_average_finder(filter_list=[ex1], data=data, cols=cols)

# _______

prints.info('Анализ сигнализации со стороны ВН')
w1 = 1.0
w2 = 1.5
print(f'\nПревышение уровней {ex1} для срабатывания предупредительной (±{w1}) или аварийной (±{w2}) сигнализации: \r')
status = prints.answering('Вывести только срабатывания аварийной сигнализации?', yes='y', no='n')
if status == 'y':
    prints.warning_printer([ex1], w1, w2, 'accident')
elif status == 'n':
    prints.warning_printer([ex1], w1, w2, 'warning')
    prints.warning_printer([ex1], w1, w2, 'accident')

w1 = 3.0
w2 = 4.5
print(f'\nПревышение уровней {ex2} для срабатывания предупредительной (±{w1}) или аварийной (±{w2}) сигнализации: \r')
status = prints.answering('Вывести только срабатывания аварийной сигнализации?', yes='y', no='n')
if status == 'y':
    prints.warning_printer([ex2], w1, w2, 'accident', abs_parameter=True)
elif status == 'n':
    prints.warning_printer([ex2], w1, w2, 'warning', abs_parameter=True)
    prints.warning_printer([ex2], w1, w2, 'accident', abs_parameter=True)

mv1 = 'Графики изменения значений напряжений в фазах А, В и С стороны СН-110кВ'
prints.print_flat_graph(input_y=['U_MV'], data=data, title=mv1)

mv2 = 'Графики изменения активной составляющей токов утечек высоковольтных вводов фаз А, В и С стороны СН-110кВ'
prints.print_flat_graph(input_y=['Ia_MV'], data=data, title=mv2)

mv4 = 'Графики изменения значений tgδ высоковольтных вводов фаз А, В и С стороны СН-110кВ'
prints.print_flat_graph(input_y=['tg_MV'], data=data, title=mv4)

mv5 = 'Графики изменения значений емкостей С1 высоковольтных вводов фаз А, В и С стороны СН-110кВ'
prints.print_flat_graph(input_y=['C_MV'], data=data, title=mv5)

mv6 = 'Графики изменения значений ∆tgδ (изменение tgδ относительно начальных значений) высоковольтных вводов' \
      ' фаз А, В и С стороны СН-110кВ'
prints.print_flat_graph(input_y=['∆tg_MV'], data=data, title=mv6)

mv7 = 'Графики изменения значений ∆C/C1 (изменение емкостей С1 относительно начальных значений) высоковольтных вводов' \
      ' фаз А, В и С стороны СН-110кВ'
prints.print_flat_graph(input_y=['∆C_MV'], data=data, title=mv7)
