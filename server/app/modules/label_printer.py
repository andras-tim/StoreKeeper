import hashlib
import os
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle, StyleSheet1
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, Paragraph, TableStyle
from reportlab.graphics.barcode import code39
from reportlab.lib.units import mm

from app import configdir, tempdir
from app.server import config
from app.modules.printer import Printer


class LabelGenerationError(Exception):
    pass


class LabelPrinter:
    __logo_path = os.path.abspath(os.path.join(configdir, 'img', 'label_logo.gif'))
    __print_cache_dir = os.path.join(tempdir, 'print_cache')
    __pdf_name_template = 'label__{data}__{title_hash}.pdf'

    def __init__(self, title: str, data: str):
        self.__title = title
        self.__data = data

        self.__pdf_path = self.__get_pdf_path()

    def print_to_pdf(self) -> str:
        self.__prepare_print_cache_dir()

        if not self.__is_cached():
            self.__generate_pdf()
        return self.__pdf_path

    def print(self, printer: (Printer, None)=None, copies: int=1):
        printer = printer or Printer(config.App.LABEL_PRINTER)

        self.print_to_pdf()
        printer.print_pdf(self.__pdf_path, options={'copies': str(copies)})

    def __generate_pdf(self):
        pdf_generator = _LabelPdfGenerator()
        pdf_generator.generate_label(self.__title, self.__data, self.__logo_path, config.App.LABEL_BORDER,
                                     output_path=self.__pdf_path)

    def __prepare_print_cache_dir(self):
        os.makedirs(self.__print_cache_dir, exist_ok=True)

    def __get_pdf_path(self) -> str:
        pdf_name = self.__pdf_name_template.format(data=self.__data,
                                                   title_hash=hashlib.sha1(self.__title.encode()).hexdigest())
        return os.path.join(self.__print_cache_dir, pdf_name)

    def __is_cached(self) -> bool:
        return os.path.isfile(self.__pdf_path)


class _LabelPdfGenerator:
    page_width = 90 * mm
    page_height = 29 * mm

    margin_left = 3 * mm
    margin_top = 2 * mm
    margin_right = 4 * mm
    margin_bottom = 2 * mm

    inner_left = margin_left
    inner_top = page_height - margin_top
    inner_right = page_width - margin_right
    inner_bottom = margin_bottom
    inner_width = inner_right - margin_left
    inner_height = inner_top - margin_bottom

    pdfmetrics.registerFont(TTFont('DejaVu Sans', 'DejaVuSans.ttf'))

    stylesheet = StyleSheet1()
    stylesheet.add(ParagraphStyle(
        name='title',
        fontName='DejaVu Sans',
        fontSize=12,
        alignment=TA_CENTER,
    ))
    stylesheet.add(ParagraphStyle(
        name='data',
        fontName='DejaVu Sans',
        fontSize=10,
        alignment=TA_CENTER,
    ))

    @classmethod
    def _set_optimal_font_size(cls, title: str):
        font_size = 12
        if len(title) > 26:
            font_size = 10
        elif len(title) > 45:
            font_size = 8

        cls.stylesheet['title'].fontSize = font_size

    def generate_label(self, title: str, data: str, logo_path: str, label_border: bool, output_path: str):
        self._set_optimal_font_size(title=title)

        canv = self._create_new_canvas(pdf_path=output_path)
        canv.setAuthor(config.App.TITLE)
        canv.setTitle(title)
        canv.setSubject(data)

        if label_border:
            self._draw_border(canv)
        self._draw_logo(canv, self.inner_left + 1 * mm, self.inner_top - 8.5 * mm, logo_path)
        self._draw_title(canv, self.inner_left + 32 * mm, self.inner_top - 10 * mm, 50 * mm, 10 * mm, title)
        self._draw_barcode(canv, self.inner_bottom + 5 * mm, data, bar_height=8 * mm)

        canv.showPage()
        canv.save()

    def _create_new_canvas(self, pdf_path: str) -> canvas:
        return canvas.Canvas(pdf_path, pagesize=(self.page_width, self.page_height))

    def _draw_border(self, canv: canvas):
        canv.roundRect(self.margin_left, self.margin_bottom, self.inner_width, self.inner_height, radius=5, stroke=1,
                       fill=0)

    def _draw_title(self, canv: canvas, x: int, y: int, width: int, height: int, title: str):
        self._draw_textbox(canv, x, y, width, height, title, style_name='title')

    def _draw_logo(self, canv: canvas, x: int, y: int, image_path: str):
        canv.drawImage(image_path, x, y, 28 * mm, 7 * mm)

    def _draw_barcode(self, canv: canvas, y: int, data: str, bar_height: int=20 * mm):
        # http://en.wikipedia.org/wiki/Code_39
        barcode = code39.Standard39(data, barWidth=0.6 * mm, barHeight=bar_height,
                                    quiet=False, stop=True, checksum=False)
        if barcode.width > self.inner_width:
            raise LabelGenerationError('Generated barcode is too wide; {!s}'.format(
                {'available_mm': self.inner_width * mm, 'barcode_mm': barcode.width * mm}))

        barcode.drawOn(canv, self.inner_left + (self.inner_width - barcode.width) / 2, y)

        box_height = 4 * mm
        self._draw_textbox(canv, self.inner_left, y - 0.5 * mm - box_height,
                           self.inner_width, box_height, data, style_name='data')

    def _draw_textbox(self, canv: canvas, x: int, y: int, width: int, height: int,
                      data: str, style_name: str, border: bool=False):
        table_cells = [
            [Paragraph(data, self.stylesheet[style_name])]
        ]
        table_style = [
            ('VALIGN', (-1, -1), (-1, -1), 'MIDDLE'),
        ]
        if border:
            table_style += [('BOX', (0, 0), (-1, -1), 0.25, colors.black)]

        table = Table(table_cells, colWidths=[width], rowHeights=[height])
        table.setStyle(TableStyle(table_style))
        table.wrapOn(canv, width, height)
        table.drawOn(canv, x, y)
