#  ______________________________________ SETTING THE ENVIRONMENT ________________________________
import datetime
import io
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import analyzer
import columns
import devices
import frontend
import plots
import prints
import services
import random
sadzax.Out.reconfigure_encoding()
sadzax.Out.clear_future_warning()
dev = device_type = 'mon'
data = devices.Pkl.load(dev)
cols_list = columns.columns_list_maker(dev, data)
cols = columns.columns_analyzer(dev, cols_list)
del cols_list
story = []
trends_params = {
    '∆tg': True,
    '∆C': True,
    'Ia': False,
    'Ir': False,
    'U': False
}
ex = '∆tg_HV'

main_graph_params2 = {
    'U': 'График изменения значений напряжений',
    'Ia': 'График изменения активной составляющей токов утечек',
    'Ir': 'График изменения реактивной составляющей токов утечек',
    'tg': 'График изменения значений tgδ',
    'C': 'График изменения значений емкостей С1',
    '∆tg': 'График изменения значений ∆tgδ (изменение tgδ относительно начальных значений)',
    '∆C': 'График изменения значений ∆C/C1 (изменение емкостей С1 относительно начальных значений)'
}

main_graph_params = {
    'U': 'График изменения значений напряжений',
}

for code_key, code_desc in {'_HV': ' со стороны высокого напряжения',
                            '_MV': ' со стороны среднего напряжения'}.items():
    capture = f'Анализ значений параметров высоковольтных вводов в фазах А, В и С{code_desc}'
    temp = frontend.PDF.text(capture, frontend.style_title2)
    frontend.PDF.add_to_build_list(temp, story)
    for key, desc in main_graph_params.items():
        input_y = key + code_key
        title = desc + code_desc
        prints.print_flat_graph(input_y=[input_y], device_type=dev, data=data, cols=cols, title=title)
        img = frontend.capture_pic(width=205, height=95, hAlign='CENTER')
        frontend.PDF.add_to_build_list(img, story)
        frontend.PDF.add_to_build_list(frontend.PDF.text(f' ', frontend.style_title), story)

def capturer_for_PDF_average_with_a_logarithm(ex, data=data, cols=cols, build_list=None, width=210, height=100,
                                              hAlign='CENTER', abs_parameter=True):
    if build_list is None:
        build_list = story
    capture = frontend.capture_func(prints.average_printer, ex=ex, data=data, cols=cols, abs_parameter=abs_parameter)
    temp = frontend.PDF.text(capture, frontend.style_regular)
    frontend.PDF.add_to_build_list(temp, build_list)
    #  Choose random number from color list
    specify_color_counter = random.randint(0, len(frontend.plot_colors))
    #  Two plots - simple and logarithmic
    a = plots.histogram(value=[ex], bins=99, data=data, cols=cols, logarithm=False,
                        title=f'Распределение значений {ex}',
                        specify_color_counter=specify_color_counter)
    b = plots.histogram(value=[ex], bins=99, data=data, cols=cols, logarithm=True,
                        title=f'Логарифмическое распределение значений {ex}',
                        specify_color_counter=specify_color_counter)
    img = frontend.capture_pic_two_cols(a=a, b=b, width=width, height=height, hAlign=hAlign)
    frontend.PDF.add_to_build_list(img, build_list)


#  Average values of [∆C, ∆tg, Ia, Ir, U] and their distribution added as an object for reportlab/PD
for a_key in trends_params.keys():
    for a_voltage in ['_HV', '_MV']:
        ex = a_key+a_voltage
        capturer_for_PDF_average_with_a_logarithm(ex=ex, abs_parameter=trends_params[a_key], build_list=story)
        frontend.PDF.add_to_build_list(frontend.PDF.text(f' ', frontend.style_title), story)

frontend.PDF.builder(story,
                     filename='reports/EM_report_' + 'TEST' + '.pdf')





















