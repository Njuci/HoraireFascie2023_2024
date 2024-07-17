from django.contrib import admin
from .models import MyUser,Enseignant,Chef_Promotion,Encadreur_faculte
# Register your models here.
admin.site.register(MyUser)
admin.site.register(Enseignant)
admin.site.register(Chef_Promotion) 
admin.site.register(Encadreur_faculte)
