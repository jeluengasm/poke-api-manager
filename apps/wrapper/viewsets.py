from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from wrapper.classes.pokemon_api_wrapper import PokemonApiWrapper

from apps.wrapper import models, serializers


@extend_schema(operation_id="pokemon")
class PokemonViewSet(
    viewsets.ReadOnlyModelViewSet,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
):
    queryset = models.Pokemon.objects.all()
    serializer_class = serializers.PokemonListSerializer
    lookup_field = "pokeapi_id"

    def get_serializer_class(self):
        if self.action in ("retrieve", "update", "partial_update"):
            return serializers.PokemonSerializer
        return self.serializer_class

    @extend_schema(
        parameters=[
            OpenApiParameter("name", OpenApiTypes.STR, OpenApiParameter.QUERY),
            OpenApiParameter(
                "pokedex_id", OpenApiTypes.INT, OpenApiParameter.QUERY
            ),
        ]
    )
    @method_decorator(cache_page(60 * 60 * 24))  # 1 day
    @method_decorator(vary_on_cookie)
    def list(self, request, *args, **kwargs):
        limit = int(
            request.query_params.get(
                "limit", settings.REST_FRAMEWORK["PAGE_SIZE"]
            )
        )
        offset = int(request.query_params.get("offset", 0))
        name = request.query_params.get("name", None)
        pokedex_id = request.query_params.get("pokedex_id", None)
        query_params = {"name": name, "pokedex_id": pokedex_id}
        wrapper = PokemonApiWrapper(request)
        return wrapper.list(query_params, limit, offset)

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.queryset.get(pokeapi_id=kwargs["pokeapi_id"])
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except models.Pokemon.DoesNotExist:
            pass
        wrapper = PokemonApiWrapper(request)
        return wrapper.retrieve(kwargs["pokeapi_id"])

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        try:
            instance = self.queryset.get(pokeapi_id=kwargs["pokeapi_id"])
        except models.Pokemon.DoesNotExist:
            return self.create(request, *args, **kwargs)
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
