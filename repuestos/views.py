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
from reportlab.lib.colors import black, white, pink, lightblue, blue, lightgrey, green, lightgreen, orange, yellow
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.utils import ImageReader
from django.contrib.auth.decorators import login_required

from .forms import ArticuloForm
from django.shortcuts import redirect


A4_WIDTH = 21
A4_HEIGHT = 29.7

MARGEN_IZQ  = 1.5
MARGEN_DER  = 0.9 #0.9 #18.6

GAP_TEXTO_IZQ = 0.3
GAP_TEXTO_BOTTOM = 0.15

TABLES_ROW_HEIGTH = 0.5
TEXTO_ROW_HEIGTH = 0.4

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

MARCA_TEXT_Y = 24
MARCA_TEXT_X = 5.5

MOD_NUM_PARTE_TEXT_X = 5.5
MOD_NUM_PARTE_Y = 23.4

LINEA_TEXT_X = 5.5
LINEA_TEXT_Y = 22.8

COMENTARIOS_TEXT_X = 5.5
COMENTARIOS_Y = 22.2


DESCRIP_BAR_Y = 20.8
DESCRIP_BAR_X = (MARGEN_IZQ+GAP_TEXTO_IZQ+DESC_IMAGE_WIDTH+GAP_TEXTO_IZQ)
DESCRIP_BAR_HEIGHT = 0.5
DESCRIP_BAR_WIDTH = A4_WIDTH - MARGEN_DER - MARGEN_IZQ - DESC_IMAGE_WIDTH - 0.5

DESCRIP_TEXT_Y = 11.5
DESCRIP_TEXT_X = DESCRIP_BAR_X

DESC_IMAGE_Y = DESCRIP_BAR_Y - DESC_IMAGE_HEIGTH + DESCRIP_BAR_HEIGHT

CONTROLES_BAR_Y = 15
CONTROLES_BAR_WIDTH = A4_WIDTH - MARGEN_DER - MARGEN_IZQ
CONTROLES_BAR_HEIGTH = 0.5
CONTROLES_TEXT_X = (MARGEN_IZQ+GAP_TEXTO_IZQ+GAP_TEXTO_IZQ )

REFERENCIAS_BAR_Y = 12.5
REFERENCIAS_BAR_WIDTH = A4_WIDTH - MARGEN_DER - MARGEN_IZQ
REFERENCIAS_BAR_HEIGTH = 0.5



CONTROL_CAMBIOS_BAR_Y = 6.1
CONTROL_CAMBIOS_BAR_WIDTH = A4_WIDTH - MARGEN_DER - MARGEN_IZQ
CONTROL_CAMBIOS_BAR_HEIGTH = 0.5


APROVATION_TABLE_WIDTH = A4_WIDTH - MARGEN_DER - MARGEN_IZQ
APROVATION_TABLE_HEIGTH = 1.8
APROVATION_TABLE_COL_IZQ_WIDTH =  APROVATION_TABLE_WIDTH / 3
APROVATION_TABLE_COL_DER_WIDTH =  APROVATION_TABLE_COL_IZQ_WIDTH
APROVATION_TABLE_Y = 2.0



"""
EDIT. Another solution is to add a property to your Event model, that you can access from your template:

class Event(models.Model):
# ...
@property
def sorted_attendee_set(self):
    return self.attendee_set.order_by('last_name')
"""


@login_required
def part_list(request):
    ordering = ('-SYS_Prioridad',) # The negative sign indicate descendent order
    articulosLOCAL_count = Articulo.objects.filter(SYS_local=1).count()
    #articulosLOCAL = Articulo.objects.count()

    #articulos = Articulo.objects.all().order_by('-SYS_Prioridad')
    articulos = Articulo.objects.filter(SYS_local=1)
    articulos_count = Articulo.objects.all().count()
    #Reporter.objects.all().delete()
    return render(request, 'repuestos/part_list.html', {'articulos': articulos, 'articulos_count': articulos_count, 'articulosLOCAL_count': articulosLOCAL_count})


def part_detail(request, pk):
    #Articulo.objects.filter(pk=979).update(SYS_Prioridad='5')   OJO CON ESTO , es para realizar update en masa
    compo = get_object_or_404(Articulo , pk=pk)
    return render(request, 'repuestos/part_detail.html', {'compo': compo})

