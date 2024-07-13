from django.db import models
from horaire_univ.models import Faculte,Promotion,Anacad
from django.contrib.auth.models import AbstractUser,Group,Permission


# Create your models here.

class MyUser(AbstractUser):
    USER_TYPE_CHOICES = (
            ('admin','Admin'),
           ('cp', 'Chef de prom'),
           ('enseignant', 'Enseignant'),
       )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['email','password','full_name','user_type']
    groups = models.ManyToManyField(Group, related_name='myuser_set', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='myuser_set', blank=True
    )
    def __str__(self):
        return self.email
    

    def has_perm(self,perms):
        return True
    def has_module_perms(self,app_label):
        return True 
    class Meta:
        verbose_name='User'
        verbose_name_plural='Users'
    
#commentaire
class Enseignant(models.Model):
    id_user=models.ForeignKey(MyUser,on_delete=models.CASCADE,unique=True)    
    niveau_ens=models.CharField(max_length=10,blank=True)
    statut_choice=(('permanent','Permanant'),('visiteur','Visiteur'))

class Chef_Promotion(models.Model):
    id_user=models.ForeignKey(MyUser,on_delete=models.CASCADE,unique=True)
    id_promotion=models.ForeignKey(Promotion,on_delete=models.CASCADE)
    id_anacad=models.ForeignKey(Anacad,on_delete=models.CASCADE)
    
class Encadreur_faculte(models.Model):
    id_ens=models.ForeignKey(Enseignant,on_delete=models.CASCADE,unique=True)
    id_faculte=models.ForeignKey(Faculte,on_delete=models.CASCADE)
    id_anacad=models.ForeignKey(Anacad,on_delete=models.CASCADE)
    
    class Meta:        
        unique_together = ('id_faculte','id_anacad') 
        #pour que un enseignant ne peut pas etre encadreur de la meme faculte dans la meme année anacademique  deux fois
    
    
    
    
    
    
    
    
    
    
    
    
