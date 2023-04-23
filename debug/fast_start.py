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
import sadzax
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageTemplate, Frame, Image
sadzax.Out.reconfigure_encoding()
sadzax.Out.clear_future_warning()
#  ______________________________________ OBTAINING DATA _________________________________________
device_type = prints.device_picking()
# device_type = 'mon'
dev = device_type
# prints.file_picking(dev)
data = devices.Pkl.load(dev)
# data = analyzer.stack_data(dev)
cols_list = columns.columns_list_maker(dev, data)
cols = columns.columns_analyzer(dev, cols_list)
del cols_list
data = analyzer.pass_the_nan(device_type=device_type, data=data, cols=cols)  # update data_types
data = analyzer.set_dtypes(device_type=device_type, data=data, cols=cols)
# devices.Pkl.save(device_type=device_type, data=data)

#  ______________________________________ GO TESTINGS ____________________________________________
build_list = []
#  Returning device name and adding it as an object for reportlab/PDF
build_temp = frontend.PDF.text(f'Отчёт по устройству', frontend.style_title)
frontend.PDF.add_to_build_list(build_temp, build_list)
capture = devices.links(device_type)[9]
build_temp = frontend.PDF.text(capture, frontend.style_title2)
frontend.PDF.add_to_build_list(build_temp, build_list)
ffffnn = '1.pdf'


def capture_pic(width=160, height=160, hAlign='CENTER'):
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    return Image(buffer, width=width*mm, height=height*mm, hAlign=hAlign)


plots.histogram(['∆tg'], bins=66, data=data, cols=cols, title=f'Распределение значений')
img = capture_pic()
build_list.append(img)

plots.histogram(['∆C'], bins=66, data=data, cols=cols, title=f'Распределение значений')
img = capture_pic()
build_list.append(img)

doc = SimpleDocTemplate(ffffnn, pagesize=A4)
doc.build(build_list)


plots.histogram(['∆tg'], bins=66, data=data, cols=cols, title=f'Распределение значений')
buffer = io.BytesIO()
plt.savefig(buffer, format='png')
plt.close()
buffer.seek(0)
img = Image(buffer, width=180, height=160, hAlign='LEFT')

