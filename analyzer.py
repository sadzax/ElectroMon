import pandas as pd
import matplotlib.pyplot as plt
import columns
import devices


def get_data(usecols: list = None, file=devices.nkvv.work_file, sep=devices.nkvv.work_file_sep,
             encoding=devices.nkvv.work_file_default_encoding):
    if usecols is None:
        parse_dates = devices.nkvv.nkvv.work_file_parse_dates
    else:
        cols = []
        for k in usecols:
            if k in devices.nkvv.work_file_parse_dates:
                cols.append(k)
        parse_dates = cols
    data = pd.read_csv(file,
                       sep=sep,
                       encoding=encoding,
                       parse_dates=parse_dates,
                       usecols=usecols,
                       dayfirst=True)
    return data

