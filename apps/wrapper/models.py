from django.db import models


class PokemonAbility(models.Model):
    """
    Model representing a Pokemon's ability.
    """

    ability = models.JSONField(default=list)
    slot = models.PositiveIntegerField(null=True)
    is_hidden = models.BooleanField(default=False)

    def __str__(self) -> str:
        return "Pokemon ability " + str(self.slot if self.slot else "")

    class Meta:
        verbose_name = "Pokemon ability"
        verbose_name_plural = "Pokemon abilities"


class PokemonSprite(models.Model):
    """
    Model representing a Pokemon's sprite.
    """

    back_default = models.URLField(null=True)
    back_female = models.URLField(null=True)
    back_shiny = models.URLField(null=True)
    back_shiny_female = models.URLField(null=True)
    front_default = models.URLField(null=True)
    front_female = models.URLField(null=True)
    front_shiny = models.URLField(null=True)
    front_shiny_female = models.URLField(null=True)
    other = models.JSONField(default=dict)
    versions = models.JSONField(default=dict)

    class Meta:
        verbose_name = "Pokemon sprite"
        verbose_name_plural = "Pokemon sprites"


class PokemonType(models.Model):
    """
    Model representing a Pokemon's type.
    """

    slot = models.PositiveIntegerField(null=True)
    type = models.JSONField(default=dict)

    def __str__(self) -> str:
        return "Pokemon type " + str(self.slot if self.slot else "")

    class Meta:
        verbose_name = "Pokemon type"
        verbose_name_plural = "Pokemon types"


class Pokemon(models.Model):
    """
    Model representing a Pokemon.
    """

    pokeapi_id = models.PositiveIntegerField(
        db_index=True, verbose_name="Pokedex ID"
    )
    name = models.CharField(max_length=255)
    abilities = models.ManyToManyField(PokemonAbility)
    sprites = models.ForeignKey(
        PokemonSprite, on_delete=models.CASCADE, null=True
    )
    types = models.ManyToManyField(PokemonType)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Pokemon"
        verbose_name_plural = "Pokemons"
