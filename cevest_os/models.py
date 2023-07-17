from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User
from cevest_almoxarifado.models import Material
from autenticacao.models import Pessoa

import uuid
from django.utils import timezone

class Bairro(models.Model):
    nome = models.CharField(max_length=150, verbose_name='Bairro')


class Logradouro(models.Model):
    nome = models.CharField(max_length=150, verbose_name='Logradouro')


class Endereco(models.Model):
    referencia = models.CharField(
        max_length=200, verbose_name='Referência', blank=True)
    bairro = models.ForeignKey(
        Bairro, verbose_name='Bairro', on_delete=models.PROTECT)
    logradouro = models.ForeignKey(
        Logradouro, verbose_name='Logradouro', on_delete=models.PROTECT)

class CEVEST_Tipo_OS(models.Model):
    
    nome=models.CharField(max_length=100, verbose_name='Tipo de OS', blank=True)
    sigla=models.CharField(max_length=10, verbose_name='Sigla', blank=True, null=True)
    def __str__(self):
        return self.nome

class Funcionario_CEVEST_OS(models.Model):
    def __str__(self):
        return self.pessoa.nome
    NIVEL_CHOICES=(
        ('0','0 - Agente de atendimento'),
        ('1','1 - Suporte de campo'),
        ('2','2 - Suporte avançado'),
        ('3','3 - Coordenador de serviços públicos'),
    )

    pessoa = models.ForeignKey(Pessoa, models.CASCADE)
    tipo_os =  models.ManyToManyField(CEVEST_Tipo_OS)
    nivel = models.CharField(max_length=1, verbose_name='Nível de acesso', choices=NIVEL_CHOICES, null=True, default='0')
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')

class CEVEST_OrdemDeServico(models.Model):
    STATUS_CHOICES=(
        ('0','Novo'),
        ('1','Aguardando'),
        ('2','Em execução'),
        ('f','Finalizado')
    )
    PRIORIDADE_CHOICES=(
        ('0','Normal'),
        ('1','Moderada'),
        ('2','Urgente'),
    )

    
    tipo=models.ForeignKey(CEVEST_Tipo_OS, on_delete=models.PROTECT, null=True)
    numero = models.CharField(max_length=130, verbose_name='Nº da OS', blank=True)
    prioridade =models.CharField(max_length=1, verbose_name='Prioridade', default='0', choices=PRIORIDADE_CHOICES, null=True)

    dt_solicitacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de solicitação', blank=True)
    atendente = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
        
    bairro = models.CharField(max_length=150, verbose_name='local')    

    nome_do_contribuinte = models.CharField(max_length=200, verbose_name='Nome do solicitante', blank=True)
    telefone_do_contribuinte = models.CharField(max_length=12, verbose_name='Telefone do solicitante', blank=True)

    cadastrado_por = models.ForeignKey(Pessoa, on_delete=models.CASCADE, null=True)   

    motivo_reclamacao = models.TextField(verbose_name='Motivo da solicitação')            
    
    status =models.CharField(max_length=1, verbose_name='Status', choices=STATUS_CHOICES, null=True, default='0')
    pontos_atendidos=models.PositiveIntegerField(default=0)
    dt_conclusao = models.DateTimeField(verbose_name='Data de conclusão', blank=True, null=True)

    class Meta:
        ordering = ['-dt_solicitacao']

    def gerar_protocolo(self):        
        self.numero = f"{self.tipo.sigla}{int(uuid.uuid4().hex[:10], 16)}/{self.dt_solicitacao.strftime('%y')}"
        self.save()
        return self.numero
    
    def finalizar_chamado(self):
        
        if self.status == 'f':
            return "Chamado já foi finalizado."
            
        self.status = 'f'
        self.dt_conclusao = timezone.now()
        self.save()
        return "Chamado finalizado com sucesso."

class CEVEST_OS_ext(models.Model):    
    os=models.ForeignKey(CEVEST_OrdemDeServico, on_delete=models.PROTECT)
    equipe=models.ManyToManyField(Funcionario_CEVEST_OS, blank=True, null=True)
    cod_veiculo=models.CharField(max_length=14, verbose_name='Código do veículo', blank=True)

class CEVEST_OS_Linha_Tempo(models.Model):
    os=models.ForeignKey(CEVEST_OrdemDeServico, on_delete=models.CASCADE)
    pessoa=models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    mensagem=models.TextField()
    anexo = models.FileField(upload_to='anexos/', blank=True, null=True)
    dt_inclusao = models.DateTimeField(auto_now_add=True, verbose_name='Data da mensagem', blank=True)
    

class CEVEST_MateriaisUsados(models.Model):
    os=models.ForeignKey(CEVEST_OrdemDeServico, on_delete=models.PROTECT)
    material=models.ForeignKey(Material, on_delete=models.PROTECT)
    quantidade=models.IntegerField()

