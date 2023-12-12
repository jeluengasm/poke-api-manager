from django.db import transaction
from rest_framework import serializers

from apps.wrapper import models


class PokemonListSerializer(serializers.Serializer):
    """
    Serializer for listing basic information about Pokemon.

    This serializer provides the Pokemon's name and ID
    which can be used for generating lists of Pokemon without
    the need for detailed information.
    """

    name = serializers.CharField(max_length=255)
    id = serializers.IntegerField()

    class Meta:
        fields = ("name", "id")


class PokemonAbilitySerializer(serializers.Serializer):
    """
    Serializer for listing basic information about Pokemon abilities.

    This serializer provides the ability's name, slot, and if it is hidden
    which can be used for generating lists of Pokemon abilities without
    the need for detailed information.
    """

    ability = serializers.JSONField()
    slot = serializers.IntegerField()
    is_hidden = serializers.BooleanField()

    class Meta:
        fields = ("ability", "slot", "is_hidden")


class PokemonAbilityUpdateSerializer(
    serializers.ModelSerializer, PokemonAbilitySerializer
):
    """
    Serializer for updating a Pokemon's ability.

    This serializer extends the `PokemonAbilitySerializer` to allow updates
    to the PokemonAbility model. It inherits fields and validation from
    the base class and links them to the model for database updates.
    """

    class Meta:
        model = models.PokemonAbility
        fields = ("ability", "slot", "is_hidden")


class PokemonSpriteSerializer(serializers.Serializer):
    """
    Serializer for detailed information about Pokemon sprites.

    This serializer handles the serialization of various Pokemon sprite images,
    including default, shiny, and female variations, as well as additional
    sprite information contained within 'other' and 'versions' fields.
    """

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
    """
    Serializer for updating a Pokemon's sprite.

    This serializer extends the `PokemonSpriteSerializer` to allow updates
    to the PokemonSprite model. It inherits fields and validation from
    the base class and links them to the model for database updates.
    """

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
    """
    Serializer for listing basic information about Pokemon types.

    This serializer provides the type's slot and type
    which can be used for generating lists of Pokemon types without
    the need for detailed information.
    """

    slot = serializers.IntegerField()
    type = serializers.JSONField()

    class Meta:
        fields = ("slot", "type")


class PokemonTypeUpdateSerializer(
    serializers.ModelSerializer, PokemonTypeSerializer
):
    """
    Serializer for updating a Pokemon's type.

    This serializer extends the `PokemonTypeSerializer` to allow updates
    to the PokemonType model. It inherits fields and validation from
    the base class and links them to the model for database updates.
    """

    class Meta:
        model = models.PokemonType
        fields = ("slot", "type")


class PokemonSerializer(serializers.Serializer):
    """
    Serializer for detailed information about Pokemon.

    This serializer handles the serialization of various Pokemon information,
    including basic information, abilities, sprites, and types.
    """

    id = serializers.IntegerField()
    name = serializers.CharField(max_length=255)
    abilities = PokemonAbilitySerializer(many=True)
    sprites = PokemonSpriteSerializer()
    types = PokemonTypeSerializer(many=True)

    class Meta:
        fields = ("id", "name", "abilities", "sprites", "types")


class PokemonUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="pokeapi_id")
    name = serializers.CharField(max_length=255)
    abilities = PokemonAbilityUpdateSerializer(many=True)
    sprites = PokemonSpriteUpdateSerializer()
    types = PokemonTypeUpdateSerializer(many=True)

    class Meta:
        model = models.Pokemon
        fields = ("id", "name", "abilities", "sprites", "types")

    @transaction.atomic
    def create(self, validated_data):
        """
        Creates a new Pokemon instance in the database.

        Args:
            validated_data (dict): A dictionary containing the validated data
            for creating a new Pokemon.
                - abilities (list): A list of dictionaries containing the data
                                    for the abilities of the Pokemon.
                - sprites (dict): A dictionary containing the data for the
                                  sprites of the Pokemon.
                - types (list): A list of dictionaries containing the data for
                                the types of the Pokemon.

        Returns:
            Pokemon: The newly created Pokemon instance.
        """
        abilities = validated_data.pop("abilities")
        sprites = validated_data.pop("sprites")
        types = validated_data.pop("types")
        pokemon = models.Pokemon.objects.create(**validated_data)
        for ability in abilities:
            ability_model = models.PokemonAbility.objects.create(**ability)
            pokemon.abilities.add(ability_model)
        for type in types:
            type_model = models.PokemonType.objects.create(**type)
            pokemon.types.add(type_model)
        sprite_model = models.PokemonSprite.objects.create(**sprites)
        pokemon.sprites = sprite_model
        pokemon.save()
        return pokemon

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Updates an instance of a Pokemon with the given validated data.

        Args:
            instance (Pokemon): The Pokemon instance to be updated.
            validated_data (dict): The validated data containing the updated
            values.

        Returns:
            Pokemon: The updated Pokemon instance.

        Raises:
            None
        """
        abilities = validated_data.pop("abilities")
        sprites = validated_data.pop("sprites")
        types = validated_data.pop("types")
        instance.abilities.all().delete()
        instance.types.all().delete()
        instance.sprites.delete()
        for ability in abilities:
            ability_model = models.PokemonAbility.objects.create(**ability)
            instance.abilities.add(ability_model)
        for type in types:
            type_model = models.PokemonType.objects.create(**type)
            instance.types.add(type_model)
        sprite_model = models.PokemonSprite.objects.create(**sprites)
        instance.sprites = sprite_model
        instance.save()
        return super().update(instance, validated_data)
