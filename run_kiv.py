import pandas as pd
import analyzer
import columns
import devices
import plots
import prints
import sadzax
prints.clearing_script()


def save_pkl(dataframe: pd.core, name_file):
    save_path = '/save/' + name_file + '.pkl'
    dataframe.to_pickle(save_path)


device_type = 'kiv'

print('Доступные файлы для анализа:')
devices.work_file_listing(device_type)

devices.kiv.work_file = prints.work_file_picking(device_type)


print('Чтение и обработка файла...')
database = analyzer.get_data(device_type=device_type, raw_param=False)
cols = columns.columns_analyzer(device_type=device_type)
print('Чтение и обработка файла...')

data = database.copy()
data_slices = analyzer.values_time_slicer(device_type=device_type, data=data)
data = analyzer.values_time_slicer_choose(sliced_dict=data_slices)

data = analyzer.pass_the_nan(device_type=device_type, data=data, cols=cols)

time_analyzer_dict = analyzer.values_time_analyzer(device_type=device_type, data=data)
print(analyzer.values_time_analyzer_df(time_analyzer_dict))

prints.info('Подсчёт общего количества записей')
log_total = analyzer.total_log_counter(data=data)
print(f'Общее число записей в журнале измерений составило {log_total}')