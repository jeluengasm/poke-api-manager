import re

import pytest


@pytest.mark.django_db(transaction=True)
class TestPokemonApiV1List:
    def test_pokemon_list(self, api_client):
        # Test that the list endpoint returns a list of pokemons
        response = api_client.get("/api/v1/pokemon/")
        assert response.status_code == 200
        assert response.data

        data = response.data
        assert data.get("count", 0) > 0
        assert data.get("next", None) is not None
        assert data.get("previous", None) is None
        assert data.get("results", None) is not None
        assert isinstance(data.get("results", None), list)
        assert isinstance(data.get("results", None)[0], dict)

        regex = r"api\/v1/pokemon\/\?offset=(\d+)&limit=(\d+)"
        matches = re.findall(regex, data["next"])
        assert len(matches) > 0
        assert matches[0][0] == "10"
        assert matches[0][1] == "10"

    def test_pokemon_list_pagination(self, api_client):
        # Test that the list endpoint returns a paginated list of pokemons
        regex = r"api\/v1/pokemon\/\?offset=(\d+)&limit=(\d+)"
        offset = 10
        limit = 10

        response = api_client.get(
            f"/api/v1/pokemon/?offset={offset}&limit={limit}"
        )

        assert response.status_code == 200
        assert response.data

        data = response.data
        assert data.get("count", 0) > 0
        assert data.get("next", None) is not None
        assert data.get("previous", None) is not None
        assert len(data.get("results", None)) == int(limit)

        matches = re.findall(regex, data["next"])
        assert len(matches) > 0
        assert matches[0][0] == "20"
        assert matches[0][1] == "10"

    def test_pokemon_last_page(self, api_client):
        """
        Test that the last page returns an empty list
        """
        response = api_client.get("/api/v1/pokemon/")

        offset = int(response.data.get("count"))
        limit = 10

        response = api_client.get(
            f"/api/v1/pokemon/?offset={offset}&limit={limit}"
        )

        assert response.status_code == 200
        assert response.data

        data = response.data

        assert data.get("count", 0) > 0
        assert data.get("next", None) is None
        assert data.get("previous", None) is not None
        assert len(data.get("results", None)) == 0

    def test_pokemon_filter_by_name(self, api_client):
        # Test the query parameter "name"
        name = "char"
        response = api_client.get(f"/api/v1/pokemon/?name={name}")

        assert response.status_code == 200
        assert response.data

        data = response.data

        assert data.get("count", 0) == 9
        assert data.get("next", None) is None
        assert data.get("previous", None) is None
        assert len(data.get("results", None)) == 9
        for pokemon in data.get("results", None):
            assert name in pokemon.get("name", None)

        name = "squaw"
        response = api_client.get(f"/api/v1/pokemon/?name={name}")

        assert response.status_code == 200
        assert response.data

        data = response.data

        assert data.get("count", 0) == 4
        assert data.get("next", None) is None
        assert data.get("previous", None) is None
        assert len(data.get("results", None)) == 4
        for pokemon in data.get("results", None):
            assert name in pokemon.get("name", None)

    def test_pokemon_filter_by_pokedex_id(self, api_client):
        # Test the query parameter "pokedex_id"
        pokedex_id = "1"
        response = api_client.get(f"/api/v1/pokemon/?pokedex_id={pokedex_id}")

        assert response.status_code == 200
        assert response.data

        data = response.data

        assert data.get("count", 0) == 1
        assert data.get("next", None) is None
        assert data.get("previous", None) is None
        assert len(data.get("results", None)) == 1
        results = data.get("results", None)
        assert pokedex_id in results[0].get("url", None)
        assert "bulbasaur" in results[0].get("name", None)


@pytest.mark.django_db(transaction=True)
class TestPokemonApiV1Retrieve:
    def test_pokemon_retrieve(self, api_client):
        pk = 1
        response = api_client.get(f"/api/v1/pokemon/{pk}/")
        assert response.status_code == 200
        assert response.data

        data = response.data

        assert isinstance(data, dict)
        assert isinstance(data.get("id", None), int)
        assert isinstance(data.get("name", None), str)
        assert isinstance(data.get("abilities", None), list)
        assert isinstance(data.get("sprites", None), dict)
        assert isinstance(data.get("types", None), list)
        assert data.get("name", None) == "bulbasaur"

    def test_modified_pokemon_retrieve(
        self, api_client, db_pokemon, pokemon_params
    ):
        print(db_pokemon)
        pk = 1
        response = api_client.get(f"/api/v1/pokemon/{pk}/")
        assert response.status_code == 200
        assert response.data

        data = response.data

        assert isinstance(data, dict)
        assert data.get("id", None) == 1
        assert data.get("name", None) == pokemon_params["name"]
        assert (
            data["abilities"][0]["ability"]["name"]
            == pokemon_params["abilities"][0]["ability"]["name"]
        )
