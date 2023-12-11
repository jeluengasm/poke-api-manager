from rest_framework import serializers

from apps.wrapper import models


class PokemonListSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    id = serializers.IntegerField()


class PokemonAbilitySerializer(serializers.Serializer):
    ability = serializers.JSONField()
    slot = serializers.IntegerField()
    is_hidden = serializers.BooleanField()

    class Meta:
        fields = ("ability", "slot", "is_hidden")


class PokemonAbilityUpdateSerializer(
    serializers.ModelSerializer, PokemonAbilitySerializer
):
    class Meta:
        model = models.PokemonAbility
        fields = ("ability", "slot", "is_hidden")


class PokemonSpriteSerializer(serializers.Serializer):
    back_default = serializers.CharField(max_length=255, allow_null=True)
    back_female = serializers.CharField(max_length=255, allow_null=True)
    back_shiny = serializers.CharField(max_length=255, allow_null=True)
    back_shiny_female = serializers.CharField(max_length=255, allow_null=True)
    front_default = serializers.CharField(max_length=255, allow_null=True)
    front_female = serializers.CharField(max_length=255, allow_null=True)
    front_shiny = serializers.CharField(max_length=255, allow_null=True)
    front_shiny_female = serializers.CharField(max_length=255, allow_null=True)
    other = serializers.JSONField()
    versions = serializers.JSONField()

    class Meta:
        fields = (
            "back_default",
            "back_female",
            "back_shiny",
            "back_shiny_female",
            "front_default",
            "front_female",
            "front_shiny",
            "front_shiny_female",
            "other",
            "versions",
        )


class PokemonSpriteUpdateSerializer(
    serializers.ModelSerializer, PokemonSpriteSerializer
):
    class Meta:
        model = models.PokemonSprite
        fields = (
            "back_default",
            "back_female",
            "back_shiny",
            "back_shiny_female",
            "front_default",
            "front_female",
            "front_shiny",
            "front_shiny_female",
            "other",
            "versions",
        )


class PokemonTypeSerializer(serializers.Serializer):
    slot = serializers.IntegerField()
    type = serializers.JSONField()

    class Meta:
        fields = ("slot", "type")


class PokemonTypeUpdateSerializer(
    serializers.ModelSerializer, PokemonTypeSerializer
):
    class Meta:
        model = models.PokemonType
        fields = ("slot", "type")


class PokemonSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    abilities = PokemonAbilitySerializer(many=True)
    sprites = PokemonSpriteSerializer()
    types = PokemonTypeSerializer(many=True)

    class Meta:
        fields = ("id", "name", "abilities", "sprites", "types")


class PokemonUpdateSerializer(serializers.ModelSerializer, PokemonSerializer):
    class Meta:
        model = models.Pokemon
        fields = ("name", "abilities", "sprites", "types")
