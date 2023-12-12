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
    """
    A viewset that provides default `list` and `retrieve` operations for
    Pokemon,as well as `create` and `update` operations. This viewset uses the
    `PokemonApiWrapper` for data retrieval and caching, and different serializers
    for the different actions.

    Inherits from:
    - `ReadOnlyModelViewSet` for list and retrieve actions
    - `UpdateModelMixin` for update action
    - `CreateModelMixin` for create action

    Attributes:
        queryset: The default queryset that includes all Pokemon objects.
        serializer_class: The default serializer class used for list operations.
        lookup_field: The field used to perform object lookup, which is `pokeapi_id`.

    The `get_serializer_class` method is overridden to use `PokemonSerializer`
    for retrieve, update, and partial_update actions, allowing for different
    serialization for those endpoints.
    """

    queryset = models.Pokemon.objects.all()
    serializer_class = serializers.PokemonListSerializer
    lookup_field = "pokeapi_id"

    def get_serializer_class(self):
        """
        Returns the appropriate serializer class based on the action.

        :param self: The object instance.
        :return: The serializer class.
        """
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
        """
        Retrieves a list of Pokemon based on the given query parameters.

        Parameters:
            - request: The HTTP request object.
            - args: Additional positional arguments.
            - kwargs: Additional keyword arguments.

        Returns:
            A list of Pokemon objects that match the given query parameters.
        """
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
        """
        Retrieve and return a specific Pokemon instance by pokeapi_id.

        Parameters:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response containing the serialized Pokemon data.

        Note:
            This function first attempts to retrieve the Pokemon instance from the queryset
            based on the provided pokeapi_id. If the instance is found, it is serialized and
            returned as an HTTP response. If the instance does not exist, the function creates
            an instance of `PokemonApiWrapper` using the given request and
            invokes its `retrieve` method with the pokeapi_id to get the Pokemon
            data from the external API.
        """
        try:
            instance = self.queryset.get(pokeapi_id=kwargs["pokeapi_id"])
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except models.Pokemon.DoesNotExist:
            pass
        wrapper = PokemonApiWrapper(request)
        return wrapper.retrieve(kwargs["pokeapi_id"])

    def update(self, request, *args, **kwargs):
        """
        Updates an existing object with the given request data.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The HTTP response object containing the updated data.

        Raises:
            serializers.ValidationError: If the serializer is not valid.
        """

        partial = kwargs.pop("partial", False)
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

        if getattr(instance, "_prefetched_objects_cache", None):
            # If "prefetch_related" has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)
