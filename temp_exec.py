import pandas as pd
import analyzer
import columns
import plots
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
cols = columns.columns_analyzer()
database = pd.read_pickle('main_dataframe.pkl')
data = database
# database = analyzer.pass_the_nan(None, cols)  # it's faster to use pickle above
# database.to_pickle('main_dataframe.pkl')


analyzer.warning_finder(filter_list=['time', '∆tgδ_V'], warning_amount=1, data=database, abs_parameter=True)
analyzer.warning_finder(filter_list=['time', '∆tgδ_MV'], warning_amount=1.5, data=database, abs_parameter=True)


# Okay
plots.flat_graph(input_y=['tg_HV', 'tg_MV'], data=database)
plots.histogram(['∆tgδ_HV'], data=database, data_distribution_parameter=False)
plots.correlation_plot(filter_list1=['∆tgδ_HV'], filter_list2=['∆tgδ_MV'])
analyzer.values_time_analyzer(0, 1, cols, database)
analyzer.data_average_finder(filter_list=['time', '∆tgδ_HV'], cols=None, data=database)
