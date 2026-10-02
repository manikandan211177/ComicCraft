# ComicCraft

## AI Comic Story Creator Using Gemini Models

ComicCraft is an AI-powered web application that transforms a simple story idea into a complete comic.

The application uses:

- FastAPI for the backend
- Jinja2 for the frontend
- Google Gemini for story generation
- Hugging Face / Stable Diffusion for image generation
- Pillow for image processing
- FPDF for PDF export

The application creates a five-panel comic containing:

- Story outline
- Scene descriptions
- Narration
- Dialogue
- AI-generated illustrations
- Downloadable PDF

## Run the Example Configuration on Windows

The example configuration is safe for offline demo use. Start it from
PowerShell with:

```powershell
.\scripts\run_example.ps1
```

This loads `.env.example` directly without overwriting `.env`, then starts
ComicCraft at `http://127.0.0.1:8000`. The example file contains placeholders,
not API credentials. To use real Gemini or Hugging Face services, add your
keys to the untracked local `.env` file and select the desired providers.

## Generate Hugging Face Images for All Five Panels

Run `.\scripts\run_hf_images.ps1` in PowerShell. The launcher uses demo
stories, requests a separate Hugging Face image for each panel, and prompts
for the Hugging Face token with hidden input if it is not already configured
in the local `.env`. The launcher explicitly reads the project `.env`, so a
previous example-config setting cannot silently select demo images. A token
entered at the prompt is kept only in the launcher process and is not saved
to a file. Internet access and Hugging Face inference access for the
configured model are required. The default model is
`black-forest-labs/FLUX.1-schnell`; the app uses its recommended four
inference steps and Hugging Face automatic provider routing.

---

# 1. Project Structure

```text
ComicCraft/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes.py
│   ├── config.py
│   ├── models.py
│   ├── gemini_client.py
│   ├── image_generator.py
│   ├── services.py
│   ├── layout_builder.py
│   └── exporters.py
│
├── templates/
│   ├── index.html
│   ├── comic_preview.html
│   ├── export_success.html
│   └── error.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   ├── js/
│   │   └── app.js
│   │
│   ├── panels/
│   │   └── .gitkeep
│   │
│   └── exports/
│       └── .gitkeep
│
├── tests/
│   └── test_app.py
│
├── scripts/
│   ├── run_demo.ps1
│   ├── run_example.ps1
│   ├── run_hf_images.ps1
│   └── run_demo.sh
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── requirements-local-image.txt
└── README.md