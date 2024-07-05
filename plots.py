import matplotlib.pyplot as plt
import pandas as pd
import analyzer
import columns
# import random
# import io
import frontend


#  Simple graph
def flat_graph(input_x: list = None,
               input_y: list = None,
               device_type='nkvv',
               data: pd.core = None,
               cols: dict = None,
               title='',
               size_x: int = 14,
               size_y: int = 6,
               alpha: float = 1.0,
               alpha_fade_out: bool = True,
               color_switcher: bool = True):
    if data is None:
        data = analyzer.get_data(device_type=device_type)
    if cols is None:
        cols = columns.columns_analyzer(device_type=device_type)
    if input_x is None:
        input_x = [columns.time_column(device_type=device_type, data=data)]
    if input_y is None:
        input_y = ['∆tg_HV', '∆tg_MV']
    fig, axs = plt.subplots(figsize=(size_x, size_y))
    axs.grid(axis='both', color='gray', linestyle='--')
    plt.title(title)
    df_x = analyzer.data_filter(input_x, cols=cols, data=data)
    plt.xlabel(str(df_x.columns[0]))
    df_y = analyzer.data_filter(input_y, cols=cols, data=data)
    plt.ylabel(', '.join(input_y))
    legend = []
    #  For the variety of colors in a report
    color_counter = frontend.color_switch(rand=color_switcher)
    color_scheme = frontend.plot_colors
    for y_name in [col for col in df_y.columns]:
        #  Choosing the colors
        color_counter = color_counter + 1
        while color_counter >= len(color_scheme):
            color_counter = color_counter - len(color_scheme)
        #  Alpha fading with every iteration
        if alpha_fade_out is True:
            alpha = alpha * 0.95
        #  Add a legend
        legend.append(y_name)
        #  MAIN Plotting
        x = df_x[df_x.columns[0]].tolist()
        y = df_y[y_name].tolist()
        axs.plot(x,
                 y,
                 alpha=alpha,
                 color=color_scheme[color_counter])
    plt.legend(legend)
    return fig


#  Histogram for raw data and distribution data
def histogram(value,
              bins=99,
              device_type='nkvv',
              title='',
              data_distribution_parameter=False,
              logarithm=False,
              ax_param=None,
              cols=None,
              data: pd.core = None,
              unite_parameter=False,
              alpha: float = 1.0,
              alpha_fade_out: bool = True,
              color_switcher: bool = True,
              specify_color_counter = None):
    if cols is None:
        cols = columns.columns_analyzer(device_type=device_type)
    if data is None:
        data = analyzer.get_data(device_type=device_type)
    legend = []
    fig, axs = plt.subplots()
    #  For the variety of colors in a report
    color_counter = frontend.color_switch(rand=color_switcher)
    if isinstance(specify_color_counter, int) is True:
        color_counter = specify_color_counter
    color_scheme = frontend.plot_colors
    #  Main branch
    if isinstance(value, str) is True:
        data[value].hist(bins=bins, log=logarithm)
        plt.title(title)
    if isinstance(value, list) is True:
        if data_distribution_parameter is True:
            #  Form a dataframe to work with
            data_distribution = analyzer.data_distribution_finder(value, data=data, cols=cols,
                                                                  unite_parameter=unite_parameter)
            for i in data_distribution:
                #  Choosing the colors
                color_counter = color_counter + 1
                while color_counter >= len(color_scheme):
                    color_counter = color_counter - len(color_scheme)
                #  Alpha fading with every iteration
                if alpha_fade_out is True:
                    alpha = alpha * 0.95
                #  Add a legend
                legend.append(i)
                #  MAIN Plotting
                data_distribution[i].hist(bins=bins,
                                          log=logarithm,
                                          color=color_scheme[color_counter],
                                          alpha=alpha)
        else:
            #  Form a dataframe to work with
            df = analyzer.data_filter(value, data=data, cols=cols)
            for i in df:
                #  Choosing the colors
                color_counter = color_counter + 1
                while color_counter >= len(color_scheme):
                    color_counter = color_counter - len(color_scheme)
                #  Alpha fading with every iteration
                if alpha_fade_out is True:
                    alpha = alpha * 0.95
                #  Add a legend
                legend.append(i)
                # plt.hist(df[i], bins=bins, log=logarithm, ax=ax_param)
                #  MAIN Plotting
                df[i].hist(bins=bins,
                           log=logarithm,
                           ax=ax_param,
                           alpha=alpha,
                           color=color_scheme[color_counter])
        plt.legend(legend)
        plt.title(title)
        plt.xlabel(', '.join(value))
        plt.ylabel('Количество значений')
        # plt.show()
        # plt.close()
        # plt.cla()
        # buffer = io.BytesIO()
        # plt.savefig(buffer)
    # buffer = io.BytesIO()
    # plt.savefig(buffer, format='png')
    # buffer.seek(0)
    # return buffer
    return fig


