from rest_framework import serializers
from .models import Organization, Profile
from django.contrib.auth.models import User, Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class EmailTokenObtainSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD


class EmailTokenObtainPairSerializer(EmailTokenObtainSerializer):
    def get_tokens_for_user(user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class PatchUserUpdateSerializer(serializers.Serializer):
    """This serializer is for checking the input json/dict from the api_user when updating an account.
    """
    username = serializers.CharField(max_length=64, required=False)
    password = serializers.CharField(max_length=255, required=False)
    email = serializers.CharField(max_length=255, required=False)
    first_name = serializers.CharField(max_length=64, required=False)
    last_name = serializers.CharField(max_length=64, required=False)


class PatchOrgUpdateSerializer(serializers.Serializer):
    """This serializer is for checking the input json/dict from the api_user when updating an organization.
    """
    name = serializers.CharField(max_length=50, required=False)
    phone = serializers.CharField(max_length=20, required=False)
    address = serializers.CharField(max_length=255, required=False)


class ShortUserSerializer(serializers.ModelSerializer):
    """This serializer is for the organization/<int:target_org_id>/users/' endpoint to only show the name and ID of
    the user.
    """

    class Meta:
        model = User
        fields = ['id', 'username']


class OrganizationSerializer(serializers.ModelSerializer):
    """This serializes a complete Organization object.
    """

    class Meta:
        model = Organization
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """This serializes a django user object.
    """

    class Meta:
        model = User
        exclude = ['password', 'is_staff', 'is_active', 'user_permissions', 'is_superuser']


class ProfileSerializer(serializers.ModelSerializer):
    """This serializes a profile object with limited fields for security reasons.
    """
    user = UserSerializer(User)

    class Meta:
        model = Profile
        fields = ('id', 'name', 'phone', 'email', 'birthdate', 'user')


class APIInfoSerializer(serializers.Serializer):
    """This serializer is for the API info endpoint.
    """
    user_name = serializers.CharField()
    id = serializers.IntegerField()
    organization_name = serializers.CharField()
    public_ip = serializers.CharField()


class GroupSerializer(serializers.ModelSerializer):
    """This serializer serializes an Auth Group.
    """

    class Meta:
        model = Group
        fields = '__all__'
