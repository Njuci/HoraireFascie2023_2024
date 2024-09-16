from django.shortcuts import render
from .serializers import (Programme_ec_serial,Disponibilite_serial,
                          Horaire_serial,Semestre_serial,DisponibiliteSerializer)
from .models import Programme_ec,Disponibilite,Horaire,Semestre
from horaire_univ.models import *
from horaire_univ.serializers import( Partie_ec_serial,Elenent_Const_serial,Unite_Ens_serial,Promotion_serial,Filiere_serial,Mention_serial,
                                     Faculte_serial)
# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .email_sending import envoi_email
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from User.models import Enseignant,MyUser,Encadreur_faculte
from User.serializers import Enseignant_Serial,Utilisateur_Serial
    
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





class AjouterDateDisponibleView2(APIView):
    def post(self, request):
        id_partie_ec=request.data['id_partie_ec']
        
        
        pass




class Email_envoie(APIView):
    def post(self,request,id_partie_ec):
        """ This view help to create and account for testing sending mails."""
        cxt = {}
        cxt = {'msg':'email envoie echoue.'}
        

        try:
            partie_ec = Partie_ec.objects.get(id=id_partie_ec)
            p_ec = Partie_ec_serial(partie_ec).data
            id_ec = p_ec['id_ec']
            #annacad
            id_anacad = p_ec['id_anacad']
            annacad = Anacad.objects.get(id=id_anacad)
            serial_annacad = annacad.denom_anacad
           
            
            enseignant = Enseignant.objects.get(id=p_ec['id_enseignant'])
            serial_enseignant = Enseignant_Serial(enseignant).data
            user = MyUser.objects.get(id=serial_enseignant['id_user'])
            serial_user = Utilisateur_Serial(user).data
            email = serial_user['email']
            nom_enseignant = serial_user['first_name'] + " " + serial_user['last_name']
            
            tp = ' des Travaux Pratiqes'
            if p_ec['partie_ec_choice'] == 'cmi':
                tp = " de cours magistral "
            
            ec = Elenent_Const.objects.get(id=id_ec)
            serial_ec = Elenent_Const_serial(ec).data
            ue = Unite_Ens.objects.get(id=serial_ec['id_ue'])
            serial_ue = Unite_Ens_serial(ue).data
            
            # Récupérer la promotion
            promotion = Promotion.objects.get(id=serial_ue['id_promotion'])
            serial_promotion = Promotion_serial(promotion).data
            
            # Récupérer la filière
            
            # Récupérer la mention
            mention = Mention.objects.get(id=serial_promotion['id_mention'])
            serial_mention = Mention_serial(mention).data
            
            filiere = Filiere.objects.get(id=serial_mention['id_fil'])
            serial_filiere = Filiere_serial(filiere).data
            
            # Récupérer la faculté
            faculte = Faculte.objects.get(id=serial_filiere['id_fac'])
            serial_faculte = Faculte_serial(faculte).data
             #chercher le nom de l'encadreur de la faculte dans cette anee academique
             # Rechercher l'encadreur de la faculté pour l'année académique donnée
            encadreur = Encadreur_faculte.objects.get(id_faculte=serial_filiere['id_fac'], id_anacad=id_anacad)
            
            # Accéder aux informations de l'enseignant associé
            enseignant = encadreur.id_ens
            
            # Récupérer les noms et post-noms de l'utilisateur
            nom = enseignant.id_user.first_name
            post_nom = enseignant.id_user.last_name
            encadreur=f'{nom} {post_nom}'
            
                        
            # Construire la chaîne de cours
            cours = f"""U.E: {serial_ue['denom_ue']} Element Constitutif: {serial_ec['denom_ec']}"""
            
            # Ajouter les informations supplémentaires
            cours += f"\nPromotion: {serial_promotion['nom_prom']}"
            cours += f"\nMention: {serial_mention['nom_mention']}"
            cours += f"\nFilière: {serial_filiere['nom_fil']}"
            cours += f"\nFaculté: {serial_faculte['nom_fac']}"
            
        except Partie_ec.DoesNotExist:
            return Response({"message": "Partie EC not found"}, status=status.HTTP_404_NOT_FOUND)
        except Enseignant.DoesNotExist:
            return Response({"message": "Enseignant not found"}, status=status.HTTP_404_NOT_FOUND)
        except MyUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        except Elenent_Const.DoesNotExist:
            return Response({"message": "Element Constitutif not found"}, status=status.HTTP_404_NOT_FOUND)
        except Unite_Ens.DoesNotExist:
            return Response({"message": "Unite Ens not found"}, status=status.HTTP_404_NOT_FOUND)
        except Promotion.DoesNotExist:
            return Response({"message": "Promotion not found"}, status=status.HTTP_404_NOT_FOUND)
        except Filiere.DoesNotExist:
            return Response({"message": "Filiere not found"}, status=status.HTTP_404_NOT_FOUND)
        except Mention.DoesNotExist:
            return Response({"message": "Mention not found"}, status=status.HTTP_404_NOT_FOUND)
        except Faculte.DoesNotExist:
            return Response({"message": "Faculte not found"}, status=status.HTTP_404_NOT_FOUND)       
                    
                    
            
        if request.method == "POST":
            email = email


            subjet = "Notification"
            template = 'mail.html'
            context = {
                  'enseignant':nom_enseignant,
                    'partie_ec':tp,
                    'cours':cours,
                    'annacad':serial_annacad,
                    'encadreur':encadreur,
                    'faculte':serial_faculte['nom_fac']
                    
                    
                    
                   
                }

            receivers = [email]

            has_send = envoi_email(
                    sujet=subjet,
                    desti=receivers,
                    template=template,
                    context=context
                    )

            if has_send:
                cxt =  {"msg":"mail envoyee avec success."}
            else:
                cxt = {'msg':'email envoie echoue.'}
            print(has_send)
            return Response(cxt,status=status.HTTP_200_OK)       
        
