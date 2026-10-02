import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# ---------------------------------------------------------
# PROJECT ROOT
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = Path(
    os.environ.get(
        "COMICCRAFT_ENV_FILE",
        str(BASE_DIR / ".env"),
    )
)
if not ENV_FILE.is_absolute():
    ENV_FILE = BASE_DIR / ENV_FILE


# ---------------------------------------------------------
# APPLICATION SETTINGS
# ---------------------------------------------------------

class Settings(BaseSettings):

    # Application
    app_name: str = "ComicCraft"
    environment: str = "development"

    host: str = "127.0.0.1"
    port: int = 8000

    # -----------------------------------------------------
    # GEMINI
    # -----------------------------------------------------

    gemini_api_key: str = ""

    # Current Gemini model can be changed from .env
    gemini_outline_model: str = "gemini-3.8-flash"
    gemini_story_model: str = "gemini-3.8-flash"

    # -----------------------------------------------------
    # HUGGING FACE
    # -----------------------------------------------------

    hf_api_key: str = ""

    # Supported values:
    # demo
    # hf
    # local

    image_provider: str = "demo"

    # Change this model from .env if required.
    image_model: str = (
        "black-forest-labs/FLUX.1-schnell"
    )

    # -----------------------------------------------------
    # IMAGE SETTINGS
    # -----------------------------------------------------

    image_width: int = 768
    image_height: int = 768

    image_steps: int = 4

    # -----------------------------------------------------
    # DEVELOPMENT
    # -----------------------------------------------------

    # Uses built-in story content; image generation is controlled separately
    # by image_provider.
    demo_mode: bool = True

    max_panels: int = 5

    # -----------------------------------------------------
    # ENVIRONMENT FILE
    # -----------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # -----------------------------------------------------
    # DIRECTORIES
    # -----------------------------------------------------

    @property
    def templates_dir(self) -> Path:

        return BASE_DIR / "templates"

    @property
    def static_dir(self) -> Path:

        return BASE_DIR / "static"

    @property
    def panels_dir(self) -> Path:

        return self.static_dir / "panels"

    @property
    def exports_dir(self) -> Path:

        return self.static_dir / "exports"

    @property
    def fonts_dir(self) -> Path:

        return BASE_DIR / "fonts"


# ---------------------------------------------------------
# SINGLE SETTINGS INSTANCE
# ---------------------------------------------------------

@lru_cache(maxsize=1)
def get_settings() -> Settings:

    return Settings()