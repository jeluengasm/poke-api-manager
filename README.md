# poke-api-manager
Simple API using Django REST Framework, based on public API PokéAPI.

### Create .env file from .env.dev

Create `.env` file from `.env.dev` and edit it.

```sh
cp .env.dev .env
```

### Run docker compose

If is the first time running the container, run the following command

```sh
docker compose up -d --build
```

Otherwise, run the following command

```sh
docker compose up -d
```

### Check containers logs

To check containers logs, run the following command

```sh
docker compose logs
```

### Linters and formatters

#### Black

To format code, run the following command

```sh
docker compose exec backend-pokeapi black <path/of/file>
```

#### Isort

To sort imports, run the following command

```sh
docker compose exec backend-pokeapi isort <path/of/file>
```

#### Flake8

To check code style, run the following command

```sh
docker compose exec backend-pokeapi flake8 <path/of/file>
```

### Run tests

To run tests, run the following command

```sh
docker compose exec backend-pokeapi pytest
```

### Run migrations

At the first time running the container, Python installs all migrations. However, if you want to run migrations, run the following command

```sh
docker compose exec backend-pokeapi python manage.py migrate
```

### Swagger UI

To open Swagger UI, open {{ base_url }}/api/v1/docs

### Open API 3 schema

To open Open API schema, open {{ base_url }}/api/v1/schema

### Dev container

To open dev container, Reopen the project in the dev container using Visual Studio Code

### Pre-commit hooks

To install pre-commit hooks, run the following command

```sh
pre-commit install
```

Once the hooks are installed, when you commit changes, the pre-commit hooks will run automatically.

NOTES:

- Pre-commit hooks are not installed by default.
- If you don't use Dev container, you must use a Python environment with pre-commit installed.
- Pre-commit hooks are installed inside the Dev container.
