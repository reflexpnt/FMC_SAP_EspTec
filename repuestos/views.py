import os
import urllib.request

from django.shortcuts import render, get_object_or_404
#from .models import Image
from .models import Articulo

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch, cm
from django.http import HttpResponse, HttpResponseNotFound
from reportlab.lib.colors import black, white, pink, lightblue, blue, lightgrey
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.utils import ImageReader
from django.contrib.auth.decorators import login_required




A4_WIDTH = 21
A4_HEIGHT = 29.7

MARGEN_IZQ  = 1.5
MARGEN_DER  = 0.9 #0.9 #18.6

GAP_TEXTO_IZQ = 0.3
GAP_TEXTO_BOTTOM = 0.15

TABLES_ROW_HEIGTH = 0.6

HEADER_BARRITA_HEIGHT = 0.1
HEADER_BARRITA_WIDTH = A4_WIDTH - MARGEN_DER - MARGEN_IZQ
HEADER_BARRITA_Y = 26.9

SAP_BAR_HEIGHT = 0.8
SAP_BAR_WIDTH = A4_WIDTH - MARGEN_DER - MARGEN_IZQ
SAP_BAR_Y = 26.0

DESC_IMAGE_WIDTH = 5.0
DESC_IMAGE_HEIGTH = 5.0
DESC_IMAGE_X = (MARGEN_IZQ + GAP_TEXTO_IZQ)
DESC_IMAGE_GAP = 0.1

INFORMACION_BAR_Y = 25.1
INFORMACION_BAR_WIDTH = A4_WIDTH - MARGEN_DER - MARGEN_IZQ
INFORMACION_BAR_HEIGTH = 0.5

DESCRIP_BAR_Y = 20.8
DESCRIP_BAR_HEIGHT = 0.5
DESCRIP_BAR_WIDTH = A4_WIDTH - MARGEN_DER - MARGEN_IZQ - DESC_IMAGE_WIDTH - 0.5

DESC_IMAGE_Y = DESCRIP_BAR_Y - DESC_IMAGE_HEIGTH + DESCRIP_BAR_HEIGHT

CONTROLES_BAR_Y = 14.5
CONTROLES_BAR_WIDTH = A4_WIDTH - MARGEN_DER - MARGEN_IZQ
CONTROLES_BAR_HEIGTH = 0.5

REFERENCIAS_BAR_Y = 13.5
REFERENCIAS_BAR_WIDTH = A4_WIDTH - MARGEN_DER - MARGEN_IZQ
REFERENCIAS_BAR_HEIGTH = 0.5

CONTROL_CAMBIOS_BAR_Y = 12.5
CONTROL_CAMBIOSS_BAR_WIDTH = A4_WIDTH - MARGEN_DER - MARGEN_IZQ
CONTROL_CAMBIOS_BAR_HEIGTH = 0.5

APROVATION_TABLE_WIDTH = A4_WIDTH - MARGEN_DER - MARGEN_IZQ
APROVATION_TABLE_HEIGTH = 1.8
APROVATION_TABLE_COL_IZQ_WIDTH =  APROVATION_TABLE_WIDTH / 3
APROVATION_TABLE_COL_DER_WIDTH =  APROVATION_TABLE_COL_IZQ_WIDTH
APROVATION_TABLE_Y = 2.0



"""
filename = '../media/logo.PNG'

def get_python_image():
    # Get a python logo image for this example
    #if not os.path.exists(filename):
    response2 = urllib.request.urlopen('http://www.pngall.com/wp-content/uploads/2016/05/Python-Logo-PNG-Image.png')
    #    f = open(filename, 'w')
    f.write(response2.read())
    f.close()
"""
@login_required
def part_list(request):
    articulosLOCAL_count = Articulo.objects.filter(SYS_local=1).count()
    #articulosLOCAL = Articulo.objects.count()

    #articulos = Articulo.objects.all()
    articulos = Articulo.objects.filter(SYS_local=1)
    articulos_count = Articulo.objects.all().count()
    #Reporter.objects.all().delete()
    return render(request, 'repuestos/part_list.html', {'articulos': articulos, 'articulos_count': articulos_count, 'articulosLOCAL_count': articulosLOCAL_count})


