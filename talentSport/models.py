from django.db import models
from django.contrib.auth.models import User 
from compte.models import *
from phonenumber_field.modelfields import PhoneNumberField

class CategoriePublication(models.Model):
	désignation = models.CharField(max_length=15, null = True, blank=True)
	description = models.TextField(null = True, blank=True)
 
class Publication(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=50, null = True, blank=True)
	pub_content = models.TextField(null= True, blank = True)
	categorie = models.ForeignKey(CategoriePublication, on_delete= models.CASCADE)
	discipline_sportive = models.ForeignKey(Discipline_Sportive, on_delete=models.CASCADE, null=True, blank=True)	
	date_creation = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to="image_pubs_annonces/%Y/%m/%d",null=True, blank=True)
	is_valid = models.BooleanField(default=False, null=True, blank = False)
	videofile = models.FileField(upload_to="videos/%Y/%m/%d", null=True, blank=True)
	likes = models.ManyToManyField(User, blank=True, related_name= 'likes')
	

	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url
class Image(models.Model):
    image = models.ImageField(upload_to="image_pubs_annonces/%Y/%m/%d",null=True, blank=True)
    
class Annonce(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	titre = models.CharField(max_length=50, null = True, blank=True)
	corps = models.TextField(null= True, blank = True)
	date_creation = models.DateTimeField(auto_now_add=True)
	image = models.ImageField(upload_to="image_pubs_annonces/%Y/%m/%d",null=True, blank=True)
	is_valid = models.BooleanField(default=False, null=True, blank = False)
	videofile = models.FileField(upload_to="videos/%Y/%m/%d", null=True, blank=True)
	likes = models.ManyToManyField(User, blank=True, related_name= 'jaime')
	

	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = ''
		return url

class Commentaire(models.Model):
	auteur = models.ForeignKey(User, on_delete=models.CASCADE)
	publication = models.ForeignKey(Publication, on_delete = models.CASCADE, null=True)
	date_creation = models.DateTimeField(auto_now_add=True)
	commentaire = models.TextField()
	annonce = models.ForeignKey(Annonce, on_delete = models.CASCADE, null=True)
	likes = models.ManyToManyField(User, related_name='commentaire_like', blank=True)
	parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name="+")

	@property
	def children(self):
		return Commentaire.objects.filter(parent=self).order_by('-date_creation').all()


	@property
	def is_parent(self):
		if self.parent is None:
			return True
		return False


class Notification(models.Model):
	# 1 = Like 2=Commentaire 3=Abonne
	type_notification = models.IntegerField()
	expediteur = models.ForeignKey(User, on_delete = models.CASCADE, null=True, related_name="expéditeur")
	destinataire = models.ForeignKey(User, on_delete = models.CASCADE, null=True, related_name="destinataire") 
	publication = models.ForeignKey(Publication, on_delete = models.CASCADE,blank=True, null=True, related_name="+")
	commentaire = models.ForeignKey(Commentaire, on_delete = models.CASCADE,blank=True, null = True, related_name="+")
	annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE,blank=True, null = True, related_name="+")
	date_envoi = models.DateTimeField(auto_now_add=True)
	est_vu = models.BooleanField(default=False)
 
class Tag(models.Model):
    name = models.CharField(max_length=255)