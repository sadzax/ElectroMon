import numpy as np
import pandas as pd
import analyzer
import columns
import plots
import warnings
import matplotlib.pyplot as plt
from analyzer import data_filter
warnings.simplefilter(action='ignore', category=FutureWarning)
cols = columns.columns_analyzer()
database = pd.read_pickle('main_dataframe.pkl')
data = database
# database = analyzer.pass_the_nan(None, cols)  # it's faster to use pickle above

plots.correlation_plot(filter_list1=['∆tgδ_HV'], filter_list2=['∆tgδ_MV'])


#  Okay
plots.flat_graph(input_y=['tg_HV', 'tg_MV'], data=database)

a = analyzer.data_distribution_finder(filter_list=['time', '∆tgδ_HV'], unite_parameter=False, cols=cols, data=database)
for i in a.keys():
    plots.histogram(i, data=database, bins=333)

b = analyzer.data_average_finder(filter_list=['time', '∆tgδ_HV'], unite_parameter=False, cols=cols, data=database)

c = analyzer.data_correlation(filter_list1=['∆tgδ_HV'], filter_list2=['∆tgδ_MV'])
for i in range(len(c.keys())):
    keys_list = [key for key in c.keys()]
    pd.Series(c[keys_list[i]]).plot().xlabel(keys_list[i]).legend(keys_list[i])

#  Working ones:
# analyzer.values_time_analyzer(0, 1, cols, database)
# analyzer.data_average_finder(filter_list=['time', '∆tgδ_HV'], cols=None, data=database)
