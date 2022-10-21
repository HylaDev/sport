from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from compte.models import *
from .forms import *
from .models import *
from django.http import HttpResponseRedirect, HttpResponse
from compte.models import *
from django.contrib import messages
import requests
import json


@login_required(login_url='sign_in')
def home(request):
    users = User.objects.all() 
    comptes = Compte.objects.all()
    pubs = Publication.objects.filter(is_valid = True) & Publication.objects.order_by("-date_creation")
    discipline_sportives = Discipline_Sportive.objects.all()
    commentaire = Commentaire.objects.count()
    context = {
    'discipline_sportives':discipline_sportives,
     'pubs':pubs,
     'users':users, 
     'comptes':comptes,
     'commentaire':commentaire,
     }
    return render(request, 'talentSport/home.html',context)

def index(request):
    return render(request, 'talentSport/index.html')

@login_required(login_url='sign_in')
def faq(request):
    discipline_sportives = Discipline_Sportive.objects.all()

    context = {'discipline_sportives':discipline_sportives}
    return render(request, 'talentSport/faq.html', context)

@login_required(login_url='sign_in')
def annonces(request):
    users = User.objects.all() 
    comptes = Compte.objects.all()
    annonces = Publication.objects.filter(is_valid = True).order_by("-date_creation")
    discipline_sportives = Discipline_Sportive.objects.all()
    commentaire = Commentaire.objects.count()
    context = {
    'discipline_sportives':discipline_sportives,
     'users':users, 
     'comptes':comptes,
     'commentaire':commentaire,
     'annonces':annonces,
     } 
    return render(request, 'talentSport/annonces.html',context)
@login_required(login_url='sign_in')
def publications(request):
    users = User.objects.all() 
    comptes = Compte.objects.all()
    publications = Publication.objects.filter(is_valid = True).order_by("-date_creation")
    discipline_sportives = Discipline_Sportive.objects.all()
    commentaire = Commentaire.objects.count()
    context = {
    'discipline_sportives':discipline_sportives,
     'users':users, 
     'comptes':comptes,
     'commentaire':commentaire,
     'publications':publications,
     } 
    return render(request, 'talentSport/publications.html',context)

@login_required(login_url='sign_in')
def discipline_pub(request,id):
    discipline_sportive = Discipline_Sportive.objects.get(id=id)
    users = User.objects.all()
    comptes = Compte.objects.all()
    discipline_sportives = Discipline_Sportive.objects.all()
    commentaire = Commentaire.objects.all() 
    pubs = Publication.objects.filter(discipline_sportive = id).filter(is_valid=True)  & Publication.objects.order_by("-date_creation")
    context = {
    'discipline_sportive':discipline_sportive, 
    'users':users,
    'pubs':pubs,
    'discipline_sportives':discipline_sportives,
    'comptes':comptes,
    'commentaire':commentaire,}
    return render(request, 'talentSport/home.html',context)



@login_required(login_url='sign_in')
def new_pub(request): 
    #params = {
     # 'models': 'nudity,wad,offensive,scam,text-content',
      #'api_user': '47600474',
      #'api_secret': 'es3jUsoNSDAqtMvr55La'
    #}
    #files = {'media': open('', 'rb')}
    #r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

    #output = json.loads(r.text)
    discipline_sportives =  Discipline_Sportive.objects.all()
    user = request.user
    categorie = CategoriePublication.objects.get(désignation="Publication")
    form = Publication_Form()
    if request.POST:
        form = Publication_Form(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = user
            instance.categorie = categorie
            instance.save() 
            messages.success(request,'Contenu bien publié et en cours d\'analyse') 
            return redirect('home')
    context = {
    'form':form,
    'discipline_sportives':discipline_sportives,
    'categorie':categorie}
    return render(request, 'talentSport/new_pub.html',context)


@login_required(login_url='sign_in')
def new_announce(request): 
    #params = {
     # 'models': 'nudity,wad,offensive,scam,text-content',
      #'api_user': '47600474',
      #'api_secret': 'es3jUsoNSDAqtMvr55La'
    #}
    #files = {'media': open('', 'rb')}
    #r = requests.post('https://api.sightengine.com/1.0/check.json', files=files, data=params)

    #output = json.loads(r.text)
    user = request.user
    discipline_sportives =  Discipline_Sportive.objects.all()
    categorie = CategoriePublication.objects.get(désignation="Annonce")
    form = Publication_Form()
    if request.POST:
        form = Publication_Form(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit = False)
            instance.user = user
            instance.categorie = categorie
            instance.save()
            messages.success(request,'Contenu bien publié et en cours d\'analyse')
            return redirect('home')
    context = {
    'form':form,
    'discipline_sportives':discipline_sportives,
    'categorie':categorie,
    }
    return render(request, 'talentSport/new_announce.html',context)

@login_required(login_url='sign_in')
def detail_pub(request,id):
    users = User.objects.all()
    auteur = request.user
    comptes = Compte.objects.all()
    discipline_sportives = Discipline_Sportive.objects.all()
    pub = Publication.objects.get(id=id)
    commentaires = Commentaire.objects.filter(publication=id).order_by('-date_creation')
    nbre_commentaire = Commentaire.objects.filter(publication=id).count()

    form = Pub_Commentaire_Form()

    if request.POST:
        form = Pub_Commentaire_Form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False) 
            instance.auteur = auteur
            instance.save()
            notification = Notification.objects.create(type_notification=2, expediteur = request.user, destinataire = pub.user,publication=pub)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    context={
    'pub':pub,
    'users':users,
    'comptes':comptes,
    'discipline_sportives':discipline_sportives,
    'commentaires':commentaires,
    'nbre_commentaire':nbre_commentaire,
    }

    return render(request,'talentSport/detail_pub.html',context)