"""
def articulo_new(request):
    if request.method == "POST":
            form_instance = ArticuloForm(request.POST)
            if form_instance.is_valid():
                compo = form_instance.save(commit=False)
                #compo.titulo = request.titulo
                #articulo.published_date = timezone.now()
                #post.save()
                return redirect('part_detail', pk=979)

    else:
        form = ArticuloForm()
    return render(request, 'repuestos/art_edit.html', {'form': form})
"""

def articulo_edit(request, pk ):
        art_instance = get_object_or_404(Articulo, pk=pk)
        if request.method == "POST":
            form = ArticuloForm(request.POST, instance = art_instance)
            if form.is_valid():
                art_instance = form.save(commit=False)
                #art_instance.titulo = request.user
                #art_instance.titulo =  request.titulo # add User.id as string
                #art_instance.titulo = "TEST2" #validated_data.get('titulo', instance.titulo) # anda posta
                art_instance.titulo = art_instance.titulo
                art_instance.unidad = art_instance.unidad
                art_instance.save()
                return redirect('part_detail', pk=art_instance.pk)
        else:
            form = ArticuloForm(instance=art_instance)
        return render(request, 'repuestos/art_edit.html', {'form': form})









def part_pdf(request, pdf_art_id):

    REFERENCIAS_RENGLONES = 0

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


    if OBJ.SYS_ESTADO != "Aprobado":
        p.setFont("Helvetica-Bold", 8)
        p.setStrokeColor(white)
        p.setFillColor(black)
        p.drawString(15.5 * cm, (27.8 + GAP_TEXTO_BOTTOM) * cm, "estado: ")

        p.setFont("Helvetica", 10)
        if OBJ.SYS_ESTADO == "Inicial":
            p.setFillColor(lightblue)
            p.setStrokeColor(lightblue)
        if OBJ.SYS_ESTADO == "en Edición":
            p.setFillColor(orange)
            p.setStrokeColor(orange)
        if OBJ.SYS_ESTADO == "Cerrado":
            p.setFillColor(green)
            p.setStrokeColor(green)


        p.rect( 17.3 * cm, 27.8 * cm,  2.2 * cm, 0.48 * cm, stroke=False, fill=True) # x,y, with,heigt
        p.setStrokeColor(white)
        p.setFillColor(white)
        p.drawString((17 + GAP_TEXTO_IZQ + GAP_TEXTO_IZQ )* cm, (27.8 + GAP_TEXTO_BOTTOM)* cm, OBJ.SYS_ESTADO)


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


    # tabla INFORMACIÓN PARA COMPRAS
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

    if OBJ.Reemplazable == True:
        p.drawString(19.4 * cm, 24.00 * cm, "SI")
    else:
        p.drawString(19.4 * cm, 24.00 * cm, "NO")

    if OBJ.Fab_a_Pedido == True:
        p.drawString(19.4 * cm, 23.40 * cm, "SI")
    else:
        p.drawString(19.4 * cm, 23.40 * cm, "NO")

    if OBJ.Plano == True:
        p.drawString(19.4 * cm, 22.80 * cm, "SI")
    else:
        p.drawString(19.4 * cm, 22.80 * cm, "NO")


    p.setFont("Helvetica", 10)
    p.drawString(MARCA_TEXT_X * cm, MARCA_TEXT_Y * cm,  OBJ.marca) #marca
    p.drawString(MOD_NUM_PARTE_TEXT_X * cm, MOD_NUM_PARTE_Y * cm, OBJ.modelo_NumParte) #"Mod./ # Parte")
    p.drawString(LINEA_TEXT_X * cm, LINEA_TEXT_Y * cm, OBJ.linea)  # Linea
    p.drawString(COMENTARIOS_TEXT_X * cm, COMENTARIOS_Y * cm, OBJ.comentario) #Comentarios


    #DESCRIPCIÓN
    p.setFillColor(lightblue)
    p.setStrokeColor(lightblue)
    #         x    ,     y    ,     with  ,  heigth
    p.rect(DESCRIP_BAR_X * cm, DESCRIP_BAR_Y * cm,  DESCRIP_BAR_WIDTH * cm, DESCRIP_BAR_HEIGHT * cm, stroke=False, fill=True) # x,y, with,heigt
    p.setFont("Helvetica", 10)
    p.setStrokeColor(black)
    p.setFillColor(black)
    p.drawString(( DESCRIP_BAR_X + GAP_TEXTO_IZQ) * cm, (DESCRIP_BAR_Y+GAP_TEXTO_BOTTOM) * cm, "DESCRIPCIÓN")

    # IMAGEN Rectangulo
    p.setStrokeColor(black)
    #         x    ,     y    ,     with  ,  heigth
    p.rect( DESC_IMAGE_X * cm, DESC_IMAGE_Y * cm,  DESC_IMAGE_WIDTH * cm, DESC_IMAGE_HEIGTH * cm, stroke=True, fill=False) # tabla imagen

    # IMAGEN DATA
    artImagen = ImageReader('http://reflexpnt.pythonanywhere.com/media/GUI_pictures/' + OBJ.imagen_Pri_Nombre)

    p.setFont("Helvetica", 6)
    p.setStrokeColor(black)
    p.setFillColor(black)
    p.drawImage(artImagen , (DESC_IMAGE_X * cm)+2, (DESC_IMAGE_Y * cm)+2, width= (( DESC_IMAGE_WIDTH * cm)-4 )  ,  preserveAspectRatio=True, height= (( DESC_IMAGE_HEIGTH * cm)-4 ), mask='auto')
    p.drawString(( MARGEN_IZQ + MARGEN_IZQ + 0.5) * cm, ( DESC_IMAGE_Y - TEXTO_ROW_HEIGTH - GAP_TEXTO_BOTTOM + GAP_TEXTO_BOTTOM) * cm,  "[" + OBJ.imagen_Pri_Nombre + "]")



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

    p.setFont("Helvetica", 10)
    p.setStrokeColor(black)
    p.setFillColor(black)
    if OBJ.Referencia1 != "" :
        REFERENCIAS_RENGLONES += 1
        p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ+GAP_TEXTO_IZQ ) * cm, ( REFERENCIAS_BAR_Y - (TEXTO_ROW_HEIGTH * REFERENCIAS_RENGLONES)  ) * cm,  OBJ.Referencia1) #Referencia1

    if OBJ.Referencia2 != "" :
        REFERENCIAS_RENGLONES  +=  1
        p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ+GAP_TEXTO_IZQ ) * cm, ( REFERENCIAS_BAR_Y - (TEXTO_ROW_HEIGTH * REFERENCIAS_RENGLONES)  ) * cm,  OBJ.Referencia2) #Referencia2

    if OBJ.Referencia3 != "" :
        REFERENCIAS_RENGLONES  +=  1
        p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ+GAP_TEXTO_IZQ ) * cm, ( REFERENCIAS_BAR_Y - (TEXTO_ROW_HEIGTH * REFERENCIAS_RENGLONES)  ) * cm,  OBJ.Referencia3) #Referencia3

    if OBJ.Referencia4 != "" :
        REFERENCIAS_RENGLONES  +=  1
        p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ+GAP_TEXTO_IZQ ) * cm, ( REFERENCIAS_BAR_Y - (TEXTO_ROW_HEIGTH * REFERENCIAS_RENGLONES)  ) * cm,  OBJ.Referencia4) #Referencia3

    if OBJ.Referencia5 != "" :
        REFERENCIAS_RENGLONES  +=  1
        p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ+GAP_TEXTO_IZQ ) * cm, ( REFERENCIAS_BAR_Y - (TEXTO_ROW_HEIGTH * REFERENCIAS_RENGLONES)  ) * cm,  OBJ.Referencia5) #Referencia3
    #p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ+GAP_TEXTO_IZQ ) * cm, ( REFERENCIAS_BAR_Y - (TEXTO_ROW_HEIGTH * 4)  ) * cm,  OBJ.Referencia4) #Referencia4
    #p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ+GAP_TEXTO_IZQ ) * cm, ( REFERENCIAS_BAR_Y - (TEXTO_ROW_HEIGTH * 5)  ) * cm,  OBJ.Referencia5) #Referencia5

    #CONTROL DE CAMBIOS
    p.setFillColor(lightblue)
    p.setStrokeColor(lightblue)
    p.rect((MARGEN_IZQ) * cm, CONTROL_CAMBIOS_BAR_Y  * cm,  CONTROL_CAMBIOS_BAR_WIDTH * cm, CONTROL_CAMBIOS_BAR_HEIGTH * cm, stroke=False, fill=True) # x,y, with,heigt
    p.setFont("Helvetica", 10)
    p.setStrokeColor(black)
    p.setFillColor(black)
    p.drawString(( MARGEN_IZQ+GAP_TEXTO_IZQ ) * cm, (CONTROL_CAMBIOS_BAR_Y + GAP_TEXTO_BOTTOM ) * cm, "CONTROL DE CAMBIOS")


    # tabla Rev. CONTROL DE CAMBIOS
    p.setStrokeColor(black)
    p.rect((MARGEN_IZQ) * cm, 4.0 * cm,  18.6 * cm, 1.8 * cm, stroke=True, fill=False)

    p.rect((MARGEN_IZQ) * cm, 4.00 * cm,  18.6 * cm, 0.60 * cm, stroke=True, fill=False)
    p.rect((MARGEN_IZQ) * cm, 4.60 * cm,  18.6 * cm, 0.60 * cm, stroke=True, fill=False)
    p.rect((MARGEN_IZQ) * cm, 4.00 * cm,  1.20 * cm, 1.8 * cm, stroke=True, fill=False) # tabla cuadro izq
    p.rect(18.5 * cm, 4.00 * cm,  1.60 * cm, 1.8 * cm, stroke=True, fill=False) # tabla cuadro der_2
    p.drawString((MARGEN_IZQ+GAP_TEXTO_IZQ) * cm, 5.35 * cm, "Rev.")
    p.drawString(3.0 * cm, 5.35 * cm, "Modificación")
    p.drawString(18.7 * cm, 5.35 * cm, "Fecha")

    #dato rev. CONTROL DE CAMBIOS
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
    #http://freseniusmedicalcare.pythonanywhere.com/media/ARA281001.png


    # Close the PDF object cleanly, and we're done.




    width, height = A4
    styles = getSampleStyleSheet()
    styleN = styles["BodyText"]
    styleN.alignment = TA_LEFT
    #styleN.alignment = RIGHT
    styleBH = styles["Normal"]
    styleBH.alignment = TA_CENTER

    def coord(x, y, unit=1):
        x, y = x * unit, height -  y * unit
        return x, y

    # Headers
    #data_table_hdescripcion = Paragraph('''<b>Descripción</b>''', styleN)


    # Text DESCRIPCION

    # TABLA CONTROLES/ENSAYOS
    if OBJ.Descripcion != "" :
        descripcion_data = Paragraph(OBJ.Descripcion, styleN)


        data_table_DESC= [ [descripcion_data]]

        table_DESC = Table(data_table_DESC, colWidths=[DESCRIP_BAR_WIDTH * cm])

        table_DESC.setStyle(TableStyle([
                               #('INNERGRID', (0,0), (-1,-1), 0.25, colors.blue),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.white),
                               ]))


        table_DESC.wrapOn(p, width, height)
        table_DESC.drawOn(p, *coord( DESCRIP_TEXT_X , DESCRIP_TEXT_Y, cm))


    """
    if OBJ.Ensayos != "" :
        descripcion_data = Paragraph(OBJ.Descripcion, styleN)


        data_table_DESC= [ [descripcion_data]]

        table_DESC = Table(data_table_DESC, colWidths=[DESCRIP_BAR_WIDTH * cm])

        table_DESC.setStyle(TableStyle([
                               #('INNERGRID', (0,0), (-1,-1), 0.25, colors.blue),
                               ('BOX', (0,0), (-1,-1), 0.25, colors.white),  ]))





        table_DESC.wrapOn(p, width, height)
        table_DESC.drawOn(p, *coord( DESCRIP_TEXT_X , DESCRIP_TEXT_Y, cm))
    """



    # TABLA CONTROLES/ENSAYOS
    if OBJ.Ensayos != "" :
        controEnsayos_data = Paragraph(OBJ.Ensayos, styleN)


        controEnsayos_data_table= [ [controEnsayos_data]]

        controEnsayos_table = Table(controEnsayos_data_table, colWidths=[(CONTROLES_BAR_WIDTH - MARGEN_IZQ) * cm])

        controEnsayos_table.setStyle(TableStyle([
                           #('INNERGRID', (0,0), (-1,-1), 0.25, colors.blue),
                           ('BOX', (0,0), (-1,-1), 0.25, colors.white),
                           ]))


        controEnsayos_table.wrapOn(p, width, height)
        #controEnsayos_table.drawOn(p, *coord( CONTROLES_TEXT_X , 16.7 , cm))
        controEnsayos_table.drawOn( p, (CONTROLES_TEXT_X * cm), ((CONTROLES_BAR_Y - CONTROLES_BAR_HEIGTH - CONTROLES_BAR_HEIGTH- CONTROLES_BAR_HEIGTH ) *cm) )




    p.showPage()
    p.save()
    return response



