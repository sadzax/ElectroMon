import analyzer
import columns

cols = columns.columns_analyzer()
database = analyzer.pass_the_nan(None, cols)

analyzer.values_time_analyzer(0, 1, cols, database)

analyzer.data_average_finder(filter_list=['time', '∆tgδ_HV'], abs_parameter=True, unite_parameter=True, list_of_non_math=None, cols=None, data=database)