from rest_framework import generics, authentication, viewsets
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from user.serializers import AdminUserCreateSerializer
from .serializers import TopicSerializer
from core.models import Topics


class AdminUserCreateAPIView(generics.CreateAPIView):
    serializer_class = AdminUserCreateSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class TopicCreationAPIView(generics.CreateAPIView):
    serializer_class = TopicSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]


class TopicViewSet(viewsets.ModelViewSet):
    """manage the topics created by user"""
    serializer_class = TopicSerializer
    queryset = Topics.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return all topics created by user"""
        user = self.request.user
        user_id = user.id
        queryset = Topics.objects.filter(user_id=user_id)
        return queryset

    # def get_queryset(self):
    #     """Return all topics created by user"""
    #     user = self.request.user
    #     #user_id = user.id
    #     org_id = user.organization_id
    #     queryset = Topics.objects.filter(user__organization_id=org_id)
    #     return queryset


class ManageAdminUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    """manage the authenticated user"""
    serializer_class = AdminUserCreateSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
