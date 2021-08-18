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

    def patch(self, request, id):
        """Update user information for the user_id if request user is 'Administrator' of his organization.
        Or request user is user_id.
        """
        api_user = request.user
        # validate user/admin
        if api_user.id == id or api_user.is_superuser:
            #TODO READ IN THE ACCOUNT DETAILS, MAKE THE CHANGES
            return Response({"result": "Account updated successfully."})
        else:
            return Response({"result": "You are not authorized to change this account."},
                            status=status.HTTP_403_FORBIDDEN)


class GetUsers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """List all the users for the user organization if user is `Administrator` or
        `Viewer`. Must return all the user model fields. Should support search by name, email.
        Should support filter by phone.
        """
        query_email = request.GET.get('email', None)
        query_name = request.GET.get('name', None)
        query_phone = request.GET.get('phone', None)

        api_user = request.user
        api_user_permissions = api_user.get_user_permissions()
        if 'api.view_organization' in api_user_permissions:
            org_name = api_user.profile.organization.name
            collected_profiles = Profile.objects.filter(organization__name=org_name)  # Queryset
            if query_email is not None:
                collected_profiles = collected_profiles.filter(email=query_email)
            if query_name is not None:
                collected_profiles = collected_profiles.filter(name=query_name)
            if query_phone is not None:
                collected_profiles = collected_profiles.filter(phone=query_phone)

            serializer = ProfileSerializer(collected_profiles, many=True)
            return Response(serializer.data)
        else:
            return Response({"result": "Your user account does not have an organization to reference."}, status.HTTP_200_OK)

    def post(self, request):
        """Creates a user account for the organization.
        """
        api_user = request.user
        if api_user.is_superuser:
            new_username = request.data.get('username', None)
            new_password = request.data.get('password', None)
            new_email = request.data.get('email', None)
            if new_password is not None and new_password is not None:
                try:
                    user = User.objects.create_user(username=new_username,
                                                    email=new_email,
                                                    password=new_password)
                except Exception as e:
                    return Response({"result": "User not created.",
                                     "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"result": "User created"}, status=status.HTTP_200_OK)
            else:
                return Response({"result": "Please include both the username and password to create a user."},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"result": "You are not authorized to create users."}, status=status.HTTP_400_BAD_REQUEST)
