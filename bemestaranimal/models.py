from django.db import models
from autenticacao.models import *
# Create your models here.

class Tutor(models.Model):

    TIPO_DE_MORADIA_CHOICES=[
        ('Própria', 'Própria'), 
        ('Alugada', 'Alugada'),
    ]
    pessoa=models.ForeignKey(Pessoa, on_delete=models.CASCADE)
    tipo_de_moradia=models.CharField(max_length=7, choices=TIPO_DE_MORADIA_CHOICES, verbose_name='Tipo de moradia', blank=False, null=False)

class Tipo(models.Model):

    def __str__(self):
        return '%s' % (self.nome)

    class Meta:
        ordering = ['nome']
    nome=models.CharField(max_length=64, verbose_name='', blank=False, null=False)

class Periodo(models.Model):
    def __str__(self):
        return '%s' % (self.intervalo)
    
    intervalo = models.CharField(max_length=32, blank=False, null=False)
    
class Especie(models.Model):

    def __str__(self):
        return '%s' % (self.nome_especie)
    
    class Meta:
         ordering= ['nome_especie']

    nome_especie=models.CharField(max_length=64, verbose_name='Espécie', blank=True, null=True)

class Animal(models.Model):

    SEXO_CHOICES=[
        ('o', 'Macho'), 
        ('a', 'Fêmea'),
    ]
    def __str__(self):
        return '%s' % (self.nome)
   
    nome=models.CharField(max_length=64, verbose_name='Nome/apelido', blank=True, null=True)
    idade=models.IntegerField(verbose_name='Idade', blank=True, null=True)
    tipo=models.ForeignKey(Tipo, on_delete=models.PROTECT, blank=False, null=False)
    raca=models.CharField(max_length=64, verbose_name='Raça', blank=True, null=True)
    especie=models.ForeignKey(Especie, on_delete=models.PROTECT, blank=True, null=True)
    tutor=models.ForeignKey(Tutor, on_delete=models.PROTECT, blank=True, null=True)
    sexo=models.CharField(max_length=1, choices=SEXO_CHOICES, verbose_name='Sexo do animal', blank=False, null=False)
    castrado=models.BooleanField(default=False, verbose_name='Castrado')
    anilha=models.CharField(max_length=64, verbose_name='Código da anilha', blank=True, null=True)
    animal_image = models.ImageField(upload_to='animal_tutor/', verbose_name="Foto do animal",blank=True, null=True)
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')
    
class Catalogo(models.Model):
    def __str__(self):
        return '%s' % (self.animal.nome)
    
    # nome = models.CharField(max_length=64, verbose_name='Nome', blank= True, null=True)
    animal=models.ForeignKey(Animal, on_delete=models.CASCADE, blank=True, null=True)
    pelagem=models.CharField(max_length=64, verbose_name="Pelagem", blank=False, null=False)
    vacinado=models.BooleanField(default=False, verbose_name='Vacinado')
    # sexo=models.CharField(max_length=1, choices=SEXO_CHOICES, verbose_name='Sexo do animal', blank=False, null=False)
    # castrado=models.BooleanField(default=False, verbose_name='Castrado')
    # animal_image = models.ImageField(upload_to='animal_catalogo/', verbose_name="Foto do animal (opcional)", blank=True, null=True)
    #ativo

class Adotados(models.Model):
    tutor=models.ForeignKey(Tutor, on_delete=models.PROTECT)
    catalogo=models.ForeignKey(Catalogo, on_delete=models.PROTECT)

class Informacoes_Extras(models.Model):
    class Meta:
        ordering = ['animal']

    animal=models.ForeignKey(Animal, on_delete=models.PROTECT)
    alimentacao_tipo=models.CharField(max_length=128, verbose_name='Tipo de alimentação', blank=True, null=True)
    alimentacao_periodo=models.ManyToManyField(Periodo, verbose_name='Período da alimentação')
    condicoes=models.CharField(max_length=128, verbose_name='Condições de abrigo na residência')
    dt_vacinacao=models.DateField(verbose_name='Data da última vacinação', auto_now=False, blank=True, null=True)
    dt_vermifugacao=models.DateField(verbose_name='Data da última vermifugação', auto_now=False, blank=True, null=True)
    complemento=models.CharField(max_length=256, verbose_name='Complemento', blank=True, null=True)
    dt_registro=models.DateField(verbose_name='Data do registro', blank=True, null=True)

