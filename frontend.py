import matplotlib.pyplot as plt
import sys
import io

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib import utils
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, PageTemplate, Frame
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.backends.backend_agg import FigureCanvasAgg

pdfmetrics.registerFont(TTFont('Verdana', 'misc/Verdana.ttf'))
styles = getSampleStyleSheet()
style_body = styles["BodyText"]
style_body.wordWrap = 'CJK'
style_body.fontName = 'Verdana'
style_body.fontSize = 8
style_body.alignment = 1
style_regular = styles["BodyText"]
style_regular.wordWrap = 'CJK'
style_regular.fontName = 'Verdana'
style_regular.fontSize = 8
style_regular.alignment = 0
style_title = styles["Heading1"]
style_title.wordWrap = 'CJK'
style_title.fontName = 'Verdana'
style_title.fontSize = 10
style_title.alignment = 1
style_title.spaceAfter = 3
style_title2 = styles["Heading2"]
style_title2.wordWrap = 'CJK'
style_title2.fontName = 'Verdana'
style_title2.fontSize = 14
style_title2.alignment = 1

PAGE_WIDTH, PAGE_HEIGHT = A4


class MyDocTemplate(SimpleDocTemplate):
    def __init__(self, filename, **kw):
        super().__init__(filename, pagesize=(PAGE_WIDTH, PAGE_HEIGHT), **kw)
        margin_left = 25 * mm
        margin_right = 25 * mm
        margin_top = 25 * mm
        margin_bottom = 20 * mm
        self.addPageTemplates([
            PageTemplate(
                id='OneCol',
                frames=[
                    Frame(
                        margin_left,
                        margin_bottom,
                        PAGE_WIDTH - margin_left - margin_right,
                        PAGE_HEIGHT - margin_bottom - margin_top,
                        id='Normal'
                    )
                ],
                onPage=self.add_page_number,
            ),
        ])

    def add_page_number(self, canvas, doc):
        page_num = canvas.getPageNumber()
        PAGE_NUM_POS_X = PAGE_WIDTH - 40 * mm
        PAGE_NUM_POS_Y = 15 * mm
        canvas.saveState()
        canvas.setFont('Verdana', 8)
        canvas.drawString(PAGE_NUM_POS_X, PAGE_NUM_POS_Y, f'Стр. {page_num}')
        canvas.restoreState()


def capture_on():
    buffer = io.StringIO()
    sys.stdout = buffer
    return buffer


def capture_off(buffer):
    stdout_messages = buffer.getvalue()
    sys.stdout = sys.__stdout__
    print(stdout_messages)
    return stdout_messages


def capture_on_pic():
    return io.BytesIO()


def capture_func(func, *args, **kwargs):
    buffer = capture_on()
    func(*args, **kwargs)
    capture = capture_off(buffer)
    return capture


def capture_off_pic(buffer, width=160, height=160, hAlign='CENTER'):
    if height is None:
        img = utils.ImageReader(buffer)
        iw, ih = buffer.getSize()
        aspect = ih / float(iw)
        height = (width * aspect)
    a = plt.savefig(buffer, format='png')
    buffer.seek(0)
    return [Image(buffer, width=width*mm, height=height*mm, hAlign=hAlign)]


# def arch_capture_func(func, *args, **kwargs):
#     output_buffer = io.StringIO()
#     sys.stdout = output_buffer
#     func(*args, **kwargs)
#     output = output_buffer.getvalue()
#     sys.stdout = sys.__stdout__
#     return output
#
#
# def arch_capture_off(buffer, n=1):
#     stdout_messages = buffer.getvalue().split('\n')
#     sys.stdout = sys.__stdout__
#     print('\n'.join(stdout_messages[-n-1:]))
#     return '\n'.join(stdout_messages[-n-1:])


class PDF:
    def builder(self, filename='output.pdf'):
        if isinstance(self, list) is True:
            doc = MyDocTemplate(filename)
            doc.build(self, onFirstPage=doc.add_page_number, onLaterPages=doc.add_page_number)

    # def builder(self, filename='output.pdf'):
    #     if isinstance(self, list) is True:
    #         doc = SimpleDocTemplate(filename, pagesize=A4)
    #         doc.build(self)

    def add_to_build_list(self, build_list: list = None):
        if build_list is None:
            build_list = []
        if isinstance(self, list) is True:
            for x in self:
                build_list.append(x)
        else:
            build_list.append([self])

    def table_from_df(self, title='', style_body=style_body, style_title=style_title,
                      colWidths: list = [80, 40, 40, 65, 60, 120, 130]):
        title = Paragraph(str(title), style=style_title)
        the_end = Paragraph(str(' \n \n'), style=style_title)
        if self is None:
            message = Paragraph(f' \n Ошибок не выявлено', style=style_body)
            return [title, message, the_end]
        else:
            table_data = []
            for row in [list(self.columns)] + self.values.tolist():
                new_row = []
                for item in row:
                    p = Paragraph(str(item), style=style_body)
                    new_row.append(p)
                table_data.append(new_row)
            table = Table(table_data, colWidths=colWidths)
            table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                       ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                       ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                       ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                                       ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                                       ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                                       ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                                       ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                                       ('GRID', (0, 0), (-1, -1), 1, colors.grey)]))
            return [title, table, the_end]

    def text(self, style=style_body):
        txt = Paragraph(str(self).replace('\n', '<br />\n'), style=style)
        the_end = Paragraph(str(' \n \n'), style=style_body)
        return [txt, the_end]

    def plot(self):
        return [self]
