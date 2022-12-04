import pandas as pd
import analyzer
import columns
import plots
cols = columns.columns_analyzer()
database = pd.read_pickle('main_dataframe.pkl')
# database = analyzer.pass_the_nan(None, cols) - it's faster to use pickle above
a = analyzer.data_deviation_finder(filter_list=['time', '∆tgδ_HV'], unite_parameter=False, cols=cols, data=database)
for i in a.keys():
    plots.histogram(i)

# working ones:
analyzer.values_time_analyzer(0, 1, cols, database)
analyzer.data_average_finder(filter_list=['time', '∆tgδ_HV'], cols=None, data=database)
