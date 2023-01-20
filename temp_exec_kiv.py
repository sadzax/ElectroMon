import warnings
import matplotlib.pyplot as plt
import pandas as pd
import columns
import devices
import plots
import sadzax
import analyzer
warnings.simplefilter(action='ignore', category=FutureWarning)

device_type = 'kiv'
data = analyzer.get_data(device_type)
cols = columns.columns_analyzer(device_type)

datas = analyzer.values_time_slicer(data, 1439, 300, device_type=device_type, full_param=False)

df = datas[list(datas.keys())[0]][0]


def test_plot():
    input_x=['time']
    input_y=['U_MV']
    size_x = 14
    size_y = 6
    df_x = analyzer.data_filter(input_x, cols=cols, data=df)
    df_y = analyzer.data_filter(input_y, cols=cols, data=df)
    x = df_x[df_x.columns[0]].tolist()
    y = df_y[df_y.columns[0]].tolist()
    x2 = x[:100]
    y2 = y[:100]
    fig, axs = plt.subplots(figsize=(size_x, size_y))
    plt.xlabel(', '.join(input_x))
    plt.ylabel(', '.join(input_y))
    axs.grid(axis='both', color='gray', linestyle='--')
    axs.plot(x, y)
