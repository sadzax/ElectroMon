import warnings
import matplotlib.pyplot as plt
import pandas as pd
import columns
import devices
import plots
import sadzax
import analyzer
warnings.simplefilter(action='ignore', category=FutureWarning)

data = analyzer.get_data('kiv')


ex1 = '∆tg_MV'
ex2 = '∆C_MV'

# input_x=['datetime']
# input_y=[ex1]
# size_x: int = 14
# size_y: int = 6
# df_x = analyzer.data_filter(input_x, cols=cols, data=data)
# df_y = analyzer.data_filter(input_y, cols=cols, data=data)
# y = df_y[df_y.columns[0]].tolist()
# x = df_x[df_x.columns[0]].tolist()
# x2 = pd.to_datetime(x, format="%Y/%m/%d %H:%M:%S")
# fig, axs = plt.subplots(figsize=(size_x, size_y))
# axs.plot(x2, y)

