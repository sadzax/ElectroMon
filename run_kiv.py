import pandas as pd
import analyzer
import columns
import devices
import plots
import prints
import sadzax
prints.clearing_script()


def pkl_save(dataframe: pd.core, name_file):
    save_path = './save/' + name_file + '.pkl'
    dataframe.to_pickle(save_path)


def pkl_load(name_file):
    load_path = './save/' + name_file + '.pkl'
    return pd.read_pickle(load_path)


device_type = 'kiv'
devices.kiv.work_file = prints.work_file_picking(device_type)

print('Чтение и обработка файла...')
# database = analyzer.get_data(device_type=device_type)
# pkl_save(database, device_type)
database = pkl_load(device_type)
cols_list = columns.columns_list_maker(device_type=device_type, data=database)
cols = columns.columns_analyzer(device_type=device_type, list_for_columns=cols_list)
del cols_list
print('Обработка файла завершена')

data = database.copy()
data_slices = analyzer.values_time_slicer(device_type=device_type, data=data)
data = analyzer.values_time_slicer_choose(sliced_dict=data_slices)

data = analyzer.pass_the_nan(device_type=device_type, data=data, cols=cols)
# prints.total_log_counter(device_type=device_type, data=data)
# prints.values_time_analyzer_df(device_type=device_type, data=data)
# prints.total_nan_counter_df(device_type=device_type, data=data, cols=cols)


#  ______________________________________ MIDDLE VOLTAGE ___________________________________________

ex1 = '∆C_MV'
ex2 = '∆tg_MV'

prints.info('Анализ трендов стороны СН')

print(f'Анализ корреляции данных {ex1}, {ex2} от температуры воздуха (при корреляции изменения на графике синхронны)')
plots.correlation_plot(filter_list1=[ex1, ex2], filter_list2=['tair'], device_type=device_type, data=data, cols=cols,
                       title=f"Анализ корреляции данных {ex1}, {ex2} от температуры воздуха")

prints.average_printer(ex=ex1, data=data, cols=cols)

zzz = analyzer.data_average_finder(filter_list=[ex1], data=data, cols=cols)