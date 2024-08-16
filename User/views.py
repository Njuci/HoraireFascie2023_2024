from django.shortcuts import render
# Create your views here.
from .models import MyUser,Enseignant,Chef_Promotion,Encadreur_faculte
from .serializers import Utilisateur_Serial,Enseignant_Serial,Chef_Promotion_Serial,Encadreur_faculte_Serial
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.response import Response
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
        
        
        {" first_name":"Van dam","last_name":"Jean-claude","email":"njcuimec@gmail.com",
            "password":"4355vvefeef","user_type":"enseignant", ""} exemple
            
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
        """ {" first_name":"Van dam","last_name":"Jean-claude","email":"njcuimec@gmail.com",
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
        request.data.pop(i for i in user.keys())
        enseignant.update(request.data)
        serializer=Enseignant_Serial(data=request.data)
        if serializer.is_valid(raise_exception=True):
             serializer.save()
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    def get(self,request):
        """enseignant and users type enseignant"""
        enseignant_users_list=[]
        user=MyUser.objects.filter(user_type='enseignant')
        for i in user:
            ensignant=Enseignant.objects.get(id_user=i)
            if ensignant:
                # melanger les deux dictionnaires en distinguant id_enseignant et id_user
                melange={}
                melange.update(ensignant.__dict__)
                melange.update(i.__dict__)
                melange.pop('id')
                melange['id_enseignant']=ensignant.id
                melange['id_user']=i.id 
                enseignant_users_list.append(melange)
    
        serializer=enseignant_users_list
        return Response(serializer,status=status.HTTP_200_OK)
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
        serial=Encadreur_faculte(request.data)
        if serial.is_valid():
            serial.save()
        else:
            return Response(serial.erros,status=status.HTTP_400_BAD_REQUEST)
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
        """ en cardeur par id"""
        id=request.data['id']
        user=Encadreur_faculte.objects.get(id=id)
        serializer=Encadreur_faculte_Serial(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
class LoginView(APIView):
    def get(self,request):
        email=request.data['email']
        password=request.data['password']
        try:
            user = MyUser.objects.get(email=email)
            if user.check_password(password):
                serial=Utilisateur_Serial(user)
                return Response({"user": serial.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except MyUser.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)