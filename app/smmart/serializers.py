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
