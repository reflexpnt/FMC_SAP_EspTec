from django.db import models
from django.contrib.auth.models import User
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
    ('5','5_Urgente'),
    ('4','4_Alta'),
    ('3','3_Media'),
    ('2','2_Normal'),
    ('1','1_Baja'),

)

STATUS_CHOICES = (
    ('Aprobado','Aprobado'),
    ('Cerrado','Cerrado'),
    ('enEdicion', 'en Edición'),
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
        SYS_dataEntryAuthor = models.ForeignKey( User, related_name='data_entries',  blank=True, null=True)

        ordering = ['SYS_Prioridad']
        numeroParte = models.CharField(max_length=15 , blank=False, default="ARA"  )
        titulo = models.CharField(max_length=250, blank=False, default="sin título" )
        unidad = models.CharField(max_length=4, choices=UNIT_CHOICES, default='UN')
        Descripcion = models.TextField(max_length=500, blank=True,  default="")



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




class Gallery(models.Model):
    title = models.CharField(max_length=200, help_text="Type title of file or image")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    TIPE = (
                ('image','Image'),
                ('file','File or Documents')
            )

    type_for_file = models.CharField(max_length=200, choices=TIPE, default='image', help_text="Please Choice only One Field, Image or Files")
    field_uploaded = models.FileField(upload_to='gallery/%Y/%m/%d/')

    IMAGES = ['.jpg', '.png', '.jpeg', '.gif']

    def file_type(self):
        if self.type_for_file == 'image':
            import os
            fx = str(os.path.splitext(str(self.field_uploaded.url))[1])
            if fx in self.IMAGES:
                return ('<img height="40" width="60" src="%s"/>' % self.field_uploaded.url)
        elif self.type_for_file == 'file':
            return '<img height="40" width="45" src="/static/asset/icons/file-icon.png"/>'
    file_type.short_description = 'Type'
    file_type.allow_tags = True

    domain = 'http://127.0.0.1:8000/'

    def get_absolute_url(self):
        return '<a href="'+self.domain+self.field_uploaded.url+'" target="_blank">'+self.domain+self.field_uploaded.url+'</a>'
    get_absolute_url.short_description = 'Absolute Url'
    get_absolute_url.allow_tags = True

    def save(self, *args, **kwargs):
        super(Gallery, self).save(*args, **kwargs)
        if not self.file_type():
            raise Exception('Could not uploaded- is the file type valid?')

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "Gallery Entry"
        verbose_name_plural = "Gallery and Files"
        ordering = ["-created"]
