import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import os
import io
import sys
import analyzer
import columns
import devices
import plots
import prints
import sadzax
import frontend
sadzax.Out.reconfigure_encoding()
sadzax.Out.clear_future_warning()
device_type = 'mon'
dev = device_type
data = devices.Pkl.load(dev)
cols_list = columns.columns_list_maker(dev, data)
cols = columns.columns_analyzer(dev, cols_list)
data = analyzer.set_dtypes(device_type=device_type, data=data, cols=cols)
del cols_list

# ___
build_list = []


capture = devices.links(device_type)[9]
build_temp = frontend.PDF.text(capture, frontend.style_title)
frontend.PDF.add_to_build_list(build_temp, build_list)


cols_df = columns.columns_df(dev, cols)
build_temp = frontend.PDF.table_from_df(cols_df, title='Список данных файла с раскладкой для анализа',
                                        style_body=frontend.style_body, style_title=frontend.style_title,
                                        colWidths=[80, 40, 40, 65, 60, 120, 130])
frontend.PDF.add_to_build_list(build_temp, build_list)


buffer = frontend.capture_on()
prints.total_log_counter(dev, data)
capture = frontend.capture_off(buffer)
build_temp = frontend.PDF.text(capture, frontend.style_title)
frontend.PDF.add_to_build_list(build_temp, build_list)


values_time_analyzer = analyzer.values_time_analyzer(dev, data, time_sequence_min=1, inaccuracy_sec=3)
build_temp = frontend.PDF.table_from_df(values_time_analyzer, title='Анализ периодичности и неразрывности измерений',
                                        style_body=frontend.style_body, style_title=frontend.style_title,
                                        colWidths=[70, 60, 40, 60, 40, 100])
frontend.PDF.add_to_build_list(build_temp, build_list)


values_time_slicer = analyzer.values_time_slicer(dev, data, values_time_analyzer, min_values_required=150)
data = prints.values_time_slicer(dev, data, log=values_time_slicer)


total_nan_counter = analyzer.total_nan_counter(dev, data, false_data_percentage=30.0)
total_nan_counter_ease = analyzer.total_nan_counter_ease(total_nan_counter)
build_temp = frontend.PDF.table_from_df(total_nan_counter_ease,
                                        title='Анализ периодов массовой некорректности измерений',
                                        colWidths=[70, 60, 40, 60, 40, 100])
frontend.PDF.add_to_build_list(build_temp, build_list)


# ____________
ex1 = '∆C'
ex2 = '∆tg'


buffer = frontend.capture_on()
prints.info('Анализ трендов')
capture = frontend.capture_off(buffer)
build_temp = frontend.PDF.text(capture, frontend.style_title2)
frontend.PDF.add_to_build_list(build_temp, build_list)


buffer = frontend.capture_on()
print(f'Анализ корреляции данных {ex1} от температуры воздуха (при корреляции изменения на графике синхронны)')
capture = frontend.capture_off(buffer)
build_temp = frontend.PDF.text(capture, frontend.style_title)
frontend.PDF.add_to_build_list(build_temp, build_list)

buffer = frontend.capture_on_pic()
plots.correlation_plot(filter_list1=[ex1], filter_list2=['tair'],
                       device_type=device_type, data=data, cols=cols,
                       title=f"Анализ корреляции данных {ex1} от температуры воздуха")
build_temp = frontend.capture_off_pic(buffer, aw=1, ah=1)
frontend.PDF.add_to_build_list(build_temp, build_list)


# ____________
frontend.PDF.builder(build_list, 'output.pdf')