#DOCUMENTATION DE L'API     

class Get_date_cours(APIView):
    def get(self, request):
        id_partie_ec = request.data.get('id_partie_ec')
        if not id_partie_ec:
            return Response({"message": "id_partie_ec is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Récupérer la partie EC
            partie_ec = Partie_ec.objects.get(id=id_partie_ec)
            serial_partiec = Partie_ec_serial(partie_ec)
            enseignant = Enseignant.objects.get(id=serial_partiec.data['id_enseignant'])
            
            # Récupérer la promotion de la partie EC
            promotion = Promotion.objects.get(id=partie_ec.id_ec.id_ue.id_promotion)
            
            # Obtenir les horaires déjà pris par la promotion durant la période
            dates_prises_promotion = Horaire.objects.filter(
                id_partie_ec__id_ec__id_ue__id_promotion=promotion,
                date__range=(partie_ec.date_debut, partie_ec.date_fin)
            )
            
            # Obtenir les horaires déjà pris par l'enseignant durant la période
            dates_prises_enseignant = Horaire.objects.filter(
                id_partie_ec__id_enseignant=enseignant,
                date__range=(partie_ec.date_debut, partie_ec.date_fin)
            )
            
            # Combiner les deux listes d'horaires
            dates_prises = dates_prises_promotion.union(dates_prises_enseignant)
            
            # Sérialiser les données
            serializer = Horaire_serial(dates_prises, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Partie_ec.DoesNotExist:
            return Response({"message": "Partie EC not found"}, status=status.HTTP_404_NOT_FOUND)
        except Enseignant.DoesNotExist:
            return Response({"message": "Enseignant not found"}, status=status.HTTP_404_NOT_FOUND)
        except Promotion.DoesNotExist:
            return Response({"message": "Promotion not found"}, status=status.HTTP_404_NOT_FOUND)