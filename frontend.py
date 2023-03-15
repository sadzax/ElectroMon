import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import sys
import io
import os
import analyzer
import columns
import devices
import plots
import prints
import sadzax

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from matplotlib.backends.backend_pdf import PdfPages

pdfmetrics.registerFont(TTFont('Verdana', 'misc/Verdana.ttf'))
styles = getSampleStyleSheet()
style_body = styles["BodyText"]
style_body.wordWrap = 'CJK'
style_body.fontName = 'Verdana'
style_body.fontSize = 8
style_body.alignment = 1
style_title = styles["Heading1"]
style_title.wordWrap = 'CJK'
style_title.fontName = 'Verdana'
style_title.fontSize = 10
style_title.alignment = 1
style_title2 = styles["Heading2"]
style_title2.wordWrap = 'CJK'
style_title2.fontName = 'Verdana'
style_title2.fontSize = 12
style_title2.alignment = 0


def capture_func(func, *args, **kwargs):
    output_buffer = io.StringIO()
    sys.stdout = output_buffer
    func(*args, **kwargs)
    output = output_buffer.getvalue()
    sys.stdout = sys.__stdout__
    return output


def capture_prev():
    original_stdout = sys.stdout
    buffer = io.StringIO()
    sys.stdout = buffer
    print('aaa')
    output = buffer.getvalue()
    sys.stdout = original_stdout
    return output


def capture_on():
    buffer = io.StringIO()
    sys.stdout = buffer
    return buffer


def capture_off(buffer, n=1):
    stdout_messages = buffer.getvalue().split('\n')
    sys.stdout = sys.__stdout__
    return '\n'.join(stdout_messages[-n-1:])


def get_previous_stdout(n):
    # Redirect stdout to a buffer
    buffer = io.StringIO()
    sys.stdout = buffer

    # Call print statements
    print("This is the first message")
    print("This is the second message")
    print("This is the third message")
    print("This is the fourth message")
    print("This is the fifth message")

    # Get the stdout messages and split by newline
    stdout_messages = buffer.getvalue().split('\n')

    # Restore stdout
    sys.stdout = sys.__stdout__

    # Return the last n messages
    return '\n'.join(stdout_messages[-n-1:])

# Call the function to get the last 3 stdout messages
print(get_previous_stdout(1))



class PDF:
    def builder(self, filename='output.pdf'):
        if isinstance(self, list) is True:
            doc = SimpleDocTemplate(filename, pagesize=A4)
            doc.build(self)

    def table_from_df(self, title='', style_body=style_body, style_title=style_title):
        table_data = []
        for row in [list(self.columns)] + self.values.tolist():
            new_row = []
            for item in row:
                p = Paragraph(str(item), style=style_body)
                new_row.append(p)
            table_data.append(new_row)
        table = Table(table_data, colWidths=[80, 40, 40, 65, 60, 120, 130])
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                   ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                   ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                   ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                                   ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                   ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                                   ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                                   ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                                   ('GRID', (0, 0), (-1, -1), 1, colors.grey)]))
        title = Paragraph(str(title), style=style_title)
        return [title, table]

    def text(self, style=style_body):
        txt = Paragraph(str(self), style=style)
        return [txt]