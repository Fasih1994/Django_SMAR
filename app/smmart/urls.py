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
    # path(
    #     'admin/user/create', views.AdminUserCreateAPIView.as_view(),
    #     name='new-user'
    #     ),
    path(
        'admin/user/', views.ManageAdminUserAPIView.as_view(),
        name='edit-user'
        ),
    path(
        'admin/organization', views.ManageOrganizationAPIView.as_view(),
        name='edit-organization'
         ),
    path(
        'admin/get/package',
        views.ManageOrganizationPackageAPIView.as_view(),
        name='get-package'
        ),
    path(
        'admin/assign/package',
        views.UpdatePackage.as_view(),
        name='assign-package'
    ),
    # path(
    #     'admin/assign/role/<int:pk>', views.ManageUserRoleAPIView.as_view(),
    #     name='update-role'
    #     ),
    # path('get-data/', views.GetDataAPIView.as_view(), name='get-data'),
    path('', include(router.urls)),
]
