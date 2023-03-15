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


def capture_on():
    buffer = io.StringIO()
    sys.stdout = buffer
    return buffer


def capture_off(buffer, n=1):
    stdout_messages = buffer.getvalue().split('\n')
    sys.stdout = sys.__stdout__
    print('\n'.join(stdout_messages[-n-1:]))
    return '\n'.join(stdout_messages[-n-1:])


class PDF:
    def builder(self, filename='output.pdf'):
        if isinstance(self, list) is True:
            doc = SimpleDocTemplate(filename, pagesize=A4)
            doc.build(self)

    def add_to_build_list(self, build_list: list = None):
        if build_list is None:
            build_list = []
        if isinstance(self, list) is True:
            for x in self:
                build_list.append(x)
        else:
            build_list.append([self])

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
        the_end = Paragraph(str(' \n \n'), style=style_title)
        return [title, table, the_end]

    def text(self, style=style_body):
        txt = Paragraph(str(self), style=style)
        the_end = Paragraph(str(' \n \n'), style=style_title)
        return [txt, the_end]