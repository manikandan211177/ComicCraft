from types import SimpleNamespace

from PIL import Image

from app.models import ComicRequest
from app.services import generate_comic


def test_demo_story_mode_generates_an_ai_image_for_each_panel(
    tmp_path,
    monkeypatch,
):
    settings = SimpleNamespace(
        demo_mode=True,
        image_provider="hf",
        panels_dir=tmp_path / "panels",
    )
    prompts = []

    def fake_huggingface_image(prompt, path):
        prompts.append(prompt)
        Image.new("RGB", (32, 32), "#7253a6").save(path)

    monkeypatch.setattr("app.services.get_settings", lambda: settings)
    monkeypatch.setattr(
        "app.image_generator.get_settings",
        lambda: settings,
    )
    monkeypatch.setattr(
        "app.image_generator._generate_huggingface_image",
        fake_huggingface_image,
    )
    monkeypatch.setattr(
        "app.services.save_pdf",
        lambda title, layout: "/static/exports/test.pdf",
    )

    request = ComicRequest(
        story_prompt="Arjun finds a friendly robot and saves his school.",
        character_name="Arjun",
        setting="School",
        tone="Adventure",
        art_style="Comic Book",
    )

    _, panels, pdf_url = generate_comic(request)

    assert len(panels) == 5
    assert len(prompts) == 5
    assert all(request.story_prompt in prompt for prompt in prompts)
    assert all(
        panel.scene_description in prompt
        for panel, prompt in zip(panels, prompts, strict=True)
    )
    assert all(
        (settings.panels_dir / url.rsplit("/", 1)[-1]).is_file()
        for url in (panel.image_url for panel in panels)
    )
    assert pdf_url == "/static/exports/test.pdf"
