"""
Serializers for Recipe
"""
from rest_framework import serializers
from core.models import (
    Recipe,
    Tag
)

class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tags"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_field = ['id']

class TagDetailSerializer(TagSerializer):
    """Serializer of Tag detail view."""

    class Meta(TagSerializer.Meta):
        fields = TagSerializer.Meta.fields + ['description']

class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for Recipe"""
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minutes', 'price', 'link', 'tags']
        read_only_fields = ['id']

    def create(self, validated_data):
        """Create a recipe."""
        tags = validated_data.pop('tags', [])
        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(user=auth_user, **tag)
            recipe.tags.add(tag_obj)

class RecipeDetailSerializer(RecipeSerializer):
    """Serializer of recipe detail view."""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']






