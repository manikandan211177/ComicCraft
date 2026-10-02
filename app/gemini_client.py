from __future__ import annotations

import json

from google import genai

from .config import get_settings
from .models import (
    ComicRequest,
    OutlineResponse,
    StoryResponse,
)


class GeminiService:
    """
    Handles all Gemini API operations for ComicCraft.
    """

    def __init__(self) -> None:

        self.settings = get_settings()

        if not self.settings.gemini_api_key:

            raise RuntimeError(
                "GEMINI_API_KEY is missing. "
                "Add your Gemini API key to the .env file."
            )

        self.client = genai.Client(
            api_key=self.settings.gemini_api_key
        )

    # =====================================================
    # GENERIC STRUCTURED GENERATION
    # =====================================================

    def _generate_structured(
        self,
        model: str,
        prompt: str,
        schema,
        temperature: float = 0.8,
    ):

        try:

            response = (
                self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config={
                        "response_mime_type":
                            "application/json",

                        "response_schema":
                            schema,

                        "temperature":
                            temperature,
                    },
                )
            )

        except Exception as exc:

            raise RuntimeError(
                f"Gemini API request failed: {exc}"
            ) from exc

        # New SDK may provide response.parsed.
        parsed = getattr(
            response,
            "parsed",
            None,
        )

        if parsed is not None:

            if isinstance(
                parsed,
                schema
            ):
                return parsed

            return schema.model_validate(
                parsed
            )

        # Fallback to response.text
        text = getattr(
            response,
            "text",
            None,
        )

        if not text:

            raise RuntimeError(
                "Gemini returned an empty response."
            )

        try:

            return schema.model_validate_json(
                text
            )

        except Exception as exc:

            raise RuntimeError(
                "Gemini returned invalid "
                f"structured JSON: {exc}"
            ) from exc

    # =====================================================
    # GENERATE FIVE-PANEL OUTLINE
    # =====================================================

    def generate_outline(
        self,
        request: ComicRequest,
    ) -> list:

        prompt = f"""
You are the professional story planner
for an AI comic application called ComicCraft.

Create EXACTLY 5 sequential comic panels.

USER STORY:
{request.story_prompt}

MAIN CHARACTER:
{request.character_name}

SETTING:
{request.setting}

TONE:
{request.tone}

ART STYLE:
{request.art_style}

The five panels must follow this structure:

Panel 1:
Introduce the character and situation.

Panel 2:
Develop the story.

Panel 3:
Introduce a challenge or conflict.

Panel 4:
Show the turning point.

Panel 5:
Provide a satisfying ending.

For every panel generate:

- panel number
- short title
- scene description
- detailed image generation prompt

Important requirements:

1. Exactly five panels.
2. Keep the character visually consistent.
3. Keep the setting consistent.
4. Maintain chronological story continuity.
5. Make the image prompts visually detailed.
6. Include character appearance details when useful.
7. The image should not contain readable text.
8. Do not include speech bubbles.
9. Do not include logos.
10. Do not include watermarks.
11. Make the comic visually interesting.
12. Match the requested art style.
13. Match the requested tone.

Return only the structured response.
"""

        result = self._generate_structured(
            model=(
                self.settings
                .gemini_outline_model
            ),
            prompt=prompt,
            schema=OutlineResponse,
            temperature=0.8,
        )

        if len(result.panels) != 5:

            raise RuntimeError(
                "Gemini did not generate exactly "
                f"5 panels. Generated: "
                f"{len(result.panels)}"
            )

        # Ensure numbering is correct.
        for index, panel in enumerate(
            result.panels,
            start=1,
        ):

            panel.panel = index

        return result.panels

    # =====================================================
    # GENERATE STORY / DIALOGUE
    # =====================================================

    def generate_story(
        self,
        request: ComicRequest,
        outline: list,
    ) -> list:

        outline_data = json.dumps(
            [
                panel.model_dump()
                for panel in outline
            ],
            indent=2,
            ensure_ascii=False,
        )

        prompt = f"""
You are the professional comic writer
for ComicCraft.

Write the complete text content for
exactly five comic panels.

USER STORY:
{request.story_prompt}

MAIN CHARACTER:
{request.character_name}

SETTING:
{request.setting}

TONE:
{request.tone}

ART STYLE:
{request.art_style}

PANEL OUTLINE:

{outline_data}

For each panel create:

1. caption
2. narration
3. dialogue

Requirements:

- Exactly five panels.
- Preserve panel order.
- Maintain continuity.
- Keep the character consistent.
- Keep the setting consistent.
- Caption should be short.
- Narration should be 1-3 sentences.
- Dialogue should be natural.
- Dialogue can be empty if unnecessary.
- Match the requested tone.
- Do not write an essay.
- Keep the text suitable for a general audience.

Return only the structured response.
"""

        result = self._generate_structured(
            model=(
                self.settings
                .gemini_story_model
            ),
            prompt=prompt,
            schema=StoryResponse,
            temperature=0.9,
        )

        if len(result.panels) != 5:

            raise RuntimeError(
                "Gemini did not generate exactly "
                f"5 story panels. Generated: "
                f"{len(result.panels)}"
            )

        for index, panel in enumerate(
            result.panels,
            start=1,
        ):

            panel.panel = index

        return result.panels


def get_gemini_service() -> GeminiService:

    return GeminiService()