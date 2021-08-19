from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from requests import get

from api.serializers import UserSerializer, OrganizationSerializer, ProfileSerializer, \
    EmailTokenObtainPairSerializer, PatchUserUpdateSerializer, PatchOrgUpdateSerializer, ShortUserSerializer, \
    APIInfoSerializer, GroupSerializer
from api.models import Organization, Profile


class EmailTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = EmailTokenObtainPairSerializer


class UserManagement(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, target_account_id):
        """List all the users for the user organization if user is `Administrator` or `Viewer`.
        """
        try:
            profile = Profile.objects.get(id=target_account_id)
        except Profile.DoesNotExist:
            return Response({"result": "Profile not found."}, status.HTTP_400_BAD_REQUEST)
        serializer = ProfileSerializer(profile)
        return Response({"result": "Profile was found.", "User Info": serializer.data})

    def patch(self, request, target_account_id):
        """Update user information for the user_id if request user is 'Administrator' of his organization.
        Or request user is user_id.
        """
        api_user = request.user
        administrator = Group.objects.get(name="Administrator")
        if administrator in api_user.groups.all() or api_user.id == target_account_id:
            # Validate api_user input.
            api_user_input = PatchUserUpdateSerializer(data=request.data)
            if api_user_input.is_valid():
                # Get the target account.
                target_user = User.objects.get(id=target_account_id)
                # Loop through the validated values and update the account as needed.
                for key in api_user_input.data:
                    if key == "username":
                        target_user.username = api_user_input.data[key]
                    if key == "password":
                        target_user.set_password(api_user_input.data[key])
                    if key == "email":
                        target_user.email = api_user_input.data[key]
                    if key == "first_name":
                        target_user.first_name = api_user_input.data[key]
                    if key == "last_name":
                        target_user.last_name = api_user_input.data[key]
                # After all changes to the user object are complete, save.
                api_user.save()
                serializer = UserSerializer(api_user)
                return Response({"result": "Account updated successfully.", "User Info": serializer.data})
            else:
                return Response({"result": "Account not updated.", "errors": api_user_input.errors})
        else:
            return Response({"result": "You are not authorized to change this account."},
                            status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, target_account_id):
        """Delete user for the user_id if request user is 'Administrator' of his organization.
        """
        api_user = request.user
        administrator = Group.objects.get(name="Administrator")
        if administrator in api_user.groups.all():
            try:
                user = User.objects.get(id=target_account_id)
            except User.DoesNotExist:
                return Response({"result": "User account not found with id: " + str(target_account_id)})
            user.delete()
            return Response({"result": "Account deleted successfully."})
        else:
            return Response({"result": "You are not authorized to delete this account."},
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
        viewer = Group.objects.get(name="Viewer")
        administrator = Group.objects.get(name="Administrator")
        if viewer in api_user.groups.all() or administrator in api_user.groups.all():
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
            return Response({"error": "You are not authorized to do this action."}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Creates a user account for the organization.
        """
        api_user = request.user
        administrator = Group.objects.get(name="Administrator")
        if administrator in api_user.groups.all():
            username = request.data.get('username', None)
            password = request.data.get('password', None)
            email = request.data.get('email', "")
            first_name = request.data.get('first_name', "")
            last_name = request.data.get('last_name', "")
            if username is not None and password is not None:
                try:
                    user = User.objects.create_user(username=username,
                                                    email=email,
                                                    password=password,
                                                    first_name=first_name,
                                                    last_name=last_name)
                except Exception as e:
                    return Response({"result": "User not created.",
                                     "error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                serializer = UserSerializer(user)
                return Response({"result": "User created", "User Info": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"result": "Please include both the username and password to create a user."},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"result": "You are not authorized to create users."}, status=status.HTTP_400_BAD_REQUEST)


class GetUpdateOrganizations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, target_org_id):
        """Retrieve organization information if request user is "Administrator" or "Viewer".
        """
        api_user = request.user
        api_user_permissions = api_user.get_user_permissions()
        if 'api.view_organization' in api_user_permissions or api_user.is_superuser:
            org = Organization.objects.get(id=target_org_id)
            serializer = OrganizationSerializer(org)
            return Response({"result": "Organization information retrieved.", "Org Info": serializer.data})
        else:
            return Response({"result": "You are not authorized to retrieve information for this organization."},
                            status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, target_org_id):
        """Update organization if request user is "Administrator".
        """
        api_user = request.user
        administrator = Group.objects.get(name="Administrator")
        if administrator in api_user.groups.all():
            try:
                org = Organization.objects.get(id=target_org_id)
            except Organization.DoesNotExist:
                return Response({"result": "Organization not found."}, status=status.HTTP_400_BAD_REQUEST)
            api_user_input = PatchOrgUpdateSerializer(data=request.data)
            if api_user_input.is_valid():
                # Loop through the validated values and update the org as needed.
                for key in api_user_input.data:
                    if key == "name":
                        org.name = api_user_input.data[key]
                    if key == "phone":
                        org.phone = api_user_input.data[key]
                    if key == "address":
                        org.address = api_user_input.data[key]
                    # After all changes to the user object are complete, save.
                org.save()
                serializer = OrganizationSerializer(org)
                return Response({"result": "Organization updated successfully.", "Org Info": serializer.data})
            else:
                return Response({"result": "Organization not updated.", "errors": api_user_input.errors},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"result": "You are not authorized to change this organization."},
                            status=status.HTTP_403_FORBIDDEN)


class GetOrganizationUsers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, target_org_id):
        """List all the users for the user organization if user if "Administrator" or "Viewer". Returns only the ID and
        name of the users.
        """
        api_user = request.user
        viewer = Group.objects.get(name="Viewer")
        administrator = Group.objects.get(name="Administrator")
        if viewer in api_user.groups.all() or administrator in api_user.groups.all():
            try:
                org = Organization.objects.get(id=target_org_id)
            except Organization.DoesNotExist:
                return Response({"error": "That organization does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            users = User.objects.filter(profile__organization=org)
            serializer = ShortUserSerializer(users, many=True)
            return Response({"result": "Users retrieved successfully.", "User List": serializer.data})
        else:
            return Response({"result": "You are not authorized to perform this action."},
                            status=status.HTTP_400_BAD_REQUEST)

class GetOrganizationUser(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, target_org_id, target_account_id):
        """Retrieve user id and name if user is "Administrator" or "Viewer."
        """
        api_user = request.user
        viewer = Group.objects.get(name="Viewer")
        administrator = Group.objects.get(name="Administrator")
        if viewer in api_user.groups.all() or administrator in api_user.groups.all():
            try:
                org = Organization.objects.get(id=target_org_id)
            except Organization.DoesNotExist:
                return Response({"error": "That organization does not exist."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.filter(profile__organization=org).filter(id=target_account_id)
            except Exception as exc:
                return Response({"error": exc}, status=status.HTTP_400_BAD_REQUEST)
            serializer = ShortUserSerializer(user[0])
            return Response({"result": "User retrieved successfully.", "User Info": serializer.data})
        else:
            return Response({"result": "You are not authorized to perform this action."},
                            status=status.HTTP_400_BAD_REQUEST)


class GetAPIInfo(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Returns user_name, id, organization_name, public_ip.
        """
        try:
            api_user = request.user
            user_name = api_user.username
            id = api_user.id
            organization_name = api_user.profile.organization.name
            public_ip = get('https://api.ipify.org').text
        except Exception as exc:
            return Response({"error": exc}, status=status.HTTP_400_BAD_REQUEST)
        data = dict(user_name=user_name,
                    id=id,
                    organization_name=organization_name,
                    public_ip=public_ip)
        serializer = APIInfoSerializer(data=data)
        if serializer.is_valid():
            return Response({"result": "Data collected successfully.", "API Info": serializer.data})
        else:
            return Response({"error": serializer.errors})

class AuthGroups(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Returns authentication groups.
        """
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response({"result": "Groups collected successfully.", "Group Info": serializer.data})
