from .models import *
from django import forms


class Evento_form(forms.ModelForm):
    class Meta:
        model = Evento
        widgets={
            'app_name': forms.HiddenInput()
        }
        exclude = []

    banner_img = forms.FileField(required=False, label='Imagem do banner', widget=forms.FileInput(
        attrs={'class': 'form-control','accept': 'application/image', 'enctype': "multipart/form-data"}))
