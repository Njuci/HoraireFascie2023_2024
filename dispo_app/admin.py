from django.contrib import admin
from .models import Programme_ec,Disponibilite,Horaire,Semestre
# Register your models here.
admin.site.register(Programme_ec
                    )
admin.site.register(Disponibilite)
admin.site.register(Horaire)
admin.site.register(Semestre)