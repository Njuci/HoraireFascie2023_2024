from django.urls import path
from .views import DomaineView,FaculteView,FiliereView,MentionView,PromotionView,Unite_EnsView,Elenent_ConstView,AnacadView,Partie_ecView

urlpatterns = [
    path('domaine/',DomaineView.as_view()),
    path('faculte/',FaculteView.as_view()),
    path('filiere/',FiliereView.as_view()),
    path('mention/',MentionView.as_view()),
    path('promotion/',PromotionView.as_view()),
    path('anacad/',AnacadView.as_view()),
    path('unit_enseign/',Unite_EnsView.as_view()),
    path('elem_const/',Elenent_ConstView.as_view()),
    path('partie_ec',Partie_ecView.as_view())
    
]
