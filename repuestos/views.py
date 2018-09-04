import os
import urllib.request

from django.shortcuts import render, get_object_or_404
#from .models import Image
from .models import Articulo

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3, A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib import colors
from reportlab.lib.units import inch, cm, mm
from django.http import HttpResponse, HttpResponseNotFound
from reportlab.lib.colors import black, white, pink, lightblue, blue, lightgrey, green, lightgreen, orange, yellow
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.utils import ImageReader
from django.contrib.auth.decorators import login_required

from .forms import ArticuloForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.db.models import F


from django.shortcuts import render
#from blog.models import Post
from django.http import HttpResponse
from django.core import serializers

#import requests

from reportlab.lib.styles import ParagraphStyle

from reportlab.platypus import   Spacer, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


from django.core.mail import send_mail
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText



#import sendgrid
#from sendgrid.helpers.mail import *

from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics import renderPDF

from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.contenttypes.models import ContentType

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


# Create your views here.
@login_required
def show(request):

    articulosLOCAL_count = Articulo.objects.filter(SYS_local=1).count()


    articulos = Articulo.objects.filter(SYS_local=1)
    #articulos = Articulo.objects.all()

    articulos_count = Articulo.objects.all().count()

    return render(request, 'repuestos/datatables.html', {'articulos': articulos, 'articulos_count': articulos_count, 'articulosLOCAL_count': articulosLOCAL_count})


@login_required
def postsJson(request):

    posts = Articulo.objects.filter(SYS_local=1)
    #posts = Articulo.objects.all()


    user  = request.user.username

    """
    def is_member(user):
    return user.groups.filter(name='Member').exists()
    """

    #TAL VEZ REQUIERA QUE EL GRUPO TECNICO SOLO VEA LOS APROBADOS

    if request.user.groups.filter(name='COMPRAS').exists():
        posts = Articulo.objects.filter(SYS_ESTADO = 'Aprobado').filter(SYS_local=1)

    json = serializers.serialize('json', posts )
    return HttpResponse(json, content_type='application/json')



# Pag General ___________________________________________   LISTA
#________________________________________________________
@login_required
def part_list(request):
    #ordering = ('-SYS_Prioridad',) # The negative sign indicate descendent order

    #Articulo.objects.all().update(SYS_dataEntryAuthor=F('SYS_dataEntryAuthor'))
    #articulosLOCAL = Articulo.objects.count()

    #articulos = Articulo.objects.all().order_by('-SYS_Prioridad')

    articulosLOCAL_count = Articulo.objects.filter(SYS_local=1).count()
    articulos = Articulo.objects.filter(SYS_local=1)
    articulos_count = Articulo.objects.all().count()
    #Reporter.objects.all().delete()
    return render(request, 'repuestos/part_list.html', {'articulos': articulos, 'articulos_count': articulos_count, 'articulosLOCAL_count': articulosLOCAL_count})


# Pag General _______________  NO SE USA MAS CREO _____________   DETALLE   ( ver pk)
#________________________________________________________
@login_required
def part_detail(request, pk):
    #Articulo.objects.filter(pk=979).update(SYS_Prioridad='5')   OJO CON ESTO , es para realizar update en masa
    #Articulo.objects.all().update(SYS_dataEntryAuthor = "adminFresenius")   #OJO CON ESTO , es para realizar update en masa
    #Articulo.objects.filter(a=true).exclude(pk=979)
    compo = get_object_or_404(Articulo , pk=pk)
    return render(request, 'repuestos/part_detail.html', {'compo': compo})


# Pag General ___________________________________________   DETALLE   ( ver ARAxxxx)  ESTE USAMOS
#________________________________________________________
@login_required
def ara_detail(request, numeroParte):
    compo = get_object_or_404(Articulo , numeroParte=numeroParte)

    #log_entry = LogEntry.objects.filter( object_id = compo.numeroParte , action_flag=ADDITION, content_type__id__exact = ContentType.objects.get_for_model(Articulo).numeroParte)

    #return render(request, 'repuestos/ara_detail.html', {'compo': compo , 'log_entry': log_entry })
    return render(request, 'repuestos/ara_detail.html', {'compo': compo })





