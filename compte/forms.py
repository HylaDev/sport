from django.forms import ModelForm, Form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import Group

class CreationUserForm(UserCreationForm):
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)
    class Meta:
        model = User
        fields=('username','first_name','last_name','email','password1','password2', 'group')

class SetPassword(forms.Form):
    last_password = forms.CharField(required=True)
    new_password = forms.CharField(required=True)
    repeat_password = forms.CharField(required=True)

class Compte_Form(Form):
    adresse = forms.CharField(required=False)
    taille = forms.FloatField(required=False)
    poids = forms.CharField(required=False)
    pied_main = forms.CharField(required=False)
    sexe = forms.CharField(required=False)
    date_naissance = forms.DateField(required=False)
    contact = forms.CharField(required=False)
    image = forms.ImageField(required=False)
    poste = forms.ModelChoiceField(queryset = Poste.objects.all(), required=False)
    role = forms.CharField(required=False)
    club_actuel = forms.CharField(required=False)
    historique_club = forms.CharField(required=False)
    niveau = forms.ModelChoiceField(queryset=Niveau.objects.all(), required=False)
    discipline_sportive = forms.ModelChoiceField(queryset=Discipline_Sportive.objects.all(), required=False)

class Edit_User_Form(ModelForm):
    username = forms.CharField(max_length=50,required = True)
    first_name = forms.CharField(max_length=50,required = True)
    last_name = forms.CharField(max_length=50,required = True)
    email = forms.EmailField(max_length=50)
    
    class Meta:
        model = User
        fields=('username','first_name', 'last_name', 'email')

class Edit_Compte_Form(ModelForm):
    adresse = forms.CharField(required=False)
    taille = forms.FloatField(required=False)
    poids = forms.CharField(required=False)
    pied_main = forms.CharField(required=False)
    sexe = forms.CharField(required=False)
    contact = forms.CharField(required=False)
    poste = forms.ModelChoiceField(queryset = Poste.objects.all(), required=False)
    role = forms.CharField(required=False)
    club_actuel = forms.CharField(required=False)
    niveau = forms.ModelChoiceField(queryset=Niveau.objects.all(), required=False)
    discipline_sportive = forms.ModelChoiceField(queryset=Discipline_Sportive.objects.all(), required=False)
    
    class Meta:
        model = Compte
        fields=('adresse','taille', 'poids', 'pied_main','sexe','contact','poste','role','club_actuel','niveau','discipline_sportive')