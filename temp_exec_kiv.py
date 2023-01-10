import warnings

import pandas as pd

import columns
import devices
import plots
import sadzax

warnings.simplefilter(action='ignore', category=FutureWarning)


# df = pd.read_excel(devices.kiv.work_file)
# if df.iloc[0, 1] == 'KIV':
#     serial_number = df.iloc[0, 3]
# df = pd.DataFrame(df.values[4:], columns=headers)
# df.to_pickle('main_dataframe_kiv.pkl')
df = pd.read_pickle('main_dataframe_kiv.pkl')

cols_list = columns.columns_list_maker(device_type='kiv', data=df)
cols_dict = columns.dict_maker(cols_list)


def kiv_xlsx_columns_analyzer(source_dict=None):
    if source_dict is None:
        source_dict = columns.dict_maker(columns.columns_list_maker(device_type='kiv', data=pd.read_excel(devices.kiv.work_file)))
    result_dict = source_dict.copy()
    for i in range(len(result_dict)):
        tail = sadzax.Trimmer.right(result_dict[i][0], 2)
        head = sadzax.Trimmer.left(result_dict[i][0], 4)
        for key in devices.kiv.data_types:
            if key == tail:
                result_dict[i].append(devices.kiv.data_types[key])
            elif key == head:
                result_dict[i].append(devices.kiv.data_types[key])
            elif 'ф.' in str(result_dict[i][0]):  # Works with kiv.xlsx for a phase-parameters
                if str(result_dict[i][0]).startswith(key):
                    result_dict[i].append(devices.kiv.data_types[key])
        if len(result_dict[i]) < 2:
            result_dict[i].append("other")
    for i in range(len(result_dict)):
        if result_dict[i][0].find("ф.") == -1:
            result_dict[i].append('overall')
        else:
            codename = sadzax.Trimmer.right((sadzax.Trimmer.left(source_dict[i][0],
                                                                 source_dict[i][0].find("ф.") + 3)), 1) + '0'
            source_dict[i].append(codename)
        if 'ф.' in str(result_dict[i][0]):  # Works with kiv.xlsx for a phase-parameters
            result_dict[i].append("MV")
        else:
            result_dict[i].append('no_voltage')
    for i in range(len(source_dict)):
        for a_key in devices.kiv.data_search_name:
            if sadzax.Trimmer.left(source_dict[i][0], len(a_key)) == a_key and 'ф.' in str(result_dict[i][0]):
                source_dict[i].append(devices.kiv.data_search_name[a_key][0])
                source_dict[i].append(devices.kiv.data_search_name[a_key][1])
        if len(source_dict[i]) < 5:
            source_dict[i].append('no_name')
            source_dict[i].append('no_name')
    for i in range(len(source_dict)):
        source_dict[i].append(source_dict[i][4] + '_' + source_dict[i][3])
    return result_dict

cols_dict = kiv_xlsx_columns_analyzer(cols_dict)

data = pd.DataFrame(df.values[4:], columns=cols_list)

ex1 = '∆tg_MV'
ex2 = '∆C_MV'


plots.flat_graph(cols=cols_dict, data=data, input_x='time', input_y=[ex1])