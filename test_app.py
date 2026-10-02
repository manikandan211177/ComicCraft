"""
ComicCraft - Application Tests

Run with:

    pytest -v

These tests verify:
- FastAPI application starts correctly
- Homepage loads
- Health endpoint works
- Pydantic request validation works
- JSON comic generation route works without calling real AI APIs
- Image test route works without calling real image APIs
- Export success page loads
"""


import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models import (
    ComicPanel,
    ComicRequest,
)


# =========================================================
# TEST CLIENT
# =========================================================

@pytest.fixture
def client():
    """
    Creates a FastAPI TestClient for the application.
    """

    with TestClient(app) as test_client:
        yield test_client


# =========================================================
# TEST 1 - APPLICATION STARTS
# =========================================================

def test_application_starts(client):
    """
    Verify that the FastAPI application starts successfully.
    """

    response = client.get("/")

    assert response.status_code == 200


# =========================================================
# TEST 2 - HOMEPAGE
# =========================================================

def test_homepage(client):
    """
    Verify that the ComicCraft homepage loads correctly.
    """

    response = client.get("/")

    assert response.status_code == 200

    assert "ComicCraft" in response.text

    assert "Story Prompt" in response.text

    assert "Main Character Name" in response.text

    assert "Setting" in response.text

    assert "Story Tone" in response.text

    assert "Art Style" in response.text


# =========================================================
# TEST 3 - HEALTH CHECK
# =========================================================

def test_health_endpoint(client):
    """
    Verify the /health endpoint.
    """

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"

    assert "application" in data

    assert "environment" in data

    assert "demo_mode" in data

    assert "image_provider" in data


# =========================================================
# TEST 4 - VALID COMIC REQUEST
# =========================================================

def test_valid_comic_request():
    """
    Verify that a valid ComicRequest is accepted.
    """

    request = ComicRequest(
        story_prompt=(
            "A young student discovers a mysterious robot "
            "inside his school."
        ),
        character_name="Arjun",
        setting="School",
        tone="Adventure",
        art_style="Comic Book",
    )

    assert request.story_prompt != ""

    assert request.character_name == "Arjun"

    assert request.setting == "School"

    assert request.tone == "Adventure"

    assert request.art_style == "Comic Book"


# =========================================================
# TEST 5 - EMPTY STORY PROMPT
# =========================================================

def test_empty_story_prompt_rejected():
    """
    Verify that an empty story prompt is rejected.
    """

    with pytest.raises(ValueError):

        ComicRequest(
            story_prompt="   ",
            character_name="Arjun",
            setting="School",
            tone="Funny",
            art_style="Comic Book",
        )


# =========================================================
# TEST 6 - EMPTY CHARACTER NAME
# =========================================================

def test_empty_character_name_rejected():
    """
    Verify that an empty character name is rejected.
    """

    with pytest.raises(ValueError):

        ComicRequest(
            story_prompt="A student discovers a robot.",
            character_name="   ",
            setting="School",
            tone="Funny",
            art_style="Comic Book",
        )


# =========================================================
# TEST 7 - FORM SUBMISSION VALIDATION
# =========================================================

def test_generate_without_required_fields(client):
    """
    Verify that /generate does not accept an empty form.
    """

    response = client.post(
        "/generate",
        data={}
    )

    # FastAPI should reject missing required form fields.
    assert response.status_code in (400, 422)


# =========================================================
# TEST 8 - JSON GENERATION ROUTE
# =========================================================

