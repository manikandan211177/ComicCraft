from __future__ import annotations

from fastapi import (
    APIRouter,
    Form,
    HTTPException,
    Request,
)

from fastapi.responses import (
    HTMLResponse,
    JSONResponse,
)

from fastapi.templating import (
    Jinja2Templates,
)

from .config import get_settings
from .image_generator import test_image
from .models import (
    ComicRequest,
    ComicResponse,
)
from .services import generate_comic


# =========================================================
# ROUTER
# =========================================================

router = APIRouter()


# =========================================================
# SETTINGS
# =========================================================

settings = get_settings()


# =========================================================
# JINJA2
# =========================================================

templates = Jinja2Templates(
    directory=str(
        settings.templates_dir
    )
)


# =========================================================
# HOME
# =========================================================

@router.get(
    "/",
    response_class=HTMLResponse,
)
async def home(
    request: Request,
):

    return templates.TemplateResponse(
        request=request,

        name="index.html",

        context={
            "demo_mode":
                settings.demo_mode,

            "offline_illustrations": (
                settings.image_provider.strip().lower() == "demo"
            ),

            "ai_illustrations": (
                settings.image_provider.strip().lower() == "hf"
            ),
        },
    )


# =========================================================
# GENERATE COMIC - HTML FORM
# =========================================================

@router.post(
    "/generate",
    response_class=HTMLResponse,
)
async def generate(
    request: Request,

    story_prompt: str = Form(...),

    character_name: str = Form(...),

    setting: str = Form(...),

    tone: str = Form(...),

    art_style: str = Form(...),
):

    try:

        # -----------------------------------------------
        # Validate input
        # -----------------------------------------------

        comic_request = ComicRequest(
            story_prompt=story_prompt,
            character_name=character_name,
            setting=setting,
            tone=tone,
            art_style=art_style,
        )

        # -----------------------------------------------
        # Generate comic
        # -----------------------------------------------

        title, layout, pdf_url = (
            generate_comic(
                comic_request
            )
        )

        # -----------------------------------------------
        # Render preview
        # -----------------------------------------------

        return templates.TemplateResponse(

            request=request,

            name="comic_preview.html",

            context={

                "title":
                    title,

                "layout":
                    layout,

                "pdf_url":
                    pdf_url,

                "request_data":
                    comic_request.model_dump(),

                "offline_illustrations": (
                    settings.image_provider.strip().lower() == "demo"
                ),

                "ai_illustrations": (
                    settings.image_provider.strip().lower() == "hf"
                ),
            },
        )

    except Exception as exc:

        return templates.TemplateResponse(

            request=request,

            name="error.html",

            context={
                "error": str(exc),
            },

            status_code=500,
        )


# =========================================================
# GENERATE COMIC - JSON API
# =========================================================

@router.post(
    "/generate-comic/json",
    response_model=ComicResponse,
)
async def generate_comic_json(
    payload: ComicRequest,
):

    try:

        title, layout, pdf_url = (
            generate_comic(
                payload
            )
        )

        return ComicResponse(
            title=title,
            panels=layout,
            pdf_url=pdf_url,
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# =========================================================
# TEST IMAGE
# =========================================================

@router.post(
    "/test-image",
)
async def image_generation_test(
    prompt: str = Form(...),
):

    try:

        image_url = test_image(
            prompt
        )

        return JSONResponse(
            content={
                "success": True,
                "image_url":
                    image_url,
            }
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


# =========================================================
# EXPORT SUCCESS
# =========================================================

@router.get(
    "/export-success",
    response_class=HTMLResponse,
)
async def export_success(
    request: Request,
    pdf_url: str = "",
):

    return templates.TemplateResponse(

        request=request,

        name="export_success.html",

        context={
            "pdf_url":
                pdf_url,
        },
    )


# =========================================================
# HEALTH CHECK
# =========================================================

@router.get(
    "/health",
)
async def health():

    return {

        "status": "ok",

        "application":
            settings.app_name,

        "environment":
            settings.environment,

        "demo_mode":
            settings.demo_mode,

        "image_provider":
            settings.image_provider,

        "gemini_configured":
            bool(
                settings.gemini_api_key
            ),

        "huggingface_configured":
            bool(
                settings.hf_api_key
            ),
    }