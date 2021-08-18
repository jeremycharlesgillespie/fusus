from django.urls import path

from . import views
from .views import EmailTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
app_name = "Fusus API"

urlpatterns = [
    path('test/', views.Test.as_view(), name='api-test')
]
