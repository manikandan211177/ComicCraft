from types import SimpleNamespace

from PIL import Image, ImageChops

from app.image_generator import (
    _generate_huggingface_image,
    generate_image,
)


def test_flux_huggingface_image_uses_live_provider_settings(
    tmp_path,
    monkeypatch,
):
    captured = {}

    class FakeInferenceClient:
        def __init__(self, **options):
            captured["client"] = options

        def text_to_image(self, **options):
            captured["image"] = options
            return Image.new("RGB", (64, 64), "#7253a6")

    monkeypatch.setattr(
        "app.image_generator.get_settings",
        lambda: SimpleNamespace(
            hf_api_key="test-token",
            image_model="black-forest-labs/FLUX.1-schnell",
            image_width=768,
            image_height=768,
            image_steps=25,
        ),
    )
    monkeypatch.setattr(
        "huggingface_hub.InferenceClient",
        FakeInferenceClient,
    )

    output = tmp_path / "panel.png"
    _generate_huggingface_image("A comic illustration.", output)

    assert captured["client"]["provider"] == "auto"
    assert captured["client"]["token"] == "test-token"
    assert captured["image"]["model"] == (
        "black-forest-labs/FLUX.1-schnell"
    )
    assert captured["image"]["num_inference_steps"] == 4
    assert captured["image"]["guidance_scale"] == 0.0
    assert "negative_prompt" not in captured["image"]
    assert output.is_file()
    assert Image.open(output).size == (64, 64)


def test_huggingface_provider_generates_images_in_demo_story_mode(
    tmp_path,
    monkeypatch,
):
    generated_paths = []

    def fake_huggingface_image(prompt, path):
        generated_paths.append(path)
        path.write_bytes(b"generated image")

    def fail_demo_image(*args, **kwargs):
        raise AssertionError("Demo drawing should not be used.")

    monkeypatch.setattr(
        "app.image_generator.get_settings",
        lambda: SimpleNamespace(
            panels_dir=tmp_path,
            demo_mode=True,
            image_provider="hf",
        ),
    )
    monkeypatch.setattr(
        "app.image_generator._generate_huggingface_image",
        fake_huggingface_image,
    )
    monkeypatch.setattr(
        "app.image_generator._generate_demo_image",
        fail_demo_image,
    )

    image_urls = [
        generate_image(
            prompt=f"AI comic panel {panel_number}",
            panel_number=panel_number,
        )
        for panel_number in range(1, 6)
    ]

    assert len(image_urls) == 5
    assert len(generated_paths) == 5
    assert all(path.is_file() for path in generated_paths)


def test_demo_provider_generates_distinct_images_for_all_panels(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        "app.image_generator.get_settings",
        lambda: SimpleNamespace(
            panels_dir=tmp_path,
            fonts_dir=tmp_path,
            demo_mode=False,
            image_provider="demo",
        ),
    )

    image_urls = [
        generate_image(
            prompt=f"Comic story panel {panel_number}",
            panel_number=panel_number,
        )
        for panel_number in range(1, 6)
    ]

    image_paths = [
        tmp_path / image_url.rsplit("/", 1)[-1]
        for image_url in image_urls
    ]
    assert len(image_paths) == 5
    assert all(path.is_file() for path in image_paths)

    images = [Image.open(path).convert("RGB") for path in image_paths]
    assert all(image.size == (768, 768) for image in images)

    for index, image in enumerate(images[1:], start=1):
        difference = ImageChops.difference(images[0], image)
        assert difference.getbbox() is not None, (
            f"Panel 1 and panel {index + 1} should look different."
        )
