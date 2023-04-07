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
import sadzax
sadzax.Out.reconfigure_encoding()
sadzax.Out.clear_future_warning()


#  ______________________________________ OBTAINING DATA _________________________________________
device_type = prints.device_picking()
# device_type = 'mon'
dev = device_type
# prints.file_picking(dev)
# data = devices.Pkl.load(dev)
data = analyzer.stack_data(dev)
cols_list = columns.columns_list_maker(dev, data)
cols = columns.columns_analyzer(dev, cols_list)
del cols_list
data = analyzer.pass_the_nan(device_type=device_type, data=data, cols=cols)  # update data_types
data = analyzer.set_dtypes(device_type=device_type, data=data, cols=cols)
# devices.Pkl.save(device_type=device_type, data=data)


#  ______________________________________ COUNTERS AND TIME ANALYZERS ____________________________
#  Setting a list for appending objects for reportlab/PDF
build_list = []

#  Returning device name and adding it as an object for reportlab/PDF
build_temp = frontend.PDF.text(f'Отчёт по устройству', frontend.style_title)
frontend.PDF.add_to_build_list(build_temp, build_list)
capture = devices.links(device_type)[9]
build_temp = frontend.PDF.text(capture, frontend.style_title2)
frontend.PDF.add_to_build_list(build_temp, build_list)

build_temp = frontend.PDF.text(f'Анализ неразрывности замеров и их корректности', frontend.style_title2)
frontend.PDF.add_to_build_list(build_temp, build_list)

#  Listing the columns and adding table of it as an object for reportlab/PDF
cols_df = columns.columns_df(dev, cols)
capture = cols_df
build_temp = frontend.PDF.table_from_df(capture, title='Список данных файла с раскладкой для анализа',
                                        style_of_body=frontend.style_body, style_of_title=frontend.style_title,
                                        colWidths=[80, 40, 40, 65, 60, 120, 130])
frontend.PDF.add_to_build_list(build_temp, build_list)

#  Returning total counter of measures and their period
prints.total_log_counter(dev, data)
prints.total_periods(dev, data)

#  Returning total counter of measures and adding it as an object for reportlab/PDF
status = sadzax.question(
        f"\n Хотите задать конкретный период анализа между двумя датами?"
        f"\n Eсли нет - то будут проанализированы все доступные периоды замеров\n", yes='y')
if status == 'y':
    data = analyzer.time_period_choose(data, dev)
    capture = frontend.capture_func(prints.total_log_counter, dev, data)
    build_temp = frontend.PDF.text(capture, frontend.style_title)
    frontend.PDF.add_to_build_list(build_temp, build_list)
    capture = frontend.capture_func(prints.total_periods, dev, data)
    build_temp = frontend.PDF.text(capture, frontend.style_title)
    frontend.PDF.add_to_build_list(build_temp, build_list)

#  Analyzing time measures for sequence errors and adding the table of it as an object for reportlab/PDF
values_time_analyzer = analyzer.values_time_analyzer(dev, data, time_sequence_min=1, inaccuracy_sec=3)
capture = values_time_analyzer
build_temp = frontend.PDF.table_from_df(capture, title='Анализ периодичности и неразрывности измерений',
                                        style_of_body=frontend.style_body, style_of_title=frontend.style_title,
                                        colWidths=[70, 60, 40, 60, 40, 100])
frontend.PDF.add_to_build_list(build_temp, build_list)

#  Choosing the slice of time periods (the delimiter for defining a new time slice is 1440 minutes / 1 day)
values_time_slicer = analyzer.values_time_slicer(dev, data, values_time_analyzer,
                                                 minutes_slice_mode=1440, min_values_required=150)
data = prints.values_time_slicer(dev, data, log=values_time_slicer)

#  Analyzing data for false measurements, adding the table of their continuous periods as an object for reportlab/PDF
total_nan_counter = analyzer.total_nan_counter(dev, data, false_data_percentage=30.0)
total_nan_counter_ease = analyzer.total_nan_counter_ease(total_nan_counter)
capture = total_nan_counter_ease
build_temp = frontend.PDF.table_from_df(capture, title='Анализ периодов массовой некорректности измерений',
                                        style_of_body=frontend.style_body, style_of_title=frontend.style_title,
                                        colWidths=[70, 60, 40, 60, 40, 100])
frontend.PDF.add_to_build_list(build_temp, build_list)

