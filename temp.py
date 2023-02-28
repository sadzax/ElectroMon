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
data = devices.Pkl.load(dev)

# data = analyzer.stack_data(dev)

cols_list = columns.columns_list_maker(dev, data)
cols = columns.columns_analyzer(dev, cols_list)
del cols_list
# devices.Pkl.save(device_type=device_type, data=data)

data = analyzer.pass_the_nan(device_type=device_type, data=data, cols=cols)  # update data_types

#  ______________________________________ COUNTERS AND TIME ANALYZERS ______________________________
prints.total_log_counter(dev, data)
values_time_analyzer = analyzer.values_time_analyzer(dev, data)
values_time_analyzer_df = analyzer.values_time_analyzer_df(values_time_analyzer)
values_time_slicer = analyzer.values_time_slicer(dev, data)
values_time_slicer_choose = analyzer.values_time_slicer_choose(device_type, values_time_slicer)

data = values_time_slicer_choose
