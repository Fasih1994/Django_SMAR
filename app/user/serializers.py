"""
Serializers for the User API view
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
    )
from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.schemas.openapi import AutoSchema
from core.models import Organization, Package, UserRole

from smmart.serializers import (
    OrganizationSerializer, PackageSerializer, UserRoleSerializer
    )

PACKAGES = {
    'basic',
    'pro',
    'premium',
    '',
}
ROLES = {
    'admin',
    'user',
    '',
}


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user Object"""
    organization = OrganizationSerializer(required=True)
    package = PackageSerializer(required=False)
    role = UserRoleSerializer(required=False)

    class Meta:
        model = get_user_model()
        fields = [
            'email', 'password', 'name', 'organization', 'package', 'role'
            ]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}
        read_only_fields = ['package', 'role']

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        organization_data = validated_data.pop('organization', None)
        organization = Organization.objects.create(**organization_data)

        package = Package.objects.get(name='basic')
        role = UserRole.objects.get(name='admin')

        user = get_user_model().objects.create_user(
            organization=organization, package=package, role=role, **validated_data
        )

        return user

    def get_fields(self):
        fields = super().get_fields()

        fields['package'].read_only = True
        fields['role'].read_only = True

        return fields

    def update(self, instance, validated_data) -> get_user_model():
        """Update and return user"""

        if 'email' in validated_data:
            raise serializers.ValidationError("Email cannot be changed.")

        password = validated_data.pop('password', None)
        user = super().update(instance=instance, validated_data=validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['password', 'name']
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance=instance, validated_data=validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class AdminUserCreateSerializer(UserSerializer):
    organization = OrganizationSerializer(required=False)

    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        request_user = self.context['request'].user

        organization = request_user.organization
        package = request_user.package

        role_data = validated_data.pop('role')

        if role_data['name'] in ROLES:
            role, _ = UserRole.objects.get_or_create(name=role_data['name'])
        else:
            raise ValueError('Invalid Role Name')

        user = get_user_model().objects.create_user(
            organization=organization, package=package, role=role, **validated_data
        )

        return user

    def get_fields(self):
        fields = super().get_fields()

        fields['package'].read_only = True
        fields['role'].read_only = False
        fields['organization'].read_only = True

        return fields


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['role']

    def update(self, instance, validated_data):
        """Update and return non admin user"""

        role_data = validated_data.pop('role')

        if role_data['name'] in ROLES:
            role, _ = UserRole.objects.get_or_create(name=role_data['name'])
        else:
            raise ValueError('Invalid Role Name')

        user = super().update(instance=instance, role=role, validated_data=validated_data)

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
