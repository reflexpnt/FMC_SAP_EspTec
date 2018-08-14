from django import forms
from .models import Articulo

#class ArticuloForm(forms.ModelForm):
class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ('SYS_Prioridad' , 'numeroParte', 'titulo', 'unidad', 'Descripcion', 'imagen_Pri_Nombre', 'imagen_pri' , 'marca' , 'modelo_NumParte', 'linea' , 'comentario' , 'Reemplazable' ,  'Fab_a_Pedido' , 'Plano' , 'Ensayos' , 'Referencia1', 'Referencia2', 'Referencia3', 'Referencia4', 'Referencia5'  )
        #fields = ('numeroParte', 'titulo', 'unidad',)
        #fields['titulo'].widget.attrs['size'] = 2



"""
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
"""