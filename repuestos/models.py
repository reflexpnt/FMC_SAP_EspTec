from django.db import models
from django import forms
from django import template
#from django.core.files.storage import default_storage

# Create your models here.

UNIT_CHOICES = (
    ('UN','UN'),
    (' M ', ' M '),
    ('KG ','KG '),
    ('LTS','LTS'),
)

class Image_Art_pri(models.Model):
    name = models.CharField(max_length=255)
    descripcion = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='./', max_length=254,   default='./no_image.png')
    def __str__(self):
        return self.name




class Articulo(models.Model):
        numeroParte = models.CharField(max_length=15)
        titulo = models.CharField(max_length=250, blank=False )
        unidad = models.CharField(max_length=4, choices=UNIT_CHOICES, default='UN')
        observation = models.CharField(max_length=250, blank=True, null=True)
        datasheet = models.CharField(max_length=250, blank=True, null=True)
        local = models.PositiveSmallIntegerField(  default=0)
        #EsActivo = models.BooleanField(blank=True,  default=False)
        #EsVisible = models.BooleanField(blank=True,   default=False)
        #TieneHojaDatos = models.BooleanField(blank=True,   default=False)
        ##imagen = models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no_image.png')
        #image = models.ImageField(upload_to = 'pic_folder/', default = 'no_image.png')

        def __str__(self):
            return self.numeroParte
