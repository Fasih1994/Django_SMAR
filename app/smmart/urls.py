"""
URLs Mappings for the User API
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from smmart import views

router = DefaultRouter()

router.register('admin/users', viewset=views.UserViewSet)
router.register('user/topics', viewset=views.TopicViewSet)

app_name = 'smmart'

urlpatterns = [
    # path('admin/user/create', views.AdminUserCreateAPIView.as_view(), name='new-user'),
    path('admin/user/', views.ManageAdminUserAPIView.as_view(), name='edit-user'),
    path('', include(router.urls)),
]
