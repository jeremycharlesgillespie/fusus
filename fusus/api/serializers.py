from rest_framework import serializers
from .models import Organization, Profile
from django.contrib.auth.models import User
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
    """This serializes a profile object.
    """
    user = UserSerializer(User)

    class Meta:
        model = Profile
        fields = ('id', 'name', 'phone', 'email', 'birthdate', 'user')


class GetUserByIDSerializer(serializers.Serializer):
    """This is for the 'users/<int:id>' endpoint.
    """
    organization = OrganizationSerializer(required=True)
    user = UserSerializer(required=True)


