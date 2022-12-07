import numpy as np
import pandas as pd
import analyzer
import columns
import plots
import warnings
import matplotlib.pyplot as plt
warnings.simplefilter(action='ignore', category=FutureWarning)
cols = columns.columns_analyzer()
database = pd.read_pickle('main_dataframe.pkl')
# database = analyzer.pass_the_nan(None, cols)  # it's faster to use pickle above

plots.flat_graph(input_y=['tg_HV', 'tg_MV'], data=database)

a = analyzer.data_distribution_finder(filter_list=['time', '∆tgδ_HV'], unite_parameter=False, cols=cols, data=database)
for i in a.keys():
    plots.histogram(i, data=database, bins=333)

b = analyzer.data_average_finder(filter_list=['time', '∆tgδ_HV'], unite_parameter=False, cols=cols, data=database)

c = analyzer.data_correlation(filter_list1=['Tair,°С'], filter_list2=['Tcpu,°С'])
for i in range(len(c.keys())):
    pd.Series(c[[key for key in c.keys()][i]]).plot().xlabel([key for key in c.keys()][i])

# working ones:
# analyzer.values_time_analyzer(0, 1, cols, database)
# analyzer.data_average_finder(filter_list=['time', '∆tgδ_HV'], cols=None, data=database)
