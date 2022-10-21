from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import *
from .models import *
from talentSport.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from sport.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.template.loader import get_template
from xhtml2pdf import pisa

 
@login_required(login_url='sign_in')
def create_cv(request,id):
    compte = Compte.objects.get(user=id)
    
    template_path = 'compte/resume.html'
    
    context={'compte':compte}

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="cv.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
    

@login_required(login_url='sign_in')
def gencv(request,id):
    user = request.user
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    
    discipline = Compte.objects.get(user=id)
    
    lignes = ["Mon cv",
              "================="]
    
    lignes.append(discipline.user.first_name)
    lignes.append(discipline.user.last_name)
    lignes.append(discipline.user.email)
    lignes.append(discipline.adresse)
    lignes.append(discipline.discipline_sportive.désignation)
    lignes.append(discipline.poste.désignation)
    lignes.append(discipline.role)
    lignes.append(discipline.image.url)
    lignes.append("")
        
        
    for ligne in lignes:
        textob.textLine(ligne)
        
        
    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    
    return FileResponse(buf, as_attachment=True, filename='use.pdf')
    

@login_required(login_url='sign_in')
def profil(request, id):
    user = User.objects.get(id=id)
    niveaux = Niveau.objects.all()
    discipline_sportives = Discipline_Sportive.objects.all()
    compte = user.compte

    followers = compte.followers.all()
    if len(followers)== 0:
        is_following = False


    for follower in followers :
        if follower == request.user:
            is_following = True
            break
        else:
            is_following = False

    nbre_abonne = len(followers)
    form = Compte_Form()
    if request.method == "POST":
        form = Compte_Form(request.POST, request.FILES)
        if form.is_valid():
            adresse = form.cleaned_data['adresse']
            taille = form.cleaned_data['taille']
            poids = form.cleaned_data['poids']
            poste = form.cleaned_data['poste']
            pied_main = form.cleaned_data['pied_main']
            sexe = form.cleaned_data['sexe']
            date_naissance = form.cleaned_data['date_naissance']
            role = form.cleaned_data['role']
            niveau = form.cleaned_data['niveau']
            contact = form.cleaned_data['contact']
            club_actuel = form.cleaned_data['club_actuel']
            historique_club = form.cleaned_data['historique_club']
            image = form.cleaned_data['image'] 
            discipline_sportive = form.cleaned_data['discipline_sportive']
            user.compte.adresse = adresse
            user.compte.taille = taille
            user.compte.poids = poids
            user.compte.poste = poste
            user.compte.pied_main = pied_main
            user.compte.sexe = sexe
            user.compte.date_naissance = date_naissance
            user.compte.role = role
            user.compte.niveau = niveau
            user.compte.club_actuel = club_actuel
            user.compte.historique_club = historique_club
            user.compte.contact = contact
            user.compte.image = image
            user.compte.discipline_sportive = discipline_sportive
            user.compte.save()
            messages.success(request, 'Information bien ajouté')
        else:
            messages.error(request,'Il y a une erreur')          
    context={
    'form':form,
    'niveaux':niveaux, 
    'discipline_sportives':discipline_sportives,
    'is_following':is_following,
    'nbre_abonne':nbre_abonne,
    'followers':followers}

    return render(request, 'compte/profil.html',context)

@login_required(login_url='sign_in')
def user_publications(request,id):
    user = User.objects.get(id=id)
    publications = Publication.objects.filter(user=user).order_by('-date_creation').filter(is_valid=True)
    context={'user':user,
    'publications':publications,}

    return render(request, 'compte/user_publications.html',context)

@login_required(login_url='sign_in')
def user_annonces(request,id):
    user = User.objects.get(id=id)
    annonces = Publication.objects.filter(user=user).order_by('-date_creation').filter(is_valid=True)
    context={'user':user,
    'annonces':annonces,} 

    return render(request, 'compte/user_annonces.html',context)

@login_required(login_url='sign_in')
def abonnement(request,id):
    return render(request, 'compte/abonnement.html')

@login_required(login_url='sign_in')
def user_followers(request,id):
    user = User.objects.get(id=id)
    compte = user.compte
    followers = compte.followers.all()
    nbre_abonne = len(followers)
    context={'user':user,
    'followers':followers,
    'nbre_abonne':nbre_abonne}

    return render(request, 'compte/user_followers.html',context)

    
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


@login_required(login_url='sign_in')
def get_poste(request,discipline_sportive):
    postes = Poste.objects.filter(discipline_sportive=discipline_sportive).values('id','désignation')
    return JsonResponse({'data':list(postes)},safe=False)


@login_required(login_url='sign_in')
def edit_information(request,id):
    user = User.objects.get(id=id)
    discipline_sportives = Discipline_Sportive.objects.all()
    niveaux = Niveau.objects.all()
    postes = Poste.objects.all()
    form = Edit_User_Form(instance  = user)
    if request.method == 'POST':
        form = Edit_User_Form(request.POST, instance  = user)
        if form.is_valid(): 
            username = form.cleaned_data["username"]
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]        
            email = form.cleaned_data['email']

            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            messages.success(request,'info bien modifiée')
            return redirect('/compte/edit_user_info/'+str(user.id))
    context={
    'form':form, 
    'user':user, 
    'discipline_sportives':discipline_sportives,
    'niveaux':niveaux,
    'postes':postes,
    }
    return render(request, 'compte/edit_user.html',context)