def part_detail(request, pk):
    compo = get_object_or_404(Articulo , pk=pk)
    return render(request, 'repuestos/part_detail.html', {'compo': compo})




def part_pdf(request, pdf_art_id):
    #Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    response['Content-Disposition'] = 'inline; filename="testPdf.pdf"'   # para abrirlo con el navegador

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)

    #OBJ = Articulo.objects.get(numeroParte='ARA370071')
    OBJ = Articulo.objects.get(pk=pdf_art_id)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.




    p.setFont("Helvetica", 10)
    p.setStrokeColor(black)
    p.setFillColor(black)
    p.drawString(15.5 * cm, 27.3 * cm, "Especificaciones Técnicas")

    #barrita azul header
    p.setFillColor(blue)
    p.setStrokeColor(blue)
    p.rect( (MARGEN_IZQ) * cm, HEADER_BARRITA_Y * cm,  HEADER_BARRITA_WIDTH * cm, HEADER_BARRITA_HEIGHT * cm, stroke=False, fill=True) # x,y, with,heigt

    # Log0 Fresenius
    logoImage = ImageReader('http://reflexpnt.pythonanywhere.com/media/GUI_pictures/logoFresenius.jpg')
    #p.drawImage(logoImage, (MARGEN_IZQ+GAP_TEXTO_IZQ) * cm , (HEADER_BARRITA_Y * cm)+5, width= (( DESC_IMAGE_WIDTH * cm)-4 )  ,  height=(( DESC_IMAGE_HEIGTH  * cm )-4) , mask='auto')
    p.drawImage(logoImage, (MARGEN_IZQ+GAP_TEXTO_IZQ) * cm , (HEADER_BARRITA_Y * cm)+8,  width= 100 , height=20 ,  mask='auto')


    #SAP barra AZUL
    p.rect((MARGEN_IZQ) * cm, SAP_BAR_Y * cm,  SAP_BAR_WIDTH * cm, SAP_BAR_HEIGHT * cm, stroke=False, fill=True) # x,y, with,heigt

    # SAP- ARAxxxxxx
    p.setFont("Helvetica-Bold", 18)
    p.setStrokeColor(white)
    p.setFillColor(white)
    p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ) * cm, 26.20 * cm, OBJ.numeroParte)

    # SAP- Titulo
    p.setStrokeColor(white)
    p.setFillColor(white)
    p.setFont("Helvetica-Bold", 14)
    p.drawString(7.0 * cm, 26.25 * cm, OBJ.titulo)


    #INFORMACIÓN PARA COMPRAS
    p.setFillColor(lightblue)
    p.setStrokeColor(lightblue)
    p.rect((MARGEN_IZQ) * cm, INFORMACION_BAR_Y * cm,  INFORMACION_BAR_WIDTH * cm, INFORMACION_BAR_HEIGTH * cm, stroke=False, fill=True) # x,y, with,heigt
    p.setFont("Helvetica", 10)
    p.setStrokeColor(black)
    p.setFillColor(black)
    p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ) * cm, (INFORMACION_BAR_Y + GAP_TEXTO_BOTTOM ) * cm, "INFORMACIÓN PARA COMPRAS")


    # tabla
    p.setStrokeColor(black)
    p.rect((MARGEN_IZQ) * cm, 22.0 * cm,  18.6 * cm, 2.4 * cm, stroke=True, fill=False)

    p.rect((MARGEN_IZQ) * cm, 22.00 * cm,  18.6 * cm, 0.60 * cm, stroke=True, fill=False)
    p.rect((MARGEN_IZQ) * cm, 22.60 * cm,  18.6 * cm, 0.60 * cm, stroke=True, fill=False)
    p.rect((MARGEN_IZQ) * cm, 23.20 * cm,  18.6 * cm, 0.60 * cm, stroke=True, fill=False)

    p.rect( (MARGEN_IZQ) * cm, 22.00 * cm,  3.20 * cm, 2.4 * cm, stroke=True, fill=False) # tabla cuadro izq

    p.rect(16.00 * cm, 22.60 * cm,  3.20 * cm, 1.8 * cm, stroke=True, fill=False) # tabla cuadro der_2

    #tabla Text
    p.setFont("Helvetica-Bold", 10)
    p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ) * cm, 24.00 * cm, "Marca")
    p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ) * cm, 23.40 * cm, "Mod./ # Parte")
    p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ) * cm, 22.80 * cm, "Linea")
    p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ) * cm, 22.2 * cm, "Comentarios")

    p.drawString(16.5 * cm, 24.00 * cm, "Reemplazable")
    p.drawString(16.5 * cm, 23.40 * cm, "Fab.a Pedido")
    p.drawString(16.5 * cm, 22.80 * cm, "Plano")
    p.drawString(19.4 * cm, 24.00 * cm, "SI")
    p.drawString(19.4 * cm, 23.40 * cm, "SI")
    p.drawString(19.4 * cm, 22.80 * cm, "SI")



    #DESCRIPCIÓN
    p.setFillColor(lightblue)
    p.setStrokeColor(lightblue)
    #         x    ,     y    ,     with  ,  heigth
    p.rect((MARGEN_IZQ+GAP_TEXTO_IZQ+DESC_IMAGE_WIDTH+GAP_TEXTO_IZQ) * cm, DESCRIP_BAR_Y * cm,  DESCRIP_BAR_WIDTH * cm, DESCRIP_BAR_HEIGHT * cm, stroke=False, fill=True) # x,y, with,heigt
    p.setFont("Helvetica", 10)
    p.setStrokeColor(black)
    p.setFillColor(black)
    p.drawString((MARGEN_IZQ+DESC_IMAGE_WIDTH+GAP_TEXTO_IZQ+GAP_TEXTO_IZQ+GAP_TEXTO_IZQ) * cm, (DESCRIP_BAR_Y+GAP_TEXTO_BOTTOM) * cm, "DESCRIPCIÓN")

    # imagen
    p.setStrokeColor(black)
    #         x    ,     y    ,     with  ,  heigth
    p.rect( DESC_IMAGE_X * cm, DESC_IMAGE_Y * cm,  DESC_IMAGE_WIDTH * cm, DESC_IMAGE_HEIGTH * cm, stroke=True, fill=False) # tabla imagen
    """
    MARGEN_IZQ  = 1.5
    MARGEN_DER  = 18.6

    GAP_TEXTO_IZQ = 0.3
    GAP_TEXTO_BOTTOM = 0.25
    """

    #CONTROLES / ENSAYOS
    p.setFillColor(lightblue)
    p.setStrokeColor(lightblue)
    p.rect((MARGEN_IZQ) * cm, CONTROLES_BAR_Y * cm,  CONTROLES_BAR_WIDTH * cm, CONTROLES_BAR_HEIGTH * cm, stroke=False, fill=True) # x,y, with,heigt
    p.setFont("Helvetica", 10)
    p.setStrokeColor(black)
    p.setFillColor(black)
    p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ) * cm, (CONTROLES_BAR_Y+GAP_TEXTO_BOTTOM) * cm, "CONTROLES / ENSAYOS")


    #REFERENCIAS
    p.setFillColor(lightblue)
    p.setStrokeColor(lightblue)
    p.rect((MARGEN_IZQ) * cm, REFERENCIAS_BAR_Y * cm,  REFERENCIAS_BAR_WIDTH * cm, REFERENCIAS_BAR_HEIGTH * cm, stroke=False, fill=True) # x,y, with,heigt
    p.setFont("Helvetica", 10)
    p.setStrokeColor(black)
    p.setFillColor(black)
    p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ) * cm, (REFERENCIAS_BAR_Y+GAP_TEXTO_BOTTOM) * cm, "REFERENCIAS")

    #CONTROL DE CAMBIOS
    p.setFillColor(lightblue)
    p.setStrokeColor(lightblue)
    p.rect((MARGEN_IZQ) * cm, CONTROL_CAMBIOS_BAR_Y * cm,  CONTROL_CAMBIOSS_BAR_WIDTH * cm, CONTROL_CAMBIOS_BAR_HEIGTH * cm, stroke=False, fill=True) # x,y, with,heigt
    p.setFont("Helvetica", 10)
    p.setStrokeColor(black)
    p.setFillColor(black)
    p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ) * cm, (CONTROL_CAMBIOS_BAR_Y+GAP_TEXTO_BOTTOM) * cm, "CONTROL DE CAMBIOS")


    # tabla Rev.
    p.setStrokeColor(black)
    p.rect((MARGEN_IZQ) * cm, 4.0 * cm,  18.6 * cm, 1.8 * cm, stroke=True, fill=False)

    p.rect((MARGEN_IZQ) * cm, 4.00 * cm,  18.6 * cm, 0.60 * cm, stroke=True, fill=False)
    p.rect((MARGEN_IZQ) * cm, 4.60 * cm,  18.6 * cm, 0.60 * cm, stroke=True, fill=False)
    p.rect((MARGEN_IZQ) * cm, 4.00 * cm,  1.20 * cm, 1.8 * cm, stroke=True, fill=False) # tabla cuadro izq
    p.rect(18.5 * cm, 4.00 * cm,  1.60 * cm, 1.8 * cm, stroke=True, fill=False) # tabla cuadro der_2
    p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ) * cm, 5.35 * cm, "Rev.")
    p.drawString(3.0 * cm, 5.35 * cm, "Modificación")
    p.drawString(18.7 * cm, 5.35 * cm, "Fecha")

    #dato rev.
    p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ) * cm, 4.8 * cm, "00")
    p.drawString(3.0 * cm, 4.8 * cm, "Emisión")

    # tabla Aprobacion.
    p.setStrokeColor(black)
    p.rect((MARGEN_IZQ) * cm, APROVATION_TABLE_Y * cm,  APROVATION_TABLE_WIDTH * cm, APROVATION_TABLE_HEIGTH * cm, stroke=True, fill=False)
    p.rect( (MARGEN_IZQ) * cm, APROVATION_TABLE_Y * cm,  APROVATION_TABLE_COL_IZQ_WIDTH * cm, APROVATION_TABLE_HEIGTH * cm, stroke=True, fill=False) # tabla cuadro izq
    p.rect( (MARGEN_IZQ + APROVATION_TABLE_COL_DER_WIDTH + APROVATION_TABLE_COL_DER_WIDTH) * cm, APROVATION_TABLE_Y * cm,  APROVATION_TABLE_COL_DER_WIDTH * cm, APROVATION_TABLE_HEIGTH * cm, stroke=True, fill=False) # tabla cuadro der_2
    p.drawString(1.8 * cm, 3.4 * cm, "Preparó:")
    p.drawString(8.0 * cm, 3.4 * cm, "Revisó:")
    p.drawString(14.2 * cm, 3.4 * cm, "Aprobó:")
    # TABLES_ROW_HEIGTH


    #barrita azul footer
    p.setFillColor(blue)
    p.setStrokeColor(blue)
    p.rect((MARGEN_IZQ) * cm, 1.5 * cm,  18.6 * cm, 0.1 * cm, stroke=False, fill=True) # x,y, with,heigt
    p.setFillColor(black)
    p.setStrokeColor(black)
    p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ) * cm, 1.0 * cm, "AR-PE-06-050 - Rev.00 - 15/06/2018")

     #http://reflexpnt.pythonanywhere.com/media//GUI_pictures/logo1.png
    #articuloImage = ImageReader('http://freseniusmedicalcare.pythonanywhere.com/media/no_image.png')

    artImagen = ImageReader('http://reflexpnt.pythonanywhere.com/media/GUI_pictures/no_image.png')
    p.drawImage(artImagen , (DESC_IMAGE_X * cm)+2, (DESC_IMAGE_Y * cm)+2, width= (( DESC_IMAGE_WIDTH * cm)-4 )  ,  height=(( DESC_IMAGE_HEIGTH  * cm )-4) , mask='auto')

    #p.drawImage(artImagen, (MARGEN_IZQ+GAP_TEXTO_IZQ) * cm , (HEADER_BARRITA_Y * cm)+8,  width= 100 , height=20 ,  mask='auto')

    """
    a = Image.open('https://images.vexels.com/media/users/3/147375/isolated/preview/67ae8a155355e39d23b955cfc7218d62-2018-3d-logo-verde-by-vexels.png')
    a.drawHeight = 2*inch
    a.drawWidth = 2*inch
    data=[['1',a],['3','4']]
  #  c = canvas.Canvas("Reportlabtest.pdf", pagesize=landscape(A4))
    table = Table(data, colWidths=200, rowHeights=50)
    table.setStyle(TableStyle([
                               ('INNERGRID', (0,0), (-1,-1), 0.25, lightblue),
                               ('BOX', (0,0), (-1,-1), 0.25, lightblue),
                               ('BACKGROUND',(0,0),(-1,2),lightblue)
                               ]))
    table.wrapOn(p, 200, 400)
    table.drawOn(p,20,50)
    """


    # Close the PDF object cleanly, and we're done.


    p.showPage()






    width, height = A4
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_LEFT
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER

    def coord(x, y, unit=1):
        x, y = x * unit, height -  y * unit
        return x, y

    # Headers
    hdescrpcion = Paragraph('''<b>descrpcion</b>''', styleBH)
    hpartida = Paragraph('''<b>partida</b>''', styleBH)
    hcandidad = Paragraph('''<b>candidad</b>''', styleBH)
    hprecio_unitario = Paragraph('''<b>precio_unitario</b>''', styleBH)
    hprecio_total = Paragraph('''<b>precio_total</b>''', styleBH)

    # Texts
    descrpcion = Paragraph('long paragraph vsdfvaFDV AVDFJH VA DFJHVAD FJVADJFV V ADJFVA DFV ADFJHsfvh DFVjfhv  vjADFHVAJDFV  ADJFVHADFJ VADJFV ', styleN)
    partida = Paragraph('DHVAJVAJDFJHVAD FV AJDFHVAJD JVHAJDF FVAJDFHV ADFJ DAFVAJDFV \
    ADFV VADFJV ADFVHJADF V ADFJHVA DJFHV A DJFV ADFJVHA DFV', styleBH)
    candidad = Paragraph('120', styleN)
    precio_unitario = Paragraph('$52.00', styleN)
    precio_total = Paragraph('$6240.00', styleN)

    data= [[hdescrpcion, hcandidad,hcandidad, hprecio_unitario, hprecio_total],
           [partida, candidad, descrpcion, precio_unitario, precio_total]]

    table = Table(data, colWidths=[2.05 * cm, 2.7 * cm, 5 * cm,
                                   3* cm, 3 * cm])

    table.setStyle(TableStyle([
                           ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                           ]))


    table.wrapOn(p, width, height)
    table.drawOn(p, *coord(1.8, 9.6, cm))
















    p.save()
    return response