#  Take the warning map for a sequence
for k in devices.links(device_type)[10]:
    #  Set the default warning values (1 / 1.5% for delta_tangent and 3 / 5% for delta_correlation)
    w0 = devices.links(device_type)[10][k][0]
    w1 = devices.links(device_type)[10][k][1]
    #  Title
    capture = f'\nПревышение уровней {k} для срабатывания ' \
              f'предупредительной (±{w0}) или аварийной (±{w1}) сигнализации \r'
    temp = frontend.PDF.text(capture, frontend.style_title)
    frontend.PDF.add_to_build_list(temp, story)
    #  Main operation - forming a dict with a DataFrames of warning issues
    warning_finder = analyzer.warning_finder([k], dev, data, cols, w0, w1)
    #  Setting the short/full output
    status = sadzax.question(
        f"Вывести кратко? \n (Только срабатывания аварийной сигнализации {k} без предупредительной)"
        f" \n Eсли нет - то будут выведены и предупредительные, и аварийные замеры ", yes='y', no='n')
    warnings_codes_temporal_list = {'acc': 'аварийной'}
    if status == 'n':
        warnings_codes_temporal_list = {'war': 'предупредительной', 'acc': 'аварийной'}
    for warn_code, warn_code_str in warnings_codes_temporal_list.items():
        capture = frontend.capture_func(prints.warning_printer, dev, warning_finder, warn_code,
                                        warning_param_war=w0, warning_param_acc=w1)
        temp = frontend.PDF.text(capture, frontend.style_regular)
        frontend.PDF.add_to_build_list(temp, story)
        #  Setting minimal amount of values to be printed in a table
        min_values_for_print = 60
        #  Easing the main operated data to form a DataFrame
        warning_finder_ease = analyzer.warning_finder_ease(warning_finder, dev, warn_code,
                                                           warning_param_war=w0, warning_param_acc=w1,
                                                           min_values_for_print=min_values_for_print)
        capture = warning_finder_ease
        #  Form table from DataFrame
        temp = frontend.PDF.table_from_df(capture, title=f'Таблица периодов непрерывной сигнализации'
                                                               f' (минимум {min_values_for_print} сигнальных'
                                                               f' замеров подряд)',
                                          style_of_body=frontend.style_body, style_of_title=frontend.style_title,
                                          colWidths=[180, 110, 110, 70])
        frontend.PDF.add_to_build_list(temp, story)
        warning_finder_merge = analyzer.warning_finder_merge(warning_finder, dev, data, warn_code, w0, w1)
        buffer = frontend.capture_on_pic()
        plots.scatter(df=warning_finder_merge, device_type=dev, title=f'График {warn_code_str} сигнализации',
                      scatter_size = 0.5)
        img = frontend.capture_pic(width=205, height=95, hAlign='CENTER')
        frontend.PDF.add_to_build_list(img, story)




name_file_by_user = sadzax.Enter.str('Введите имя файла для сохранения: ',
                                     arg_must_be=sadzax.Enter.allowed_symbs_default, arg_max_capacity=24,
                                     arg_error='Некорректное имя для файла')
#  Filename String
fst0 = analyzer.total_periods(dev, data)[0].strftime(format='%y%m%d')
fst1 = analyzer.total_periods(dev, data)[1].strftime(format='%y%m%d')

frontend.PDF.builder(story,
                     filename='reports/EM_report_' + dev + '_' + fst1 + '_' + fst0 + ' - ' + name_file_by_user + '.pdf')








a = plots.histogram(value=[ex], bins=99, data=data, cols=cols, logarithm=False,
                title=f'Распределение значений {ex}')

a = plots.correlation_plot(filter_list1=[ex], filter_list2=['tair'],
                           device_type=device_type, data=data, cols=cols,
                           title=f"Зависимость {ex} от температуры воздуха")


#  Correlation with and air operative function
# noinspection PyPep8Naming
def capturer_for_PDF_air_correlation_double_HV_and_MV(ex, data=data, cols=cols, build_list=None,
                                                      width=200, height=100, hAlign='CENTER'):
    if build_list is None:
        build_list = story
    a = plots.correlation_plot(filter_list1=[ex+'_HV'], filter_list2=['tair'],
                               device_type=device_type, data=data, cols=cols,
                               title=f"Зависимость {ex} от температуры воздуха")
    b = plots.correlation_plot(filter_list1=[ex+'_MV'], filter_list2=['tair'],
                               device_type=device_type, data=data, cols=cols,
                               title=f"Зависимость {ex} от температуры воздуха")
    img = frontend.capture_pic_two_cols(a=a, b=b, width=width, height=height, hAlign=hAlign)
    frontend.PDF.add_to_build_list(img, build_list)


#  Average values of [∆C, ∆tg, Ia, Ir, U] and their distribution added as an object for reportlab/PD
for a_key in trends_params.keys():
    ex = a_key
    capturer_for_PDF_air_correlation_double_HV_and_MV(ex, build_list=story)
    frontend.PDF.add_to_build_list(frontend.PDF.text(f' ', frontend.style_title), story)


#  Step 2 lines after submodule
frontend.PDF.add_to_build_list(frontend.PDF.text(f' ', frontend.style_title), story)
frontend.PDF.add_to_build_list(frontend.PDF.text(f' ', frontend.style_title), story)















ex = '∆C'
a = plots.correlation_plot(filter_list1=[ex + '_MV'], filter_list2=['tair'], device_type=dev, data=data, cols=cols, title=f"Зе {ex} от здуха")
b = plots.correlation_plot(filter_list1=[ex + '_HV'], filter_list2=['tair'], device_type=dev, data=data, cols=cols, title=f"За {ex} от теуха")


figure3 = plt.figure(figsize=(12.8, 4.8))
grid = figure3.add_gridspec(1, 2)

buffer = io.BytesIO()
a.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
buffer.seek(0)
ax1 = figure3.add_subplot(grid[0, 0])
ax1.axis('off')
ax1.imshow(plt.imread(buffer))

buffer = io.BytesIO()
b.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
buffer.seek(0)
ax2 = figure3.add_subplot(grid[0, 1])
ax2.axis('off')
ax2.imshow(plt.imread(buffer))

figure3.tight_layout()
figure3.show()



plots.correlation_plot(filter_list1=[ex + '_MV'], filter_list2=['tair'], device_type=dev, data=data, cols=cols, title=f"Зе {ex} от здуха")
plots.correlation_plot(filter_list1=[ex + '_HV'], filter_list2=['tair'], device_type=dev, data=data, cols=cols, title=f"За {ex} от теуха")
