from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


async def homepage(request):
    return JSONResponse({"hello": "world 2"})


def make_app() -> Starlette:
    app = Starlette(
        debug=True,
        routes=[
            Route("/", homepage),
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
