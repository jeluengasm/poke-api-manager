import requests


class PokemonApi:
    _BASE_URI = "https://pokeapi.co/api/v2/"
    _pokemon_list: list = []

    @property
    def BASE_URI(self):
        return self._BASE_URI

    def get_pokemon_list(self, limit: int, offset: int) -> list:
        endpoint = f"{self.BASE_URI}pokemon?limit={limit}&offset={offset}"
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        return []

    def get_pokemon_by_id(self, pokeapi_id: int) -> dict:
        endpoint = f"{self.BASE_URI}pokemon/{pokeapi_id}"
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        return {}
