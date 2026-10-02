from __future__ import annotations

import hashlib
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .config import get_settings


# =========================================================
# FILE NAME
# =========================================================

def _create_filename(
    prompt: str,
    panel_number: int,
) -> str:

    digest = hashlib.sha256(
        prompt.encode("utf-8")
    ).hexdigest()[:16]

    return (
        f"panel_{panel_number}_"
        f"{digest}.png"
    )


# =========================================================
# DEMO FONT
# =========================================================

def _get_font(size: int):

    settings = get_settings()

    possible_fonts = [

        settings.fonts_dir /
        "DejaVuSans.ttf",

        Path(
            "C:/Windows/Fonts/arial.ttf"
        ),

        Path(
            "C:/Windows/Fonts/segoeui.ttf"
        ),
    ]

    for font_path in possible_fonts:

        try:

            if font_path.exists():

                return ImageFont.truetype(
                    str(font_path),
                    size,
                )

        except Exception:
            continue

    return ImageFont.load_default()


# =========================================================
# DEMO IMAGE
# =========================================================

def _generate_demo_image(
    prompt: str,
    path: Path,
    panel_number: int,
) -> None:
    panel_art = {
        1: {
            "sky": "#b9e8ff",
            "ground": "#8dcc78",
            "accent": "#ffd166",
            "label": "A NEW ADVENTURE",
        },
        2: {
            "sky": "#c9b6ff",
            "ground": "#8d79c6",
            "accent": "#ffe066",
            "label": "A MYSTERIOUS DISCOVERY",
        },
        3: {
            "sky": "#64748b",
            "ground": "#475569",
            "accent": "#fb7185",
            "label": "A CHALLENGE APPEARS",
        },
        4: {
            "sky": "#ffcf99",
            "ground": "#69b7a4",
            "accent": "#fff176",
            "label": "THE TURNING POINT",
        },
        5: {
            "sky": "#fbcfe8",
            "ground": "#86c98b",
            "accent": "#facc15",
            "label": "A HAPPY ENDING",
        },
    }
    art = panel_art.get(
        panel_number,
        panel_art[1],
    )

    image = Image.new(
        "RGB",
        (768, 768),
        "#eaf2ff",
    )

    draw = ImageDraw.Draw(
        image
    )

    # Outer frame
    draw.rounded_rectangle(
        (25, 25, 743, 743),
        radius=30,
        fill="#ffffff",
        outline="#283593",
        width=6,
    )

    # Sky
    draw.rectangle(
        (60, 70, 708, 480),
        fill=art["sky"],
    )

    # Ground
    draw.rectangle(
        (60, 390, 708, 480),
        fill=art["ground"],
    )

    # Sun or moon
    draw.ellipse(
        (570, 110, 650, 190),
        fill=art["accent"],
    )

    # Give each story beat its own visual scene.
    if panel_number == 2:
        draw.ellipse(
            (500, 285, 610, 395),
            fill="#fff7ae",
            outline="#ffffff",
            width=8,
        )
        draw.ellipse(
            (525, 310, 585, 370),
            fill="#ffd54f",
        )
        draw.line(
            (555, 260, 555, 230),
            fill="#fff7ae",
            width=7,
        )
        draw.line(
            (480, 340, 450, 340),
            fill="#fff7ae",
            width=7,
        )
    elif panel_number == 3:
        for cloud_x in (140, 310, 500):
            draw.ellipse(
                (cloud_x, 105, cloud_x + 115, 170),
                fill="#475569",
            )
        draw.line(
            (575, 175, 540, 235, 570, 235, 525, 300),
            fill="#ffe066",
            width=12,
        )
        draw.ellipse(
            (520, 345, 675, 475),
            fill="#334155",
        )
    elif panel_number == 4:
        draw.ellipse(
            (500, 265, 630, 395),
            fill=art["accent"],
            outline="#ffffff",
            width=8,
        )
        for ray_y in (280, 330, 380):
            draw.line(
                (485, ray_y, 455, ray_y),
                fill="#fff7ae",
                width=7,
            )
    elif panel_number == 5:
        for confetti_x, confetti_y, color in (
            (130, 150, "#f97316"),
            (230, 110, "#3b82f6"),
            (480, 180, "#a855f7"),
            (640, 245, "#ef4444"),
            (170, 300, "#db2777"),
            (620, 120, "#14b8a6"),
        ):
            draw.line(
                (confetti_x, confetti_y, confetti_x + 20, confetti_y + 30),
                fill=color,
                width=9,
            )
        draw.arc(
            (120, 155, 650, 490),
            start=190,
            end=350,
            fill="#ffffff",
            width=12,
        )

    # Character head and body
    draw.ellipse(
        (285, 245, 485, 445),
        fill="#ffb74d",
        outline="#673800",
        width=5,
    )

    # Eyes
    draw.ellipse(
        (335, 305, 360, 335),
        fill="#202020",
    )

    draw.ellipse(
        (410, 305, 435, 335),
        fill="#202020",
    )

    if panel_number == 3:
        draw.line(
            (350, 370, 420, 370),
            fill="#202020",
            width=6,
        )
    else:
        draw.arc(
            (350, 330, 420, 385),
            start=10,
            end=170,
            fill="#202020",
            width=5,
        )

    # Panel-specific action makes the character part of the story beat.
    if panel_number == 1:
        draw.line(
            (300, 330, 225, 265, 195, 220),
            fill="#ffb74d",
            width=28,
        )
        draw.ellipse(
            (175, 198, 215, 238),
            fill="#ffb74d",
        )
    elif panel_number == 2:
        draw.line(
            (470, 365, 525, 335),
            fill="#ffb74d",
            width=25,
        )
    elif panel_number == 3:
        draw.line(
            (300, 365, 235, 420),
            fill="#ffb74d",
            width=27,
        )
        draw.line(
            (470, 365, 520, 420),
            fill="#ffb74d",
            width=27,
        )
    elif panel_number == 4:
        draw.line(
            (300, 345, 235, 285),
            fill="#ffb74d",
            width=27,
        )
        draw.line(
            (470, 345, 520, 270),
            fill="#ffb74d",
            width=27,
        )
    elif panel_number == 5:
        draw.line(
            (300, 345, 235, 260),
            fill="#ffb74d",
            width=27,
        )
        draw.line(
            (470, 345, 520, 260),
            fill="#ffb74d",
            width=27,
        )

    # Panel label
    title_font = _get_font(28)
    text_font = _get_font(17)

    draw.text(
        (90, 525),
        art["label"],
        font=title_font,
        fill="#182230",
    )

    clean_prompt = re.sub(
        r"\s+",
        " ",
        prompt,
    ).strip()

    if len(clean_prompt) > 90:

        clean_prompt = (
            clean_prompt[:90]
            + "..."
        )

    draw.text(
        (90, 580),
        clean_prompt,
        font=text_font,
        fill="#52606d",
    )

    draw.text(
        (90, 640),
        "Offline comic illustration",
        font=text_font,
        fill="#52606d",
    )

    image.save(
        path,
        format="PNG",
    )


