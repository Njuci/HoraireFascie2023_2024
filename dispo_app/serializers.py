from .models import Programme_ec,Disponibilite,Horaire,Semestre
from rest_framework.serializers import ModelSerializer,SerializerMethodField



class Programme_ec_serial(ModelSerializer):
    class Meta:
        model=Programme_ec
        fields='__all__'
        
class Disponibilite_serial(ModelSerializer):
    class Meta:
        model=Disponibilite
        fields='__all__'

class Horaire_serial(ModelSerializer):
    class Meta:
        model=Horaire
        fields='__all__'

class Semestre_serial(ModelSerializer):
    class Meta:
        model=Semestre
        fields='__all__'
        
        
