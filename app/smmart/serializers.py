from rest_framework import serializers

from core.models import (
    Organization,
    Package,
    UserRole)


class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for organization Object"""
    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'description', 'linkedin_profile',
            'industry', 'creation_date', 'created_by',
            'last_update_date', 'last_updated_by', 'last_update_login']

        read_only_fields = ['id', 'creation_date', 'created_by']


class PackageSerializer(serializers.ModelSerializer):
    """Serializer for Package Object"""
    class Meta:
        model = Package
        fields = ['id', 'name', 'price', 'creation_date', 'created_by',
            'last_update_date', 'last_updated_by', 'last_update_login']

        read_only_fields = ['id', 'creation_date', 'created_by']


class UserRoleSerializer(serializers.ModelSerializer):
    """Serializer for UserRole Object"""
    class Meta:
        model = UserRole
        fields = ['id', 'name', 'creation_date', 'created_by',
            'last_update_date', 'last_updated_by', 'last_update_login']

        read_only_fields = ['id', 'creation_date', 'created_by']