@login_required(login_url='sign_in')
def detail_annonce(request,id):
    users = User.objects.all()
    auteur = request.user
    comptes = Compte.objects.all()
    discipline_sportives = Discipline_Sportive.objects.all()
    pub = Publication.objects.get(id=id)
    commentaires = Commentaire.objects.filter(publication=id).order_by('-date_creation')
    nbre_commentaire = Commentaire.objects.filter(publication=id).count()

    form = Pub_Commentaire_Form()

    if request.POST:
        form = Pub_Commentaire_Form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False) 
            instance.auteur = auteur
            instance.save()
            notification = Notification.objects.create(type_notification=2, expediteur = request.user, destinataire = pub.user,publication=pub)
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
    context={
    'pub':pub,
    'users':users,
    'comptes':comptes,
    'discipline_sportives':discipline_sportives,
    'commentaires':commentaires,
    'nbre_commentaire':nbre_commentaire,
    }

    return render(request,'talentSport/detail_annonce.html',context)

@login_required(login_url='sign_in')
def ReponseCommentaire(request, id,pub_id):
    pubs = Publication.objects.get(id=pub_id)
    commentaire_parent = Commentaire.objects.get(id=id)
    form = Commentaire_Form()
    if request.POST:
        form = Commentaire_Form(request.POST)
        if form.is_valid():
            nouveau_commentaire = form.save(commit=False)
            nouveau_commentaire.auteur = request.user
            nouveau_commentaire.parent = commentaire_parent

            nouveau_commentaire.save()
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)



@login_required(login_url='sign_in')
def AddLike(request, id):
    publication = Publication.objects.get(id=id)


    #for dislike in publication.dislikes.all():
    #    if dislike == request.user:
    #        is_dislike = True
    #        break

    #if is_dislike:
    #    publication.dislikes.remove(request.user)

    is_like  = False

    for like in publication.likes.all():
        if like == request.user:
            is_like = True
            break
    if not is_like:
        publication.likes.add(request.user)
        notification = Notification.objects.create(type_notification = 1, expediteur = request.user, destinataire = publication.user,publication=publication)

    if is_like:
        publication.likes.remove(request.user)

    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next) 

@login_required(login_url='sign_in')
def LikeAnnounce(request, id):
    annonce = Annonce.objects.get(id=id)

    is_like  = False

    for like in annonce.likes.all():
        if like == request.user:
            is_like = True
            break
    if not is_like:
        annonce.likes.add(request.user)
        notification = Notification.objects.create(type_notification = 1, expediteur = request.user, destinataire = annonce.user,annonce=annonce)

    if is_like:
        annonce.likes.remove(request.user)

    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)

@login_required(login_url='sign_in')
def AddCommentLike(request, id):
    commentaire = Commentaire.objects.get(id=id)

    #for dislike in publication.dislikes.all():
    #    if dislike == request.user:
    #        is_dislike = True
    #        break

    #if is_dislike:
    #    publication.dislikes.remove(request.user)

    is_like  = False

    for like in commentaire.likes.all():
        if like == request.user:
            is_like = True
            break
    if not is_like:
        commentaire.likes.add(request.user)
        notification = Notification.objects.create(type_notification = 1, expediteur = request.user, destinataire = commentaire.auteur,commentaire=commentaire)

    if is_like:
        commentaire.likes.remove(request.user)

    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)


@login_required(login_url='sign_in')
def partager_pub(request,id):
    publication = Publication.objects.get(id =id)
    discipline_sportives =  Discipline_Sportive.objects.all()
    context={
        'publication':publication,
        'discipline_sportives':discipline_sportives
        }
    return render(request, 'talentSport/partager.html',context)

@login_required(login_url='sign_in')
def notification_annonce(request,notif_id,annonce_id):
    notification = Notification.objects.get(id=notif_id)
    annonce = Annonce.objects.get(id=annonce_id)

    notification.est_vu=True
    notification.save()

    return redirect('detail_annonce',id=annonce_id)


@login_required(login_url='sign_in')
def notification_publication(request,notif_id,pub_id):
    notification = Notification.objects.get(id=notif_id)
    publication = Publication.objects.get(id=pub_id)

    notification.est_vu=True
    notification.save()

    return redirect('detail_pub',id=pub_id)

@login_required(login_url='sign_in')
def notification_abonnes(request,notif_id,id):
    notification = Notification.objects.get(id=notif_id)
    user = User.objects.get(id=id)
    notification.est_vu = True
    notification.save()

    return redirect('user_followers',id=id)

@login_required(login_url="sign_in")
def retirer_notification(request, notif_id):
    notification = Notification.objects.get(id=notif_id)

    notification.est_vu= True
    notification.save()

    return HttpResponse('Success', content_type='text/plain')