#  Step 2 lines after submodule
frontend.PDF.add_to_build_list(frontend.PDF.text(f' ', frontend.style_title), build_list)
frontend.PDF.add_to_build_list(frontend.PDF.text(f' ', frontend.style_title), build_list)


#  ______________________________________ CORRELATIONS AND AVERAGES ______________________________
#  Defining the most usual 'ex'amples (deviation delta and tangent delta) for further correlation analyze
ex1 = '∆C'
ex2 = '∆tg'

#  Adding the heading of the module as an object for reportlab/PD
capture = f'Анализ трендов и средних показателей'
build_temp = frontend.PDF.text(capture, frontend.style_title2)
frontend.PDF.add_to_build_list(build_temp, build_list)

#  Adding the heading of the submodule as an object for reportlab/PD
capture = f'Анализ распределения значений'
build_temp = frontend.PDF.text(capture, frontend.style_title)
frontend.PDF.add_to_build_list(build_temp, build_list)


#  Average values operative function
# noinspection PyPep8Naming
def capturer_for_PDF_average(ex, data=data, cols=cols, build_list=None, width=120, height=100,
                             hAlign='CENTER', abs_parameter=True):
    if build_list is None:
        build_list = build_list
    capture = frontend.capture_func(prints.average_printer, ex=ex, data=data, cols=cols, abs_parameter=abs_parameter)
    build_temp = frontend.PDF.text(capture, frontend.style_regular)
    frontend.PDF.add_to_build_list(build_temp, build_list)
    buffer = frontend.capture_on_pic()
    plots.histogram([ex], data=data, cols=cols, title=f'Распределение значений {ex}')
    build_temp = frontend.capture_off_pic(buffer, width=width, height=height, hAlign=hAlign)
    frontend.PDF.add_to_build_list(build_temp, build_list)


#  Average values of [∆C, ∆tg, Ia, Ir, U] and their distribution added as an object for reportlab/PD
capturer_for_PDF_average(ex1)
capturer_for_PDF_average(ex2)
capturer_for_PDF_average('Ia', abs_parameter=False)
capturer_for_PDF_average('Ir', abs_parameter=False)
capturer_for_PDF_average('U', abs_parameter=False)

#  Step 2 lines after submodule
frontend.PDF.add_to_build_list(frontend.PDF.text(f' ', frontend.style_title), build_list)
frontend.PDF.add_to_build_list(frontend.PDF.text(f' ', frontend.style_title), build_list)

#  Adding the heading of the submodule as an object for reportlab/PD
capture = f'Анализ корреляций'
build_temp = frontend.PDF.text(capture, frontend.style_title)
frontend.PDF.add_to_build_list(build_temp, build_list)
capture = f'(чем более явная корреляция, тем больше отклонение графа от оси шагов:' \
          f' вверх для прямой корреляции, вниз - для обратной)'
build_temp = frontend.PDF.text(capture, frontend.style_regular)
frontend.PDF.add_to_build_list(build_temp, build_list)


#  Correlation with and air operative function
# noinspection PyPep8Naming
def capturer_for_PDF_air_correlation(ex, data=data, cols=cols, build_list=None, width=140, height=110,
                                     hAlign='RIGHT'):
    if build_list is None:
        build_list = build_list
    buffer = frontend.capture_on_pic()
    plots.correlation_plot(filter_list1=[ex], filter_list2=['tair'],
                           device_type=device_type, data=data, cols=cols,
                           title=f"Анализ корреляции данных {ex1} от температуры воздуха")
    build_temp = frontend.capture_off_pic(buffer, width=width, height=height, hAlign=hAlign)
    frontend.PDF.add_to_build_list(build_temp, build_list)


#  Correlation of [∆C, ∆tg, Ia, Ir, U] and temperature with a plot added as an object for reportlab/PD
capturer_for_PDF_air_correlation(ex1)
capturer_for_PDF_air_correlation(ex2)
capturer_for_PDF_air_correlation('Ia')
capturer_for_PDF_air_correlation('Ir')
capturer_for_PDF_air_correlation('U')

#  Step 2 lines after submodule
frontend.PDF.add_to_build_list(frontend.PDF.text(f' ', frontend.style_title), build_list)
frontend.PDF.add_to_build_list(frontend.PDF.text(f' ', frontend.style_title), build_list)


#  ______________________________________ WARNINGS _______________________________________________
#  Adding the heading of the module as an object for reportlab/PD
capture = f'Анализ срабатываний предупредительной и аварийной сигнализации'
build_temp = frontend.PDF.text(capture, frontend.style_title2)
frontend.PDF.add_to_build_list(build_temp, build_list)