class Errante(models.Model):
    def __str__(self):
        return '%s' % (self.pelagem)
    
    pelagem=models.CharField(max_length=64, verbose_name="Pelagem", blank=False, null=False)
    tipo=models.ForeignKey(Tipo, on_delete=models.PROTECT, blank=False, null=False)
    especie=models.ForeignKey(Especie, on_delete=models.PROTECT, blank=True, null=True)
    animal_image = models.ImageField(upload_to='animal_errante/', verbose_name="Foto do animal (opcional)",blank=True, null=True)
    dt_inclusao=models.DateField(auto_now_add=True, verbose_name='Data de inclusão')

#não sei quantos vão ser por tutor, mas por enquanto é um
#acho que dar mais de um seria um incentivo p cadastrar

#como vai ser 1 por cadastro:::
class TokenDesconto(models.Model):
    token = models.CharField(max_length=12, unique=True)
    used = models.BooleanField(default=False)
    tutor = models.ForeignKey(Tutor, on_delete=models.PROTECT)
    dt_inclusao = models.DateField(auto_now_add=True)

class EntrevistaPrevia(models.Model):
    ESCOLHAS_CHOICES=[
        (True, 'SIM'),
        (False, 'NÃO')
    ]
    
    animal = models.ForeignKey(Catalogo, on_delete=models.CASCADE)
    nome=models.CharField(max_length=64, verbose_name='Nome', blank=False, null=False)
    cpf=models.CharField(max_length=14, verbose_name='CPF', blank=False, null=False)
    telefone=models.CharField(max_length=15, verbose_name='Telefone', blank=True, null=True)
    bairro=models.CharField(max_length=64, verbose_name='Bairro', blank=False, null=False)
    endereco=models.CharField(max_length=128, verbose_name='Endereco', blank=False, null=False)
    quest_um=models.CharField(max_length=128, verbose_name='Porque você quer adotar um animal?',blank=False, null=False)
    quest_dois=models.BooleanField(choices=ESCOLHAS_CHOICES, default=False, verbose_name='Todas as pessoas que residem na casa gostam de animais?')
    quest_tres=models.BooleanField(choices=ESCOLHAS_CHOICES, default=False, verbose_name='A residência que pretende acolher o animal tem o quintal completamente fechado?')
    quest_quatro=models.BooleanField(choices=ESCOLHAS_CHOICES, default=False, verbose_name='Você tem consciência de que filhotes exigem cuidados especiais, pois podem chorar, destruir objetos da casa e precisagem de um tempo de adaptação?')
    quest_cinco=models.BooleanField(choices=ESCOLHAS_CHOICES, default=False, verbose_name='Você tem condições de tratar o animal com ração de qualidade e água limpa diariamente?')
    quest_seis=models.BooleanField(choices=ESCOLHAS_CHOICES, default=False, verbose_name='Você compromete-se com os cuidados veterinários necessários, além da vacinação anual do animal?')
    quest_sete=models.BooleanField(choices=ESCOLHAS_CHOICES, default=False, verbose_name='Você tem consciência de que um animal vive cerca de 15 anos e que voc~e teá responsabilidade sobre sua vida durante todo esse tempo?')
    quest_oito=models.BooleanField(choices=ESCOLHAS_CHOICES, default=False, verbose_name='Você tem plena consciência de que precisará higienizar, diariamente, o espaço onde o animal viverá, estando sujeito ao contato com suas necessidades fisiológicas?')
    quest_nove=models.BooleanField(choices=ESCOLHAS_CHOICES, default=False, verbose_name='Você tem consciência de que, às vezes o animal poderá fazer suas necessidades em local indesejado?')
    quest_dez=models.BooleanField(choices=ESCOLHAS_CHOICES, default=False, verbose_name='Você tem consciência de que, como fiel depositário do animal, ele não pode ser doado, vendido ou abandonado sob NENHUMA hipótese?')











