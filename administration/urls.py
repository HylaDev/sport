from django.urls import path
from administration.views import * 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [ 
    path('', dashbord, name="dashbord"),
    path('connexion', connexion, name="connexion"),
    path('deconnexion/', deconnexion, name="deconnexion"),
    path('utilisateurs', utilisateurs, name="utilisateurs"),
    path('groupes', groupes, name="groupes"),
    path('publication', publication, name="publication"),
    path('commentaire', commentaires, name="commentaires"),
    path('supprimer/<int:id>', delete_publication, name="delete_publication"),
    path('modifier_publications/<int:id>', edit_publications, name="edit_publications"),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)