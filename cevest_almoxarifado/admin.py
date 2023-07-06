from django.contrib import admin
from .models import Log_estoque, Material, Tipo_Material
# Register your models here.
admin.site.register(Log_estoque)
admin.site.register(Tipo_Material)
admin.site.register(Material)