from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

import phone_books.contacts as core


async def homepage(request):
    return JSONResponse({"hello": "world 2"})

async def contacts_store(request):
    data = await request.json()
    assert isinstance(data, dict)
    assert "name" in data
    assert "phone" in data
    assert "email" in data

    contact = await core.create_contact(data)

    return JSONResponse(contact)



def make_app() -> Starlette:
    app = Starlette(
        debug=True,
        routes=[
            Route("/", homepage),
            Route("/contacts", contacts_store, methods=["POST"]),
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
