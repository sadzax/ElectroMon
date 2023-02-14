import warnings
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import os
import columns
import devices
import plots
import prints
import sadzax
import analyzer
warnings.simplefilter(action='ignore', category=FutureWarning)
prints.clearing_script()

device_type = 'mon'
data = analyzer.get_data(device_type=device_type)
file, sep, encoding, parse_dates = devices.links(device_type)[1:5]
data[parse_dates[0]] = eval(device_type).file_parse_dates_basis[0] +eval(device_type).file_parse_dates_basis[1]
