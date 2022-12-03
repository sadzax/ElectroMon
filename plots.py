import matplotlib.pyplot as plt
import columns
import analyzer

#  Get variable for data
cols = columns.columns_analyzer()
cols_len = len(columns.columns_maker())
database = analyzer.get_data()


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


def histogram(val=columns.paste_values_rus[4], bin_parameter=100):
    # df = analyzer.data_filter([val])  # AttributeError: partially initialized module 'analyzer_main' has no attribute 'data_filter' (most likely due to a circular import)
    database[val].hist(bin=bin_parameter)


print(histogram())