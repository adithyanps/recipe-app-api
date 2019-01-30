from rest_framework import serializers

from core.models import Tag,Ingredient

class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object """

    class Meta:
        model =Tag
        fields = ('id','name')
        read_only_Fields = ('id',)


class IngredientSerializer(serializers.ModelSerializer):
    """serialzer for an ingredient object"""

    class Meta:
        model = Ingredient
        fields = ('id','name')
        read_only_Fields = ('id',)
