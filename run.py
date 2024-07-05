#  ______________________________________ SETTING THE ENVIRONMENT ________________________________
import datetime
import io
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import analyzer
import columns
import devices
import frontend
import plots
import prints
import services
services.Out.reconfigure_encoding()
services.Out.clear_future_warning()


#  ______________________________________ OBTAINING DATA _________________________________________
prints.info('Установление параметров для анализа')

dev = prints.device_picking()
# device_type = 'mon'
# prints.file_picking(dev)
# data = devices.Pkl.load(dev)
[data, used_files] = analyzer.stack_data(dev)
cols_list = columns.columns_list_maker(dev, data)
cols = columns.columns_analyzer(dev, cols_list)
del cols_list
data = analyzer.pass_the_nan(device_type=dev, data=data, cols=cols)  # update data_types
data = analyzer.set_dtypes(device_type=dev, data=data, cols=cols)
# devices.Pkl.save(device_type=dev, data=data)


#  ______________________________________ COUNTERS AND TIME ANALYZERS ____________________________
prints.info('Анализ неразрывности замеров и их корректности')

#  Returning total counter of measures and their period
prints.total_log_counter(dev, data)
prints.total_periods(dev, data)

#  Asking for a period to choose
status = services.question(
        f"\n Хотите задать конкретный период анализа между двумя датами?"
        f"\n Если нет - то будут проанализированы все доступные периоды замеров\n", yes='y')
if status == 'y':
    data = analyzer.time_period_choose(data, dev)
    prints.total_log_counter(dev, data)
    prints.total_periods(dev, data)


#  Analyzing time measures for sequence errors
values_time_analyzer = analyzer.values_time_analyzer(dev, data, time_sequence_min=1, inaccuracy_sec=3)
prints.values_time_analyzer(dev, data, log=values_time_analyzer)

#  Choosing the slice of time periods (the delimiter for defining a new time slice is 1440 minutes / 1 day)
values_time_slicer = analyzer.values_time_slicer(dev, data, values_time_analyzer,
                                                 minutes_slice_mode=1440, min_values_required=150)
data = prints.values_time_slicer(dev, data, log=values_time_slicer)

#  Analyzing data for false measurements
total_nan_counter = analyzer.total_nan_counter(dev, data, false_data_percentage=30.0)
prints.total_nan_counter(dev, data, false_data_percentage=30.0, log=total_nan_counter)
total_nan_counter_ease = analyzer.total_nan_counter_ease(total_nan_counter)
if total_nan_counter_ease is not None:
    print(total_nan_counter_ease)


#  ______________________________________ CORRELATIONS AND AVERAGES ______________________________
prints.info('Анализ трендов и средних показателей')

trends_params = {
    '∆tg': 'Изменения значений ∆tgδ (изменение tgδ относительно начальных значений)',
    '∆C': 'Изменения значений ∆C/C1 (изменение емкостей С1 относительно начальных значений)'
}

for a_key in trends_params.keys():
    for a_voltage in ['_HV', '_MV']:
        ex = a_key+a_voltage
        plots.correlation_plot(filter_list1=[ex], filter_list2=['tair'], device_type=dev, data=data, cols=cols,
                               title=f"Анализ корреляции данных {ex} от температуры воздуха")
        plt.show()

for a_key in trends_params.keys():
    for a_voltage in ['_HV', '_MV']:
        ex = a_key+a_voltage
        prints.average_printer(ex=ex, data=data, cols=cols, abs_parameter=True)
        plots.histogram(value=[ex], bins=99, data=data, cols=cols, logarithm=False,
                        title=f'Распределение значений {ex}')
        plt.show()
        plots.histogram(value=[ex], bins=99, data=data, cols=cols, logarithm=True,
                        title=f'Логарифмическое распределение значений {ex}')
        plt.show()


#  ______________________________________ WARNINGS AND ACCIDENTS _________________________________
prints.info('Анализ срабатываний предупредительной и аварийной сигнализации')

for k in devices.links(dev)[10]:
    w0 = devices.links(dev)[10][k][0]
    w1 = devices.links(dev)[10][k][1]
    print(
        f'\nПревышение уровней {k} для срабатывания предупредительной (±{w0}) или аварийной (±{w1}) сигнализации: \r')
    #  Main operation
    warning_finder = analyzer.warning_finder([k], dev, data, cols, w0, w1)
    status = services.question(
        f"Вывести кратко? \n (Только срабатывания аварийной сигнализации {k} без предупредительной)"
        f" \n Если нет - то будут выведены и предупредительные, и аварийные замеры ", yes='y', no='n')
    warnings_codes_temporal_list = {'acc': 'аварийной'}
    if status == 'n':
        warnings_codes_temporal_list = {'war': 'предупредительной', 'acc': 'аварийной'}
    for warn_code, warn_code_str in warnings_codes_temporal_list.items():
        prints.warning_printer(dev, warning_finder, warn_code, warning_param_war=w0, warning_param_acc=w1)
        warning_finder_ease = analyzer.warning_finder_ease(warning_finder, dev, warn_code, min_values_for_print=10,
                                                           warning_param_war=w0, warning_param_acc=w1)
        print(warning_finder_ease)
        #  Scattering
        warning_finder_merge = analyzer.warning_finder_merge(warning_finder, dev, data, warn_code, w0, w1)
        plots.scatter(df=warning_finder_merge, device_type=dev, title=f'График {warn_code_str} сигнализации')
        plt.show()


#  ______________________________________ DATA ENG. ______________________________________________

main_graph_params = {
    'U': 'График изменения значений напряжений',
    'Ia': 'График изменения активной составляющей токов утечек',
    'Ir': 'График изменения реактивной составляющей токов утечек',
    'tg': 'График изменения значений tgδ',
    'C': 'График изменения значений емкостей С1',
    '∆tg': 'График изменения значений ∆tgδ (изменение tgδ относительно начальных значений)',
    '∆C': 'График изменения значений ∆C/C1 (изменение емкостей С1 относительно начальных значений)'
}

for code_key, code_desc in {'_HV': ' со стороны высокого напряжения',
                            '_MV': ' со стороны среднего напряжения'}.items():
    prints.info(f'Анализ значений параметров высоковольтных вводов в фазах А, В и С{code_desc}')
    for key, desc in main_graph_params.items():
        input_y = key + code_key
        title = desc + code_desc
        prints.print_flat_graph(input_y=[input_y], device_type=dev, data=data, cols=cols, title=title)
        plt.show()
