from django.db import models
from django import forms
from django import template
from django.db.models.functions import Lower
#from django.core.files.storage import default_storage
from django.db.models import F

# Create your models here.

UNIT_CHOICES = (
    ('UN','UN'),
    (' M ', ' M '),
    ('KG ','KG '),
    ('LTS','LTS'),
)

PRIORITY_CHOICES = (
    ('5','Urgente'),
    ('4','Alta'),
    ('3','Media'),
    ('2','Normal'),
    ('1','Baja'),

)

STATUS_CHOICES = (
    ('Aprobado','Aprobado'),
    ('Cerrado','Cerrado'),
    ('en Edición', 'en Edición'),
    ('Inicial','Inicial'),
   )

class Image_Art_pri(models.Model):
    name = models.CharField(max_length=255)
    #descripcion = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='./', max_length=254,   default='./no_image.png')
    def __str__(self):
        return self.name




class Articulo(models.Model):
        SYS_local = models.PositiveSmallIntegerField(  default=0)
        SYS_Prioridad = models.CharField(max_length=8, choices=PRIORITY_CHOICES, default='1')
        SYS_EsActivo = models.BooleanField(  default=True)
        SYS_EsVisible = models.BooleanField(   default=True)
        SYS_ESTADO = models.CharField(max_length=10, choices = STATUS_CHOICES, default='Inicial')

        ordering = ['SYS_Prioridad']
        numeroParte = models.CharField(max_length=15)
        titulo = models.CharField(max_length=250, blank=False )
        unidad = models.CharField(max_length=4, choices=UNIT_CHOICES, default='UN')
        #observation = models.CharField(max_length=250, blank=True, null=True)
        Descripcion = models.TextField(max_length=500, blank=True,  default="")
        #datasheet = models.CharField(max_length=250, blank=True, null=True, default="")



        imagen_Pri_Nombre = models.CharField(max_length=250, default='no_image.png', blank=True )
        imagen_pri = models.ImageField(upload_to = './pic_folder/', default = './no_image.png', blank=True)
        #image = models.ImageField(upload_to = 'pic_folder/', default = 'no_image.png')

        marca = models.CharField(max_length=40, blank=True, default="")
        modelo_NumParte = models.CharField(max_length=40, blank=True, default="")
        linea = models.CharField(max_length=40, blank=True, default="")
        comentario = models.CharField(max_length=40, blank=True, default="")

        Reemplazable = models.BooleanField(blank=True,  default=False)
        Fab_a_Pedido = models.BooleanField(blank=True,  default=False)
        Plano = models.BooleanField(blank=True,  default=False)

        Ensayos = models.TextField(max_length=500, blank=True, default="")

        Referencia1 = models.CharField(max_length=100, blank=True, default="")
        Referencia2 = models.CharField(max_length=100, blank=True, default="")
        Referencia3 = models.CharField(max_length=100, blank=True, default="")
        Referencia4 = models.CharField(max_length=100, blank=True, default="")
        Referencia5 = models.CharField(max_length=100, blank=True, default="")

        def __str__(self):
            return self.numeroParte
            #return [self.name.lower()]
