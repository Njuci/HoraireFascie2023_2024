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
    nom_prom=models.CharField(max_length=70,unique=True,blank=True)

class Unite_Ens(models.Model):
    id_promotion=models.ForeignKey(Promotion,on_delete=models.CASCADE)
    code_ue=models.CharField(max_length=10,blank=True,unique=True)
    denom_ue=models.CharField(max_length=70,blank=True)
    #choise 
    sem_choice=(("premier","Premier Semestre"),("second","Second Semestre"))
    semstre=models.CharField(max_length=7,choices=sem_choice)
class Elenent_Const(models.Model):
    id_ue=models.ForeignKey(Unite_Ens,on_delete=models.CASCADE)
    denom_ue=models.CharField(max_length=70)
    niveau_ue=models.CharField(max_length=8)
 
class Anacad(models.Model):
    denom_anacad=models.CharField(max_length=9,unique=True,blank=True)

class Partie_ec(models.Model):
    id_ec=models.ForeignKey(Elenent_Const,on_delete=models.CASCADE)
    id_anacad=models.ForeignKey(Anacad,on_delete=models.CASCADE)
    #id_enseignant
    id_enseignant=models.ForeignKey('User.Enseignant',on_delete=models.CASCADE)#pour eviter l'erreir d'importation circulaire 
    #partie_ec choice
    partie_choice=(('tp','Travail Pratique'),('cmi','Cours magistral'))
    partie=models.CharField(max_length=3,choices=partie_choice)
    class Meta:
        unique_together=(('id_ec','partie','id_anacad'))#pour qu'un partie ne soit assigner une seul fois durant une année
        
class Programme_ec(models.Model):
    id_partie_ec=models.OneToOneField(Partie_ec,on_delete=models.CASCADE)#pour eviter l'erreur de duplication des programmes des partie_ec
    date_debut=models.DateField()
    date_fin=models.DateField()
class Disponibilite(models.Model):
    id_enseignant=models.ForeignKey('User.Enseignant',on_delete=models.CASCADE)
    id_partie_ec=models.ForeignKey(Partie_ec,on_delete=models.CASCADE)
    liste_jours=models.TextField()
     
    def set_nombres(self, liste):
        self.liste_jours = json.dumps(liste)

    def get_nombres(self):
        return json.loads(self.liste_jours)
    
    class Meta:
        unique_together=(('id_enseignant','id_partie_ec'))
class Horaire(models.Model):
    id_partie_ec=models.ForeignKey(Partie_ec,on_delete=models.CASCADE)
    date=models.DateField()
    partie_journ_choice=(('matin','Matin'),('soir','Soir'))
    partie_journ=models.CharField(max_length=5,choices=partie_journ_choice)
    
    class Meta:
        unique_together=(('date','partie_journ')) #qu'une promotion n'a pas deux partie_ec dans la meme date et la meme partie de la journee
