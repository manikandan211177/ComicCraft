from __future__ import annotations

import re

from .config import get_settings
from .exporters import save_pdf
from .gemini_client import get_gemini_service
from .image_generator import generate_image
from .layout_builder import build_comic_layout
from .models import (
    ComicRequest,
    PanelOutline,
    PanelStory,
)


# =========================================================
# DEMO OUTLINE
# =========================================================

def _create_demo_outline(
    request: ComicRequest,
):

    character = request.character_name
    setting = request.setting
    style = request.art_style

    return [

        PanelOutline(
            panel=1,
            title="The Beginning",
            scene_description=(
                f"{character} begins an "
                f"unexpected adventure in "
                f"{setting}."
            ),
            image_prompt=(
                f"{character} beginning an "
                f"adventure in {setting}, "
                f"{style} comic art, "
                "cinematic composition, "
                "beautiful lighting, "
                "consistent character design, "
                "no text"
            ),
        ),

        PanelOutline(
            panel=2,
            title="A Strange Discovery",
            scene_description=(
                f"{character} discovers "
                "something mysterious."
            ),
            image_prompt=(
                f"{character} discovering "
                f"a mysterious object in "
                f"{setting}, "
                f"{style} comic art, "
                "cinematic lighting, "
                "expressive character, "
                "no text"
            ),
        ),

        PanelOutline(
            panel=3,
            title="The Challenge",
            scene_description=(
                f"A difficult challenge "
                f"appears before {character}."
            ),
            image_prompt=(
                f"{character} facing a "
                f"dramatic challenge in "
                f"{setting}, "
                f"{style} comic art, "
                "dynamic composition, "
                "cinematic lighting, "
                "no text"
            ),
        ),

        PanelOutline(
            panel=4,
            title="The Turning Point",
            scene_description=(
                f"{character} finds a clever "
                "way to overcome the "
                "challenge."
            ),
            image_prompt=(
                f"{character} solving the "
                f"problem in {setting}, "
                f"{style} comic illustration, "
                "heroic composition, "
                "dramatic lighting, "
                "no text"
            ),
        ),

        PanelOutline(
            panel=5,
            title="A New Beginning",
            scene_description=(
                f"{character} reaches the "
                "end of the adventure "
                "with hope for the future."
            ),
            image_prompt=(
                f"{character} celebrating "
                f"after the adventure in "
                f"{setting}, "
                f"{style} comic art, "
                "warm cinematic lighting, "
                "happy ending, "
                "no text"
            ),
        ),
    ]


# =========================================================
# DEMO STORY
# =========================================================

def _create_demo_story(
    request: ComicRequest,
):

    character = request.character_name

    return [

        PanelStory(
            panel=1,
            caption="A new adventure begins.",
            narration=(
                f"{character} steps into "
                "the unknown with curiosity."
            ),
            dialogue=(
                f"{character}: "
                "I wonder what awaits me."
            ),
        ),

        PanelStory(
            panel=2,
            caption="Something unexpected appears.",
            narration=(
                f"{character} discovers "
                "a mysterious clue."
            ),
            dialogue=(
                f"{character}: "
                "What could this mean?"
            ),
        ),

        PanelStory(
            panel=3,
            caption="The challenge begins.",
            narration=(
                "The path becomes difficult, "
                "but giving up is not an option."
            ),
            dialogue=(
                f"{character}: "
                "I have to keep going!"
            ),
        ),

        PanelStory(
            panel=4,
            caption="A clever idea changes everything.",
            narration=(
                f"{character} notices a "
                "hidden solution and acts quickly."
            ),
            dialogue=(
                f"{character}: "
                "Now I understand!"
            ),
        ),

        PanelStory(
            panel=5,
            caption="The adventure reaches its end.",
            narration=(
                f"{character} looks back "
                "at the journey with a smile."
            ),
            dialogue=(
                f"{character}: "
                "What an incredible adventure!"
            ),
        ),
    ]


# =========================================================
# CREATE TITLE
# =========================================================

def _create_title(
    request: ComicRequest,
) -> str:

    words = re.findall(
        r"[A-Za-z0-9']+",
        request.story_prompt,
    )

    short_prompt = " ".join(
        words[:7]
    )

    if not short_prompt:

        short_prompt = "My Comic Adventure"

    return (
        f"{request.character_name}: "
        f"{short_prompt}"
    )


# =========================================================
# MAIN COMIC GENERATION
# =========================================================

def generate_comic(
    request: ComicRequest,
):

    settings = get_settings()

    # =====================================================
    # STEP 1 - STORY OUTLINE
    # =====================================================

    if settings.demo_mode:

        outline = _create_demo_outline(
            request
        )

    else:

        gemini = get_gemini_service()

        outline = (
            gemini.generate_outline(
                request
            )
        )

    # =====================================================
    # STEP 2 - STORY / DIALOGUE
    # =====================================================

    if settings.demo_mode:

        stories = _create_demo_story(
            request
        )

    else:

        gemini = get_gemini_service()

        stories = (
            gemini.generate_story(
                request,
                outline,
            )
        )

    # =====================================================
    # STEP 3 - IMAGE GENERATION
    # =====================================================

    image_urls = []

    for panel in outline:

        image_prompt = (
            f"{panel.image_prompt}. "
            f"Story concept: {request.story_prompt}. "
            f"Panel scene: {panel.scene_description}. "
            f"Art style: {request.art_style}. "
            f"Tone: {request.tone}. "
            "Single comic panel. "
            "No readable text. "
            "No letters. "
            "No words. "
            "No speech bubbles. "
            "No watermark. "
            "No logo."
        )

        image_url = generate_image(
            prompt=image_prompt,
            panel_number=panel.panel,
        )

        image_urls.append(
            image_url
        )

    # =====================================================
    # STEP 4 - BUILD LAYOUT
    # =====================================================

    layout = build_comic_layout(
        outline=outline,
        stories=stories,
        image_urls=image_urls,
    )

    # =====================================================
    # STEP 5 - TITLE
    # =====================================================

    title = _create_title(
        request
    )

    # =====================================================
    # STEP 6 - PDF
    # =====================================================

    pdf_url = save_pdf(
        title=title,
        layout=layout,
    )

    return (
        title,
        layout,
        pdf_url,
    )