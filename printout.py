import pandas as pd
import analyzer
import columns
import plots
import devices
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
cols = columns.columns_analyzer()
database = analyzer.pass_the_nan(None, cols)
database.to_pickle('main_dataframe.pkl')









print(analyzer.values_time_analyzer())
print(f"\nОбщее число записей в журнале измерений составило {analyzer.total_log_counter()}")

print(f"\nСреднее отклонение ∆tgδ стороны ВН составляет"
      f" по модулю {round(sum(delta_tg_HV_check) / len(delta_tg_HV_check), 3)}%"
      f" при общем количестве {len(delta_tg_HV_check)} показателей (исключены значения '∆tgδ = -10')")
print(f"\nПревышение уровня ∆tgδ ±1% для срабатывания"
      f" предупредительной сигнализации: {len(analyzer.delta_tg_checker_warning())}"
      f" случая(-ев) \n {analyzer.delta_tg_checker_warning()}")
