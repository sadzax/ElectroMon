#  ______________________________________ SETTING THE ENVIRONMENT ________________________________
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import os
import analyzer
import columns
import devices
import plots
import prints
import sadzax
sadzax.Out.reconfigure_encoding()
# sadzax.Out.clear_future_warning()


#  ______________________________________ OBTAINING DATA _________________________________________
device_type = 'mon'
dev = device_type
# prints.file_picking(dev)
data = devices.Pkl.load(dev)
# data = analyzer.stack_data(dev)
cols_list = columns.columns_list_maker(dev, data)
cols = columns.columns_analyzer(dev, cols_list)
del cols_list
# devices.Pkl.save(device_type=device_type, data=data)
# data = analyzer.pass_the_nan(device_type=device_type, data=data, cols=cols)  # update data_types


#  ______________________________________ COUNTERS AND TIME ANALYZERS ____________________________
prints.total_log_counter(dev, data)

time_analyzer = analyzer.values_time_analyzer(dev, data)
prints.values_time_analyzer(dev, data, time_analyzer)


values_time_slicer = analyzer.values_time_slicer(dev, data, time_analyzer)
prints.values_time_slicer(dev, data, values_time_slicer)

values_time_slicer_choose = analyzer.values_time_slicer_choose(device_type, values_time_slicer)

data = values_time_slicer_choose
