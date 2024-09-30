
from django.urls import path
from .views import (RegisterView_user,RegisterView_enseignant,RegisterView_chef_promotion,RegisterView_encadreur_faculte,
                    EnseignantPartieEcAPIView,LoginView,LoginViewEncadreur,LoginEnseignant
)
urlpatterns=[ 
              path('user/',RegisterView_user.as_view()),
                path('enseignant/',RegisterView_enseignant.as_view()),
                path('chef_promotion/',RegisterView_chef_promotion.as_view()),
                path('encadreur_faculte/',RegisterView_encadreur_faculte.as_view()),
                 path('enseignant-partie-ec/<str:email>/', EnseignantPartieEcAPIView.as_view(), name='enseignant-partie-ec'),
                 
                 path('login/<str:email>/', LoginView.as_view(), name='login'),
                 
                 path('login_encadreur/<str:email>/<str:anacad>/', LoginViewEncadreur.as_view(), name='login_encadreur'),
                 path('login_enseignant/<str:email>/<str:anacad>', LoginEnseignant.as_view(), name='login_enseignant'),
                  
                  
              
          ]