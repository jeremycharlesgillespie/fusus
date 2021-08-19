from django.urls import path

from . import views
from .views import EmailTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
app_name = "Fusus API"

urlpatterns = [
    path('auth/login/', EmailTokenObtainPairView.as_view(), name='api-token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='api-token_refresh'),
    path('users/<int:target_account_id>/', views.UserManagement.as_view(), name='api-user_management'),
    path('users/', views.GetUsers.as_view(), name='api-get_users'),
    path('organizations/<int:target_org_id>/', views.GetUpdateOrganizations.as_view(),
         name='api-get_update_organizations'),
    path('organization/<int:target_org_id>/users/', views.GetOrganizationUsers.as_view(),
         name='api-get_organization_users'),
    path('organization/<int:target_org_id>/users/<int:target_account_id>/', views.GetOrganizationUser.as_view(),
         name='api-get_organization_user'),
    path('info/', views.GetAPIInfo.as_view(), name='api-get_api_info'),
    path('auth/groups/', views.AuthGroups.as_view(), name='api-auth_groups'),
]