#  ara_revision
#  ____________________________________________________________________________________
#      btnRechazar  btnsave   btnsaveandaprobe
@login_required
def ara_revision(request, numeroParte ):

    art_instance = get_object_or_404(Articulo , numeroParte=numeroParte)

    #enviar a aprobar
    if request.method == "POST" and 'btnsaveandaprobe' in request.POST:
        form = ArticuloForm(request.POST, instance = art_instance)
        if form.is_valid():
            art_instance = form.save(commit=False)
            art_instance.user = request.user
            art_instance.SYS_RevisedByAuthor = request.user
            art_instance.SYS_ESTADO = "Revisado"
            #art_instance.SYS_locked = True
            art_instance.save()

            return redirect('ara_revision', numeroParte=art_instance.numeroParte)


    #enviar a btnRechazar
    if request.method == "POST" and 'btnRechazar' in request.POST:
        form = ArticuloForm(request.POST, instance = art_instance)
        if form.is_valid():
            art_instance = form.save(commit=False)
            #art_instance.user = request.user
            art_instance.SYS_RevisedByAuthor = request.user
            art_instance.SYS_ESTADO = "enEdicion"
            art_instance.SYS_locked = False
            art_instance.save()

            return redirect('ara_revision', numeroParte=art_instance.numeroParte)

    #Grabar solamente
    if request.method == "POST" and 'btnsave' in request.POST:
        form = ArticuloForm(request.POST, instance = art_instance)
        if form.is_valid():
            art_instance = form.save(commit=False)
            art_instance.user = request.user
            art_instance.SYS_RevisedByAuthor = request.user
            #if art_instance.SYS_ESTADO == "Cerrado":
            #    art_instance.SYS_locked = True
            art_instance.SYS_ESTADO = "enRevision"
            art_instance.SYS_locked = False
            art_instance.save()
    else:
        form = ArticuloForm(instance=art_instance)
    return render(request, 'repuestos/ara_revision.html', {'form': form, 'articulo_instance': art_instance})





# Pag General ___________________________________________   EDICION
#________________________________________________________
@login_required
def articulo_edit(request, pk ):

    art_instance = get_object_or_404(Articulo, pk=pk)

    #enviar a revision
    if request.method == "POST" and 'btnsaveandaprobe' in request.POST:
        form = ArticuloForm(request.POST, instance = art_instance)
        if form.is_valid():
            art_instance = form.save(commit=False)
            art_instance.user = request.user
            art_instance.SYS_dataEntryAuthor = request.user
            art_instance.SYS_ESTADO = "enRevision"
            art_instance.SYS_locked = True
            art_instance.save()


            """
            mensaje_cuerpo = " Ud Tiene Pendientes para Revisión:\r\n"
            mensaje_cuerpo += art_instance.numeroParte
            #mensaje_cuerpo +=  {{art_instance.numeroParte}} #+ "&nbsp;&nbsp;[" + {{art_instance.SYS_dataEntryAuthor}} +"]"
            """



            # Create the body of the message (a plain-text and an HTML version).
            text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"

            html =" Ud Tiene Pendientes para Revisión:\r\n"
            html +=  "\r\n"
            #html +=  "    " + art_instance.numeroParte + "   de [ "+art_instance.SYS_dataEntryAuthor+" ]"
            html +=  "    " + art_instance.numeroParte +  "   de [ "+ art_instance.SYS_dataEntryAuthor.username   +" ]" + "\r\n"
            html +=  "           http://freseniusmedicalcare.pythonanywhere.com/sapnum/" + art_instance.numeroParte

            # Record the MIME types of both parts - text/plain and text/html.
            part1 = MIMEText(text, 'plain')
            part2 = MIMEText(html, 'html')

            # Attach parts into message container.
            # According to RFC 2046, the last part of a multipart message, in this case
            # the HTML message, is best and preferred.
            msg.attach(part1)
            msg.attach(part2)


            #send_mail('Especificaciones Técnicas - Pendientes para Revisión', html,'to email',  ['to email','cc_to email'],  fail_silently=False,    )






            return redirect('ara_detail', numeroParte=art_instance.numeroParte)


    #Grabar solamente
    if request.method == "POST" and 'btnsave' in request.POST:
        form = ArticuloForm(request.POST, instance = art_instance)
        if form.is_valid():
            art_instance = form.save(commit=False)
            art_instance.user = request.user
            art_instance.SYS_dataEntryAuthor = request.user
            #if art_instance.SYS_ESTADO == "Cerrado":
            #    art_instance.SYS_locked = True
            art_instance.SYS_ESTADO = "enEdicion"
            art_instance.SYS_locked = False
            art_instance.save()


            """
            send_mail(
            'Subject here',
            'Here is the message.',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False,
            )
            """
    else:
        form = ArticuloForm(instance=art_instance)
    return render(request, 'repuestos/art_edit.html', {'form': form, 'articulo_instance': art_instance})






