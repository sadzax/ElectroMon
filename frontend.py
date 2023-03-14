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
