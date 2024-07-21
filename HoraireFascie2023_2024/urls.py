
from django.contrib import admin
from django.urls import path,include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Hora Ucb API",
        default_version='v1',
        description="Documentation de l'API de l'application Hora Ucb,\n Cette API permet de gerer les horaires des enseignants et faire le pointage des matieres enseignées",
        terms_of_service="",
        contact=openapi.Contact(email="augustinnjuci@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('schedule/',include('horaire_univ.urls')), 
    path('user/',include('User.urls')),
    path('dispo/',include('dispo_app.urls')),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
]
# 