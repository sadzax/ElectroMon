import devices
import pandas as pd
import columns
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


# df = pd.read_excel(devices.kiv.work_file)
# if df.iloc[0, 1] == 'KIV':
#     serial_number = df.iloc[0, 3]
# df = pd.DataFrame(df.values[4:], columns=headers)
# df.to_pickle('main_dataframe_kiv.pkl')


df = pd.read_pickle('main_dataframe_kiv.pkl')


cols_list = columns.columns_list_maker(device_type='kiv', data=df)
cols_dict = columns.dict_maker(cols_list)

a = ''
a = columns.kiv_xlsx_columns_analyzer(cols_dict)
