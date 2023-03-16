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
del cols_list
# ___
build_list = []

capture = devices.links(device_type)[9]
build_temp = frontend.PDF.text(capture, frontend.style_title2)
frontend.PDF.add_to_build_list(build_temp, build_list)
del capture

cols_df = columns.columns_df(dev, cols)
build_temp = frontend.PDF.table_from_df(cols_df, title='Список данных файла с раскладкой для анализа')
frontend.PDF.add_to_build_list(build_temp, build_list)

buffer = frontend.capture_on()
prints.total_log_counter(dev, data)
capture = frontend.capture_off(buffer)
build_temp = frontend.PDF.text(capture, frontend.style_title2)
frontend.PDF.add_to_build_list(build_temp, build_list)

values_time_analyzer = analyzer.values_time_analyzer(dev, data, time_sequence_min=1, inaccuracy_sec=3)
build_temp = frontend.PDF.table_from_df(values_time_analyzer, title='Анализ периодичности и неразрывности измерений',
                                        colWidths=[70, 60, 40, 60, 40, 100])
frontend.PDF.add_to_build_list(build_temp, build_list)

values_time_slicer = analyzer.values_time_slicer(dev, data, values_time_analyzer, min_values_required=150)
data = prints.values_time_slicer(dev, data, log=values_time_slicer)

total_nan_counter = analyzer.total_nan_counter(dev, data, false_data_percentage=30.0)
build_temp = frontend.PDF.table_from_df(total_nan_counter, title='Анализ периодов массовой некорректности измерений',
                                        colWidths=[70, 60, 40, 60, 40, 100])
frontend.PDF.add_to_build_list(build_temp, build_list)







# ____________
frontend.PDF.builder(build_list, 'output.pdf')