"""
Views for the User API
"""
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    UserUpdateSerializer
)

from django.contrib.auth import get_user_model


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system

    Args:
        generics (_type_): _description_
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """manage the authenticated user"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authneticated user"""
        return self.request.user

    def get_serializer_class(self):
        # Use UserUpdateSerializer for PUT and PATCH requests
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer
