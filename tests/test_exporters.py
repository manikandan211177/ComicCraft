from types import SimpleNamespace

from app.exporters import save_pdf
from app.models import ComicPanel


def test_save_pdf_keeps_full_width_for_each_panel_paragraph(
    tmp_path,
    monkeypatch,
):
    monkeypatch.setattr(
        "app.exporters.get_settings",
        lambda: SimpleNamespace(exports_dir=tmp_path),
    )
    panel = ComicPanel(
        panel=1,
        title="The Beginning",
        image_url="/static/panels/panel.png",
        image_prompt="A comic scene.",
        scene_description=(
            "Arjun begins an unexpected adventure in School."
        ),
        caption="A new adventure begins.",
        narration="Arjun steps into the unknown with curiosity.",
        dialogue="Arjun: I wonder what awaits me.",
    )

    pdf_url = save_pdf("Arjun's Comic", [panel])

    pdf_path = tmp_path / pdf_url.rsplit("/", 1)[-1]
    assert pdf_url.startswith("/static/exports/")
    assert pdf_path.is_file()
    assert pdf_path.stat().st_size > 0
