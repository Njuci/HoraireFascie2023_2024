from django.urls import path
from .views import DomaineView,FaculteView,FiliereView,MentionView,PromotionView


urlpatterns = [
    path('domaine/',DomaineView.as_view()),
    path('faculte/',FaculteView.as_view()),
    path('filiere/',FiliereView.as_view()),
    path('mention/',MentionView.as_view()),
    path('promotion/',PromotionView.as_view()),

    
]
