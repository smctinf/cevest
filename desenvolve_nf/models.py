from django.db import models


# Create your models here.
class Carousel_Index(models.Model):
    
    nome = models.CharField(max_length=64, verbose_name="Nome para identificação ou para texto alternativo", blank=False, null=False)
    image = models.ImageField(upload_to='carousel_index/', verbose_name="Imagem 987x394", blank=False, null=True)
    url = models.CharField(max_length=64, verbose_name="Url, caso tenha para redirecionar", blank=True)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return '%s - %s' % (self.nome, self.id)


class ClimaTempo(models.Model):
    maxTemp = models.CharField(verbose_name="Temperatura máxima", max_length=3)
    minTemp = models.CharField(verbose_name="Temperatura mínima", max_length=3)
    madrugada = models.CharField(verbose_name="Clima na madrugada", max_length=50, blank=True)
    manha = models.CharField(verbose_name="Clima na manhã", max_length=50, blank=True)
    tarde = models.CharField(verbose_name="Clima na tarde", max_length=50, blank=True)
    noite = models.CharField(verbose_name="Clima na noite", max_length=50, blank=True)
    dt_inclusao = models.DateTimeField( auto_now_add=True, unique=True)

    def imgNameMaker(self, texto):
        texto.replace(",", "")
        palavras = texto.split(" ")
        if "noite" in palavras:
            imgName = "noite"
        elif "sol" in palavras:
            imgName = "sol"
        if "nuvens" in palavras or "nublada":
            imgName += "_nuvem"
        if "chuva" in palavras:
            imgName += "_chuva"
        if "trovoada" in palavras or "trovoadas" in palavras:
            imgName += "_trovoada"
        return imgName + ".png"


    class Meta:
        ordering = ['-dt_inclusao']
        verbose_name = "Relatório"
        verbose_name_plural = "Relatórios de clima"

    def getImg(self, turno):
        imgUrl = "/static/images/clima_icons/"
        if turno == "madrugada":
            imgUrl += self.imgNameMaker(self.madrugada)
        elif turno == "manha":
            imgUrl += self.imgNameMaker(self.manha)
        elif turno == "tarde":
            imgUrl += self.imgNameMaker(self.tarde)
        elif turno == "noite":
            imgUrl += self.imgNameMaker(self.noite)
        else:
            imgUrl += "error.png"
        return imgUrl
    
    def turno(self):
        TURNOS={
                'madrugada': [0,6],
                'manha':     [6,12],
                'tarde':     [12,18],
                'noite':     [18,00]
        }
        hora = int(self.dt_inclusao.strftime('%H'))-3
        for i in TURNOS:
            if hora >= TURNOS[i][0] and hora < TURNOS[i][1]:
                return i
            
    def timeBeholder(self):
        turno = self.turno()
        try:
            return self.getImg(turno)
        except:
            return self.getImg("erro")