@login_required
def part_pdf(request, pdf_art_id):

    REFERENCIAS_RENGLONES = 0

    #OBJ = Articulo.objects.get(numeroParte='ARA370071')
    OBJ = Articulo.objects.get(pk=pdf_art_id)

    nombreArchivo = OBJ.numeroParte + ".pdf"

    Usuario_editor = None
    Usuario_editor_nombre = None
    Usuario_editor_email = None

    """
    if request.user.is_authenticated():
        Usuario_editor = str( request.user.username )
        Usuario_editor_nombre =  str( request.user.first_name ) + " " + str( request.user.last_name )
        Usuario_editor_email =  str( request.user.email )
    """

    Usuario_editor = str( OBJ.SYS_dataEntryAuthor.username )
    Usuario_editor_nombre =  str( OBJ.SYS_dataEntryAuthor.first_name ) + " " + str( OBJ.SYS_dataEntryAuthor.last_name )
    Usuario_editor_email =  str( OBJ.SYS_dataEntryAuthor.email )

    """
    SYS_RevisedByAuthor  = models.ForeignKey( User, related_name='revisers',  blank=True, null=True)
    SYS_ApprovedByAuthor = models.ForeignKey( User, related_name='approvers',  blank=True, null=True)
    """

    #Usuario_editor = request.user

    #Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="{}"'.format(nombreArchivo)
    #response['Content-Disposition'] = 'inline; filename="{}"'.format(nombreArchivo)   # para abrirlo con el navegador

    """
    if downloable == True:
        response['Content-Disposition'] = 'attachment; filename="{}"'.format(nombreArchivo)   # para abrirlo con el navegador
    else:
        response['Content-Disposition'] = 'inline; filename="{}"'.format(nombreArchivo)   # para abrirlo con el navegador
    """

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response)



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
        if OBJ.SYS_ESTADO == "enEdicion":
            p.setFillColor(orange)
            p.setStrokeColor(orange)
        if OBJ.SYS_ESTADO == "Cerrado":
            p.setFillColor(green)
            p.setStrokeColor(green)


        p.rect( 17.3 * cm, 27.8 * cm,  2.2 * cm, 0.48 * cm, stroke=False, fill=True) # x,y, with,heigt
        p.setStrokeColor(white)
        p.setFillColor(white)
        p.drawString((17 + GAP_TEXTO_IZQ + GAP_TEXTO_IZQ )* cm, (27.8 + GAP_TEXTO_BOTTOM)* cm, OBJ.SYS_ESTADO)

    """
    if OBJ.SYS_ESTADO == "Aprobado":
    si esta aprobado se llenaria los usuarios correspondientes aqui



    """




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

    # IMAGEN DATA - http://freseniusmedicalcare.pythonanywhere.com/media/pic_folder/
    # ANDA  artImagen = ImageReader('http://reflexpnt.pythonanywhere.com/media/GUI_pictures/' + OBJ.imagen_Pri_Nombre)
    # NO FUNCIONA - NI IDEA PORQ artImagen =  ImageReader('http://freseniusmedicalcare.pythonanywhere.com/media/pic_folder/' + OBJ.imagen_Pri_Nombre)
    # artImagen = ImageReader('http://reflexpnt.pythonanywhere.com/media/pic_folder2/' + OBJ.numeroParte + '.png')

    p.setFont("Helvetica", 6)
    p.setStrokeColor(black)
    p.setFillColor(black)
    imagenTest = "http://reflexpnt.pythonanywhere.com/media/pic_folder2/" + OBJ.numeroParte + ".png"
    #imagenTest = "http://freseniusmedicalcare.pythonanywhere.com/media/pic_folder/" + OBJ.numeroParte + ".png"

    """
    if os.path.exists(imagenTest) and os.path.getsize(imagenTest) > 0:
        imagenTest = "http://reflexpnt.pythonanywhere.com/media/pic_folder2/no_image.png"
        p.drawString(( MARGEN_IZQ + MARGEN_IZQ + 0.5) * cm, ( DESC_IMAGE_Y - TEXTO_ROW_HEIGTH - GAP_TEXTO_BOTTOM + GAP_TEXTO_BOTTOM) * cm,  "[ " + OBJ.numeroParte +".png------------------------" + " ]")
    """

    artImagen = ImageReader(imagenTest)
    p.drawImage(artImagen , (DESC_IMAGE_X * cm)+2, (DESC_IMAGE_Y * cm)+2, width= (( DESC_IMAGE_WIDTH * cm)-4 )  ,  preserveAspectRatio=True, height= (( DESC_IMAGE_HEIGTH * cm)-4 ), mask='auto')
    p.drawString(( MARGEN_IZQ + MARGEN_IZQ + 0.5) * cm, ( DESC_IMAGE_Y - TEXTO_ROW_HEIGTH - GAP_TEXTO_BOTTOM + GAP_TEXTO_BOTTOM) * cm,  "[ " + OBJ.numeroParte +".png" + " ]-no vacio")

    """
    try:
        if os.path.getsize(imagenTest) > 0:
            # Non empty file exists
            # ... your code ...
            imagenTest = "http://reflexpnt.pythonanywhere.com/media/pic_folder2/" + OBJ.numeroParte + ".png"
            artImagen = ImageReader(imagenTest)
            p.drawImage(artImagen , (DESC_IMAGE_X * cm)+2, (DESC_IMAGE_Y * cm)+2, width= (( DESC_IMAGE_WIDTH * cm)-4 )  ,  preserveAspectRatio=True, height= (( DESC_IMAGE_HEIGTH * cm)-4 ), mask='auto')
            p.drawString(( MARGEN_IZQ + MARGEN_IZQ + 0.5) * cm, ( DESC_IMAGE_Y - TEXTO_ROW_HEIGTH - GAP_TEXTO_BOTTOM + GAP_TEXTO_BOTTOM) * cm,  "[ " + OBJ.numeroParte +".png" + " ]-no vacio")
        else:
            # Empty file exists
            # ... your code ...
            imagenTest = "http://reflexpnt.pythonanywhere.com/media/pic_folder2/no_image.png"
            artImagen = ImageReader(imagenTest)
            p.drawImage(artImagen , (DESC_IMAGE_X * cm)+2, (DESC_IMAGE_Y * cm)+2, width= (( DESC_IMAGE_WIDTH * cm)-4 )  ,  preserveAspectRatio=True, height= (( DESC_IMAGE_HEIGTH * cm)-4 ), mask='auto')
            p.drawString(( MARGEN_IZQ + MARGEN_IZQ + 0.5) * cm, ( DESC_IMAGE_Y - TEXTO_ROW_HEIGTH - GAP_TEXTO_BOTTOM + GAP_TEXTO_BOTTOM) * cm,  "[ " + OBJ.numeroParte +".png" + " ]-vacio")
    except OSError as e:
        # File does not exists or is non accessible
        # ... your code ...
        imagenTest = "http://reflexpnt.pythonanywhere.com/media/pic_folder2/no_image.png"
        artImagen = ImageReader(imagenTest)
        p.drawImage(artImagen , (DESC_IMAGE_X * cm)+2, (DESC_IMAGE_Y * cm)+2, width= (( DESC_IMAGE_WIDTH * cm)-4 )  ,  preserveAspectRatio=True, height= (( DESC_IMAGE_HEIGTH * cm)-4 ), mask='auto')
        p.drawString(( MARGEN_IZQ + MARGEN_IZQ + 0.5) * cm, ( DESC_IMAGE_Y - TEXTO_ROW_HEIGTH - GAP_TEXTO_BOTTOM + GAP_TEXTO_BOTTOM) * cm,  "[ " + OBJ.numeroParte +".png" + " ]-exception")
    """


    p.setFont("Helvetica", 6)
    p.setStrokeColor(black)
    p.setFillColor(black)
    #p.drawImage(artImagen , (DESC_IMAGE_X * cm)+2, (DESC_IMAGE_Y * cm)+2, width= (( DESC_IMAGE_WIDTH * cm)-4 )  ,  preserveAspectRatio=True, height= (( DESC_IMAGE_HEIGTH * cm)-4 ), mask='auto')
    #p.drawString(( MARGEN_IZQ + MARGEN_IZQ + 0.5) * cm, ( DESC_IMAGE_Y - TEXTO_ROW_HEIGTH - GAP_TEXTO_BOTTOM + GAP_TEXTO_BOTTOM) * cm,  "[ " + OBJ.numeroParte +".png" + " ]")



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
    p.setFont("Helvetica-Bold", 10)
    p.drawString(1.8  * cm, 3.4 * cm,  "Preparó:")
    p.drawString(8.0  * cm, 3.4 * cm,  "Revisó:")
    p.drawString(14.2 * cm, 3.4 * cm,  "Aprobó:")

    p.setFont("Helvetica", 10)
    p.drawString(1.8 * cm, (3.4 - (1 * TEXTO_ROW_HEIGTH)) * cm, Usuario_editor_nombre )
    p.drawString(1.8 * cm, (3.4 - (2 * TEXTO_ROW_HEIGTH)) * cm,  Usuario_editor_email       )
    p.drawString(1.8 * cm, (3.4 - (3 * TEXTO_ROW_HEIGTH)) * cm, "[" + Usuario_editor + "]"  )



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

    #styleN.alignment = TA_LEFT
    styleN.alignment = TA_LEFT

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


    p.setStrokeColor(black)
    p.setFillColor(white)
    p.rect( 520, (25.18) * cm,  46, 46, stroke=True, fill=True) # x,y, with,heigt

    string_QR = OBJ.numeroParte + OBJ.titulo + '\r\n' + "http://freseniusmedicalcare.pythonanywhere.com/sapnum/" + OBJ.numeroParte

    qrw = QrCodeWidget( string_QR )
    b = qrw.getBounds()

    w=b[2]-b[0]
    h=b[3]-b[1]

    d = Drawing(50,50,transform=[50./w,0,0,50./h,0,0])
    d.add(qrw)

    renderPDF.draw(d, p, 518  , (25.12) * cm)
    """

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

    """

    p.showPage()
    p.setTitle(nombreArchivo)
    p.save()
    return response


