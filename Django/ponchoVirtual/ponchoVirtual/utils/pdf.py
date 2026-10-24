import io
from xml.sax.saxutils import escape

from django.http import HttpResponse
from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

COLOR_ENCABEZADO = colors.HexColor('#5c3d2e')
COLOR_FILA_ALTERNA = colors.HexColor('#f5efe9')


class CanvasNumerado(canvas.Canvas):
    """Canvas que dibuja 'Página X de Y' en el pie de cada hoja."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._paginas = []

    def showPage(self):
        self._paginas.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._paginas)
        for estado in self._paginas:
            self.__dict__.update(estado)
            self.setFont('Helvetica', 8)
            self.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f'Página {self._pageNumber} de {total}')
            super().showPage()
        super().save()


def generar_reporte_pdf(nombre_archivo, titulo, subtitulo, encabezados, filas, anchos, totales=None):
    """
    Devuelve un HttpResponse con un PDF que contiene una tabla.

    anchos: proporción del ancho útil de cada columna (se normalizan solos).
    totales: lista de (etiqueta, valor) que se muestra debajo de la tabla.
    """
    estilos = getSampleStyleSheet()
    estilo_celda = ParagraphStyle('celda', parent=estilos['BodyText'], fontSize=8, leading=10)
    estilo_titulo_celda = ParagraphStyle('titulo_celda', parent=estilo_celda, textColor=colors.white,
                                         fontName='Helvetica-Bold')

    def celda(valor, estilo=estilo_celda):
        # Paragraph interpreta markup: se escapa para que el texto cargado por usuarios no lo rompa
        return Paragraph(escape(str(valor)), estilo)

    buffer = io.BytesIO()
    documento = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm,
                                  topMargin=2 * cm, bottomMargin=2 * cm, title=titulo,
                                  author='Poncho Digital')

    ancho_util = A4[0] - 4 * cm
    suma = sum(anchos)
    anchos_cm = [ancho_util * a / suma for a in anchos]

    datos = [[celda(e, estilo_titulo_celda) for e in encabezados]]
    datos += [[celda(valor) for valor in fila] for fila in filas]
    if not filas:
        datos.append([celda('Sin registros')] + [''] * (len(encabezados) - 1))

    tabla = Table(datos, colWidths=anchos_cm, repeatRows=1)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), COLOR_ENCABEZADO),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, COLOR_FILA_ALTERNA]),
        ('GRID', (0, 0), (-1, -1), 0.25, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    emitido = timezone.localtime().strftime('%d/%m/%Y %H:%M')
    elementos = [
        Paragraph('Poncho Digital', estilos['Heading3']),
        Paragraph(escape(titulo), estilos['Title']),
        Paragraph(escape(subtitulo), estilos['Normal']),
        Paragraph(f'Emitido el {emitido}', estilos['Normal']),
        Spacer(1, 0.5 * cm),
        tabla,
    ]
    if totales:
        elementos.append(Spacer(1, 0.4 * cm))
        for etiqueta, valor in totales:
            elementos.append(Paragraph(f'<b>{escape(etiqueta)}:</b> {escape(str(valor))}', estilos['Normal']))

    documento.build(elementos, canvasmaker=CanvasNumerado)

    respuesta = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    respuesta['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'
    return respuesta
