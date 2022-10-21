# Generated by Django 4.0.4 on 2022-07-03 17:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Discipline_Sportive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('désignation', models.CharField(max_length=20)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Niveau',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('désignation', models.CharField(max_length=20)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Profil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('désignation', models.CharField(max_length=20)),
                ('est_public', models.BooleanField(default=False, null=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Poste',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('désignation', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('discipline_sportive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compte.discipline_sportive')),
            ],
        ),
        migrations.CreateModel(
            name='Compte',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL, verbose_name='User')),
                ('adresse', models.CharField(blank=True, max_length=50, null=True, verbose_name='Adresse')),
                ('taille', models.FloatField(blank=True, max_length=50, null=True)),
                ('poids', models.CharField(blank=True, max_length=50, null=True)),
                ('pied_main', models.CharField(blank=True, choices=[('Droit', 'Droit'), ('Gauche', 'Gauche'), ('Les deux', 'Les deux')], max_length=50, null=True)),
                ('sexe', models.CharField(blank=True, choices=[('Masculin', 'Masculin'), ('Féminin', 'Féminin')], max_length=20, null=True)),
                ('date_naissance', models.DateField(blank=True, null=True)),
                ('role', models.CharField(blank=True, choices=[('Joueur', 'Joueur'), ('Coach', 'Coach')], max_length=20, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='photo_profil/%Y/%m/%d')),
                ('contact', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, verbose_name='Mobile')),
                ('club_actuel', models.CharField(blank=True, max_length=255, null=True)),
                ('historique_club', models.CharField(blank=True, max_length=255, null=True)),
                ('discipline_sportive', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compte.discipline_sportive')),
                ('followers', models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('niveau', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compte.niveau')),
                ('poste', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compte.poste')),
            ],
        ),
    ]