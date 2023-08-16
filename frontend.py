import io
import sys
import matplotlib.pyplot as plt

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, PageTemplate, Frame, Image

pdfmetrics.registerFont(TTFont('Verdana', 'misc/verdana.ttf'))
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
style_title = styles["Heading3"]
style_title.wordWrap = 'CJK'
style_title.fontName = 'Verdana'
style_title.fontSize = 10
style_title.alignment = 1
style_title2 = styles["Heading1"]
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
                ]#,
                #onPage=self.add_page_number,
            ),
        ])

    @staticmethod
    def add_page_number(canvas):
        page_num = canvas.getPageNumber()
        page_num_pos_x = PAGE_WIDTH - 40 * mm
        page_num_pos_y = 15 * mm
        canvas.saveState()
        canvas.setFont('Verdana', 8)
        canvas.drawString(page_num_pos_x, page_num_pos_y, f'Стр. {page_num}')
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


def capture_func(func, *args, **kwargs):
    buffer = capture_on()
    func(*args, **kwargs)
    capture = capture_off(buffer)
    return capture


# noinspection PyPep8Naming
def capture_pic(width=160, height=160, hAlign='CENTER'):
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300)
    buffer.seek(0)
    plt.close()
    return Image(buffer, width=width*mm, height=height*mm, hAlign=hAlign)


# noinspection PyPep8Naming
def capture_pic_two_cols(a, b, width=200, height=100, hAlign='CENTER'):
    """
    Takes figure objects
    Args:
        a:
        b:
        width:
        height:
        hAlign:

    Returns: Image
    """
    figure3 = plt.figure(figsize=(9.6, 4.8))
    grid = figure3.add_gridspec(1, 2)
    buffer = io.BytesIO()
    a.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    ax1 = figure3.add_subplot(grid[0, 0])
    ax1.axis('off')
    ax1.imshow(plt.imread(buffer))
    buffer = io.BytesIO()
    b.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    ax2 = figure3.add_subplot(grid[0, 1])
    ax2.axis('off')
    ax2.imshow(plt.imread(buffer))
    figure3.tight_layout()
    buffer = io.BytesIO()
    figure3.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
    buffer.seek(0)
    plt.close()
    return Image(buffer, width=width*mm, height=height*mm, hAlign=hAlign)


def capture_on_pic():
    return io.BytesIO()


# noinspection PyPep8Naming
def capture_off_pic(buffer, width=160, height=160, hAlign='CENTER'):
    if height is None:
        iw, ih = buffer.getSize()
        aspect = ih / float(iw)
        height = (width * aspect)
    buffer.seek(0)
    return [Image(buffer, width=width*mm, height=height*mm, hAlign=hAlign)]


class PDF:
    def __init__(self):
        self.columns = None
        self.values = None

    def builder(self, filename='output.pdf'):
        if isinstance(self, list) is True:
            doc = MyDocTemplate(filename)
            # doc.build(self, onFirstPage=doc.add_page_number, onLaterPages=doc.add_page_number)
            doc.build(self)

    def add_to_build_list(self, build_list: list = None):
        if build_list is None:
            build_list = []
        if isinstance(self, list) is True:
            for x in self:
                build_list.append(x)
        else:
            build_list.append(self)

    # noinspection PyPep8Naming
    def table_from_df(self, title='', style_of_body=style_body, style_of_title=style_title,
                      colWidths: list = None):
        if colWidths is None:
            colWidths = [80, 40, 40, 65, 60, 120, 130]
        title = Paragraph(str(title), style=style_of_title)
        the_end = Paragraph(str(' \n \n'), style=style_of_title)
        #  For functions that return None if errors not found
        if self is None:
            message = Paragraph(f' \n Ошибок не выявлено', style=style_of_body)
            return [title, message, the_end]
        #  For functions that return one string with a description
        elif type(self) is str:
            message = Paragraph(self, style=style_regular)
            return [message, the_end]
        else:
            table_data = []
            for row in [list(self.columns)] + self.values.tolist():
                new_row = []
                for item in row:
                    p = Paragraph(str(item), style=style_of_body)
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
