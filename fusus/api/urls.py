from django.urls import path

from . import views
from .views import EmailTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
app_name = "Fusus API"

urlpatterns = [
    path('test/', views.Test.as_view(), name='api-test'),
    path('users/<int:id>/', views.GetUserByID.as_view(), name='api-get_user_by_id'),
    path('users/', views.GetUsers.as_view(), name='api-get_user_by_id'),
    path('auth/login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
