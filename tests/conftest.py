from typing import AsyncIterator

import pytest
import pytest_asyncio
from psycopg import AsyncConnection, AsyncRawCursor
from psycopg_pool import AsyncConnectionPool
from uvicorn import importer

from phone_books_web.settings import Config


def pytest_addoption(
    parser: pytest.Parser, pluginmanager: pytest.PytestPluginManager
) -> None:
    parser.addini(
        "app_dotenv",
        help="file to read for environment variables",
        default=".env.test",
    )
    parser.addini(
        "app_migration_file",
        type="string",
        help="Python import string to migration package.module:element",
        default=None,
    )


@pytest.fixture(scope="session")
def app_dotenv(pytestconfig: pytest.Config) -> dict:
    source = pytestconfig.getini("app_dotenv")
    import dotenv

    env = dotenv.dotenv_values(source)
    return env


@pytest.fixture(scope="session")
def app_config(app_dotenv: dict) -> Config:
    config = Config.from_dotenv(source=app_dotenv)
    return config


@pytest_asyncio.fixture(scope="session")
async def pg_pool(
    app_dotenv: dict,
) -> AsyncIterator[AsyncConnectionPool]:
    async with AsyncConnectionPool(
        app_dotenv["POSTGRES_URL"], kwargs={"cursor_factory": AsyncRawCursor}, timeout=3
    ) as pool:
        yield pool


@pytest_asyncio.fixture
async def pg_conn(
    pytestconfig: pytest.Config, pg_pool: AsyncConnectionPool
) -> AsyncIterator[AsyncConnection]:
    async with pg_pool.connection() as conn:
        migration_python_import_string = pytestconfig.getini("app_migration_file")
        if migration_python_import_string:
            migration = importer.import_from_string(migration_python_import_string)
            await migration.up(conn)
            yield conn
            await migration.down(conn)
        else:
            yield conn
