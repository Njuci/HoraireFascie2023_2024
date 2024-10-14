from django.urls import path
from .views import DisponibiliteView,Get_date_cours,GetHorairebyPromo,GetHorairebyEnseignant


urlpatterns = [
    path('disponibilite/', DisponibiliteView.as_view()),
    #path('horaire/', HoraireView.as_view()),
    path('get_disponibilite/<str:id_partie_ec>', Get_date_cours.as_view()),
    path('get_horaire_by_promo/<str:id_promotion>/<str:id_anacad>', GetHorairebyPromo.as_view()),
    path('get_horaire_by_enseignant/<str:id_enseignant>/<str:id_anacad>', GetHorairebyEnseignant.as_view())
    #path('semestre/', SemestreView.as_view())
]

