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

fig, axes = plt.subplots(1, 2)
# fig.show()
x = plots.histogram(value=['∆C_MV'], bins=99,data=data,cols=cols, title=f'Распределение значений ∆C_MV')
# axes[0] = plots.histogram(value=['∆C_MV'], bins=99,data=data,cols=cols, title=f'Распределение значений ∆C_MV')
# axes[0].show()
# axes[0].plot(range(3), range(3))
# axes[1] = plots.histogram(value=['∆C_HV'], bins=99,data=data,cols=cols, title=f'Распределение значений ∆C_HV')
y = plots.histogram(value=['∆C_HV'], bins=99,data=data,cols=cols, title=f'Распределение значений ∆C_HV')
axes[0] = x
axes[1] = y

fig.show()

fig, axes = plt.subplots(1, 2)
axes[0].plot(range(3), range(3))
axes[1].plot(range(9), [2*x for x in range(9)])