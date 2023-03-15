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

data.info()
cols_df = columns.columns_df(dev, cols)
# ___

a = frontend.capture_func(prints.total_log_counter, dev, data)

buffer = frontend.capture_on()
prints.total_log_counter(dev, data)
captured = frontend.capture_off(buffer, 2)
print(captured)
build_list_total_log_counter = frontend.PDF.text(captured, frontend.style_title2)


# ____________
build_list_cols = frontend.PDF.table_from_df(cols_df, title='Список данных файла с раскладкой для анализа')

build_list_total = build_list_total_log_counter + build_list_cols
frontend.PDF.builder(build_list_total, 'output.pdf')
