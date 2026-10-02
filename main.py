from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .routes import router


# =========================================================
# SETTINGS
# =========================================================

settings = get_settings()


# =========================================================
# APPLICATION LIFESPAN
# =========================================================

@asynccontextmanager
async def lifespan(
    app: FastAPI,
):

    # Create required directories
    settings.panels_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    settings.exports_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    yield


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(

    title=(
        "ComicCraft - "
        "AI Comic Story Creator"
    ),

    description=(
        "Generate personalized "
        "five-panel comics using "
        "Gemini and AI image generation."
    ),

    version="1.0.0",

    lifespan=lifespan,
)


# =========================================================
# STATIC FILES
# =========================================================

app.mount(

    "/static",

    StaticFiles(
        directory=str(
            settings.static_dir
        )
    ),

    name="static",
)


# =========================================================
# ROUTES
# =========================================================

app.include_router(
    router
)