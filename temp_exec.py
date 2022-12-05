import pandas as pd
import numpy as np
import analyzer
import columns
import plots
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
cols = columns.columns_analyzer()
database = pd.read_pickle('main_dataframe.pkl')
# database = analyzer.pass_the_nan(None, cols) - it's faster to use pickle above

a = analyzer.data_distribution_finder(filter_list=['time', '∆tgδ_HV'], unite_parameter=False, cols=cols, data=database)
for i in a.keys():
    plots.histogram(i, data=database, bins=333)

b = analyzer.data_average_finder(filter_list=['time', '∆tgδ_HV'], unite_parameter=False, cols=cols, data=database)

c = analyzer.data_correlation(filter_list1=['∆tgδ_HV'], filter_list2=['temperature'])
for i in c.keys():
    print(i)

c1 = c[[i for i in c.keys()][2]]

# working ones:
# analyzer.values_time_analyzer(0, 1, cols, database)
# analyzer.data_average_finder(filter_list=['time', '∆tgδ_HV'], cols=None, data=database)
