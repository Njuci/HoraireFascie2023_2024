from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Domaine,Faculte,Filiere,Mention,Promotion,Unite_Ens,Elenent_Const,Partie_ec,Anacad


from .serializers import (Domaine_serial,Faculte_serial,Filiere_serial,Mention_serial,Promotion_serial,Unite_Ens_serial,
                          Anacad_serial,Elenent_Const_serial,Partie_ec_serial)
class DomaineView(APIView):
    def get(self,request):
        domaine=Domaine.objects.all()
        serializer=Domaine_serial(domaine,many=True)
        return Response(serializer.data)
    def post(self,request):
        """ 
        post method for domaine
        {"nom_dom":"Sciences et Technologies"}
        
        """
        serializer=Domaine_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        id=request.data['id']
        domaine=Domaine.objects.get(id=id)
        serializer=Domaine_serial(domaine,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        id=request.data['id']
        domaine=Domaine.objects.get(id=id)
        domaine.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#faculte
class FaculteView(APIView):
    def get(self,request):
        faculte=Faculte.objects.all()
        serializer=Faculte_serial(faculte,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=Faculte_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        id=request.data['id']
        faculte=Faculte.objects.get(id=id)
        serializer=Faculte_serial(faculte,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        id=request.data['id']
        faculte=Faculte.objects.get(id=id)
        faculte.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#filiere
class FiliereView(APIView):
    def get(self,request):
        filiere=Filiere.objects.all()
        serializer=Filiere_serial(filiere,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=Filiere_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        id=request.data['id']
        filiere=Filiere.objects.get(id=id)
        serializer=Filiere_serial(filiere,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        id=request.data['id']
        filiere=Filiere.objects.get(id=id)
        filiere.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#mention
class MentionView(APIView):
    def get(self,request):
        mention=Mention.objects.all()
        serializer=Mention_serial(mention,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=Mention_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        id=request.data['id']
        mention=Mention.objects.get(id=id)
        serializer=Mention_serial(mention,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        id=request.data['id']
        mention=Mention.objects.get(id=id)
        if mention:
            mention.delete()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
#promotion
class PromotionView(APIView):
    def get(self,request):
        promotion=Promotion.objects.all()
        serializer=Promotion_serial(promotion,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=Promotion_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        id=request.data['id']
        promotion=Promotion.objects.get(id=id)
        serializer=Promotion_serial(promotion,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        id=request.data['id']
        promotion=Promotion.objects.get(id=id)
        promotion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#unite_ens

class Unite_EnsView(APIView):
    def get(self,request):
        unite_ens=Unite_Ens.objects.all()
        serializer=Unite_Ens_serial(unite_ens,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=Unite_Ens_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        id=request.data['id']
        unite_ens=Unite_Ens.objects.get(id=id)
        serializer=Unite_Ens_serial(unite_ens,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        id=request.data['id']
        unite_ens=Unite_Ens.objects.get(id=id)
        unite_ens.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#anacad
class AnacadView(APIView):
    def get(self,request):
        anacad=Anacad.objects.all()
        serializer=Anacad_serial(anacad,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=Anacad_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        id=request.data['id']
        anacad=Anacad.objects.get(id=id)
        serializer=Anacad_serial(anacad,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        id=request.data['id']
        anacad=Anacad.objects.get(id=id)
        anacad.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#elenent_const
class Elenent_ConstView(APIView):
    def get(self,request):
        elenent_const=Elenent_Const.objects.all()
        serializer=Elenent_Const_serial(elenent_const,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=Elenent_Const_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        id=request.data['id']
        elenent_const=Elenent_Const.objects.get(id=id)
        serializer=Elenent_Const_serial(elenent_const,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        id=request.data['id']
        elenent_const=Elenent_Const.objects.get(id=id)
        elenent_const.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#partie_ec
class Partie_ecView(APIView):
    def get(self,request):
        partie_ec=Partie_ec.objects.all()
        serializer=Partie_ec_serial(partie_ec,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer=Partie_ec_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        id=request.data['id']
        partie_ec=Partie_ec.objects.get(id=id)
        serializer=Partie_ec_serial(partie_ec,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        id=request.data['id']
        partie_ec=Partie_ec.objects.get(id=id)
        partie_ec.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)














