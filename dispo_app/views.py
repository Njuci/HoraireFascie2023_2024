from django.shortcuts import render
from .serializers import Programme_ec_serial,Disponibilite_serial,Horaire_serial,Semestre_serial
from .models import Programme_ec,Disponibilite,Horaire,Semestre
from horaire_univ.models import *

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

    
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


