from django.urls import path
from compte.views import * 
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('profil/<str:id>', profil, name="profil"),
    path('detail/<str:id>', detail_profil, name="detail_profil"),
    path('sign_in/', sign_in, name="sign_in"), 
    path('sign_up/', sign_up, name="sign_up"),
    path('edit_user_info/<int:id>', edit_information, name="edit_information"),
    path('edit_compte/', edit_compte, name="edit_compte"),
    path('set_password', set_password, name="set_password"),
    path('logout/', logout_view, name="logout_view"),
    path('ajouter_abonne/<int:id>', ajouter_abonne, name="ajouter_abonne"),
    path('se_désabonne/<int:id>', se_desabonne, name="se_desabonne"),
    path('search/', Search, name="Search"),
    path('search/publications', SearchPub, name="SearchPub"),
    path('<str:discipline_sportive>', get_poste, name="get_poste"),
    path('mes_publications/<int:id>', user_publications, name="user_publications"),
    path('mes_annonces/<int:id>', user_annonces, name="user_annonces"),
    path('mes_abonnes/<int:id>', user_followers, name="user_followers"),
    path('create_cv/<int:id>', create_cv, name="create_cv"),
    path('gencv/<int:id>', gencv, name="gencv"),
    path('mon_abonnement/<int:id>', abonnement, name="abonnement"),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)