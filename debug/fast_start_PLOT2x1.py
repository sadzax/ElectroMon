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
dev = device_type = 'mon'
data = devices.Pkl.load(dev)
cols_list = columns.columns_list_maker(dev, data)
cols = columns.columns_analyzer(dev, cols_list)
del cols_list

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
plots.histogram(value=['∆C_MV'], ax_param=axes[0], bins=99,data=data,cols=cols, title=f'Распределение значений ∆C_MV')
plots.histogram(value=['∆C_HV'], ax_param=axes[1], bins=99,data=data,cols=cols, title=f'Распределение значений ∆C_HV')

fig.show()
