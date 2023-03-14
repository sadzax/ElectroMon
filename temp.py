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

build_list_cols = frontend.PDF.table_from_df(cols_df, title='Список данных файла с раскладкой для анализа')

prints.total_log_counter(dev, data)
a = prints.output()


old_stdout = sys.stdout
new_stdout = io.StringIO()
sys.stdout = new_stdout

prints.total_log_counter(dev, data)
output = new_stdout.getvalue()
print(output)

sys.stdout = old_stdout

build_list_total = build_list_cols
frontend.PDF.builder(build_list_total, 'output.pdf')
