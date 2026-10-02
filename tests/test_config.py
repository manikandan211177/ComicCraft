from app.config import Settings


def test_example_environment_is_safe_to_run():
    settings = Settings(_env_file=".env.example")

    assert settings.demo_mode is True
    assert settings.image_provider == "demo"
    assert settings.gemini_api_key == ""
    assert settings.hf_api_key == ""
    assert settings.image_model == (
        "black-forest-labs/FLUX.1-schnell"
    )
    assert settings.image_steps == 4
