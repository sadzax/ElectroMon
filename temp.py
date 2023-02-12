import warnings
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import os
import columns
import devices
import plots
import sadzax
import analyzer
warnings.simplefilter(action='ignore', category=FutureWarning)
import pathlib

device_type = 'mon'

d = pd.read_csv('ffile', delimiter=r"\s+", encoding='WINDOWS-1251')

for filepath in pathlib.Path('db').glob('**/*'):
    print(filepath.name)

