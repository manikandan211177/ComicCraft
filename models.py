from pydantic import BaseModel, Field, field_validator


# =========================================================
# USER INPUT
# =========================================================

class ComicRequest(BaseModel):

    story_prompt: str = Field(
        ...,
        min_length=5,
        max_length=2000,
        description="Main idea for the comic story.",
    )

    character_name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Main character name.",
    )

    setting: str = Field(
        ...,
        min_length=1,
        max_length=150,
        description="Story setting.",
    )

    tone: str = Field(
        ...,
        min_length=1,
        max_length=80,
        description="Story tone.",
    )

    art_style: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Comic art style.",
    )

    # -----------------------------------------------------
    # Clean all string values
    # -----------------------------------------------------

    @field_validator(
        "story_prompt",
        "character_name",
        "setting",
        "tone",
        "art_style",
    )
    @classmethod
    def clean_text(cls, value: str) -> str:

        value = value.strip()

        if not value:
            raise ValueError(
                "This field cannot be empty."
            )

        return value


# =========================================================
# GEMINI OUTLINE
# =========================================================

class PanelOutline(BaseModel):

    panel: int

    title: str

    scene_description: str

    image_prompt: str


class OutlineResponse(BaseModel):

    panels: list[PanelOutline]


# =========================================================
# GEMINI STORY
# =========================================================

class PanelStory(BaseModel):

    panel: int

    caption: str

    narration: str

    dialogue: str


class StoryResponse(BaseModel):

    panels: list[PanelStory]


# =========================================================
# FINAL COMIC PANEL
# =========================================================

class ComicPanel(BaseModel):

    panel: int

    title: str

    image_url: str

    image_prompt: str

    scene_description: str

    caption: str

    narration: str

    dialogue: str


# =========================================================
# FINAL API RESPONSE
# =========================================================

class ComicResponse(BaseModel):

    title: str

    panels: list[ComicPanel]

    pdf_url: str