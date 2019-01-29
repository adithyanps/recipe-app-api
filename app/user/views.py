# from django.shortcuts import render
from rest_framework import generics
from user.serializers import UserSerializer,AuthTokenSerializer
from django.contrib.auth import get_user_model

from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken

# Create your views here.
class CreateUserView(generics.ListCreateAPIView):
    '''Create a new user in the system'''
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

class CreateUserView(generics.CreateAPIView):
    """create a new user in the system"""
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
