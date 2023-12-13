"""
Serializers for the User API view
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
    )
from django.utils.translation import gettext as _

from rest_framework import serializers
from core.models import Organization

from smmart.serializers import (
    OrganizationSerializer, PackageSerializer, UserRoleSerializer
    )


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user Object"""
    organization = OrganizationSerializer(read_only=True)
    package = PackageSerializer(read_only=True)
    role = UserRoleSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = [
            'email', 'password', 'name', 'organization', 'package', 'role'
            ]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data) -> get_user_model():
        """Create and return a user with encrypted password"""
        organization_data = validated_data.pop('organization')
        organization = Organization.objects.create(**organization_data)
        user = get_user_model().objects.create_user(
            organization=organization, **validated_data
            )
        return user

    def update(self, instance, validated_data) -> get_user_model():
        """Update and return user"""
        password = validated_data.pop('password', None)
        user = super().update(instance=instance, validated_data=validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user Auth Token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        '''validate and authenticate user'''
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _("Unable to authenticate with provided credentials!")
            raise serializers.ValidationError(msg, code='authorization')
        attrs['user'] = user
        return attrs
