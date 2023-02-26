#  ______________________________________ SETTING THE ENVIRONMENT ________________________________
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
dev = device_type
# data = devices.Pkl.load(dev)

data = analyzer.stack_data(dev)

cols_list = columns.columns_list_maker(dev, data)
cols = columns.columns_analyzer(dev, cols_list)
del cols_list
# devices.Pkl.save(device_type=device_type, data=data)

data = analyzer.pass_the_nan(device_type=device_type, data=data, cols=cols)  # update data_types

prints.total_log_counter(device_type=device_type, data=data)

data_slices = analyzer.values_time_slicer(device_type, data)
data_slices_choose = analyzer.values_time_slicer_choose(device_type, data_slices)


#  ______________________________________ COUNTERS AND TIME ANALYZERS ______________________________

prints.total_log_counter(device_type=device_type, data=data)
prints.values_time_analyzer_df(device_type=device_type, data=data)
prints.total_nan_counter_df(device_type=device_type, data=data, cols=cols)  # optimize


