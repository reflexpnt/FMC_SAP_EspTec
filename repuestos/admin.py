from django.contrib import admin
from .models import Articulo
#from .models import Image
from .models import Image_Art_pri




class ArticuloAdmin(admin.ModelAdmin):
  list_display = ('numeroParte', 'titulo', 'unidad', 'SYS_Prioridad','SYS_local', 'SYS_EsActivo', 'SYS_EsVisible')
  ordering = ('-SYS_Prioridad','-SYS_local','numeroParte',) # The negative sign indicate descendent order

  def view_homepage_link(self, obj):
    return '<a href="%s" target="_blank">%s</a>' % (obj.numeroParte, obj.numeroParte,)
  view_homepage_link.allow_tags = True
  view_homepage_link.short_description = 'numeroParte' # Optional

admin.site.register(Articulo, ArticuloAdmin)
#admin.site.register(Articulo)
admin.site.register(Image_Art_pri)