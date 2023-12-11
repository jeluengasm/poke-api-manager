from rest_framework import routers

from apps.wrapper.viewsets import PokemonViewSet

# Settings
api = routers.DefaultRouter()
api.trailing_slash = '/?'


api.register(r"pokemon", PokemonViewSet, basename="pokemon")
