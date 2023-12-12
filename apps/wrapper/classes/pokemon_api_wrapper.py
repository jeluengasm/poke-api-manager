import re

from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response

from apps.wrapper.classes.list_paginator import ListPaginator
from apps.wrapper.classes.pokemon_api import PokemonApi
from apps.wrapper.serializers import PokemonSerializer


class PokemonApiWrapper(ListPaginator):
    """
    A class that wraps the `PokemonApi` class and provides additional
    functionality
    """

    def __init__(self, request: Request) -> None:
        """
        Initializes the object with the given request.

        Args:
            request (Request): The request object used to build the base URI.

        Returns:
            None
        """
        self._pokemon_list = []
        self._count = 0
        self._pokemon_api = PokemonApi()
        self.base_uri = "{}api/v1/".format(request.build_absolute_uri("/"))
        super().__init__(request)

    @property
    def pokemon_list(self) -> list:  # pylint: disable=used-before-assignment
        """
        Returns the list of pokemons.

        Returns:
            list: The list of pokemons.
        """
        return self._pokemon_list

    @pokemon_list.setter
    def pokemon_list(self, value: list) -> None:
        """
        Sets the list of pokemons.

        Args:
            value (list): The list of pokemons.
        """
        self._pokemon_list = value

    @property
    def count(self) -> int:
        """
        Returns the count of pokemons.

        Returns:
            int: The count of pokemons.
        """
        return self._count

    @count.setter
    def count(self, value: int) -> None:
        """
        Sets the count of pokemons.

        Args:
            value (int): The count of pokemons.
        """
        self._count = value

    def pokemon_api_list(
        self,
        limit: int = settings.REST_FRAMEWORK["PAGE_SIZE"],
        offset: int = 0,
    ) -> list:
        """
        Returns the list of pokemons from the `PokemonApi` class.

        Args:
            limit (int): The maximum number of pokemons to return.
            offset (int): The number of pokemons to skip.

        Returns:
            list: The list of pokemons.
        """
        return self._pokemon_api.get_pokemon_list(limit, offset)

    def filter_pokemons(self, **kwargs) -> None:
        """
        Filters the list of pokemons based on the given query parameters.

        Args:
            kwargs (dict): The query parameters.
        """
        if kwargs.get("name", None):
            self._pokemon_list = [
                pokemon
                for pokemon in self._pokemon_list
                if kwargs["name"] in pokemon["name"]
            ]
        if kwargs.get("pokedex_id", None):
            regex = r"\/(\d+)\/"
            self._pokemon_list = [
                pokemon
                for pokemon in self._pokemon_list
                if kwargs["pokedex_id"] == re.findall(regex, pokemon["url"])[0]
            ]

    def replace_urls(self):
        """
        Replaces the base URI in the list of pokemons with the base URI of the
        PokemonApiWrapper class.
        """
        for index, pokemon in enumerate(self._pokemon_list):
            self._pokemon_list[index]["url"] = re.sub(
                rf"{self._pokemon_api.BASE_URI}",
                f"{self.base_uri}",
                pokemon["url"],
            )

    def list(self, query_params, limit, offset):
        """
        Retrieves a list of pokemons based on the given query parameters and
        pagination settings.

        Args:
            query_params (dict): A dictionary containing the query parameters
                                 for filtering the pokemons. The supported
                                 parameters are 'name'and 'pokedex_id'.
            limit (int): The maximum number of pokemons to retrieve.
            offset (int): The starting index of the retrieved pokemons.

        Returns:
            Response: The paginated list of pokemons matching the query
            parameters.
        """

        response = self.pokemon_api_list()
        self.count = response.get("count", 0)
        self.pokemon_list = self.pokemon_api_list(limit=self.count).get(
            "results", []
        )
        if "name" in query_params or "pokedex_id" in query_params:
            self.filter_pokemons(**query_params)
        self.replace_urls()
        return Response(
            data=self.paginate_list(self.pokemon_list, limit, offset),
            status=status.HTTP_200_OK,
        )

    def retrieve(self, pk):
        """
        Retrieves a Pokemon by its ID.

        Parameters:
            pk (int): The ID of the Pokemon to retrieve.

        Returns:
            Response: The response object containing the Pokemon data if found,
                      or a 404 Not Found response if the Pokemon does not exist.
        """

        response = self._pokemon_api.get_pokemon_by_id(pk)
        if response:
            serializer = PokemonSerializer(response)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)
