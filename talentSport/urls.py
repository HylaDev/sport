from django.urls import path
from compte.views import * 
from django.conf import settings
from django.conf.urls.static import static
from .views import *
 
urlpatterns = [
    path('accueil/', home, name="home"),
    path('', index, name="index"),
    path('faq/', faq, name="faq"),
    path('annonces/', annonces, name="annonces"),
    path('publications/', publications, name="publications"),
    path('nouvelle_publication/', new_pub, name="new_pub"),
    path('partager_publication/<int:id>', partager_pub, name="partager_pub"),
    path('nouvelle_annonce/', new_announce, name="new_announce"),
    path('detail_publication/<int:id>', detail_pub, name="detail_pub"),
    path('detail_annonce/<int:id>', detail_annonce, name="detail_annonce"),
    path('publication_discipline/<int:id>', discipline_pub, name="discipline_pub"),
    path('publication/<int:id>', AddLike, name="like"),
    path('annonce/<int:id>', LikeAnnounce, name="jaime"),
    path('commentaire/<int:id>/like', AddCommentLike, name="comment-like"),
    path('publication/<int:pub_id>/commentaire/<int:id>/reponse', ReponseCommentaire, name="reponse-commentaire"),
    path('notification/<int:notif_id>/annonce/<int:annonce_id>', notification_annonce, name="notifi_annonce"),
    path('notification/<int:notif_id>/publication/<int:pub_id>', notification_publication, name="notifi_pub"),
    path('notification/<int:notif_id>/mes_abonnes/<int:id>', notification_abonnes, name="notif_abonne"),
    path('notification/suppression/<int:notif_id>', retirer_notification, name="sup_notif"),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)