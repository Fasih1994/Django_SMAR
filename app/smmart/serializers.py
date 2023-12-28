from rest_framework import serializers

from core.models import (
    Organization,
    Package,
    UserRole,
    Topics
)


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


class TopicSerializer(serializers.ModelSerializer):
    """Serializer for Topics Object"""
    user = 'user.serializers.UserSerializer'
    print(user)
    class Meta:
        model = Topics
        fields = [
            'id', 'name', 'prompt', 'keywords', 'platform', 'status', 'user',
            'creation_date', 'created_by', 'last_update_date',
            'last_updated_by', 'last_update_login']

        read_only_fields = ['id', 'creation_date', 'created_by']

    def create(self, validated_data):
        """Create and return a topic"""
        user_id = self.context['request'].user
        name = validated_data.pop('name', 'Untitled')
        prompt = validated_data.pop('prompt', '')
        keywords = validated_data.pop('keywords', '')
        platform = validated_data.pop('platform', '')
        status = validated_data.pop('status', 't')

        topic = Topics.objects.create(
            user=user_id,
            name=name,
            prompt=prompt,
            keywords=keywords,
            platform=platform,
            status=status,
            **validated_data
        )

        return topic
