from django.db import models
import json
from horaire_univ.models import *
# Create your models here.

class Disponibilite(models.Model):
    id_partie_ec=models.OneToOneField(Partie_ec,on_delete=models.CASCADE)
    liste_jours=models.TextField()
     
    def set_nombres(self, liste):
        self.liste_jours = json.dumps(liste)

    def get_nombres(self):
        return json.loads(self.liste_jours)
    
    
class Horaire(models.Model):
    id_partie_ec=models.ForeignKey(Partie_ec,on_delete=models.CASCADE)
    date=models.DateField()
    partie_journ_choice=(('matin','Matin'),('soir','Soir'))
    partie_journ=models.CharField(max_length=5,choices=partie_journ_choice)
    
    class Meta:
        unique_together=(('date','partie_journ')) #qu'une promotion n'a pas deux partie_ec dans la meme date et la meme partie de la journe

class Semestre(models.Model):
    anacad=models.ForeignKey(Anacad,on_delete=models.CASCADE)
    sem_choice=(("premier","Premier Semestre"),("second","Second Semestre"))
    senestre_period=models.CharField(max_length=7,choices=sem_choice)
    date_debut_semestre=models.DateField()
    date_fin_semestre=models.DateField()
    
    class Meta:
        unique_together=(('anacad','senestre_period'))#pour qu'un semestre ne soit assigner une seul fois durant une année