for k in devices.links(device_type)[10]:
    #  Set the default warning values (1 / 1.5% for delta_tangent and 3 / 5% for delta_correlation)
    w0 = devices.links(device_type)[10][k][0]
    w1 = devices.links(device_type)[10][k][1]
    #  Title
    capture = f'\nПревышение уровней {k} для срабатывания ' \
              f'предупредительной (±{w0}) или аварийной (±{w1}) сигнализации \r'
    build_temp = frontend.PDF.text(capture, frontend.style_title)
    frontend.PDF.add_to_build_list(build_temp, build_list)
    #  Main operation - forming a dict with a DataFrames of warning issues
    warning_finder = analyzer.warning_finder([k], dev, data, cols, w0, w1)
    #  Setting the short/full output
    status = sadzax.question(
        f"Вывести кратко? \n (Только срабатывания аварийной сигнализации {k} без предупредительной)"
        f" \n Eсли нет - то будут выведены и предупредительные, и аварийные замеры ", yes='y', no='n')
    warnings_codes_temporal_list = {'acc': 'аварийной'}
    if status == 'n':
        warnings_codes_temporal_list = {'war': 'предупредительной', 'acc': 'аварийной'}
    for warn_code, warn_code_str in warnings_codes_temporal_list.items():
        capture = frontend.capture_func(prints.warning_printer, dev, warning_finder, warn_code,
                                        warning_param_war=w0, warning_param_acc=w1)
        build_temp = frontend.PDF.text(capture, frontend.style_regular)
        frontend.PDF.add_to_build_list(build_temp, build_list)
        #  Setting minimal amout of values to be printed in a table
        min_values_for_print = 10
        #  Easing the main operated data to form a DataFrame
        warning_finder_ease = analyzer.warning_finder_ease(warning_finder, dev, warn_code,
                                                           warning_param_war=w0, warning_param_acc=w1,
                                                           min_values_for_print=min_values_for_print)
        capture = warning_finder_ease
        #  Form table from DataFrame
        build_temp = frontend.PDF.table_from_df(capture, title=f'Таблица периодов непрерывной сигнализации'
                                                               f' (минимум {min_values_for_print} сигнальных'
                                                               f' замеров подряд)',
                                                style_of_body=frontend.style_body, style_of_title=frontend.style_title,
                                                colWidths=[180, 110, 110, 70])
        frontend.PDF.add_to_build_list(build_temp, build_list)

        warning_finder_merge = analyzer.warning_finder_merge(warning_finder, dev, data, warn_code, w0, w1)
        buffer = frontend.capture_on_pic()
        plots.scatter(df=warning_finder_merge, device_type=dev, title=f'График {warn_code_str} сигнализации')
        build_temp = frontend.capture_off_pic(buffer, width=205, height=95, hAlign='CENTER')
        frontend.PDF.add_to_build_list(build_temp, build_list)

#  Step 2 lines after submodule
frontend.PDF.add_to_build_list(frontend.PDF.text(f' ', frontend.style_title), build_list)
frontend.PDF.add_to_build_list(frontend.PDF.text(f' ', frontend.style_title), build_list)


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
    capture = f'Анализ значений параметров высоковольтных вводов в фазах А, В и С{code_desc}'
    build_temp = frontend.PDF.text(capture, frontend.style_title2)
    frontend.PDF.add_to_build_list(build_temp, build_list)
    for key, desc in main_graph_params.items():
        input_y = key + code_key
        title = desc + code_desc
        buffer = frontend.capture_on_pic()
        prints.print_flat_graph(input_y=[input_y], device_type=dev, data=data, cols=cols, title=title)
        build_temp = frontend.capture_off_pic(buffer, width=205, height=95, hAlign='CENTER')
        frontend.PDF.add_to_build_list(build_temp, build_list)
        frontend.PDF.add_to_build_list(frontend.PDF.text(f' ', frontend.style_title), build_list)


#  ______________________________________ OUTPUT IN PDF __________________________________________
name_file_by_user = sadzax.Enter.str('Введите имя файла для сохранения: ',
                                     arg_must_be=sadzax.Enter.allowed_symbs_default, arg_max_capacity=24,
                                     arg_error='Некорректное имя для файла')
frontend.PDF.builder(build_list, filename=name_file_by_user + '.pdf')
