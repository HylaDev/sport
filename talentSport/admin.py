from django.contrib import admin
from .models import *

# Register your models here.

class PublicationAdmin(admin.ModelAdmin):
    list_display=('id','user','title','pub_content','categorie','discipline_sportive','image','videofile','is_valid','date_creation')
    ordering=('user',)

class AnnonceAdmin(admin.ModelAdmin):
    list_display=('id','user','titre','corps','image','videofile','is_valid','date_creation')
    ordering=('user',)

class CommentaireAdmin(admin.ModelAdmin):
    list_display=('id','auteur','publication','annonce','commentaire','date_creation')
    ordering=('auteur',)


admin.site.register(Publication,PublicationAdmin)
admin.site.register(Annonce,AnnonceAdmin)
admin.site.register(Commentaire,CommentaireAdmin)
admin.site.register(Notification)
admin.site.register(CategoriePublication)

