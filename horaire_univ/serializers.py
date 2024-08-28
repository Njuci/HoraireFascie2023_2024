from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import (Domaine,Faculte,Filiere,Mention,Promotion,Unite_Ens,Anacad,Elenent_Const
                     ,Partie_ec)











class Domaine_serial(ModelSerializer):
    class Meta:
        model=Domaine
        fields='__all__'
        
class Faculte_serial(ModelSerializer):
    class Meta:
        model=Faculte
        fields='__all__'

class Filiere_serial(ModelSerializer):
    class Meta:
        model=Filiere
        fields='__all__'
class Mention_serial(ModelSerializer):
    class Meta:
        model=Mention
        fields='__all__'
        
class Promotion_serial(ModelSerializer):
    class Meta:
        model=Promotion
        fields='__all__'
        
class Unite_Ens_serial(ModelSerializer):
    class Meta:
        model=Unite_Ens
        fields='__all__'
        
class Anacad_serial(ModelSerializer):
    class Meta:
        model=Anacad
        fields='__all__'

class Elenent_Const_serial(ModelSerializer):
    class Meta:
        model=Elenent_Const
        fields='__all__'
        
class Partie_ec_serial(ModelSerializer):
    class Meta:
        model=Partie_ec
        fields='__all__'
        
    def get_promotion(self, obj):
        return f"{obj.id_ec.id_ue.id_promotion.nom_prom}"

    def get_unite_ens(self, obj):
        return f"{obj.id_ec.id_ue.code_ue} - {obj.id_ec.id_ue.denom_ue}"

    def get_element_const(self, obj):
        return f"{obj.id_ec.denom_ec}"


"""class MyListSerial(ModelSerializer):
    class Meta:
        model = MaListe
        fields = '__all__'



class MaListeSerializer(ModelSerializer):
    # Utilisez un SerializerMethodField pour personnaliser la sérialisation
    nombres = SerializerMethodField()

    class Meta:
        model = MaListe
        fields = ['nombres']

    def get_nombres(self, obj):
        # Utilisez la méthode get_nombres du modèle pour récupérer la liste
        return obj.get_nombres()

    def to_internal_value(self, data):
        # Surchargez la méthode to_internal_value pour convertir la liste entrante en JSON
        internal_value = super(MaListeSerializer, self).to_internal_value(data)
        internal_value['nombres'] = json.dumps(data['nombres'])
        return internal_value

    def create(self, validated_data):
        # Surchargez la méthode create pour utiliser set_nombres lors de la création de l'objet
        nombres = validated_data.pop('nombres')
        instance = MaListe.objects.create(**validated_data)
        instance.set_nombres(json.loads(nombres))
        instance.save()
        return instance

    def update(self, instance, validated_data):
        # Surchargez la méthode update pour utiliser set_nombres lors de la mise à jour de l'objet
        nombres = validated_data.get('nombres', None)
        if nombres is not None:
            instance.set_nombres(json.loads(nombres))
        instance.save()
        return instance
"""