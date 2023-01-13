import warnings

import pandas as pd

import columns
import devices
import plots
import sadzax
import analyzer

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

plots.flat_graph(cols=cols_dict, data=df, input_x='datetime', input_y=[ex1])

data = df
df = data
cols = cols_dict
input_x='datetime'
input_y=[ex1]