#  Correlation Plot
def correlation_plot(filter_list1=None,
                     filter_list2=None,
                     device_type='nkvv',
                     title='',
                     cols=None,
                     data: pd.core = None,
                     ax_param=None):
    if cols is None:
        cols = columns.columns_analyzer(device_type=device_type)
    if data is None:
        data = analyzer.get_data(device_type=device_type)
    if filter_list1 is None:
        filter_list1 = ['∆tg_HV']
    if filter_list2 is None:
        filter_list2 = ['∆tg_MV']
    cr = analyzer.data_correlation(filter_list1=filter_list1,
                                   filter_list2=filter_list2,
                                   cols=cols,
                                   data=data)
    keys_list = [key for key in cr.keys()]
    fig, axs = plt.subplots()
    axs.grid(axis='both', color='gray', linestyle='--')
    max_len = 0
    plt.title(title)
    legend = []
    for i in range(len(cr.keys())):
        if len(cr[keys_list[i]]) > max_len:
            max_len = len(cr[keys_list[i]])
            axs.set_ylim(max_len * -1, max_len)
            axs.set_xlim(0, max_len)
            legend.append(keys_list[i])
        plt.xlabel('Шаги')
        plt.ylabel('Совпадения')
        y = cr[keys_list[i]]
        legend.append(keys_list[i])
        axs.plot([i for i in range(max_len)], y)
    plt.legend(legend)
    return fig


#  Warning plots
def scatter(input_x: list = None,
            input_y: list = None,
            device_type='mon',
            df: pd.core = None,
            cols_inside: dict = None,
            title: str = '',
            size_x: int = 14,
            size_y: int = 6,
            scatter_size: float = 1,
            color=None,
            area=None):
    """
    Designed to get dataframes from analyzer.warning_finder_merge function
    """
    #  If there are only datetime and '+' and '-' warnings - don't scatter it
    if df.shape[1] < 4:
        pass
    else:
        if df is None:
            df = analyzer.get_data(device_type=device_type)
        if cols_inside is None:
            cols_inside = columns.columns_analyzer(device_type=device_type, list_for_columns=list(df.columns))
        if input_x is None:
            input_x = [columns.time_column(device_type=device_type, data=df)]
        if input_y is None:
            input_y = []
            for a_column in list(df.columns):
                if a_column in input_x:
                    pass
                else:
                    input_y.append(a_column)
        fig, axs = plt.subplots(figsize=(size_x, size_y))
        axs.grid(axis='both', color='gray', linestyle='--')
        plt.title(title)
        df_x = analyzer.data_filter(input_x, cols=cols_inside, data=df)
        plt.xlabel(str(df_x.columns[0]))
        df_y = analyzer.data_filter(input_y, cols=cols_inside, data=df)
        plt.ylabel('Значения по (' + ', '.join(input_y) + ')')
        legend = []
        for y_name in [col for col in df_y.columns]:
            x = df_x[df_x.columns[0]].tolist()
            y = df_y[y_name].tolist()
            if y_name.find('отриц.') != -1 or y_name.find('полож.') != -1:
                axs.scatter(x, y, c='k', marker='.', s=scatter_size)
            else:
                axs.scatter(x, y, c=color, s=scatter_size)
                legend.append(y_name)
        plt.legend(legend)
        return fig
