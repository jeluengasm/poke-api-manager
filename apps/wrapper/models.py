from django.db import models


class PokemonAbility(models.Model):
    """Pokemon ability. Stores the name, url, slot and if it is hidden

    Args:
        internal_id (int):

    Returns:
        _type_: _description_
    """

    ability = models.JSONField(default=list)
    slot = models.PositiveIntegerField(null=True)
    is_hidden = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Pokemon ability"
        verbose_name_plural = "Pokemon abilities"


class PokemonSprite(models.Model):
    back_default = models.URLField()
    back_female = models.URLField()
    back_shiny = models.URLField()
    back_shiny_female = models.URLField()
    front_default = models.URLField()
    front_female = models.URLField()
    front_shiny = models.URLField()
    front_shiny_female = models.URLField()
    other = models.JSONField(default=dict)
    versions = models.JSONField(default=dict)

    class Meta:
        verbose_name = "Pokemon sprite"
        verbose_name_plural = "Pokemon sprites"


class PokemonType(models.Model):
    slot = models.PositiveIntegerField(null=True)
    type = models.JSONField(default=dict)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Pokemon type"
        verbose_name_plural = "Pokemon types"


class Pokemon(models.Model):
    pokeapi_id = models.PositiveIntegerField(
        db_index=True, verbose_name="Pokedex ID"
    )
    name = models.CharField(max_length=255)
    abilities = models.ManyToManyField(PokemonAbility)
    sprites = models.ManyToManyField(PokemonSprite)
    types = models.ManyToManyField(PokemonType)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Pokemon"
        verbose_name_plural = "Pokemons"
