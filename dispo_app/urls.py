from django.urls import path
from .views import Programme_ecView,DisponibiliteView

urlpatterns = [
    path('programme_ec/', Programme_ecView.as_view()),
    path('disponibilite/', DisponibiliteView.as_view()),
    #path('horaire/', HoraireView.as_view()),
    #path('semestre/', SemestreView.as_view())
]
