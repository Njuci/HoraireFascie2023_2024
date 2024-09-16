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
    username=models.CharField(max_length=50,unique=True,blank=True)
    email=models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','password','first_name','last_name','user_type']
    groups = models.ManyToManyField(Group, related_name='myuser_set', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='myuser_set', blank=True
    )
    
    def __str__(self):
        return self.email
    def save(self, *args, **kwargs):
        
        if not self.username:
            self.username = self.email  # or any default value like 'default_username'
        super().save(*args, **kwargs)

    def has_perm(self,perms):
        return True
    def has_module_perms(self,app_label):
        return True 
    class Meta:
        verbose_name='User'
        verbose_name_plural='Users'
    
#commentaire
class Enseignant(models.Model):
    id_user=models.OneToOneField(MyUser,on_delete=models.CASCADE)    

    niveau_ens=models.CharField(max_length=100,blank=True)
    statut_choice=(('permanent','Permanant'),('visiteur','Visiteur'))
    statut=models.CharField(max_length=10,choices=statut_choice)
    def __str__(self):
        return self.id_user.email

class Chef_Promotion(models.Model):
    id_user=models.OneToOneField(MyUser,on_delete=models.CASCADE,unique=True)
    id_promotion=models.ForeignKey(Promotion,on_delete=models.CASCADE)
    id_anacad=models.ForeignKey(Anacad,on_delete=models.CASCADE)
    
class  Encadreur_faculte(models.Model):
    id_ens=models.ForeignKey(Enseignant,on_delete=models.CASCADE)
    id_faculte=models.ForeignKey(Faculte,on_delete=models.CASCADE)
    id_anacad=models.ForeignKey(Anacad,on_delete=models.CASCADE)
    def __str__(self):
        return self.id_ens.id_user.email
    class Meta:        
        unique_together = (('id_faculte','id_anacad'),('id_ens','id_anacad') )
        #pour que un enseignant ne peut pas etre encadreur de la meme faculte dans la meme année anacademique  deux fois
    
    

    
    
    
    
    
    
    
    
