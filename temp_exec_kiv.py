import warnings
import matplotlib.pyplot as plt
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

data = df
cols = cols_dict
input_x='datetime'
input_y=[ex1]
size_x: int = 14
size_y: int = 6
df_x = analyzer.data_filter(input_x, cols=cols, data=data)
df_y = analyzer.data_filter(input_y, cols=cols, data=data)
y = df_y[df_y.columns[0]].tolist()
x = df_x[df_x.columns[0]].tolist()
x2 = pd.to_datetime(x, format="%Y/%m/%d %H:%M:%S")
fig, axs = plt.subplots(figsize=(size_x, size_y))
axs.plot(x2, y)
