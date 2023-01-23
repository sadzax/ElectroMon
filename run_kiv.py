import sys
import warnings
import pandas as pd
import analyzer
import columns
import devices
import plots
warnings.simplefilter(action='ignore', category=FutureWarning)
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')


def info_print(the_string):
    print(f'\n\n          {the_string}...\r')


def save_pkl(dataframe: pd.core, name_file):
    save_path = '/save/' + name_file + '.pkl'
    dataframe.to_pickle(save_path)


def answering(question, yes='', no='', answer_list=None):
    answer = input(f'  {question}  ')
    if answer_list is None:
        answer_list = {'yes': ['yes', 'ye', 'yeah', 'ok', 'y', 'да', 'ага', 'ок', 'хорошо', 'давай', 'го', 'д', 'lf'],
                       'no': ['no', 'nope', 'nah', 'n', 'нет', 'не', 'не надо', 'н', 'не-а', 'yt', 'ytn']}
    for answer_example in answer_list['yes']:
        if answer == answer_example:
            return yes
    for answer_example in answer_list['no']:
        if answer == answer_example:
            return no


device_type = 'kiv'

print('Чтение и обработка файла...')
database = analyzer.get_data(device_type=device_type, raw_param=False)
# save_pkl(database, device_type)
cols = columns.columns_analyzer(device_type=device_type)

data = database.copy()
data_slices = analyzer.values_time_slicer(device_type=device_type, data=data)
data = analyzer.values_time_slicer_choose(sliced_dict=data_slices)

data = analyzer.pass_the_nan(device_type=device_type, data=data, cols=cols)

time_analyzer_dict = analyzer.values_time_analyzer(device_type=device_type, data=data)
print(analyzer.values_time_analyzer_df(time_analyzer_dict))