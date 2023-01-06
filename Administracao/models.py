from django.db import models

# O DJANGO já possui permissões, a gente tem que dar uma olhada boa nisso pq é desnecessário
class Permissao(models.Model):
    class Meta:
        permissions = (
            ("pode_emitir_certificado","Pode emitir certificados"),
            ("acesso_admin","Acesso à area de admin"),
            ("eh_professor","Permissão para professores"),
            ("pode_fazer_alocacao","Permissão para fazer alocação"),
            )
