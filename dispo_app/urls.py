from django.urls import path
from .views import DisponibiliteView,Get_date_cours


urlpatterns = [
    path('disponibilite/', DisponibiliteView.as_view()),
    #path('horaire/', HoraireView.as_view()),
    path('get_disponibilite/<str:id_partie_ec>', Get_date_cours.as_view()),
    #path('semestre/', SemestreView.as_view())
]

