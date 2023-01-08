import os
import devices
import pandas as pd
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import columns
import analyzer

#  took from devices
kiv = devices.Device('KIV')
devices.kiv.work_file_folder = 'upload/kiv/'
devices.kiv.file_names_starts = {'measure': 'MeasJ', 'event': 'WorkJ'}


#  took from columns
def kiv_xlsx_files_form():
    a_list_of_files = [filename for filename
         in os.listdir(devices.kiv.work_file_folder)if filename.startswith(devices.kiv.file_names_starts['measure'])]
    return a_list_of_files


def dict_maker(list_for_columns=None,
               file=devices.nkvv.work_file,
               sep=devices.nkvv.work_file_sep,
               encoding=devices.nkvv.work_file_default_encoding):
    if list_for_columns is None:
        list_for_columns = columns_maker(file=file, sep=sep, encoding=encoding)
    return {v: [k] for v, k in enumerate(list_for_columns)}


measj = 'upload/kiv/' + kiv_xlsx_files_form()[0]
# df = pd.read_excel(measj)
# df.to_pickle('main_dataframe_kiv.pkl')

df = pd.read_pickle('main_dataframe.pkl')

if df.iloc[0, 0] == 'Модуль:':
    devices.kiv.serial_number = df.iloc[0, 3]

headers = df.iloc[3]
df = pd.DataFrame(df.values[4:], columns=headers)
cols = list(headers)
cols_dict = columns.dict_maker(cols)

a = columns.kiv_xlsx_columns_analyzer(cols_dict)




