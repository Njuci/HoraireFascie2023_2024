from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Domaine,Faculte,Filiere,Mention,Promotion,Unite_Ens,Elenent_Const,Partie_ec,Anacad
from User.models import *
from User.serializers import *


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
        """ 
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
    def get(self,request):
        """
           [
                                    {
                                        "id": 1,
                                        "nom_fac": "Faculté des sciences",
                                        "id_dom": 1,
                                        "nom_dom": "Sciences et technologies"
                                    }
                                    ]    
        
        """
        dernier_anacad = Anacad.objects.latest('id')
        serial_anacad=Anacad_serial(dernier_anacad)
        
        faculte=Faculte.objects.all()
        
        serializer=Faculte_serial(faculte,many=True)
        liste_fac=[]
        for i in serializer.data:
            domaine=Domaine.objects.get(id=i['id_dom'])
            print(i['id'],serial_anacad.data['id'])
            i['nom_dom'] = domaine.nom_dom
            try:
                encadreur = Encadreur_faculte.objects.get(id_faculte=i['id'], id_anacad=serial_anacad.data['id'])
                serial_encadreur = Encadreur_faculte_Serial(encadreur).data  # Ajout de .data pour accéder aux données sérialisées
                enseignant = Enseignant.objects.get(id=serial_encadreur['id_ens'])  # Utilisation de id= pour la requête
                serial_enseignant = Enseignant_Serial(enseignant).data  # Ajout de .data pour accéder aux données sérialisées
                user = MyUser.objects.get(id=serial_enseignant['id_user'])  # Utilisation de id= pour la requête
                serial_user = Utilisateur_Serial(user).data  # Ajout de .data pour accéder aux données sérialisées
                i['nom_encadreur'] = serial_user['first_name'] + " " + serial_user['last_name']
            except Encadreur_faculte.DoesNotExist:
                print("errors")
                pass
            except Enseignant.DoesNotExist:
                print("print")
                pass
            
            
            
            liste_fac.append(i)
            
        return Response(liste_fac)
    def post(self,request):
        """ {"nom_fac": "Faculte des sciences informatiques",
        "id_dom": 1
            }"""
        serializer=Faculte_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def put(self,request):
        """
                             {   "id": 1,
                                "nom_fac": "Faculte des sciences informatiques",
                                "id_dom": 1
                            }        """
        id=request.data['id']
        faculte=Faculte.objects.get(id=id)
        serializer=Faculte_serial(faculte,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def delete(self,request):
        """{"id":1}"""
        id=request.data['id']
        faculte=Faculte.objects.get(id=id)
        faculte.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#filiere
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
    def post(self,request):
        """{ "nom_fil": "Informatique",
                                "id_fac": 1}"""
        serializer=Filiere_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
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
    def post(self,request,id_facul):
       
        id_fac=id_facul
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
#unite_ens

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
#anacad
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
#partie_ec
class Partie_ecView(APIView):
    def get(self,request):
        """[
    {
        "id": 1,
        "volume_horaire": 45,
        "partie_ec_choice": "cmi",
        "id_ec": 1,
        "id_anacad": 1,
        "id_enseignant": 1
    },
    {
        "id": 2,
        "volume_horaire": 1,
        "partie_ec_choice": "cmi",
        "id_ec": 2,
        "id_anacad": 1,
        "id_enseignant": 2
    },
    {
        "id": 3,
        "volume_horaire": 1,
        "partie_ec_choice": "tp",
        "id_ec": 1,
        "id_anacad": 1,
        "id_enseignant": 2
    },
    {
        "id": 4,
        "volume_horaire": 1,
        "partie_ec_choice": "tp",
        "id_ec": 2,
        "id_anacad": 1,
        "id_enseignant": 1
    },
    {
        "id": 5,
        "volume_horaire": 1,
        "partie_ec_choice": "tp",
        "id_ec": 3,
        "id_anacad": 1,
        "id_enseignant": 2
    },
    {
        "id": 6,
        "volume_horaire": 1,
        "partie_ec_choice": "cmi",
        "id_ec": 3,
        "id_anacad": 1,
        "id_enseignant": 2
    },
    {
        "id": 7,
        "volume_horaire": 1,
        "partie_ec_choice": "cmi",
        "id_ec": 4,
        "id_anacad": 1,
        "id_enseignant": 2
    },
    {
        "id": 8,
        "volume_horaire": 1,
        "partie_ec_choice": "tp",
        "id_ec": 4,
        "id_anacad": 1,
        "id_enseignant": 1
    },
    {
        "id": 10,
        "volume_horaire": 1,
        "partie_ec_choice": "cmi",
        "id_ec": 5,
        "id_anacad": 1,
        "id_enseignant": 1
    },
    {
        "id": 11,
        "volume_horaire": 1,
        "partie_ec_choice": "tp",
        "id_ec": 5,
        "id_anacad": 1,
        "id_enseignant": 2
    }
]""" 
        partie_ec=Partie_ec.objects.all()
        serializer=Partie_ec_serial(partie_ec,many=True)
        return Response(serializer.data)
    def post(self,request):
        """{
            "volume_horaire": 1,
            "partie_ec_choice": "tp",
            "id_ec": 5,
            "id_anacad": 1,
            "id_enseignant": 2      }"""
            
        serializer=Partie_ec_serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
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














