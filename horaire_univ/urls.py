from django.urls import path
from .views import (DomaineView,FaculteView,FiliereView,MentionView,PromotionView,Unite_EnsView,Get_UeByPromotion,Get_EcByUe,
                    Elenent_ConstView,AnacadView,Partie_ecView,Get_FiliereByFaculte,Get_MentionByFiliere,Get_MentionByFaculte,Get_PromotionByFaculte)

urlpatterns = [
    path('domaine/',DomaineView.as_view()),
    path('faculte/',FaculteView.as_view()),
    path('filiere/',FiliereView.as_view()),
    path('get_filiere_by_faculte/<str:id_fac>/',Get_FiliereByFaculte.as_view(), name='get_filiere_by_faculte'),
    path('mention/',MentionView.as_view()),
    path('get_mention_by_filiere/<str:id_fil>/',Get_MentionByFiliere.as_view()),
    path('get_mention_by_faculte/<str:id_fac>/',Get_MentionByFaculte.as_view()),
    
    
    path('promotion/',PromotionView.as_view()),
    path('get_promotion_by_faculte/<str:id_fac>/',Get_PromotionByFaculte.as_view()),
    path('get_ue_by_promotion/<str:id_promotion>/',Get_UeByPromotion.as_view()),
    path('get_ec_by_ue/<str:id_ue>/',Get_EcByUe.as_view()),
    path('anacad/',AnacadView.as_view()),
    path('unit_enseign/',Unite_EnsView.as_view()),
    path('elem_const/',Elenent_ConstView.as_view()),
    path('partie_ec/',Partie_ecView.as_view())
    
]
