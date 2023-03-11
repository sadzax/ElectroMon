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
sadzax.Out.clear_future_warning()

#  ______________________________________ OBTAINING DATA _________________________________________
device_type = prints.device_picking()
# device_type = 'mon'
dev = device_type
# prints.file_picking(dev)
data = devices.Pkl.load(dev)
# data = analyzer.stack_data(dev)
cols_list = columns.columns_list_maker(dev, data)
cols = columns.columns_analyzer(dev, cols_list)
del cols_list
data = analyzer.pass_the_nan(device_type=device_type, data=data, cols=cols)  # update data_types
data = analyzer.set_dtypes(device_type=device_type, data=data, cols=cols)
# devices.Pkl.save(device_type=device_type, data=data)

#  ______________________________________ COUNTERS AND TIME ANALYZERS ____________________________
prints.total_log_counter(dev, data)

values_time_analyzer = analyzer.values_time_analyzer(dev, data, time_sequence_min=1, inaccuracy_sec=3)
prints.values_time_analyzer(dev, data, log=values_time_analyzer)

values_time_slicer = analyzer.values_time_slicer(dev, data, values_time_analyzer, min_values_required=150)
data = prints.values_time_slicer(dev, data, log=values_time_slicer)

total_nan_counter = analyzer.total_nan_counter(dev, data, false_data_percentage=30.0)
prints.total_nan_counter(dev, data, false_data_percentage=30.0, log=total_nan_counter)

#  ______________________________________ DATA ENG. _____________________________________________

hv1 = 'Графики изменения значений напряжений в фазах А, В и С стороны ВН-220кВ'
prints.print_flat_graph(input_y=['U_HV', 'U_MV'], device_type=dev, data=data, cols=cols, title=hv1)

hv2 = 'Графики изменения активной составляющей токов утечек высоковольтных вводов фаз А, В и С стороны ВН-220кВ'
prints.print_flat_graph(input_y=['Ia_HV'], device_type=dev, data=data, cols=cols, title=hv2)

hv3 = 'Графики изменения реактивной составляющей токов утечек высоковольтных вводов фаз А, В и С стороны ВН-220кВ'
prints.print_flat_graph(input_y=['Ir_HV'], device_type=dev, data=data, cols=cols, title=hv3)

hv4 = 'Графики изменения значений tgδ высоковольтных вводов фаз А, В и С стороны ВН-220кВ'
prints.print_flat_graph(input_y=['tg_HV'], device_type=dev, data=data, cols=cols, title=hv4)

hv5 = 'Графики изменения значений емкостей С1 высоковольтных вводов фаз А, В и С стороны ВН-220кВ'
prints.print_flat_graph(input_y=['C_HV'], device_type=dev, data=data, cols=cols, title=hv5)

hv6 = 'Графики изменения значений ∆tgδ (изменение tgδ относительно начальных значений) высоковольтных вводов' \
      ' фаз А, В и С стороны ВН-220кВ'
prints.print_flat_graph(input_y=['∆tg_HV'], device_type=dev, data=data, cols=cols, title=hv6)

hv7 = 'Графики изменения значений ∆C/C1 (изменение емкостей С1 относительно начальных значений) высоковольтных вводов' \
      ' фаз А, В и С стороны ВН-220кВ'
prints.print_flat_graph(input_y=['∆C_HV'], device_type=dev, data=data, cols=cols, title=hv7)

