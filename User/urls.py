
from django.urls import path
from .views import RegisterView_user,RegisterView_enseignant,RegisterView_chef_promotion,RegisterView_encadreur_faculte



urlpatterns=[ 
              path('user/',RegisterView_user.as_view()),
                path('enseignant/',RegisterView_enseignant.as_view()),
                path('chef_promotion/',RegisterView_chef_promotion.as_view()),
                path('encadreur_faculte/',RegisterView_encadreur_faculte.as_view()),

              
              
              ]