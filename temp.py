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
data = devices.Pkl.load(dev)
# data = analyzer.stack_data(dev)
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
build_temp = frontend.PDF.text(capture, frontend.style_title3)
frontend.PDF.add_to_build_list(build_temp, build_list)

#  Listing the columns and adding table of it as an object for reportlab/PDF
cols_df = columns.columns_df(dev, cols)
capture = cols_df
build_temp = frontend.PDF.table_from_df(capture, title='Список данных файла с раскладкой для анализа',
                                        style_body=frontend.style_body, style_title=frontend.style_title,
                                        colWidths=[80, 40, 40, 65, 60, 120, 130])
frontend.PDF.add_to_build_list(build_temp, build_list)

#  Returning total counter of measures and adding it as an object for reportlab/PDF
capture = frontend.capture_func(prints.total_log_counter, dev, data)
build_temp = frontend.PDF.text(capture, frontend.style_title2)
frontend.PDF.add_to_build_list(build_temp, build_list)

#  Analyzing time measures for sequence errors and adding the table of it as an object for reportlab/PDF
values_time_analyzer = analyzer.values_time_analyzer(dev, data, time_sequence_min=1, inaccuracy_sec=3)
capture = values_time_analyzer
build_temp = frontend.PDF.table_from_df(capture, title='Анализ периодичности и неразрывности измерений',
                                        style_body=frontend.style_body, style_title=frontend.style_title,
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
                                        style_body=frontend.style_body, style_title=frontend.style_title,
                                        colWidths=[70, 60, 40, 60, 40, 100])
frontend.PDF.add_to_build_list(build_temp, build_list)


#  ______________________________________ CORRELATIONS AND AVERAGES ______________________________
#  Defining the most usual 'ex'amples (deviation delta and tangent delta) for further correlation analyze
ex1 = '∆C'
ex2 = '∆tg'

#  Adding the heading of the module as an object for reportlab/PD
capture = frontend.capture_func(prints.info, f'Анализ трендов и средних показателей')
build_temp = frontend.PDF.text(capture, frontend.style_title2)
frontend.PDF.add_to_build_list(build_temp, build_list)
capture = f'Анализ корреляций (чем более явная корреляция, тем больше отклонение графа от оси шагов:' \
          f' вверх для прямой корреляции, вниз - для обратной)'
build_temp = frontend.PDF.text(capture, frontend.style_title)
frontend.PDF.add_to_build_list(build_temp, build_list)

#  Correlation of ∆C and temperature with a plot added as an object for reportlab/PD
buffer = frontend.capture_on_pic()
plots.correlation_plot(filter_list1=[ex1], filter_list2=['tair'],
                       device_type=device_type, data=data, cols=cols,
                       title=f"Анализ корреляции данных {ex1} от температуры воздуха")
build_temp = frontend.capture_off_pic(buffer, width=140, height=100, hAlign='RIGHT')
frontend.PDF.add_to_build_list(build_temp, build_list)

#  Correlation of ∆tg and temperature with a plot added as an object for reportlab/PD
buffer = frontend.capture_on_pic()
plots.correlation_plot(filter_list1=['U'], filter_list2=['tair'],
                       device_type=device_type, data=data, cols=cols,
                       title=f"Анализ корреляции данных {'U'} от температуры воздуха")
build_temp = frontend.capture_off_pic(buffer, width=140, height=100, hAlign='RIGHT')
frontend.PDF.add_to_build_list(build_temp, build_list)

#  Correlation of ∆tg and temperature with a plot added as an object for reportlab/PD
buffer = frontend.capture_on_pic()
plots.correlation_plot(filter_list1=['Ia'], filter_list2=['tair'],
                       device_type=device_type, data=data, cols=cols,
                       title=f"Анализ корреляции данных {'Ia'} от температуры воздуха")
build_temp = frontend.capture_off_pic(buffer, width=140, height=100, hAlign='RIGHT')
frontend.PDF.add_to_build_list(build_temp, build_list)

#  Correlation of ∆tg and temperature with a plot added as an object for reportlab/PD
buffer = frontend.capture_on_pic()
plots.correlation_plot(filter_list1=['Ir'], filter_list2=['tair'],
                       device_type=device_type, data=data, cols=cols,
                       title=f"Анализ корреляции данных {'Ir'} от температуры воздуха")
build_temp = frontend.capture_off_pic(buffer, width=140, height=100, hAlign='RIGHT')
frontend.PDF.add_to_build_list(build_temp, build_list)

#  Correlation of ∆tg and temperature with a plot added as an object for reportlab/PD
buffer = frontend.capture_on_pic()
plots.correlation_plot(filter_list1=[ex2], filter_list2=['tair'],
                       device_type=device_type, data=data, cols=cols,
                       title=f"Анализ корреляции данных {ex2} от температуры воздуха")
build_temp = frontend.capture_off_pic(buffer, width=140, height=100, hAlign='RIGHT')
frontend.PDF.add_to_build_list(build_temp, build_list)

#  Average values of ∆C and their distribution added as an object for reportlab/PD
capture = frontend.capture_func(prints.average_printer, ex=ex1, data=data, cols=cols, abs_parameter=True)
build_temp = frontend.PDF.text(capture, frontend.style_regular)
frontend.PDF.add_to_build_list(build_temp, build_list)
buffer = frontend.capture_on_pic()
plots.histogram([ex1], data=data, cols=cols, title=f'Распределение значений {ex1}')
build_temp = frontend.capture_off_pic(buffer, width=80, height=70, hAlign='CENTER')
frontend.PDF.add_to_build_list(build_temp, build_list)

#  Average values of ∆tg and their distribution added as an object for reportlab/PD
capture = frontend.capture_func(prints.average_printer, ex=ex2, data=data, cols=cols, abs_parameter=True)
build_temp = frontend.PDF.text(capture, frontend.style_regular)
frontend.PDF.add_to_build_list(build_temp, build_list)
buffer = frontend.capture_on_pic()
plots.histogram([ex2], data=data, cols=cols, title=f'Распределение значений {ex2}')
build_temp = frontend.capture_off_pic(buffer, width=80, height=70, hAlign='CENTER')
frontend.PDF.add_to_build_list(build_temp, build_list)


# ____________
frontend.PDF.builder(build_list, 'output.pdf')
