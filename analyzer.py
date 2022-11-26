import pandas as pd
import matplotlib.pyplot as plt
import columns
import devices


def get_data(usecols: list = None, file=devices.nkvv.work_file, sep=devices.nkvv.work_file_sep,
             encoding=devices.nkvv.work_file_default_encoding):
    if usecols is None:
        parse_dates = devices.nkvv.nkvv.work_file_parse_dates
    else:
        cols = []
        for k in usecols:
            if k in devices.nkvv.work_file_parse_dates:
                cols.append(k)
        parse_dates = cols
    data = pd.read_csv(file,
                       sep=sep,
                       encoding=encoding,
                       parse_dates=parse_dates,
                       usecols=usecols,
                       dayfirst=True)
    return data


def plot_2d_simple(val_x: str, val_y: str, size_x: int = 14, size_y: int = 4):
    df = get_data([val_x, val_y])
    fig, axs = plt.subplots(figsize=(size_x, size_y))
    plt.xlabel(val_x)
    plt.ylabel(val_y)
    x = df[val_x].tolist()
    y = df[val_y].tolist()
    axs.plot(x, y)


def columns_dict(columns_of_file=columns.rus):
    columns_dict_maker = {k: v for v, k in enumerate(columns_of_file)}
    return columns_dict_maker
