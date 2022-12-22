import pandas as pd
import analyzer
import columns
import plots
import devices
import warnings

answer_list = {'yes': ['yes', 'ye', 'yeah', 'ok', 'y', 'да', 'ага', 'ок', 'хорошо', 'давай', 'го', 'д', 'lf'], 'no': ['no', 'nope', 'nah', 'n', 'нет', 'не', 'не надо', 'н', 'не-а', 'yt', 'ytn']}
warnings.simplefilter(action='ignore', category=FutureWarning)
cols = columns.columns_analyzer()
# database = analyzer.pass_the_nan(None, cols)  # it's faster to use pickle below
# database.to_pickle('main_dataframe.pkl')
database = pd.read_pickle('main_dataframe.pkl')
data = database

log_total = analyzer.total_log_counter(data=database)
print(f"\nОбщее число записей в журнале измерений составило {log_total}")


subprocess = 'Анализ периодичности и неразрывности измерений'
print(f"\n {subprocess}...")
log_time = analyzer.values_time_analyzer(data=database)
log_time_df = analyzer.values_time_analyzer_df(source_dict=log_time, orient='index')
if len(log_time) == 0:
    print(f"\n Периоды измерений НКВВ не нарушены")
else:
    print(f"\n Выявлено {len(log_time)} нарушений периодов измерений НКВВ")
    answer1 = input(f"\n Хотите вывести подробные данные? ")
    for i in answer_list['yes']:
        if answer1 == i:
            print("\n", log_time_df, "\n")

subprocess = 'Анализ периодов массовой некорректности измерений (более 33% данных)'
print(f"\n {subprocess}...")
log_nans = analyzer.total_nan_counter(data=database, cols=cols)
log_nans_df = analyzer.total_nan_counter_df(source_dict=log_nans, orient='index')
if len(log_nans) == 0:
    print(f"\n Периоды некорректных измерений не выявлены")
else:
    print(f"\n Выявлено {len(log_nans)} замеров с некорректными данными НКВВ")
    answer2 = input(f"\n Хотите вывести примеры некорректных данных?")


print(f"\n")

print(f"\nСреднее отклонение ∆tgδ стороны ВН составляет"
      # f" по модулю {round(sum(delta_tg_HV_check) / len(delta_tg_HV_check), 3)}%"
      # f" при общем количестве {len(delta_tg_HV_check)} "
      f"показателей (исключены значения '∆tgδ = -10')")
print(f"\nПревышение уровня ∆tgδ ±1% для срабатывания"
      # f" предупредительной сигнализации: {len(analyzer.delta_tg_checker_warning())}"
      # f" случая(-ев) \n {analyzer.delta_tg_checker_warning()}' - "
      f"")
