# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from .models import Curso

admin.site.register(Curso)

from .models import Instrutor

admin.site.register(Instrutor)

from .models import Cidade

admin.site.register(Cidade)

from .models import Bairro

admin.site.register(Bairro)

from .models import Escolaridade

admin.site.register(Escolaridade)

from .models import Profissao

admin.site.register(Profissao)

from .models import Aluno

admin.site.register(Aluno)

from .models import Aluno_Quer_Curso

admin.site.register(Aluno_Quer_Curso)
