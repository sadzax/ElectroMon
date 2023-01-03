import os
import devices
import pandas as pd

kiv = devices.Device()
devices.kiv.work_file_folder = 'upload/kiv/'
devices.kiv.file_names_starts = {'measure': 'MeasJ', 'event': 'WorkJ'}

a = [filename for filename in os.listdir(devices.kiv.work_file_folder)
     if filename.startswith(devices.kiv.file_names_starts['measure'])]
for i in a:
    measj = ("upload/kiv/" + i)

measj = ('upload/kiv/' + a[0])

df = pd.read_excel(measj)

if df.iloc[0, 0] == 'Модуль:':
    devices.kiv.serial_number = df.iloc[0, 3]

def kiv_columns_maker():
    if df.iloc[0, 0] == 'Модуль:':
        df.columns = df.iloc[3]

columns = df.iloc[3]