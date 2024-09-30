from django.shortcuts import render
# Create your views here.
from .models import MyUser,Enseignant,Chef_Promotion,Encadreur_faculte,Faculte
from .serializers import Utilisateur_Serial,Enseignant_Serial,Chef_Promotion_Serial,Encadreur_faculte_Serial
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.response import Response
from dispo_app.models import Anacad,Disponibilite,Horaire
from dispo_app.serializers import Disponibilite_serial,Horaire_serial
from horaire_univ.models import Partie_ec,Anacad,Elenent_Const,Unite_Ens,Promotion,Mention,Filiere,Faculte
from horaire_univ.serializers import Partie_ec_serial,Faculte_serial,Anacad_serial

from django.db.models import Max
from rest_framework import status



class RegisterView_user(APIView):
    def post(self,request):
        """register user
            {" first_name":"Van dam","last_name":"Jean-claude","email":"njcuimec@gmail.com",
            "password":"4355vvefeef","user_type":"admin"}
            Il y a trios types d'utilisateurs: admin, enseignant, cp (chef de promotion)
        """
        serializer=Utilisateur_Serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
             serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def get(self,request):
        """ 
        
        get all users
        
        response:
                            [
                        {
                            "id": 1,
                            "password": "4355vvefeef",
                            "last_login": null,
                            "is_superuser": false,
                            "first_name": "",
                            "last_name": "Jean-claude",
                            "is_staff": false,
                            "is_active": true,
                            "date_joined": "2024-07-14T17:58:39.295047Z",
                            "username": "njcuimec@gmail.com",
                            "email": "njcuimec@gmail.com",
                            "user_type": "admin",
                            "groups": [],
                            "user_permissions": []
                        },
                        {
                            "id": 2,
                            "password": "4355vvefeef",
                            "last_login": null,
                            "is_superuser": false,
                            "first_name": "",
                            "last_name": "Jean-claude",
                            "is_staff": false,
                            "is_active": true,
                            "date_joined": "2024-07-14T18:00:13.958968Z",
                            "username": "njcuiweslay@gmail.com",
                            "email": "njcuiweslay@gmail.com",
                            "user_type": "cp",
                            "groups": [],
                            "user_permissions": []
                        }
                    ]
        
        """
        user=MyUser.objects.all()
        serializer=Utilisateur_Serial(user,many=True)
        return Response(serializer.data)
    def put(self,request):
        """
        update user
        
         exemple 
            
            on peut ou ne pas mettre tous les champs
            
            """
        id=request.data['id']
        user=MyUser.objects.get(id=id)
        serializer=Utilisateur_Serial(user,data=request.data)
        if serializer.is_valid(raise_exception=True):
             serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        id=request.data['id']
        user=MyUser.objects.get(id=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class RegisterView_enseignant(APIView):
    def post(self,request):
        print(request.data)
        """ {"first_name":"Van dam","last_name":"Jean-claude","email":"njcuimec@gmail.com",
            "password":"4355vvefeef","user_type":"enseignant","niveau_ens":"assistnt","statut":""}"""
        user={'first_name':request.data['first_name'],'last_name':request.data['last_name'],
              'email':request.data['email'],'password':request.data['password'],'user_type':'enseignant'}
        serial_user =Utilisateur_Serial(data=user)
        
        if serial_user.is_valid(raise_exception=True):
             serial_user.save()
        else:
            return Response(serial_user.errors,status=status.HTTP_400_BAD_REQUEST)
        id_user=MyUser.objects.get(email=request.data['email'])
        enseignant={'id_user':id_user.id}
        #lkeys and values of request.data - user
        enseignant['niveau_ens']=request.data['niveau_ens']
        enseignant['statut']=request.data['statut']
        serializer=Enseignant_Serial(data=enseignant)
        if serializer.is_valid(raise_exception=True):
             serializer.save()
        else:
            id_user.delete()
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    def get(self, request):
        """enseignant and users type enseignant"""
        enseignant_users_list = []
        users = MyUser.objects.filter(user_type='enseignant')
        
        for user in users:
            serial_user = Utilisateur_Serial(user)
            if Enseignant.objects.filter(id_user=serial_user.data['id']).exists():
                enseignant = Enseignant.objects.get(id_user=serial_user.data['id'])
                enseignant_serial = Enseignant_Serial(enseignant).data
                user_serial = serial_user.data
                
                # Mélanger les deux dictionnaires en distinguant id_enseignant et id_user
                melange = {**enseignant_serial, **user_serial}
                melange['id_enseignant'] = enseignant.id
                melange['id_user'] = user.id
                #pop id in melange
                melange.pop('id')
                enseignant_users_list.append(melange)
        
        return Response(enseignant_users_list, status=status.HTTP_200_OK)
    def put(self,request):
        id=request.data['id']
        user=MyUser.objects.get(id=id)
        serializer=Enseignant_Serial(user,data=request.data)
        if serializer.is_valid(raise_exception=True):
             serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        id=request.data['id']
        user=Enseignant.get(id=id)
        if user:
            user.delete()
        else:
            return Response({"message":"user not found"},status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)  
class RegisterView_chef_promotion(APIView):
    def post(self,request):
        serializer=Chef_Promotion_Serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
             serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def get(self,request):
        """chef_promotion and users type chef_promotion"""
        chef_promotion_users_list=[]
        user=MyUser.objects.filter(user_type='cp')
        for i in user:
            chef_promotion=Chef_Promotion.objects.get(id_user=i)
            if chef_promotion:
                # melanger les deux dictionnaires en distinguant id_chef_promotion et id_user
                melange={}
                melange.update(chef_promotion.__dict__)
                melange.update(i.__dict__)
                melange.pop('id')
                melange['id_chef_promotion']=chef_promotion.id
                melange['id_user']=i.id 
                chef_promotion_users_list.append(melange)
    
        serializer=chef_promotion_users_list
        return Response(serializer,status=status.HTTP_200_OK)
    def put(self,request):
        id=request.data['id']
        user=MyUser.objects.get(id=id)
        serializer=Chef_Promotion_Serial(user,data=request.data)
        if serializer.is_valid(raise_exception=True):
             serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        id=request.data['id']
        user=Chef_Promotion.get(id=id)
        if user:
            user.delete()
        else:
            return Response({"message":"user not found"},status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
class RegisterView_encadreur_faculte(APIView):
    def post(self,request):
        """ 
        
            { "id_ens": 4,
        "id_faculte": 2,
        "id_anacad": 1}
        
        """
        serial=Encadreur_faculte_Serial(data=request.data)
        if serial.is_valid():
            serial.save()
        else:
            return Response(serial.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serial.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        id = request.data['id']
        user = Encadreur_faculte.objects.get(id=id)
        
        serializer = Encadreur_faculte_Serial(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    def delete(self,request):
        id = request.data['id']
        user = Encadreur_faculte.get(id=id)
        if user:
            user.delete()
        else:
            return Response({"message": "user not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    def get(self,request):
        """
        """
    
        user=Encadreur_faculte.objects.all()
        serializer=Encadreur_faculte_Serial(user,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
class LoginView(APIView):
    def get(self,request,email):
        
        try:
            user=MyUser.objects.get(email=email)
            serial=Utilisateur_Serial(user)
            return Response(serial.data,status=status.HTTP_200_OK)        
        except MyUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
class LoginViewEncadreur(APIView):
    def get(self, request, email, anacad):
        """ 
        
        
            """
        try:
            user = MyUser.objects.get(email=email)
            user_serial = Utilisateur_Serial(user).data
            
            enseignant = Enseignant.objects.get(id_user=user)
            enseignant_serial = Enseignant_Serial(enseignant).data
            
            anacadem = Anacad.objects.get(denom_anacad=anacad)
            anacadem_serial = Anacad_serial(anacadem).data
            
            encadreur = Encadreur_faculte.objects.get(id_anacad=anacadem, id_ens=enseignant)
            encadreur_serial = Encadreur_faculte_Serial(encadreur).data
            faculte = Faculte.objects.get(id=encadreur.id_faculte.id)
            faculte_serial = Faculte_serial(faculte).data
            # Mélanger les dictionnaires sérialisés
            melange = {**enseignant_serial, **user_serial, **anacadem_serial, **encadreur_serial, **faculte_serial}
            melange['id_encadreur'] = encadreur.id
            melange['id_fac'] = faculte.id
            melange.pop('id', None)  # Supprimer la clé 'id' si elle existe
            
            return Response(melange, status=status.HTTP_200_OK)
        
        except MyUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Enseignant.DoesNotExist:
            return Response({"message": "User is not an enseignant"}, status=status.HTTP_404_NOT_FOUND)
        
        except Anacad.DoesNotExist:
            return Response({"message": "Anacad not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except Encadreur_faculte.DoesNotExist:
            return Response({"message": "Cette encadreur n'a pas de faculte pour cette annee"}, status=status.HTTP_404_NOT_FOUND)

class EnseignantPartieEcAPIView(APIView):  

    def get(self, request, email,anacad):
        try:
            # 1. Trouver l'utilisateur par email
            user = MyUser.objects.get(email=email)
            
            # 2. Trouver l'instance d'Enseignant associée
            enseignant = Enseignant.objects.get(id_user=user)
            
            anacad = Anacad.objects.get(denom_anacad=anacad)
            
            # 4. Récupérer les parties EC assignées à cet enseignant pour la dernière année académique
            parties_ec = Partie_ec.objects.filter(id_enseignant=enseignant, id_anacad=anacad)
            if not parties_ec.exists():
                return Response({'error': 'Aucune partie EC trouvée pour cet enseignant.'}, status=status.HTTP_404_NOT_FOUND)
            
            # 5. Sérialiser les résultats
            serializer = Partie_ec_serial(parties_ec, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except MyUser.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Enseignant.DoesNotExist:
            return Response({'error': 'Enseignant non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Anacad.DoesNotExist:
            return Response({'error': 'Année académique non trouvée.'}, status=status.HTTP_404_NOT_FOUND
                            )
            
            
class LoginEnseignant(APIView):
    def get(self, request, email, anacad):
        
        try:
            user = MyUser.objects.get(email=email)
            serial_user = Utilisateur_Serial(user)
            enseignant = Enseignant.objects.get(id_user=user)
            serial_enseignant = Enseignant_Serial(enseignant)
            anacad = Anacad.objects.get(denom_anacad=anacad)
            parties_ec = Partie_ec.objects.filter(id_enseignant=enseignant, id_anacad=anacad)
            if not parties_ec.exists():
                return Response({'error': 'Aucune partie EC trouvée pour cet enseignant.'}, status=status.HTTP_404_NOT_FOUND)
            serial_parties_ec = Partie_ec_serial(parties_ec, many=True)
            
            # Initialiser les structures de données imbriquées
            # Condenser l'objet user et l'objet enseignant dans un seul dictionnaire
            data = {**serial_user.data, **serial_enseignant.data}
            # Spécifier l'id user et l'id enseignant
            data['anacad'] = anacad.denom_anacad
            data['id_user'] = user.id
            data['id_enseignant'] = enseignant.id
            #drop id in data
            data.pop('id')   
            # Ajouter les parties EC
            data['parties_ec'] = []
            for i in serial_parties_ec.data:
                if Disponibilite.objects.filter(id_partie_ec=i['id']).exists():
                    i['dispo'] = 'completé'
                else:
                    i['dispo'] = 'pas encore completé'
                
                total_heure = 0
                horaires = Horaire.objects.filter(id_partie_ec=i['id'])
                if horaires.exists():
                    for j in horaires:
                        if j.partie_journ == 'matin':
                            total_heure += 4
                        else:
                            total_heure += 4
                    pourcentage = (total_heure / i['volume_horaire']) * 100
                else:
                    pourcentage = 0
                i['pourcentage'] = pourcentage

                # Récupérer les informations de la promotion, mention, filière et faculté
                ec = Elenent_Const.objects.get(id=i['id_ec'])
                ue = Unite_Ens.objects.get(id=ec.id_ue.id)
                # denomination de l'unité d'enseignement
                i['ue'] = ue.denom_ue
                # DENOMINATION DE L'ELEMENT CONSTITUTIF
                i['ec'] = ec.denom_ec
                promotion = Promotion.objects.get(id=ue.id_promotion.id)
                mention = Mention.objects.get(id=promotion.id_mention.id)
                filiere = Filiere.objects.get(id=mention.id_fil.id)
                faculte = Faculte.objects.get(id=filiere.id_fac.id)

                # Organiser les données dans les dictionnaires imbriqués
                partie_ec_data = {
                    'faculte': faculte.nom_fac,
                    'filiere': filiere.nom_fil,
                    'mention': mention.nom_mention,
                    'promotion': promotion.nom_prom,
                    'partie_ec': i
                }

                data['parties_ec'].append(partie_ec_data)
            
            return Response(data, status=status.HTTP_200_OK)
        
        except MyUser.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Enseignant.DoesNotExist:
            return Response({'error': 'Enseignant non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Anacad.DoesNotExist:
            return Response({'error': 'Année académique non trouvée.'}, status=status.HTTP_404_NOT_FOUND)
        except Elenent_Const.DoesNotExist:
            return Response({'error': 'Element Constitutif non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Unite_Ens.DoesNotExist:
            return Response({'error': 'Unite Ens non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Promotion.DoesNotExist:
            return Response({'error': 'Promotion non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Filiere.DoesNotExist:
            return Response({'error': 'Filiere non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Mention.DoesNotExist:
            return Response({'error': 'Mention non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Faculte.DoesNotExist:
            return Response({'error': 'Faculte non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        
        
        
 
class EnseignantPartieEc(APIView):
    def get(self, request, email, anacad):
        
        try:
            user = MyUser.objects.get(email=email)
            serial_user = Utilisateur_Serial(user)
            enseignant = Enseignant.objects.get(id_user=user)
            serial_enseignant = Enseignant_Serial(enseignant)
            anacad = Anacad.objects.get(denom_anacad=anacad)
            parties_ec = Partie_ec.objects.filter(id_enseignant=enseignant, id_anacad=anacad)
            if not parties_ec.exists():
                return Response({'error': 'Aucune partie EC trouvée pour cet enseignant.'}, status=status.HTTP_404_NOT_FOUND)
            serial_parties_ec = Partie_ec_serial(parties_ec, many=True) 
            data=[]	
                        # Ajouter les parties EC
         
            for i in serial_parties_ec.data:
                if Disponibilite.objects.filter(id_partie_ec=i['id']).exists():
                    i['dispo'] = 'completé'
                else:
                    i['dispo'] = 'pas encore completé'
                
                total_heure = 0
                horaires = Horaire.objects.filter(id_partie_ec=i['id'])
                if horaires.exists():
                    for j in horaires:
                        if j.partie_journ == 'matin':
                            total_heure += 4
                        else:
                            total_heure += 4
                    pourcentage = (total_heure / i['volume_horaire']) * 100
                else:
                    pourcentage = 0
                if pourcentage>100:
                    i['pourcentage']=100
                else:
                    i['pourcentage'] = pourcentage

                # Récupérer les informations de la promotion, mention, filière et faculté
                ec = Elenent_Const.objects.get(id=i['id_ec'])
                ue = Unite_Ens.objects.get(id=ec.id_ue.id)
                # denomination de l'unité d'enseignement
                i['ue'] = ue.denom_ue
                # DENOMINATION DE L'ELEMENT CONSTITUTIF
                i['ec'] = ec.denom_ec
                promotion = Promotion.objects.get(id=ue.id_promotion.id)
                mention = Mention.objects.get(id=promotion.id_mention.id)
                filiere = Filiere.objects.get(id=mention.id_fil.id)
                faculte = Faculte.objects.get(id=filiere.id_fac.id)

                # Organiser les données dans les dictionnaires imbriqués
                partie_ec_data = {
                    'faculte': faculte.nom_fac,
                    'filiere': filiere.nom_fil,
                    'mention': mention.nom_mention,
                    'promotion': promotion.nom_prom,
                    'partie_ec': i
                }

                data.append(partie_ec_data)
            
            return Response(data, status=status.HTTP_200_OK)
        
        except MyUser.DoesNotExist:
            return Response({'error': 'Utilisateur non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Enseignant.DoesNotExist:
            return Response({'error': 'Enseignant non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Anacad.DoesNotExist:
            return Response({'error': 'Année académique non trouvée.'}, status=status.HTTP_404_NOT_FOUND)
        except Elenent_Const.DoesNotExist:
            return Response({'error': 'Element Constitutif non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Unite_Ens.DoesNotExist:
            return Response({'error': 'Unite Ens non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Promotion.DoesNotExist:
            return Response({'error': 'Promotion non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Filiere.DoesNotExist:
            return Response({'error': 'Filiere non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Mention.DoesNotExist:
            return Response({'error': 'Mention non trouvé.'}, status=status.HTTP_404_NOT_FOUND)
        except Faculte.DoesNotExist:
            return Response({'error': 'Faculte non trouvé.'}, status=status.HTTP_404_NOT_FOUND)       