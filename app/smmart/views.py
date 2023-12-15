from rest_framework import generics, authentication, viewsets
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from user.serializers import AdminUserCreateSerializer


class AdminUserCreateAPIView(generics.CreateAPIView):
    serializer_class = AdminUserCreateSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class ManageAdminUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    """manage the authenticated user"""
    serializer_class = AdminUserCreateSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        """Return authenticated admin user"""
        return self.request.user


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = AdminUserCreateSerializer
    queryset = get_user_model().objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        """Return all users created by the admin user"""
        admin_user = self.request.user
        organization_id = admin_user.organization_id
        queryset = get_user_model().objects.filter(organization_id=organization_id)
        return queryset