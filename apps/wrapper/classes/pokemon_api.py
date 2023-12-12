import requests


class PokemonApi:
    """
    A class that provides access to the Pokemon API.
    """

    _BASE_URI = "https://pokeapi.co/api/v2/"
    _pokemon_list: list = []

    @property
    def BASE_URI(self):  # pylint: disable=invalid-name
        """
        Gets the base URI of the object.

        Returns:
            str: The base URI of the object.
        """

        return self._BASE_URI

    def get_pokemon_list(self, limit: int, offset: int) -> list:
        """
        Retrieves a list of Pokemon from the API.

        Args:
            limit (int): The maximum number of Pokemon to retrieve.
            offset (int): The starting position of the Pokemon list.

        Returns:
            list: A list of Pokemon objects retrieved from the API.
        """

        endpoint = f"{self.BASE_URI}pokemon?limit={limit}&offset={offset}"
        response = requests.get(endpoint, timeout=10)
        if response.status_code == 200:
            return response.json()
        return []

    def get_pokemon_by_id(self, pokeapi_id: int) -> dict:
        """
        Retrieves a Pokemon from the PokeAPI based on its ID.

        Args:
            pokeapi_id (int): The ID of the Pokemon to retrieve.

        Returns:
            dict: A dictionary containing information about the Pokemon. If the
                  Pokemon does not exist, an empty dictionary is returned.
        """

        endpoint = f"{self.BASE_URI}pokemon/{pokeapi_id}"
        response = requests.get(endpoint, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {}
