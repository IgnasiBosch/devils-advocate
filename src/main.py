from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from src.config import get_settings
from src.db import Base, get_engine, NoResultFound
from src.routes import router


def get_app() -> FastAPI:
    Base.metadata.create_all(get_engine())
    app = FastAPI()
    app.include_router(router)

    return app


app = get_app()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def error_handling_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except PermissionError:
        return JSONResponse(
            content={"error": "Not allowed"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    except NoResultFound:
        return JSONResponse(
            content={"error": "Not found"},
            status_code=status.HTTP_404_NOT_FOUND,
        )
    except ValueError:
        return JSONResponse(
            content={"error": "Value error"},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    except Exception:
        if get_settings().debug:
            raise

        return JSONResponse(
            content={"error": "Something went wrong"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
