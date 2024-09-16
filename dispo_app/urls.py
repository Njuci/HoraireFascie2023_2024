from django.urls import path
from .views import Programme_ecView,DisponibiliteView,Get_date_cours, Email_envoie


urlpatterns = [
    path('programme_ec/', Programme_ecView.as_view()),
    path('disponibilite/', DisponibiliteView.as_view()),
    #path('horaire/', HoraireView.as_view()),
    path('get_disponibilite/', Get_date_cours.as_view()),
    #path('semestre/', SemestreView.as_view())
    path('email/<int:id_partie_ec>', Email_envoie.as_view())
]

