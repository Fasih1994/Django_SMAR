from rest_framework import serializers, status
from django.utils import timezone
from rest_framework.response import Response
from core.models import (
    Organization,
    Package,
    UserRole,
    Topics,
    PackageStatus
)
from django.contrib.auth import get_user_model



class OrganizationSerializer(serializers.ModelSerializer):
    """Serializer for organization Object"""

    user = 'user.serializers.UserSerializer'

    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'description', 'linkedin_profile',
            'facebook_profile', 'instagram_profile',
            'industry', 'creation_date', 'created_by',
            'last_update_date', 'last_updated_by', 'last_update_login']

        read_only_fields = ['id', 'creation_date', 'created_by']

    def update(self, instance, validated_data):
        """Update and return an organization instance"""
        user = self.context['request'].user

        if 'name' in validated_data:
            raise serializers.ValidationError("Name cannot be updated.")

        instance.id = user.organization_id
        instance.description = validated_data.get(
            'description', instance.description
            )
        instance.linkedin_profile = validated_data.get(
            'linkedin_profile', instance.linkedin_profile
            )
        instance.facebook_profile = validated_data.get(
            'facebook_profile', instance.facebook_profile
            )
        instance.instagram_profile = validated_data.get(
            'instagram_profile', instance.instagram_profile
            )
        instance.industry = validated_data.get(
            'industry', instance.industry
            )
        instance.created_by = user.id
        instance.last_updated_by = user.id

        instance.save()

        return instance


class PackageSerializer(serializers.ModelSerializer):
    """Serializer for Package Object"""
    class Meta:
        model = Package
        fields = [
            'id', 'name', 'price', 'creation_date', 'created_by',
            'last_update_date', 'last_updated_by', 'last_update_login'
            ]

        read_only_fields = [
            'id', 'creation_date', 'created_by',
            'price', 'last_updated_by', 'last_update_login'
            ]


class UserRoleSerializer(serializers.ModelSerializer):
    """Serializer for UserRole Object"""
    class Meta:
        model = UserRole
        fields = [
            'id', 'name', 'creation_date', 'created_by',
            'last_update_date', 'last_updated_by', 'last_update_login'
            ]

        read_only_fields = ['id', 'creation_date', 'created_by']


class TopicSerializer(serializers.Serializer):
    """Serializer for Topics Object"""

    user = 'user.serializers.UserSerializer'

    user_id = serializers.IntegerField(required=False)
    topic_id = serializers.IntegerField(required=False)
    name = serializers.CharField(max_length=255, required=False)
    prompt = serializers.CharField(max_length=255, required=False)
    keywords = serializers.ListField()
    platform = serializers.ListField()
    status = serializers.CharField(max_length=1, required=False)

    def create(self, validated_data):
        """Create and return a topic"""
        user_id = self.context['request'].user
        name = validated_data.pop('name', 'Untitled')
        prompt = validated_data.pop('prompt', '')
        keywords = validated_data.pop('keywords', [])
        platform = validated_data.pop('platform', [])
        status = validated_data.pop('status', 't')

        keyword = ",".join(keywords)
        platforms = ",".join(platform)

        topic = Topics.objects.create(
            user=user_id,
            name=name,
            prompt=prompt,
            keywords=keyword,
            platform=platforms,
            status=status,
            **validated_data
        )

        return topic

    def to_representation(self, instance):
        """Include topic_id in the serialized representation"""
        representation = super().to_representation(instance)
        representation['topic_id'] = instance.id
        representation['platform'] = instance.platform.split(",")
        representation['keywords'] = instance.keywords.split(",")

        return representation

    def update(self, instance, validated_data):
        """Update and return the topic"""
        instance.name = validated_data.get('name', instance.name)
        instance.prompt = validated_data.get('prompt', instance.prompt)
        keywords = validated_data.get('keywords', instance.keywords)
        platform = validated_data.get('platform', instance.platform)
        instance.status = validated_data.get('status', instance.status)

        instance.keywords = ",".join(keywords)
        instance.platform = ",".join(platform)

        instance.save()

        return instance


class GetDataSerializer(serializers.Serializer):
    """Serializer for GetData API"""
    user_id = serializers.IntegerField()
    organization_id = serializers.IntegerField()
    topic_id = serializers.IntegerField(required=False)
    keywords = serializers.ListField()
    platforms = serializers.ListField()

    def validate(self, data):
        topic_id = data.get('topic_id')

        if not topic_id:
            topic_data = {
                'name': '',
                'prompt': '',
                'keywords': data.get('keywords', ''),
                'platform': data.get('platforms', ''),
                'status': '',
                'user': data.get('user_id'),
            }
            topic_serializer = TopicSerializer(data=topic_data)
            topic_serializer.is_valid(raise_exception=True)
            data['topic'] = topic_serializer.save()

        return data


class PackageStatusSerializer(serializers.ModelSerializer):
    """Serializer for PackageStatus Object"""

    class Meta:
        model = PackageStatus
        fields = [
            'id', 'organization', 'package', 'start_date', 'end_date', 'status', 'created_by',
            'last_update_date', 'last_updated_by', 'last_update_login'
        ]

        read_only_fields = ['id', 'creation_date', 'created_by']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation