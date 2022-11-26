import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import columns


def plot_2d_simple(val_x: str, val_y: str, size_x: int = 14, size_y: int = 4):
    df = get_data([val_x, val_y])
    fig, axs = plt.subplots(figsize=(size_x, size_y))
    plt.xlabel(val_x)
    plt.ylabel(val_y)
    x = df[val_x].tolist()
    y = df[val_y].tolist()
    axs.plot(x, y)