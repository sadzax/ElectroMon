import matplotlib.pyplot as plt
import pandas as pd
import columns
import analyzer


def plot2(val_x: str = columns.paste_values_rus[0],
          val_y: str = columns.paste_values_rus[4],
          size_x: int = 14,
          size_y: int = 4):
    df = analyzer.get_data([val_x, val_y])
    fig, axs = plt.subplots(figsize=(size_x, size_y))
    plt.xlabel(val_x)
    plt.ylabel(val_y)
    axs.grid(axis='both', color='gray', linestyle='--')
    x = df[val_x].tolist()
    y = df[val_y].tolist()
    axs.plot(x, y)


database = pd.read_pickle('main_dataframe.pkl')


def histogram(value, bin_parameter=100):
    database[value].hist(bins=bin_parameter)
    # if value = list:
    # a = analyzer.data_deviation_finder(filter_list=['time', '∆tgδ_HV'])
    # xex = lambda b: database[b].hist()
    # return xex([i for i in a.keys()])
