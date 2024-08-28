from django.apps import apps
from django.db import models
import json
class MaListe(models.Model):
    nombres = models.TextField()

    def set_nombres(self, liste):
        self.nombres = json.dumps(liste)

    def get_nombres(self):
        return json.loads(self.nombres)

class Domaine(models.Model):
    nom_dom=models.CharField(max_length=70,blank=True,unique=True)

class Faculte(models.Model):
    id_dom=models.ForeignKey(Domaine,on_delete=models.CASCADE)
    nom_fac=models.CharField(max_length=70,blank=True,unique=True)

class Filiere(models.Model):
    id_fac=models.ForeignKey(Faculte,on_delete=models.CASCADE)
    nom_fil=models.CharField(max_length=70,unique=True,blank=True)

class Mention(models.Model):
    id_fil=models.ForeignKey(Filiere,on_delete=models.CASCADE)
    nom_mention=models.CharField(max_length=70,unique=True,blank=True)

class Promotion(models.Model):
    id_mention=models.ForeignKey(Mention,on_delete=models.CASCADE)
    nom_prom=models.CharField(max_length=70,blank=True)
    def __str__(self) -> str:
        return f"{self.id_mention.nom_mention} {self.nom_prom.capitalize()}"
class Unite_Ens(models.Model):
    id_promotion=models.ForeignKey(Promotion,on_delete=models.CASCADE)
    code_ue=models.CharField(max_length=10,blank=True,unique=True)
    denom_ue=models.CharField(max_length=70,blank=True)
    #choise 
    sem_choice=(("premier","Premier Semestre"),("second","Second Semestre"))
    semstre=models.CharField(max_length=7,choices=sem_choice)
    def __str__(self) -> str:
        return f"{self.id_promotion.nom_prom} {self.code_ue} {self.denom_ue}"
class Elenent_Const(models.Model):
    id_ue=models.ForeignKey(Unite_Ens,on_delete=models.CASCADE)
    denom_ec=models.CharField(max_length=70)
    niveau_ec=models.CharField(max_length=8)
    def __str__(self) -> str:
        return f"{self.id_ue} {self.denom_ec}"
class Anacad(models.Model):
    denom_anacad=models.CharField(max_length=9,unique=True,blank=True)
    def __str__(self) -> str:
        return self.denom_anacad
class Partie_ec(models.Model):
    id_ec = models.ForeignKey(Elenent_Const, on_delete=models.CASCADE)
    id_anacad = models.ForeignKey(Anacad, on_delete=models.CASCADE)
    id_enseignant = models.ForeignKey('User.Enseignant', on_delete=models.CASCADE,default=1)
    volume_horaire=models.IntegerField()

    # Définir les choix pour partie_ec
    PARTIE_CHOICES = (
        ('tp', 'Travail Pratique'),
        ('cmi', 'Cours magistral'),
    )
    

    partie_ec_choice = models.CharField(max_length=68, choices=PARTIE_CHOICES)
    date_debut=models.DateField()
    date_fin=models.DateField()
    def __str__(self) -> str:
        return f"{self.id_anacad.denom_anacad} {self.id_ec.denom_ec}  {self.partie_ec_choice}"
    
    class Meta:
        unique_together = (('id_ec', 'partie_ec_choice', 'id_anacad')) # Assurer l'unicité de la combinaison de ces trois champs
        
class Programme_ec(models.Model):
    pass
