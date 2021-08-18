from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from api.serializers import GetUserByIDSerializer, UserSerializer, OrganizationSerializer, ProfileSerializer, \
    EmailTokenObtainPairSerializer
from api.models import Organization, Profile


class EmailTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """Initial test.
        """
        return Response("Test good.", status=status.HTTP_200_OK)

