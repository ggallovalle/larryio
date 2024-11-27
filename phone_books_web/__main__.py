from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
from starlette.responses import Response


import phone_books.contacts as core


async def homepage(request: Request) -> Response:
    return JSONResponse({"hello": "world 2"})


async def contacts_index(request: Request) -> Response:
    name = request.query_params.get("filter[name]")
    phone = request.query_params.get("filter[phone]")
    email = request.query_params.get("filter[email]")

    contacts = await core.get_all_contacts(name=name, phone=phone, email=email)

    return JSONResponse(contacts)


async def contacts_store(request: Request) -> Response:
    data = await request.json()
    assert isinstance(data, dict)
    assert "name" in data
    assert "phone" in data
    assert "email" in data

    contact = await core.create_contact(data)

    return JSONResponse(contact)


async def contacts_show(request: Request) -> Response:
    ref = request.path_params["id"]

    contact = await core.get_contact_by_id(ref)

    return JSONResponse(contact)


async def contacts_update(request: Request) -> Response:
    ref = request.path_params["id"]
    data = await request.json()
    assert isinstance(data, dict)

    contact = await core.update_contact(ref, data)

    return JSONResponse(contact)


async def contacts_delete(request: Request) -> Response:
    ref = request.path_params["id"]

    deleted = await core.delete_contact(ref)

    if not deleted:
        return JSONResponse({"message": "Contact not found"}, status_code=404)

    return JSONResponse({"message": "Contact deleted"})


def make_app() -> Starlette:
    app = Starlette(
        debug=True,
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
    )


if __name__ == "__main__":
    main()
