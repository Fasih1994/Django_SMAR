from rest_framework import (
    generics,
    authentication,
    viewsets,
    status
)
from rest_framework.generics import GenericAPIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view

from django.utils import timezone
from core.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from user.serializers import (
    AdminUserCreateSerializer, AdminUserUpdateSerializer,
    PackageSerializer
    )
from .serializers import (
    TopicSerializer,
    # GetDataSerializer,
    OrganizationSerializer,
    PackageStatusSerializer
)
from core.models import (
    Topics,
    Organization,
    User,
    Package,
    # UserRole,
    PackageStatus
    )


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
#                 return Response(
    # {'error': 'Topic not found'},
    # status=status.HTTP_404_NOT_FOUND
    # )
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
        queryset = get_user_model().objects.filter(
            organization_id=organization_id
            )
        return queryset


class ManageOrganizationPackageAPIView(generics.RetrieveAPIView):
    serializer_class = PackageStatusSerializer
    queryset = PackageStatus.objects.all()
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def retrieve(self, request, *args, **kwargs):
        user_organization_id = request.user.organization_id
        instance = PackageStatus.objects.filter(
            organization_id=user_organization_id,
            status='y'
            ).first()

        if not instance:
            return Response(
                {'error': 'Package status not found for the user organization'},
                status=status.HTTP_404_NOT_FOUND
                )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class UpdatePackage(GenericAPIView):

    serializer_class = PackageSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    authentication_classes = [authentication.TokenAuthentication]

    def put(self, request):

        package_name = request.data.get('name')

        user_organization_id = request.user.organization_id

        current_package = PackageStatus.objects.filter(
            organization=user_organization_id, status='y'
        ).first()

        try:
            selected_package = Package.objects.get(name=package_name)
        except Package.DoesNotExist:
            return Response(
                {'error': 'Package does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )

        if selected_package.id == current_package.package_id:
            current_package.start_date = timezone.now()
            current_package.end_date = current_package.start_date + timezone.timedelta(days=30)
            current_package.save()
            new_package_status = current_package
        else:
            current_package.status = 'n'
            current_package.save()

            start_date = timezone.now()
            end_date = start_date + timezone.timedelta(days=30)
            status_value = 'y'

            new_package_status = PackageStatus.objects.create(
                organization_id=user_organization_id,
                package=selected_package,
                start_date=start_date,
                end_date=end_date,
                status=status_value,
                created_by=request.user.id
            )

            users_to_update = get_user_model().objects.filter(organization_id=user_organization_id)
            for user in users_to_update:
                user.package_id = selected_package.id
                user.save()

        serializer = PackageStatusSerializer(new_package_status)
        return Response(serializer.data, status=status.HTTP_200_OK)