# =========================================================
# HUGGING FACE
# =========================================================

def _generate_huggingface_image(
    prompt: str,
    path: Path,
) -> None:

    settings = get_settings()

    if not settings.hf_api_key:

        raise RuntimeError(
            "HF_API_KEY is missing. "
            "Add it to your .env file."
        )

    try:

        from huggingface_hub import (
            InferenceClient,
        )

    except ImportError as exc:

        raise RuntimeError(
            "huggingface_hub is not installed. "
            "Run: pip install huggingface-hub"
        ) from exc

    try:

        client = InferenceClient(
            provider="auto",
            token=settings.hf_api_key,
            timeout=180,
        )

        image_options = {
            "prompt": prompt,
            "height": settings.image_height,
            "width": settings.image_width,
            "num_inference_steps": settings.image_steps,
            "model": settings.image_model,
        }

        if "flux.1-schnell" in settings.image_model.lower():
            image_options["num_inference_steps"] = max(
                1,
                min(settings.image_steps, 4),
            )
            image_options["guidance_scale"] = 0.0
        else:
            image_options["negative_prompt"] = (
                "low quality, blurry, "
                "distorted face, "
                "extra fingers, "
                "extra arms, "
                "extra legs, "
                "bad anatomy, "
                "text, letters, words, "
                "watermark, logo, "
                "speech bubble"
            )

        image = client.text_to_image(**image_options)

        image.save(
            path,
            format="PNG",
        )

    except Exception as exc:

        raise RuntimeError(
            "Hugging Face image generation failed: "
            f"{exc}. Check that HF_API_KEY is valid, the selected inference "
            "provider is enabled for your account, and the model supports "
            "text-to-image generation."
        ) from exc


# =========================================================
# LOCAL DIFFUSERS
# =========================================================

def _generate_local_image(
    prompt: str,
    path: Path,
) -> None:

    settings = get_settings()

    try:

        import torch

        from diffusers import (
            StableDiffusionPipeline,
        )

    except ImportError as exc:

        raise RuntimeError(
            "Local Stable Diffusion is not "
            "installed.\n\n"
            "Run:\n"
            "pip install "
            "-r requirements-local-image.txt"
        ) from exc

    device = (
        "cuda"
        if torch.cuda.is_available()
        else "cpu"
    )

    dtype = (
        torch.float16
        if device == "cuda"
        else torch.float32
    )

    try:

        pipe = (
            StableDiffusionPipeline
            .from_pretrained(
                settings.image_model,
                torch_dtype=dtype,
            )
        )

        pipe = pipe.to(device)

        result = pipe(
            prompt=prompt,

            negative_prompt=(
                "blurry, low quality, "
                "text, letters, "
                "watermark, logo, "
                "speech bubble"
            ),

            width=settings.image_width,

            height=settings.image_height,

            num_inference_steps=(
                settings.image_steps
            ),
        )

        result.images[0].save(
            path,
            format="PNG",
        )

    except Exception as exc:

        raise RuntimeError(
            "Local Stable Diffusion failed: "
            f"{exc}"
        ) from exc


# =========================================================
# PUBLIC IMAGE FUNCTION
# =========================================================

def generate_image(
    prompt: str,
    panel_number: int,
) -> str:

    settings = get_settings()

    settings.panels_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = _create_filename(
        prompt,
        panel_number,
    )

    output_path = (
        settings.panels_dir /
        filename
    )

    provider = (
        settings.image_provider
        .strip()
        .lower()
    )

    # -----------------------------------------------------
    # DEMO
    # -----------------------------------------------------

    if provider == "demo":

        _generate_demo_image(
            prompt,
            output_path,
            panel_number,
        )

    # -----------------------------------------------------
    # HUGGING FACE
    # -----------------------------------------------------

    elif provider == "hf":

        _generate_huggingface_image(
            prompt,
            output_path,
        )

    # -----------------------------------------------------
    # LOCAL
    # -----------------------------------------------------

    elif provider == "local":

        _generate_local_image(
            prompt,
            output_path,
        )

    else:

        raise RuntimeError(
            "Invalid IMAGE_PROVIDER. "
            "Use demo, hf, or local."
        )

    return (
        f"/static/panels/{filename}"
    )


# =========================================================
# TEST IMAGE
# =========================================================

def test_image(
    prompt: str,
) -> str:

    return generate_image(
        prompt=prompt,
        panel_number=0,
    )