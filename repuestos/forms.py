from django import forms
from .models import Articulo

#class ArticuloForm(forms.ModelForm):
class ArticuloForm(forms.ModelForm):
    class Meta:
        model = Articulo
        fields = ('numeroParte', 'titulo', 'unidad',)
        #fields = ('numeroParte', 'titulo', 'unidad',)