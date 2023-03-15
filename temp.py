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

prints.total_log_counter(dev, data)
buffer = frontend.capture_on()
prints.total_log_counter(dev, data)
capture = frontend.capture_off(buffer, 2)
build_temp = frontend.PDF.text(capture, frontend.style_title2)
frontend.PDF.add_to_build_list(build_temp, build_list)

build_temp = frontend.capture_func(prints.total_log_counter, dev, data)
frontend.PDF.add_to_build_list(build_temp, build_list)


buffer = frontend.capture_on()
prints.total_log_counter(dev, data)
capture = frontend.capture_off(buffer, 2)
build_list_total_log_counter = frontend.PDF.text(capture, frontend.style_title2)

values_time_analyzer = analyzer.values_time_analyzer(dev, data, time_sequence_min=1, inaccuracy_sec=3)
build_temp = frontend.PDF.table_from_df(values_time_analyzer, title='Анализ периодичности и неразрывности измерений')
frontend.PDF.add_to_build_list(build_temp, build_list)




# ____________


frontend.PDF.builder(build_list, 'output.pdf')