"""
def part_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="testPdf.pdf"'   # para abrirlo con el navegador

    buff = BytesIO()

    get_python_image()


    doc = SimpleDocTemplate(buff,
                            pagesize=A4,
                            rightMargin=40,
                            leftMargin=40,
                            topMargin=60,
                            bottomMargin=18,
                            )
    parts = []
    parts.append(Image(filename))
    doc.build(parts)
    response.write(buff.getvalue())
    buff.close()
    return response
"""


"""
def part_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="testPdf.pdf"'   # para abrirlo con el navegador
    doc = SimpleDocTemplate(response,topMargin=2)

    doc.pagesize = landscape(A4)
    elements = []
    I = Image('https://images.vexels.com/media/users/3/147375/isolated/preview/67ae8a155355e39d23b955cfc7218d62-2018-3d-logo-verde-by-vexels.png')
    I.drawHeight =  0.7*inch
    I.drawWidth = 0.7*inch
    elements.append(I)
    doc.build(elements)
    return response
"""



"""
def part_pdf(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'
    response['Content-Disposition'] = 'inline; filename="testPdf.pdf"'   # para abrirlo con el navegador

    c = canvas.Canvas(response)


    c.setFont("Helvetica", 12)
    c.setStrokeColor(lightblue)
    c.setFillColor(lightblue)
    c.drawString(10 * cm, 5 * cm , "OBJ.numeroParte")


    a = Image.open("path/to/temp.jpg")
    a.drawHeight = 2*inch
    a.drawWidth = 2*inch
    data=[['1',a],['3','4']]
  #  c = canvas.Canvas("Reportlabtest.pdf", pagesize=landscape(A4))
    table = Table(data, colWidths=200, rowHeights=50)
    table.setStyle(TableStyle([
                               ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.black),
                               ('BACKGROUND',(0,0),(-1,2),colors.lightgrey)
                               ]))
    table.wrapOn(c, 200, 400)
    table.drawOn(c,20,50)
    c.save()
    return response

"""
