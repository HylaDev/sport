from django import forms
from .models import *
from talentSport.models import *
from django.forms import ModelForm, Form

class Edit_pub_form(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ('title','pub_content','discipline_sportive','categorie','image', 'videofile','is_valid')
        
        widgets = {
            
        }
        



 
 