@login_required(login_url='sign_in')
def edit_compte(request):
    compte = request.user
    form = Edit_Compte_Form(instance  = compte)

    if request.method == 'POST':
        form = Edit_Compte_Form(request.POST,instance  = compte)
        if form.is_valid():
            adresse = form.cleaned_data['adresse']
            taille = form.cleaned_data['taille']
            poids = form.cleaned_data['poids']
            poste = form.cleaned_data['poste']
            pied_main = form.cleaned_data['pied_main']
            sexe = form.cleaned_data['sexe']
            role = form.cleaned_data['role']
            niveau = form.cleaned_data['niveau']
            contact = form.cleaned_data['contact']
            club_actuel = form.cleaned_data['club_actuel']
            historique_club = form.cleaned_data['historique_club']

            compte.adresse = adresse
            compte.taille = taille
            compte.poids = poids
            compte.poste = poste
            compte.pied_main = pied_main
            compte.sexe = sexe
            compte.role = role
            compte.niveau = niveau
            compte.club_actuel = club_actuel
            compte.historique_club = historique_club
            compte.contact = contact
            compte.save()
            messages.success(request,'info bien modifiée')
            return redirect('/compte/edit_user_info/'+str(compte.id))
    return render(request, 'compte/edit_user.html')

@login_required(login_url='sign_in')
def set_password(request):
    user = request.user
    if request.method == 'POST':
        form = SetPassword(request.POST)
        if form.is_valid():
            last_password = form.cleaned_data['last_password']
            new_password = form.cleaned_data['new_password']
            repeat_password = form.cleaned_data['repeat_password']
            utilisateur = authenticate(request, username=user.username, password=last_password)
            if utilisateur is not None:
                if new_password == repeat_password:
                    user.set_password(new_password)
                    user.save()
                    user = authenticate(request, username=user.username, password=new_password)
                    if user is not None:
                        login(request, user)
                        messages.success(request,'Mot de passe modifié')
                        return redirect('/compte/edit_user_info/'+str(user.id))


@login_required(login_url='sign_in')
def ajouter_abonne(request, id):
    user = User.objects.get(id = id)
    user.compte.followers.add(request.user)

    notification = Notification.objects.create(type_notification = 3, expediteur = request.user, destinataire = user.compte.user )

    return redirect ('detail_profil', id=id)

@login_required(login_url='sign_in')
def se_desabonne(request, id):
    user = User.objects.get(id = id)
    user.compte.followers.remove(request.user) 

    return redirect ('detail_profil',id=id)
@login_required(login_url='sign_in') 
def detail_profil(request,id):
    user = User.objects.get(id=id)
    compte = user.compte
    nbre_pubs = Publication.objects.filter(user = user).filter(is_valid=True).count()
    pubs = Publication.objects.filter(user= user).order_by('-date_creation').filter(is_valid=True)
    followers = compte.followers.all()

    if len(followers)== 0:
        is_following = False


    for follower in followers :
        if follower == request.user:
            is_following = True
            break
        else:
            is_following = False

    nbre_abonne = len(followers)

    context={
    'user':user,
    'pubs':pubs,
    'nbre_abonne':nbre_abonne,
    'is_following':is_following,
    'nbre_pubs':nbre_pubs,
    }
    return render(request, 'compte/details.html',context)

def sign_in(request):
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Vous êtes bien connecté')
            return redirect('home')
    context={}
    return render(request, 'compte/sign_in.html',context)

def sign_up(request):
    groups = Group.objects.all()
    form = CreationUserForm()

    if request.POST:
        form = CreationUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = form.cleaned_data['group']
            group.user_set.add(user) 
            Compte.objects.create(
                user = user
            )
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request,'Compte bien crée')
                return redirect('/compte/profil/'+str(user.id))
    context={'groups':groups, 'form':form}
    return render(request, 'compte/sign_up.html',context)

@login_required(login_url='sign_in')
def Search(request):
    discipline_sportives = Discipline_Sportive.objects.all()
    query = request.GET.get('query')
    comptes = Compte.objects.filter(Q(user__first_name__icontains=query)|Q(user__last_name__icontains=query))
    publications = Publication.objects.filter(Q(pub_content__icontains=query))

    context = {
    'comptes':comptes,
    'discipline_sportives':discipline_sportives,
    'publications':publications
    }
    return render (request, 'compte/search.html', context)


def SearchPub(request):
    discipline_sportives = Discipline_Sportive.objects.all()
    query = request.GET.get('query')
    publications = Publication.objects.filter(Q(pub_content__icontains=query))

    context = {
    'discipline_sportives':discipline_sportives,
    'publications':publications
    }
    return render (request, 'compte/search_pub_answers.html', context)

def user_role(request):
    groups = Group.objects.all()
    context = {'groups':groups}
    return render(request, 'compte/user_role.html', context)

@login_required(login_url='sign_in')
def logout_view(request):
    logout(request)
    return redirect('sign_in')