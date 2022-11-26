import csv
import pandas as pd
import matplotlib.pyplot as plt
import columns
import devices
import analyzer


def plot2(val_x: str = columns.rus[0], val_y: str = columns.rus[2], size_x: int = 14, size_y: int = 4):
    df = analyzer.get_data([val_x, val_y])
    fig, axs = plt.subplots(figsize=(size_x, size_y))
    plt.xlabel(val_x)
    plt.ylabel(val_y)
    axs.grid(axis='both', color='gray', linestyle='--')
    x = df[val_x].tolist()
    y = df[val_y].tolist()
    axs.plot(x, y)