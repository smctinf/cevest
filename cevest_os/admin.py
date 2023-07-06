from django.contrib import admin
from .models import *

admin.site.register(CEVEST_OrdemDeServico)
admin.site.register(Funcionario_CEVEST_OS)
admin.site.register(Bairro)
admin.site.register(Logradouro)
admin.site.register(CEVEST_Tipo_OS)
admin.site.register(CEVEST_OS_ext)
admin.site.register(CEVEST_OS_Linha_Tempo)

# Register your models here.
