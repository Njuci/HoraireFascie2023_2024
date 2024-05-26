from rest_framework.serializers import ModelSerializer,SerializerMethodField
from .models import *


class MyListSerial(ModelSerializer):
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
