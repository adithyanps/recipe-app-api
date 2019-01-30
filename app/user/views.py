# from django.shortcuts import render
from rest_framework import generics, authentication, permissions
from user.serializers import UserSerializer,AuthTokenSerializer
from django.contrib.auth import get_user_model

from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken

# Create your views here.
class CreateUserView(generics.ListCreateAPIView):
    '''Create a new user in the system'''
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """manage the authenticated user"""

    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user
