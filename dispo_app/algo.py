from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Disponibilite, Horaire, Partie_ec
from .serializers import DisponibiliteSerializer
from datetime import datetime
import json

class AjouterDateDisponibleView(APIView):
    def post(self, request):
        serializer = DisponibiliteSerializer(data=request.data)
        if serializer.is_valid():
            id_enseignant = serializer.validated_data['id_enseignant']
            id_partie_ec = serializer.validated_data['id_partie_ec']
            date_libre = serializer.validated_data['date_libre']
            
            # Récupérer la partie_ec
            try:
                partie_ec = Partie_ec.objects.get(id=id_partie_ec)
            except Partie_ec.DoesNotExist:
                return Response({'error': 'Partie_ec not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Récupérer la promotion de la partie_ec
            promotion = partie_ec.id_ec.id_ue.id_promotion
            
            # Vérifier les horaires de la promotion à la date proposée
            cours_promotion = Horaire.objects.filter(id_partie_ec__id_ec__id_ue__id_promotion=promotion, date=date_libre)
            if cours_promotion.exists():
                return Response({'error': 'La promotion a déjà un cours à cette date'}, status=status.HTTP_400_BAD_REQUEST)

            # Récupérer les disponibilités de l'enseignant
            disponibilite, created = Disponibilite.objects.get_or_create(
                id_enseignant_id=id_enseignant,
                id_partie_ec_id=id_partie_ec,
            )

            # Charger la liste des jours disponibles
            jours_disponibles = disponibilite.get_nombres()

            # Vérifier si la date est déjà dans les disponibilités
            if date_libre.isoformat() in jours_disponibles:
                return Response({'error': 'Cette date est déjà dans les disponibilités'}, status=status.HTTP_400_BAD_REQUEST)

            # Ajouter la nouvelle date aux disponibilités
            jours_disponibles.append(date_libre.isoformat())
            disponibilite.set_nombres(jours_disponibles)
            disponibilite.save()

            return Response({'success': 'Date ajoutée avec succès'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    














from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Disponibilite, Horaire, Partie_ec
from .serializers import DisponibiliteSerializer
from datetime import datetime
import json

class AjouterDateDisponibleView(APIView):
    def post(self, request):
        serializer = DisponibiliteSerializer(data=request.data)
        if serializer.is_valid():
            id_enseignant = serializer.validated_data['id_enseignant']
            id_partie_ec = serializer.validated_data['id_partie_ec']
            date_libre = serializer.validated_data['date_libre']
            partie_journ = serializer.validated_data['partie_journ']
            
            # Récupérer la partie_ec
            try:
                partie_ec = Partie_ec.objects.get(id=id_partie_ec)
            except Partie_ec.DoesNotExist:
                return Response({'error': 'Partie_ec not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Récupérer la promotion de la partie_ec
            promotion = partie_ec.id_ec.id_ue.id_promotion
            
            # Vérifier les horaires de la promotion à la date proposée
            cours_promotion = Horaire.objects.filter(
                id_partie_ec__id_ec__id_ue__id_promotion=promotion, 
                date=date_libre, 
                partie_journ=partie_journ
            )
            if cours_promotion.exists():
                return Response({'error': 'La promotion a déjà un cours à cette date et à cette partie de la journée'}, status=status.HTTP_400_BAD_REQUEST)

            # Récupérer les disponibilités de l'enseignant
            disponibilite, created = Disponibilite.objects.get_or_create(
                id_enseignant_id=id_enseignant,
                id_partie_ec_id=id_partie_ec,
            )

            # Charger la liste des jours disponibles
            jours_disponibles = disponibilite.get_nombres()

            # Vérifier si la date et la partie de la journée sont déjà dans les disponibilités
            if any(dispo['date'] == date_libre.isoformat() and dispo['partie_journ'] == partie_journ for dispo in jours_disponibles):
                return Response({'error': 'Cette date et partie de la journée sont déjà dans les disponibilités'}, status=status.HTTP_400_BAD_REQUEST)

            # Ajouter la nouvelle date et partie de la journée aux disponibilités
            jours_disponibles.append({'date': date_libre.isoformat(), 'partie_journ': partie_journ})
            disponibilite.set_nombres(jours_disponibles)
            disponibilite.save()

            return Response({'success': 'Date ajoutée avec succès'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