def test_json_generation_route(client, monkeypatch):
    """
    Test /generate-comic/json without calling Gemini
    or Hugging Face.

    The actual comic-generation service is replaced with
    a small fake function.
    """

    fake_panels = [

        ComicPanel(
            panel=1,
            title="The Discovery",
            image_url="/static/panels/test_panel_1.png",
            image_prompt="A student discovers a robot.",
            scene_description=(
                "Arjun finds a mysterious robot "
                "inside his school."
            ),
            caption="Something strange is happening.",
            narration="Arjun carefully approaches the robot.",
            dialogue="Arjun: Who are you?",
        ),

        ComicPanel(
            panel=2,
            title="The Robot Awakens",
            image_url="/static/panels/test_panel_2.png",
            image_prompt="A robot wakes up in a classroom.",
            scene_description=(
                "The robot suddenly activates."
            ),
            caption="The machine comes alive.",
            narration="The classroom fills with a bright light.",
            dialogue="Robot: Hello, Arjun.",
        ),

        ComicPanel(
            panel=3,
            title="A New Friend",
            image_url="/static/panels/test_panel_3.png",
            image_prompt="Student and robot talking.",
            scene_description=(
                "Arjun learns that the robot needs help."
            ),
            caption="A surprising friendship begins.",
            narration="Arjun decides to help the robot.",
            dialogue="Arjun: I will help you.",
        ),

        ComicPanel(
            panel=4,
            title="The Challenge",
            image_url="/static/panels/test_panel_4.png",
            image_prompt="Student and robot facing danger.",
            scene_description=(
                "A dangerous machine enters the school."
            ),
            caption="Their biggest challenge begins.",
            narration="Arjun and the robot work together.",
            dialogue="Robot: We must stop it!",
        ),

        ComicPanel(
            panel=5,
            title="The New Beginning",
            image_url="/static/panels/test_panel_5.png",
            image_prompt="Student and robot celebrating.",
            scene_description=(
                "The school is safe again."
            ),
            caption="Every adventure creates a new story.",
            narration=(
                "Arjun and his new friend look toward "
                "their next adventure."
            ),
            dialogue="Arjun: What should we do next?",
        ),
    ]


    def fake_generate_comic(request):

        return (
            "Arjun and the Mysterious Robot",
            fake_panels,
            "/static/exports/test_comic.pdf",
        )


    # Replace the real generation function used by routes.py.

    monkeypatch.setattr(
        "app.routes.generate_comic",
        fake_generate_comic,
    )


    payload = {
        "story_prompt": (
            "A student discovers a mysterious robot "
            "inside his school."
        ),
        "character_name": "Arjun",
        "setting": "School",
        "tone": "Adventure",
        "art_style": "Comic Book",
    }


    response = client.post(
        "/generate-comic/json",
        json=payload,
    )


    assert response.status_code == 200


    data = response.json()


    assert data["title"] == (
        "Arjun and the Mysterious Robot"
    )


    assert len(data["panels"]) == 5


    assert data["panels"][0]["panel"] == 1

    assert data["panels"][4]["panel"] == 5


    assert data["pdf_url"] == (
        "/static/exports/test_comic.pdf"
    )


# =========================================================
# TEST 9 - IMAGE TEST ROUTE
# =========================================================

def test_image_test_route(client, monkeypatch):
    """
    Test /test-image without calling Hugging Face.
    """

    def fake_test_image(prompt):

        return "/static/panels/test_image.png"


    monkeypatch.setattr(
        "app.routes.test_image",
        fake_test_image,
    )


    response = client.post(
        "/test-image",
        data={
            "prompt": "A superhero standing in a city"
        },
    )


    assert response.status_code == 200


    data = response.json()


    assert "image_url" in data


    assert data["image_url"] == (
        "/static/panels/test_image.png"
    )


# =========================================================
# TEST 10 - TEST IMAGE WITHOUT PROMPT
# =========================================================

def test_image_test_without_prompt(client):
    """
    Verify that /test-image rejects a missing prompt.
    """

    response = client.post(
        "/test-image",
        data={}
    )


    assert response.status_code in (400, 422)


# =========================================================
# TEST 11 - EXPORT SUCCESS PAGE
# =========================================================

def test_export_success_page(client):
    """
    Verify that the export success page loads.
    """

    response = client.get(
        "/export-success"
    )


    assert response.status_code == 200


    assert "Comic" in response.text


# =========================================================
# TEST 12 - STATIC FILES
# =========================================================

def test_static_directory_available(client):
    """
    Verify that the static directory is mounted.

    The exact CSS file is requested because the HTML
    templates reference it through FastAPI's static mount.
    """

    response = client.get(
        "/static/css/style.css"
    )


    assert response.status_code == 200


    assert "ComicCraft" in response.text


# =========================================================
# TEST 13 - INVALID JSON DATA
# =========================================================

def test_invalid_json_request(client):
    """
    Verify that invalid/missing comic data is rejected.
    """

    response = client.post(
        "/generate-comic/json",
        json={
            "story_prompt": "",
            "character_name": "",
            "setting": "",
            "tone": "",
            "art_style": "",
        },
    )


    assert response.status_code in (400, 422)