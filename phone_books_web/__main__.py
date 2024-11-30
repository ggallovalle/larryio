import contextlib
from typing import Any, AsyncIterator, TypedDict

from psycopg import AsyncRawCursor
from psycopg_pool import AsyncConnectionPool
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from phone_books.db_schema import MIGRATION

import phone_books.contacts as core
from phone_books_web import settings
import json

def default_to_str(obj):
    print(f"obj: {obj}")
    print(f"type(obj): {type(obj)}")
    return obj

class OrjsonResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        str_content =  json.dumps(content, default=str)
        return str_content.encode("utf-8")

JSONResponse = OrjsonResponse

async def homepage(request: Request) -> Response:
    return JSONResponse({"hello": "world 2"})


async def contacts_index(request: Request) -> Response:
    name = request.query_params.get("filter[name]")
    phone = request.query_params.get("filter[phone]")
    email = request.query_params.get("filter[email]")

    pg_pool = State.get_pg_pool(request)

    async with pg_pool.connection() as pg_conn:
        contacts = await core.get_all_contacts(name=name, phone=phone, email=email, conn=pg_conn)

    return JSONResponse(contacts)


async def contacts_store(request: Request) -> Response:
    data = await request.json()
    assert "name" in data
    assert "phone" in data
    assert "email" in data
    pg_pool = State.get_pg_pool(request)

    async with pg_pool.connection() as pg_conn:
        contact = await core.create_contact(data, conn=pg_conn)

    return JSONResponse(contact)


async def contacts_show(request: Request) -> Response:
    ref = request.path_params["id"]

    pg_pool = State.get_pg_pool(request)

    async with pg_pool.connection() as pg_conn:
        contact = await core.get_contact_by_id(ref, conn=pg_conn)

    return JSONResponse(contact)


async def contacts_update(request: Request) -> Response:
    ref = request.path_params["id"]
    data = await request.json()
    assert isinstance(data, dict)

    pg_pool = State.get_pg_pool(request)

    async with pg_pool.connection() as pg_conn:
        contact = await core.update_contact(ref, data, conn=pg_conn)

    return JSONResponse(contact)


async def contacts_delete(request: Request) -> Response:
    ref = request.path_params["id"]

    pg_pool = State.get_pg_pool(request)

    async with pg_pool.connection() as pg_conn:
        deleted = await core.delete_contact(ref, conn=pg_conn)

    if not deleted:
        return JSONResponse({"message": "Contact not found"}, status_code=404)

    return JSONResponse({"message": "Contact deleted"})


class State(TypedDict):
    pg_pool: AsyncConnectionPool

    @staticmethod
    def get_pg_pool(request: Request) -> AsyncConnectionPool:
        return request.state.pg_pool


def make_app_lifespan(config: settings.Config):
    @contextlib.asynccontextmanager
    async def app_lifespan(app: Starlette) -> AsyncIterator[State]:
        async with AsyncConnectionPool(config.postgres_url, kwargs={"cursor_factory": AsyncRawCursor}) as pool:
            async with pool.connection() as conn:
                await MIGRATION.up(conn)
            yield State(pg_pool=pool)
            async with pool.connection() as conn:
                await MIGRATION.down(conn)

    return app_lifespan


def make_app(config: settings.Config | None = None) -> Starlette:
    if config is None:
        config = settings.Config.from_dotenv(verbose=True)

    app = Starlette(
        debug=config.debug,
        lifespan=make_app_lifespan(config),
        routes=[
            Route("/", homepage),
            Route("/contacts", contacts_index, methods=["GET"]),
            Route("/contacts", contacts_store, methods=["POST"]),
            Route("/contacts/{id}", contacts_show, methods=["GET"]),
            Route("/contacts/{id}", contacts_update, methods=["PATCH"]),
            Route("/contacts/{id}", contacts_delete, methods=["DELETE"]),
        ],
    )
    return app


def main():
    import uvicorn

    uvicorn.run(
        "phone_books_web.__main__:make_app",
        factory=True,
        port=5000,
        reload=True,
        reload_dirs=["phone_books_web", "phone_books"],
        reload_includes=[".env"]
    )


if __name__ == "__main__":
    main()
