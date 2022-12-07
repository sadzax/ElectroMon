import matplotlib.pyplot as plt
import pandas as pd
import columns
import analyzer
import devices
database = pd.read_pickle('main_dataframe.pkl')


def flat_graph(input_x: str = None,
               input_y: list = None,
               cols=None,
               data: pd.core = None,
               file=devices.nkvv.work_file,
               sep=devices.nkvv.work_file_sep,
               encoding=devices.nkvv.work_file_default_encoding,
               size_x: int = 14,
               size_y: int = 6):
    if data is None:
        data = analyzer.get_data(file=file, sep=sep, encoding=encoding)
    if cols is None:
        cols = columns.columns_analyzer(file=file, sep=sep, encoding=encoding)
    if input_x is None:
        input_x = 'Дата создания записи'
    if input_y is None:
        input_y = ['∆tgδ_HV', '∆tgδ_MV']
    fig, axs = plt.subplots(figsize=(size_x, size_y))
    axs.grid(axis='both', color='gray', linestyle='--')
    plt.xlabel(input_x)
    df_x = analyzer.data_filter(input_x, cols=cols, data=data)
    plt.ylabel(', '.join(input_y))
    df_y = analyzer.data_filter(input_y, cols=cols, data=data)
    legend = []
    for y_name in [col for col in df_y.columns]:
        x = df_x[input_x].tolist()
        y = df_y[y_name].tolist()
        legend.append(y_name)
        axs.plot(x, y)
        plt.legend(legend)


def histogram(value, data: pd.core = None, bins=333, file=devices.nkvv.work_file, sep=devices.nkvv.work_file_sep, encoding=devices.nkvv.work_file_default_encoding):
    if data is None:
        data = analyzer.get_data(file=file, sep=sep, encoding=encoding)
    data[value].hist(bins=bins)
    # if value = list:
    # a = analyzer.data_deviation_finder(filter_list=['time', '∆tgδ_HV'])
    # xex = lambda b: database[b].hist()
    # return xex([i for i in a.keys()])
