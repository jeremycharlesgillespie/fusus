from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from api.serializers import GetUserByIDSerializer, UserSerializer, OrganizationSerializer, ProfileSerializer, \
    EmailTokenObtainPairSerializer
from api.models import Organization, Profile


class EmailTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = EmailTokenObtainPairSerializer


class GetUserByID(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        """List all the users for the user organization if user is `Administrator` or `Viewer`.
        """
        profile = Profile.objects.get(id=id)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

class GetUsers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List all the users for the user organization if user is `Administrator` or
        `Viewer`. Must return all the user model fields. Should support search by name, email.
        Should support filter by phone.
        """
        apiuser = request.user
        auth = request.auth
        email = request.GET.get('email', None)
        name = request.GET.get('name', None)
        phone = request.GET.get('phone', None)
        return Response("")
