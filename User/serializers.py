from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import MyUser,Enseignant,Chef_Promotion,Encadreur_faculte

class Utilisateur_Serial(ModelSerializer):
    class Meta:
        model=MyUser
        fields='__all__'
class Enseignant_Serial(ModelSerializer):
    class Meta:
        model=Enseignant
        fields='__all__'
        
class Chef_Promotion_Serial(ModelSerializer):
    class Meta:
        model=Chef_Promotion
        fields='__all__'

class Encadreur_faculte_Serial(ModelSerializer): 
    class Meta:
        model=Encadreur_faculte
        fields='__all__'
# Create your serializers here.