#______________________________________________________________________________________________________________________________________
#______________________________________________________________________________________________________________________________________


def test_pdf(request):

    CARD_WIDTH = 50
    CARD_HEIGTH = 80
    CARD_EXT_RADIUS = 4
    CARD_EXT_MARGEN = 3

    CARD_X = 50
    CARD_Y = 50





    #Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="{}"'.format("cardTest.pdf")

    #Create the PDF object, using the response object as its "file."
    pdf = canvas.Canvas(response)

    #barrita azul footer
    pdf.setFillColor(blue)
    pdf.setStrokeColor(blue)
    pdf.rect((MARGEN_IZQ) * cm, 1.5 * cm,  18.6 * cm, 0.1 * cm, stroke=False, fill=True) # x,y, with,heigt
    #canvas.roundRect(15, 625, 250, 125, 4, stroke=1, fill=0)
    #pdf.roundRect(self, x, y, width, height, radius, stroke=1, fill=0)
    pdf.setFillColor(black)
    pdf.setStrokeColor(black)
    #pdf.strokeWidth = (15)
    pdf.roundRect((CARD_X * mm), (CARD_Y * mm), (CARD_WIDTH * mm), (CARD_HEIGTH * mm), (CARD_EXT_RADIUS * mm), stroke=1, fill=1)

    pdf.setFillColor(white)
    pdf.setStrokeColor(white)
    pdf.roundRect( ((CARD_X + CARD_EXT_MARGEN) * mm), ((CARD_Y + CARD_EXT_MARGEN) * mm), ((CARD_WIDTH - CARD_EXT_MARGEN - CARD_EXT_MARGEN) * mm),  ((CARD_HEIGTH - CARD_EXT_MARGEN - CARD_EXT_MARGEN) * mm), ((CARD_EXT_RADIUS-2) * mm), stroke=1, fill=1)


    # imagen 1
    imagenUNO = ImageReader('http://reflexpnt.pythonanywhere.com/media/GUI_pictures/user_icon.png')
    pdf.drawImage(imagenUNO, (6) * cm , (5)*cm,  width= 100  ,  mask='auto',  preserveAspectRatio=True)

    imagenDOS = ImageReader('http://reflexpnt.pythonanywhere.com/media/GUI_pictures/png2.png')
    pdf.drawImage(imagenDOS, (5.5) * cm , (1.0)*cm,  width= 100  ,  mask='auto',  preserveAspectRatio=True)


    """
    width, height = A4
    styles = getSampleStyleSheet()
    """


    pdf.showPage()
    pdf.setTitle("test_pdf")
    pdf.save()
    return response
