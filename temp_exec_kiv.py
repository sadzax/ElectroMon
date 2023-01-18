import warnings
import matplotlib.pyplot as plt
import pandas as pd
import columns
import devices
import plots
import sadzax
import analyzer
warnings.simplefilter(action='ignore', category=FutureWarning)

device_type='kiv'
data = analyzer.get_data(device_type)
cols = columns.columns_analyzer(device_type)

def test_plot():
    input_x=['time']
    input_y=['U_MV']
    size_x = 14
    size_y = 6
    df_x = analyzer.data_filter(input_x, cols=cols, data=data)
    df_y = analyzer.data_filter(input_y, cols=cols, data=data)
    x = df_x[df_x.columns[0]].tolist()
    y = df_y[df_y.columns[0]].tolist()
    x2 = x[:100]
    y2 = y[:100]
    fig, axs = plt.subplots(figsize=(size_x, size_y))
    plt.xlabel(', '.join(input_x))
    plt.ylabel(', '.join(input_y))
    axs.grid(axis='both', color='gray', linestyle='--')
    axs.plot(x2, y2)
    plots.flat_graph(['time'], ['U_MV'], device_type='kiv', data=data, cols=cols)


