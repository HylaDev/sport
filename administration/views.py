from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from talentSport.models import *
from compte.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from sport.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.db.models import Q
from django.http import JsonResponse
@login_required(login_url='connexion')
def dashbord(request):
	users = Compte.objects.count()
	publications = Publication.objects.count()
	commentaires = Commentaire.objects.count()
	discipline_sportives = Discipline_Sportive.objects.count()
	context ={
	'users':users,
	'publications':publications,
	'commentaires':commentaires,
	'discipline_sportives':discipline_sportives,
	}
	return render(request, 'admin/pages/dashbord.html',context)

@login_required(login_url='connexion')
def utilisateurs(request):
	users = User.objects.order_by('-date_joined')
	context ={
	'users':users,
	}
	return render(request, 'admin/pages/utilisateurs.html',context)

@login_required(login_url='connexion')
def publication(request):
	publications = Publication.objects.order_by('-date_creation')
	context ={
	'publications':publications,
	} 
	return render(request, 'admin/pages/publications.html',context)

@login_required(login_url='connexion')
def delete_publication(request, id):
    publication = Publication.objects.get(id=id)
    
    if request.method== 'POST':
        publication.delete()
        messages.success(request,'Publication bien supprimée')
        return redirect('publication')
    context = {'publication':publication}
    
    return render(request, 'admin/pages/delete_pub.html',context)
@login_required(login_url='connexion')
def commentaires(request):
	commentaires = Commentaire.objects.order_by('-date_creation')
	context ={
	'commentaires':commentaires,
	} 
	return render(request, 'admin/pages/commentaires.html',context)

@login_required(login_url='connexion')
def edit_publications(request,id):
	publications = Publication.objects.get(id=id)
	users = User.objects.all()
	categories = CategoriePublication.objects.all()
	disciplines = Discipline_Sportive.objects.all()
 
	form = Edit_pub_form(
					  instance=publications,
                      initial={
						'user':publications.user,
						'title':publications.title,
						'pub_content':publications.pub_content,
						'categorie':publications.categorie,
						'discipline_sportive':publications.discipline_sportive,
						'image':publications.image,
						'videofile':publications.videofile,
						'is_valid':publications.is_valid,
					  })
	if request.POST:
		form = Edit_pub_form(request.POST,
			          instance=publications,
                      initial={
						'user':publications.user,
						'title':publications.title,
						'pub_content':publications.pub_content,
						'categorie':publications.categorie,
						'discipline_sportive':publications.discipline_sportive,
						'image':publications.image,
						'videofile':publications.videofile,
						'is_valid':publications.is_valid,
					  })
		if form.is_valid():
			form.save()
			messages.success(request, 'Publication bien modifiée')
			return redirect('publication')
	context ={
    'form':form,
	'publications':publications,
	'users':users,
 	'categories':categories,
	'disciplines':disciplines,
	}
	return render(request, 'admin/pages/edit_publication.html',context)


@login_required(login_url='connexion')
def groupes(request):
	groupes = Group.objects.all()
	context ={
	'groupes':groupes,
	}
	return render(request, 'admin/pages/groupes.html',context)

def connexion(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_superuser == True:
                login(request, user)
                messages.success(request, 'Vous êtes bien connecté')
                return redirect('dashbord')
            else:
                messages.error(request,'Vous n\'êtes pas autorisé à vous connecter')
                return redirect('connexion')

    context={}
    return render(request, 'admin/compte/connexion.html',context)

@login_required(login_url='connexion')
def deconnexion(request):
    logout(request)
    return redirect('connexion')