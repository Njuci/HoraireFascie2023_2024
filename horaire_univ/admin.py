from django.contrib import admin
from .models import Domaine,Faculte,Filiere,Mention,Promotion,Unite_Ens,Anacad,Elenent_Const,Partie_ec
# Register your models here.
admin
admin.site.register(Domaine)
admin.site.register(Faculte)
admin.site.register(Filiere)
admin.site.register(Mention)
admin.site.register(Promotion)
admin.site.register(Unite_Ens)
admin.site.register(Anacad)
admin.site.register(Elenent_Const)
admin.site.register(Partie_ec)
"""admin.site.register(Programme_ec)
admin.site.register(Disponibilite)
admin.site.register(Horaire)
admin.site.register(Semestre)"""
