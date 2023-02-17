import warnings
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import os
import columns
import devices
import plots
import prints
import sadzax
import analyzer
warnings.simplefilter(action='ignore', category=FutureWarning)
prints.clearing_script()

device_type = 'mon'
data = devices.Pkl.load(device_type=device_type)

# data = analyzer.stack_data(device_type=device_type)
cols_list = columns.columns_list_maker(device_type=device_type, data=data)
cols = columns.columns_analyzer(device_type=device_type, list_for_columns=cols_list)
del cols_list
# devices.Pkl.save(device_type=device_type, data=data)

# ___

# data = analyzer.pass_the_nan(device_type=device_type, data=data, cols=cols)  # update data_types

data_slices = analyzer.values_time_slicer(device_type, data)
data_slices_choose = analyzer.values_time_slicer_choose(device_type, data_slices)


#  ______________________________________ COUNTERS AND TIME ANALYZERS ______________________________

prints.total_log_counter(device_type=device_type, data=data)
prints.values_time_analyzer_df(device_type=device_type, data=data)
prints.total_nan_counter_df(device_type=device_type, data=data, cols=cols)  # optimize


