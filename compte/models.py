from django.db import models
from django.contrib.auth.models import User 
from django.db.models.deletion import CASCADE
from phonenumber_field.modelfields import PhoneNumberField

class Profil(models.Model):
	désignation = models.CharField(max_length=20)
	est_public = models.BooleanField(default=False,null=True, blank = False)
	description = models.TextField()

	def __str__(self):
	    return str(self.désignation)

class Niveau(models.Model):
	désignation = models.CharField(max_length=20)
	description = models.TextField()

	def __str__(self):
		return str(self.désignation)

class Discipline_Sportive(models.Model):
	désignation = models.CharField(max_length=20)
	description = models.TextField()

	def __str__(self):
	    return str(self.désignation)

class Poste(models.Model):
	désignation = models.CharField(max_length=50)
	description = models.TextField()
	discipline_sportive = models.ForeignKey(Discipline_Sportive, on_delete=models.CASCADE)

	def __str__(self):
		return str(self.désignation)
	

class Compte(models.Model):
	ROLES = [
	('Joueur', 'Joueur'),
	('Coach', 'Coach'),
	]
	PIED_MAIN = [
	('Droit','Droit'),
	('Gauche','Gauche'),
	('Les deux','Les deux')
	]
	SEXE = [
	('Masculin', 'Masculin'),
	('Féminin', 'Féminin'),
	]
	user = models.OneToOneField(User, verbose_name="User", on_delete=models.CASCADE, primary_key=True,)
	adresse = models.CharField(max_length=50, verbose_name="Adresse", null=True,blank=True)
	taille = models.FloatField(max_length=50, null=True, blank=True)
	poids = models.CharField(max_length=50 ,blank = True, null = True)
	pied_main = models.CharField(max_length=50,choices = PIED_MAIN, null = True, blank=True)
	sexe = models.CharField(max_length=20, choices = SEXE, null = True,blank=True)
	date_naissance = models.DateField( null = True,blank=True)
	poste = models.ForeignKey(Poste, on_delete = models.CASCADE,null = True,blank=True)
	role = models.CharField(max_length=20,choices=ROLES,null = True,blank=True)
	niveau = models.ForeignKey(Niveau, on_delete=models.CASCADE,null = True,blank=True)
	discipline_sportive = models.ForeignKey(Discipline_Sportive, on_delete=models.CASCADE,null = True,blank=True)
	image = models.ImageField(upload_to="photo_profil/%Y/%m/%d",null=True, blank=True)
	contact = PhoneNumberField(null=True, blank=True,verbose_name="Mobile")
	club_actuel = models.CharField(max_length=255,null = True,blank=True)
	historique_club = models.CharField(max_length=255,null = True, blank = True)
	followers = models.ManyToManyField(User, blank=True, related_name='followers') 

	def __str__(self):
	    return str(self.user)





