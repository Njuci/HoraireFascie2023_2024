from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Domaine,Faculte,Filiere,Mention,Promotion,Unite_Ens,Elenent_Const,Partie_ec,Anacad
from User.models import *
from User.serializers import *
from dispo_app.views import sending_mail

from .serializers import (Domaine_serial,Faculte_serial,Filiere_serial,Mention_serial,Promotion_serial,Unite_Ens_serial,
                          Anacad_serial,Elenent_Const_serial,Partie_ec_serial)
class DomaineView(APIView):
    def get(self,request):
        """
        Pour faire un get des domaines
                        [
                    {
                        "id": 1,
                        "nom_dom": "Sciences et Technologie"
                    }
                ]
        """
        domaine=Domaine.objects.all()
        serializer=Domaine_serial(domaine,many=True)
        return Response(serializer.data)
    def post(self,request):
        
        """ 
        Pour faire un post d'un domaine
        {"nom_dom": "Sciences et Technologie"}
        
        
        """
       
        serializer=Domaine_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        """
        Pour faiee un Put
                    {
                        "id": 1,
                        "nom_dom": "Sciences et Technologie"
                    }
        """
        id=request.data['id']
        domaine=Domaine.objects.get(id=id)
        serializer=Domaine_serial(domaine,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        """ z
        pour supprimer un domaine
        {"id":1}
        """
        id=request.data['id']
        domaine=Domaine.objects.get(id=id)
        if domaine.delete():
            return Response({"messafe":"domaine supprimé"},status=status.HTTP_204_NO_CONTENT)
        return Response({"message":"domaine non supprimé"},status=status.HTTP_400_BAD_REQUEST)

#faculte
class FaculteView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            # Récupérer la dernière année académique
            derniere_anacad = Anacad.objects.latest('id')
            
            # Récupérer les facultés avec leurs domaines
            faculte = Faculte.objects.select_related('id_dom').all()
            liste_fac = []

            # Précharger les encadreurs pour la dernière année académique
            encadreurs = Encadreur_faculte.objects.filter(id_faculte__in=faculte, id_anacad=derniere_anacad).select_related('id_ens__id_user')
            encadreurs_dict = {enc.id_faculte_id: enc for enc in encadreurs}
            
            for i in faculte:
                data = {
                    'id': i.id,
                    'nom_fac': i.nom_fac,
                    'id_dom': i.id_dom.id,
                    'nom_dom': i.id_dom.nom_dom
                }

                # Recherche de l'encadreur pour la faculté
                encadreur = encadreurs_dict.get(i.id)
                if encadreur:
                    try:
                        enseignant = encadreur.id_ens
                        user = enseignant.id_user
                        data['nom_encadreur'] = f"{user.first_name} {user.last_name}"
                    except (Enseignant.DoesNotExist, MyUser.DoesNotExist):
                        data['nom_encadreur'] = "Non assigné"
                else:
                    data['nom_encadreur'] = "Non assigné"

                liste_fac.append(data)

            return Response(liste_fac, status=status.HTTP_200_OK)

        except Anacad.DoesNotExist:
            return Response({"message": "Aucune année académique trouvée"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error in FaculteView GET method: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Ajouter une nouvelle faculté
    def post(self, request, *args, **kwargs):
        try:
            # Sérialiser et valider les données
            serial_data = Faculte_serial(data=request.data)
            if serial_data.is_valid():
                serial_data.save()
                return Response(serial_data.data, status=status.HTTP_201_CREATED)
            return Response(serial_data.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            print(f"Error in FaculteView POST method: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Supprimer une faculté
    def delete(self, request, id):
        try:
            faculte = Faculte.objects.get(pk=id)
            faculte.delete()
            return Response({"message": "Faculté supprimée avec succès"}, status=status.HTTP_204_NO_CONTENT)

        except Faculte.DoesNotExist:
            return Response({"error": "Faculté non trouvée"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(f"Error in FaculteView DELETE method: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Mettre à jour une faculté
    def put(self, request, pk):
        try:
            faculte = Faculte.objects.get(pk=pk)
            serial_data = Faculte_serial(faculte, data=request.data)
            if serial_data.is_valid():
                serial_data.save()
                return Response(serial_data.data, status=status.HTTP_200_OK)
            return Response(serial_data.errors, status=status.HTTP_400_BAD_REQUEST)

        except Faculte.DoesNotExist:
            return Response({"error": "Faculté non trouvée"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(f"Error in FaculteView PUT method: {e}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class FiliereView(APIView):
    def get(self,request):
        """ 
            [
                    {
                        "id": 1,
                        "nom_fil": "Informatique",
                        "id_fac": 1,
                        "nom_fac": "Faculte des sciences informatiques",
                        "nom_dom": "Sciences et Technologie"
                    }
            ]   """
        filiere=Filiere.objects.all()
        serializer=Filiere_serial(filiere,many=True)
        liste_filiere=[]
        
        for i in serializer.data:
            
            fac=Faculte.objects.get(id=i['id_fac'])
            fac_serial=Faculte_serial(fac)
            domaine=Domaine.objects.get(id=fac_serial.data['id_dom'])
            
            i['nom_fac']=fac.nom_fac
            i['nom_dom']=domaine.nom_dom
            
            liste_filiere.append(i)

        return Response(liste_filiere,status=status.HTTP_200_OK)
    def post(self, request):
        """{ "nom_fil": "Informatique", "id_fac": 1 }"""
        print(request.data)
        serializer = Filiere_serial(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self,request):
        """{"id": 1,"nom_fil": "Informatique","id_fac": 1}"""
        id=request.data['id']
        filiere=Filiere.objects.get(id=id)
        serializer=Filiere_serial(filiere,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        """{"id":1}"""
        
        id=request.data['id']
        filiere=Filiere.objects.get(id=id)
        filiere.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Get_FiliereByFaculte(APIView):
    def get(self,request,id_fac):
       
        id_fac=id_fac
        filiere=Filiere.objects.filter(id_fac=id_fac)
        serializer=Filiere_serial(filiere,many=True)
        liste_filiere=[]
        
        for i in serializer.data:
            
            fac=Faculte.objects.get(id=i['id_fac'])
            fac_serial=Faculte_serial(fac)
            domaine=Domaine.objects.get(id=fac_serial.data['id_dom'])
            
            i['nom_fac']=fac.nom_fac
            i['nom_dom']=domaine.nom_dom
            liste_filiere.append(i)
        return Response(liste_filiere,status=status.HTTP_200_OK)    
#mention

class MentionView(APIView):
    def get(self,request):
        """ [
    {
        "id": 1,
        "nom_mention": "Genie Logiciel",
        "id_fil": 1,
        "nom_fac": "Faculte des sciences informatiques",
        "nom_dom": "Sciences et Technologie",
        "nom_fil": "Informatique"
    }]
        """
        mention=Mention.objects.all()
        liste_mention=[]
        serializer=Mention_serial(mention,many=True)
        for i in serializer.data:
            fil=Filiere.objects.get(id=i['id_fil'])
            filserial=Filiere_serial(fil)
            fac=Faculte.objects.get(id=filserial.data['id_fac'])
            fac_serial=Faculte_serial(fac)
            domaine=Domaine.objects.get(id=fac_serial.data['id_dom'])            
            i['nom_fac']=fac.nom_fac
            i['nom_dom']=domaine.nom_dom
            i['nom_fil']=fil.nom_fil
            liste_mention.append(i)
        
        
        return Response(liste_mention,status=status.HTTP_200_OK)
    def post(self,request):
        """ {"nom_mention": "Genie Logiciel", "id_fil": 1}"""
        serializer=Mention_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        """
        { "id": 1,
        "nom_mention": "Genie Logiciel",
        "id_fil": 1} """
        id=request.data['id']
        mention=Mention.objects.get(id=id)
        serializer=Mention_serial(mention,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        """ {"id":1}"""
        id=request.data['id']
        mention=Mention.objects.get(id=id)
        if mention:
            mention.delete()
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)

class Get_MentionByFiliere(APIView):
    def get(self,request,id_fil):
        """
        pour faire un get
        [
    {
    "id": 1,
        "nom_mention": "Genie Logiciel",
        "id_fil": 1,
        "nom_fac": "Faculte des sciences informatiques",
        "nom_dom": "Sciences et Technologie",
        "nom_fil": "Informatique"
    }"""
        mention=Mention.objects.filter(id_fil=id_fil)
        
        liste_mention=[]
        serializer=Mention_serial(mention,many=True)
        for i in serializer.data:
            fil=Filiere.objects.get(id=i['id_fil'])
            filserial=Filiere_serial(fil)
            fac=Faculte.objects.get(id=filserial.data['id_fac'])
            fac_serial=Faculte_serial(fac)
            domaine=Domaine.objects.get(id=fac_serial.data['id_dom'])            
            i['nom_fac']=fac.nom_fac
            i['nom_dom']=domaine.nom_dom
            i['nom_fil']=fil.nom_fil
            liste_mention.append(i)
        
        
        return Response(liste_mention,status=status.HTTP_200_OK)
#promotion
class Get_MentionByFaculte(APIView):
    def get(self,request,id_fac):
        """
        pour faire un get
        [
    {
    "id": 1,
        "nom_mention": "Genie Logiciel",
        "id_fil": 1,
        "nom_fac": "Faculte des sciences informatiques",
        "nom_dom": "Sciences et Technologie",
        "nom_fil": "Informatique"
    }"""
        filiere=Filiere.objects.filter(id_fac=id_fac)
        liste_filiere=[]
        serializer=Filiere_serial(filiere,many=True)
        for i in serializer.data:
            mention=Mention.objects.filter(id_fil=i['id'])
            serializer_mention=Mention_serial(mention,many=True)
            for j in serializer_mention.data:
                fil=Filiere.objects.get(id=j['id_fil'])
                filserial=Filiere_serial(fil)
                fac=Faculte.objects.get(id=filserial.data['id_fac'])
                fac_serial=Faculte_serial(fac)
                domaine=Domaine.objects.get(id=fac_serial.data['id_dom'])            
                j['nom_fac']=fac.nom_fac
                j['nom_dom']=domaine.nom_dom
                j['nom_fil']=fil.nom_fil
                liste_filiere.append(j)
        return Response(liste_filiere,status=status.HTTP_200_OK)
    
class PromotionView(APIView):
    def get(self,request):
        """
        [
    {
        "id": 1,
        "nom_prom": "Bac 1",
        "id_mention": 1
    }
]
            """
        liste_promotion=[]
        promotion=Promotion.objects.all()
        serializer=Promotion_serial(promotion,many=True)
        for i in serializer.data:
            mention=Mention.objects.get(id=i['id_mention'])
            mention_serial=Mention_serial(mention)
            fil=Filiere.objects.get(id=mention_serial.data['id_fil'])
            filserial=Filiere_serial(fil)
            fac=Faculte.objects.get(id=filserial.data['id_fac'])
            fac_serial=Faculte_serial(fac)
            domaine=Domaine.objects.get(id=fac_serial.data['id_dom'])            
            i['nom_fac']=fac.nom_fac
            i['nom_dom']=domaine.nom_dom    
            i['nom_fil']=fil.nom_fil
            i['nom_mention']=mention.nom_mention
            liste_promotion.append(i)
        return Response(liste_promotion,status=status.HTTP_200_OK)
    def post(self,request):
        """{   "nom_prom": "Bac 1",
        "id_mention": 1} """
        serializer=Promotion_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        """{ "id": 1,"nom_prom": "Bac 1","id_mention": 1}"""
        id=request.data['id']
        promotion=Promotion.objects.get(id=id)
        serializer=Promotion_serial(promotion,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        """{"id":1}"""
        id=request.data['id']
        promotion=Promotion.objects.get(id=id)
        promotion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#Gst Promotions by faculty
class Get_PromotionByFaculte(APIView):
    def get(self,request,id_fac):
        """
        pour faire un get
        [
    {   "id": 1,
        "nom_prom": "Bac 1",
        "id_mention": 1,
        "nom_fac": "Faculte des sciences informatiques",
        "nom_dom": "Sciences et Technologie",
        "nom_fil": "Informatique",
        "nom_mention": "Genie Logiciel"
    }
    ]"""
        filiere=Filiere.objects.filter(id_fac=id_fac)
        liste_filiere=[]
        serializer=Filiere_serial(filiere,many=True)
        for i in serializer.data:
            mention=Mention.objects.filter(id_fil=i['id'])
            serializer_mention=Mention_serial(mention,many=True)
            for j in serializer_mention.data:
                #promotion by mention
                promotion=Promotion.objects.filter(id_mention=j['id'])
                serializer_promotion=Promotion_serial(promotion,many=True)
                for k in serializer_promotion.data:
                    fil=Filiere.objects.get(id=j['id_fil'])
                    filserial=Filiere_serial(fil)
                    fac=Faculte.objects.get(id=filserial.data['id_fac'])
                    fac_serial=Faculte_serial(fac)
                    domaine=Domaine.objects.get(id=fac_serial.data['id_dom'])            
                    k['nom_fac']=fac.nom_fac
                    k['nom_dom']=domaine.nom_dom    
                    k['nom_fil']=fil.nom_fil
                    k['nom_mention']=j['nom_mention']
                    #ajout de la promotion
                    liste_filiere.append(k)
                
        return Response(liste_filiere,status=status.HTTP_200_OK)


class Unite_EnsView(APIView):
    def get(self,request):
        """
                            [
                        {
                            "id": 1,
                            "code_ue": "INI001",
                            "denom_ue": "Initiation à la programmation",
                            "semstre": "premier",
                            "id_promotion": 1
                        },
                        {
                            "id": 2,
                            "code_ue": "Inf203",
                            "denom_ue": "Modelisation",
                            "semstre": "premier",
                            "id_promotion": 1
                        },
                        {
                            "id": 3,
                            "code_ue": "Inf2034",
                            "denom_ue": "Modelisation",
                            "semstre": "premier",
                            "id_promotion": 1
                        },
                        {
                            "id": 4,
                                 "code_ue": "inf304",
                            "denom_ue": "Language de programmation mobil",
                            "semstre": "premier",
                            "id_promotion": 1
                        },
                        {
                            "id": 5,
                            "code_ue": "inf245",
                            "denom_ue": "introduction a la cryptologie",
                            "semstre": "premier",
                            "id_promotion": 1
                        }a
                    ]  
                    
                    
                    semstre: premier ou second
                    """
        unite_ens=Unite_Ens.objects.all()
        serializer=Unite_Ens_serial(unite_ens,many=True)
        return Response(serializer.data)
    def post(self,request):
        """ {
                            "code_ue": "inf245",
                            "denom_ue": "introduction a la cryptologie",
                            "semstre": "premier",
                            "id_promotion": 1
                            }
                            
            """
        
        serializer=Unite_Ens_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        """{
                            "id": 5,
                            "code_ue": "inf245",
                            "denom_ue": "introduction a la cryptologie",
                            "semstre": "premier",
                            "id_promotion": 1
                        }"""
        id=request.data['id']
        unite_ens=Unite_Ens.objects.get(id=id)
        serializer=Unite_Ens_serial(unite_ens,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        """{"id":1} """
        id=request.data['id']
        unite_ens=Unite_Ens.objects.get(id=id)
        unite_ens.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#get ue by promotion
class Get_UeByPromotion(APIView):
    def get(self,request,id_promotion):
        """
        pour faire un get
        [  {
            "id": 1,
            "code_ue": "INI001",
            "denom_ue": "Initiation à la programmation",
            "semstre": "premier",
            "id_promotion": 1
        },
        {
            "id": 2,
            "code_ue": "Inf203",
            "denom_ue": "Modelisation",
            "semstre": "premier",
            "id_promotion": 1
        },
        {
            "id": 3,
            "code_ue": "Inf2034",
            "denom_ue": "Modelisation",
            "semstre": "premier",
            "id_promotion": 1
        },
        {
            "id": 4,
            "code_ue": "inf304",
            "denom_ue": "Language de programmation mobil",
            "semstre": "premier",
            "id_promotion": 1
        },
        {
            "id": 5,
            "code_ue": "inf245",
            "denom_ue": "introduction a la cryptologie",
            "semstre": "premier",
            "id_promotion": 1
        }]
        
        """
        unite_ens=Unite_Ens.objects.filter(id_promotion=id_promotion)
        serializer=Unite_Ens_serial(unite_ens,many=True)
        return Response(serializer.data)
    



class AnacadView(APIView):
    def get(self,request):
        """ 
        pour faire un get
            [
            {
                "id": 1,
                "denom_anacad": "2023-2024"
            },
            {
                "id": 2,
                "denom_anacad": "2024-2025"
            }]        
        
        """
        
        anacad=Anacad.objects.all()
        serializer=Anacad_serial(anacad,many=True)
        return Response(serializer.data)
    def post(self,request):
        """{"denom_anacad": "2023-2024"}"""
        serializer=Anacad_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        """{
            "id": 1,
            "denom_anacad": "2023-2024"
        }"""
        
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
        """
                [
            {
                "id": 1,
                "denom_ec": "Language de programmation mobil",
                "niveau_ec": "1",
                "id_ue": 4
            },
            {
                "id": 2,
                "denom_ec": "UML2",
                "niveau_ec": "2",
                "id_ue": 3
            },
            {
                "id": 3,
                "denom_ec": "TBD",
                "niveau_ec": "2",
                "id_ue": 3
            },
            {
                "id": 4,
                "denom_ec": "Langage  Kotkin",
                "niveau_ec": "2",
                "id_ue": 4
            },
            {
                "id": 5,
                "denom_ec": "Python",
                "niveau_ec": "2",
                "id_ue": 1
            }
        ]

 """
        elenent_const=Elenent_Const.objects.all()
        serializer=Elenent_Const_serial(elenent_const,many=True)
        return Response(serializer.data)
    def post(self,request):
        """ {
            "denom_ec": "Python",
            "niveau_ec": "2",
            "id_ue": 1
        }"""
        serializer=Elenent_Const_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        """{
            "id": 5,
            "denom_ec": "Python",
            "niveau_ec": "2",
            "id_ue": 1
        }"""
        id=request.data['id']
        elenent_const=Elenent_Const.objects.get(id=id)
        serializer=Elenent_Const_serial(elenent_const,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        """{"id":1}"""
        id=request.data['id']
        elenent_const=Elenent_Const.objects.get(id=id)
        elenent_const.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Get Element_const by UE

class Get_EcByUe(APIView):
    def get(self,request,id_ue):
        """
        pour faire un get
        [
    {
        "id": 1,
        "denom_ec": "Python",
        "niveau_ec": "2",
        "id_ue": 1
        "id_promotion": 1,
        "nom_prom": "Bac 1",
        "nom_ue": "Initiation à la programmation"
    },

]"""
        elenent_const=Elenent_Const.objects.filter(id_ue=id_ue)
        serializer=Elenent_Const_serial(elenent_const,many=True)
        liste_ec=[]
        for i in serializer.data:
            ue=Unite_Ens.objects.get(id=i['id_ue'])
            ue_serial=Unite_Ens_serial(ue)
            promotion=Promotion.objects.get(id=ue_serial.data['id_promotion'])
            promotion_serial=Promotion_serial(promotion)
            i['nom_prom']=promotion_serial.data['nom_prom']
            i['nom_ue']=ue_serial.data['denom_ue']
            liste_ec.append(i)
        return Response(liste_ec,status=status.HTTP_200_OK)





class Get_Partie_ecByEcAnacad(APIView):
    def get(self, request, id_ec, id_anacad):
        """
        pour faire un get
        [
            {
                "id": 2,
                "volume_horaire": 45,
                "partie_ec_choice": "cmi",
                "date_debut": "2024-11-13",
                "date_fin": "2025-05-24",
                "id_ec": 3,
                "id_anacad": 1,
                "id_enseignant": 4,
                "denom_ec": "Python",
                "niveau_ec": "2",
                "id_ue": 1,
                "id_promotion": 1,
                "nom_prom": "Bac 1",
                "nom_ue": "Initiation à la programmation"
            }
        ]
        """
        # 
        partie_ec = Partie_ec.objects.filter(id_ec=id_ec, id_anacad=id_anacad)
        # Sérialiser les données
        serializer = Partie_ec_serial(partie_ec, many=True)
        
        # Ajouter les informations de l'EC, de l'UE et de la promotion
        liste_partie_ec = []
        for partie in serializer.data:
            ec = Elenent_Const.objects.get(id=partie['id_ec'])
            ue = Unite_Ens.objects.get(id=ec.id_ue.id)
            
            partie['denom_ec'] = ec.denom_ec
            partie['niveau_ec'] = ec.niveau_ec
            partie['id_ue'] = ue.id
            partie['nom_ue'] = ue.denom_ue

            
            liste_partie_ec.append(partie)
        
        return Response(liste_partie_ec, status=status.HTTP_200_OK)
#partie_ec




class Partie_ecView(APIView):
    def get(self,request):
        """[

    {
        "id": 2,
        "volume_horaire": 45,
        "partie_ec_choice": "cmi",
        "date_debut": "2024-11-13",
        "date_fin": "2025-05-24",
        "id_ec": 3,
        "id_anacad": 1,
        "id_enseignant": 4
    }
]""" 
        partie_ec=Partie_ec.objects.all()
        serializer=Partie_ec_serial(partie_ec,many=True)
        return Response(serializer.data)
    def post(self,request):
        
        """

    {
        "volume_horaire": 45,
        "partie_ec_choice": "cmi",
        "date_debut": "2024-11-13",
        "date_fin": "2025-05-24",
        "id_ec": 3,
        "id_anacad": 1,
        "id_enseignant": 4
    }
        """
        print(request.data)
            
        serializer=Partie_ec_serial(data=request.data)
        if not serializer.is_valid():
            print(serializer.errors)  # Affiche les erreurs de validation pour diagnostiquer le problème
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            email_sending=sending_mail(serializer.data['id'])
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
    def put(self,request):
        """{
        "id": 11,
        "volume_horaire": 1,
        "partie_ec_choice": "tp",
        "id_ec": 5,
        "id_anacad": 1,
        "id_enseignant": 2
    } """
        
        

        id=request.data['id']
        partie_ec=Partie_ec.objects.get(id=id)
        serializer=Partie_ec_serial(partie_ec,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        """{"id":1}"""
        id=request.data['id']
        partie_ec=Partie_ec.objects.get(id=id)
        partie_ec.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)














