from django.db import models

class Permissao(models.Model):
    class Meta:
        permissions = (
            ("pode_emitir_certificado","Pode emitir certificados"),
            ("acesso_admin","Acesso à area de admin"),
            )
