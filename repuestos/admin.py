from django.contrib import admin
from .models import Articulo
#from .models import Image
from .models import Image_Art_pri
from django.contrib.auth.models import User
#from .resource import ArticuloResource
### ==================
### admin.py
### ==================


from . import models
from import_export.admin import  ImportExportMixin






#class ArticuloAdmin(admin.ModelAdmin ):
class ArticuloAdmin(ImportExportMixin, admin.ModelAdmin  ):
  #resource_class = ArticuloResource
  #pass
  list_display = ('numeroParte', 'titulo', 'unidad', 'SYS_Prioridad','SYS_local','SYS_locked','SYS_ESTADO','SYS_dataEntryAuthor','SYS_RevisedByAuthor','SYS_ApprovedByAuthor', 'imagen_Pri_Nombre' , 'SYS_EsActivo', 'SYS_EsVisible', 'SYS_lastModif_date')
  ordering = ('-SYS_Prioridad','-SYS_local','numeroParte',) # The negative sign indicate descendent order
  search_fields = ('numeroParte', 'titulo',  )

  def view_homepage_link(self, obj):
    return '<a href="%s" target="_blank">%s</a>' % (obj.numeroParte, obj.numeroParte,)
  view_homepage_link.allow_tags = True
  view_homepage_link.short_description = 'numeroParte' # Optional


### ==================
### admin.py
### ==================

class GalleryAdmin(admin.ModelAdmin):
    list_display = ("file_type", "title", "get_absolute_url", "created")
    search_fields= ['title']
    list_filter = ['created']
    list_per_page = 5





### =============================================================================================
admin.site.register(Articulo, ArticuloAdmin )



#admin.site.register(Articulo)
admin.site.register(Image_Art_pri)


### ==================
### admin.py
### ==================
admin.site.register(models.Gallery, GalleryAdmin)
