from django.forms import ModelForm, Form
from django import forms
from .models import *
from phonenumber_field.modelfields import PhoneNumberField

class Publication_Form(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('title','pub_content','discipline_sportive','image', 'videofile')

 
class Annonce_Form(forms.ModelForm):
    class Meta:
        model = Annonce
        fields = ('titre','corps','image', 'videofile')

class Pub_Commentaire_Form(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ('publication','commentaire',)


class Annonce_Commentaire_Form(forms.ModelForm):
    class Meta:
        model = Commentaire
        fields = ('annonce','commentaire',)