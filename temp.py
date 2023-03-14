import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import os
import analyzer
import columns
import devices
import plots
import prints
import sadzax
sadzax.Out.reconfigure_encoding()
sadzax.Out.clear_future_warning()

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

data.info()
cols_df = columns.columns_df(dev, cols)

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from matplotlib.backends.backend_pdf import PdfPages


doc = SimpleDocTemplate("output.pdf", pagesize=A4)

# Adding Pandas DataFrame Table to PDF File

pdfmetrics.registerFont(TTFont('Verdana', 'misc/Verdana.ttf'))
table = Table([list(cols_df.columns)] + cols_df.values.tolist(),
              colWidths=[70, 40, 40, 65, 60, 120, 130])
table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                           ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('FONTNAME', (0, 0), (-1, 0), 'Verdana'),
                           ('FONTSIZE', (0, 0), (-1, 0), 10),
                           ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                           ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                           ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                           ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                           ('FONTNAME', (0, 1), (-1, -1), 'Verdana'),
                           ('FONTSIZE', (0, 1), (-1, -1), 10),
                           ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                           ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
doc.build([table])



import PyPDF2


pdf_file = open('example.pdf', 'rb')
pdf_reader = PyPDF2.PdfFileReader(pdf_file)
pdf_writer = PyPDF2.PdfFileWriter()

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
df = cols_df
c = canvas.Canvas("output.pdf", pagesize=letter)
ddata = [df.columns.tolist()] + df.values.tolist()
t = Table(ddata, repeatRows=1)
t.setStyle(TableStyle([
    ('FONTSIZE', (0,0), (-1,-1), 16),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TEXTCOLOR', (0,0), (-1,0), colors.black),
    ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ('BOX', (0,0), (-1,-1), 1, colors.black),
    ('GRID', (0,0), (-1,-1), 1, colors.lightgrey),
]))

t.wrapOn(c, inch, inch)
t.drawOn(c, 0, 0)

c.save()



from matplotlib.backends.backend_pdf import PdfPages

with PdfPages('table.pdf') as pdf:
    fig = plt.figure(figsize=(8.27, 11.69), dpi=100)  # A4 page size in inches
    ax = fig.add_subplot(111)
    table = ax.table(cellText=cols_df.values,
                     colLabels=cols_df.columns,
                     loc='center',
                     cellLoc='center',
                     fontsize=16)
    ax.set_title('Данные устройства и их соотнесение к параметрам', fontsize=20)
    for key, cell in table.get_celld().items():
        cell.set_linewidth(0)
    pdf.savefig(fig)





fig, ax = plt.subplots()
ax.axis('tight')
ax.axis('off')
ax.set_fontsize(14)

the_table = ax.table(cellText=cols_df.values, colLabels=cols_df.columns, loc='center', cellloc='center', fontsize=16)
pp = PdfPages("foo.pdf")
pp.savefig(fig, bbox_inches='tight')
pp.close()
