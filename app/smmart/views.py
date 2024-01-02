from rest_framework import (
    generics,
    authentication,
    viewsets,
    status
)
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from user.serializers import (
    AdminUserCreateSerializer, AdminUserUpdateSerializer,
    PackageSerializer
    )
from .serializers import (
    TopicSerializer,
    GetDataSerializer,
    OrganizationSerializer
)
from core.models import Topics, Organization, User, Package, UserRole
from rest_framework.response import Response


class AdminUserCreateAPIView(generics.CreateAPIView):
    serializer_class = AdminUserCreateSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]


class ManageOrganizationAPIView(generics.RetrieveUpdateDestroyAPIView):
    """manage the Organization created by admin user"""
    serializer_class = OrganizationSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        """Return authenticated admin user"""
        return self.request.user.organization


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
        """Return all topics created by the user"""
        user = self.request.user
        topics = Topics.objects.filter(user=user)
        # Serialize the queryset using TopicSerializer

        return topics

    # def get_queryset(self):
    #     """Return all topics created by user"""
    #     user = self.request.user
    #     #user_id = user.id
    #     org_id = user.organization_id
    #     queryset = Topics.objects.filter(user__organization_id=org_id)
    #     return queryset


# class GetDataAPIView(generics.CreateAPIView):
#     serializer_class = GetDataSerializer
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         serializer = GetDataSerializer(data=request.query_params)
#         serializer.is_valid(raise_exception=True)

#         user_id = serializer.validated_data['user_id']
#         organization_id = serializer.validated_data['organization_id']
#         topic_id = serializer.validated_data.get('topic_id')
#         keywords = serializer.validated_data['keywords']
#         platforms = serializer.validated_data['platforms']

#         if topic_id:
#             try:
#                 topic = Topics.objects.get(id=topic_id)
#             except Topics.DoesNotExist:
#                 return Response({'error': 'Topic not found'}, status=status.HTTP_404_NOT_FOUND)
#         else:
#             topic_data = {
#                 'name': '',
#                 'prompt': '',
#                 'keywords': keywords,
#                 'platform': platforms,
#                 'status': '',
#                 'user': user_id,
#             }
#             topic_serializer = TopicSerializer(data=topic_data)
#             topic_serializer.is_valid(raise_exception=True)
#             topic = topic_serializer.save()

#         for keyword in keywords:
#             print(f'Keyword: {keyword}')

#         for platform in platforms:
#             print(f'Platform: {platform}')

#         data = {
#             'user_id': user_id,
#             'organization_id': organization_id,
#             'topic_id': topic.id,
#             'platform': topic.platform,
#             'keywords': topic.keywords,
#         }

#         return Response(data)


class ManageAdminUserAPIView(generics.RetrieveUpdateDestroyAPIView):
    """manage the authenticated user"""
    serializer_class = AdminUserCreateSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        """Return authenticated admin user"""
        return self.request.user

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AdminUserUpdateSerializer
        return AdminUserCreateSerializer


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


class ManageOrganizationPackageAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = PackageSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)

        user_organization_id = self.request.user.organization_id
        organization = Organization.objects.get(pk=user_organization_id)

        package_name = request.data.get('name')

        try:
            package = Package.objects.get(name=package_name)
        except Package.DoesNotExist:
            return Response({'error': 'Package does not exist'}, status=status.HTTP_404_NOT_FOUND)

        new_package_id = package.id

        users_to_update = User.objects.filter(organization=organization)
        for user in users_to_update:
            user.package_id = new_package_id
            user.save()

        serializer = self.get_serializer(organization, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        user_package_id = self.request.user.package_id
        package = Package.objects.get(pk=user_package_id)
        return package


# class ManageUserRoleAPIView(generics.UpdateAPIView):
#     serializer_class = UserRoleSerializer
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [IsAuthenticated, IsAdminUser]

#     def update(self, request, *args, **kwargs):
#         user_organization_id = self.request.user.organization_id

#         try:
#             user_id_to_update = kwargs.get('pk')
#             user = User.objects.get(pk=user_id_to_update, organization_id=user_organization_id)
#         except User.DoesNotExist:
#             return Response({'error': 'User does not exist or does not belong to the organization'}, status=status.HTTP_404_NOT_FOUND)

#         role_name = request.data.get('name')

#         try:
#             role = UserRole.objects.get(name=role_name)
#         except UserRole.DoesNotExist:
#             return Response({'error': 'Role does not exist'}, status=status.HTTP_404_NOT_FOUND)

#         user.role_id = role.id
#         user.save()

#         serializer = self.get_serializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
