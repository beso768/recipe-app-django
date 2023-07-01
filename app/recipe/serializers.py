"""Serializer for recipe objects"""

from rest_framework import serializers
from core.models import Recipe, Tag, Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag objects"""

    class Meta:
        model = Tag
        fields = ("id", "name")
        read_only_fields = ("id",)


class IngredientSerializer(serializers.ModelSerializer):
    """Serializer for ingredient objects"""

    class Meta:
        model = Ingredient
        fields = ("id", "name")
        read_only_fields = ("id",)


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipe objects"""

    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ("id", "title", "time_minutes", "price", "link", "tags", "ingredients")
        read_only_fields = ("id",)

    def create(self, validated_data):
        """Create a recipe"""
        tags = validated_data.pop("tags", [])
        ingredients = validated_data.pop("ingredients", None)

        recipe = Recipe.objects.create(**validated_data)
        auth_user = self.context["request"].user
        if ingredients is not None:
            for ingredient in ingredients:
                ingredient_obj, created = Ingredient.objects.get_or_create(
                    user=auth_user, **ingredient
                )
                recipe.ingredients.add(ingredient_obj)

        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(user=auth_user, **tag)
            recipe.tags.add(tag_obj)
        return recipe

    def update(self, instance, validated_data):
        """Update a recipe"""
        tags = validated_data.pop("tags", [])
        ingredients = validated_data.pop("ingredients", None)
        recipe = super().update(instance, validated_data)
        recipe.tags.clear()
        auth_user = self.context["request"].user

        if ingredients is not None:
            recipe.ingredients.clear()
            for ingredient in ingredients:
                ingredient_obj, created = Ingredient.objects.get_or_create(
                    user=auth_user, **ingredient
                )
                recipe.ingredients.add(ingredient_obj)

        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(user=auth_user, **tag)
            recipe.tags.add(tag_obj)
        return recipe


class RecipeDetailSerializer(RecipeSerializer):
    """Serializer for recipe detail objects"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ("description",)
