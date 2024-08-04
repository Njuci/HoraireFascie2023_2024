from django.shortcuts import render
from .serializers import (Programme_ec_serial,Disponibilite_serial,
                          Horaire_serial,Semestre_serial,DisponibiliteSerializer)
from .models import Programme_ec,Disponibilite,Horaire,Semestre
from horaire_univ.models import *

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from User.models import Enseignant
    
#programme_ec
class Programme_ecView(APIView):
    def get(self,request):
        programme_ec=Programme_ec.objects.all()
        serializer=Programme_ec_serial(programme_ec,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=Programme_ec_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        id=request.data['id']
        programme_ec=Programme_ec.objects.get(id=id)
        serializer=Programme_ec_serial(programme_ec,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        id=request.data['id']
        programme_ec=Programme_ec.objects.get(id=id)
        programme_ec.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#disponibilite
class DisponibiliteView(APIView):
    def get(self,request):
        disponibilite=Disponibilite.objects.all()
        serializer=Disponibilite_serial(disponibilite,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        id_partie_ec=request.data['id_partie_ec']
        #verifier si l'enseignant a deja une disponibilite pour cette partie_ec
        disponibilite=Disponibilite.objects.filter(id_partie_ec=id_partie_ec)
        partie_ec=Partie_ec.objects.get(id=id_partie_ec)
        #verifier si la partie_ec a deja un programme_ec
        programme_ec=Programme_ec.objects.filter(id_partie_ec=id_partie_ec)
        #avoir la promotion de la partie_ec
        promotion=Promotion.objects.get(id=partie_ec.id_ec.id_ue.id_promotion) 
        #avoir la mention de la promotion
        
    def put(self,request):
        id=request.data['id']
        disponibilite=Disponibilite.objects.get(id=id)
        serializer=Disponibilite_serial(disponibilite,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        id=request.data['id']
        disponibilite=Disponibilite.objects.get(id=id)
        disponibilite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
from datetime import datetime
import json

class AjouterDateDisponibleView(APIView):
    def post(self, request):
        serializer = DisponibiliteSerializer(data=request.data)
        if serializer.is_valid():
           
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
            #recuperer l'enseignant de la partie_ec
            id_enseignant = partie_ec.id_enseignant.id
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





