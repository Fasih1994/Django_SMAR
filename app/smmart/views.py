from rest_framework import (
    generics,
    authentication,
    viewsets,
    status
)
from rest_framework.permissions import IsAuthenticated
from core.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from user.serializers import AdminUserCreateSerializer
from .serializers import (
    TopicSerializer,
    # GetDataSerializer
)
from core.models import Topics
from rest_framework.response import Response


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
