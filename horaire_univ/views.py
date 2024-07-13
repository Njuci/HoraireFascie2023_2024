from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializer import *
from rest_framework.decorators import api_view
from datetime import datetime
from django.contrib.auth import authenticate
from django.conf import settings
import jwt


def maiwn():
    return{"message":"Tout haut"}