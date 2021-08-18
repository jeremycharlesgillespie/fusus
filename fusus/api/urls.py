from django.urls import path

from . import views
from .views import EmailTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
app_name = "Fusus API"

urlpatterns = [
    path('users/<int:id>/', views.GetUserByID.as_view(), name='api-get_user_by_id'),
    path('users/', views.GetUsers.as_view(), name='api-get_users'),
    path('auth/login/', EmailTokenObtainPairView.as_view(), name='api-token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='api-token_refresh'),
]
