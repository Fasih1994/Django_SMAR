"""
Serializers for the User API view
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
    )
from django.utils.translation import gettext as _

from rest_framework import serializers

from core.models import Organization, Package, PackageStatus, UserRole


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for organization Object"""
    class Meta:
        model = Organization
        fields = ['organization_id', 'organization_name', 'description',
                  'linkedin_profile', 'industry', 'creation_date',
                  'created_by', 'last_update_date', 'last_updated_by',
                  'last_update_login']
        read_only_fields = ['organization_id', 'creation_date', 'created_by']


class PackageSerializer(serializers.ModelSerializer):
    """Serializer for Package Object"""
    class Meta:
        model = Package
        fields = ['package_id', 'package_name', 'package_price',
                  'creation_date', 'created_by', 'last_update_date',
                  'last_updated_by', 'last_update_login']
        read_only_fields = ['package_id', 'creation_date', 'created_by']


class PackageStatusSerializer(serializers.ModelSerializer):
    """Serializer for PackageStatus Object"""
    class Meta:
        model = PackageStatus
        fields = ['organization_id', 'package_id', 'package_status',
                  'package_start_date', 'package_end_date', 'creation_date',
                  'created_by', 'last_update_date', 'last_updated_by',
                  'last_update_login']
        read_only_fields = ['creation_date', 'created_by']


class UserRoleSerializer(serializers.ModelSerializer):
    """Serializer for UserRole Object"""
    class Meta:
        model = UserRole
        fields = ['user_role_id', 'user_role_name', 'creation_date',
                  'created_by', 'last_update_date',
                  'last_updated_by', 'last_update_login']
        read_only_fields = ['user_role_id', 'creation_date', 'created_by']


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user Object"""
    # organization_id = OrganizationSerializer(read_only=True)
    # package_id = PackageSerializer(read_only=True)
    # user_role_id = UserRoleSerializer(read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        # , 'user_role_id', 'organization_id', 'package_id']
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data) -> get_user_model():
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data)

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
