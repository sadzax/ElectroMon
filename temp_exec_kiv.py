import warnings

import pandas as pd

import columns
import devices
import plots
import sadzax

warnings.simplefilter(action='ignore', category=FutureWarning)


# data_raw = pd.read_excel(devices.kiv.work_file)
# cols_list = columns.columns_list_maker(device_type='kiv', data=data_raw)
#
# df = pd.DataFrame(data_raw.values[4:], columns=cols_list)
# df.to_pickle('main_dataframe_kiv.pkl')

df = pd.read_pickle('main_dataframe_kiv.pkl')

cols_list = columns.columns_list_maker(device_type='kiv', data=df)
cols_dict = columns.columns_analyzer(device_type='kiv', list_for_columns=cols_list)

ex1 = '∆tg_MV'
ex2 = '∆C_MV'

plots.flat_graph(cols=cols_dict, data=data, input_x='time', input_y=[ex1])