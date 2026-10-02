from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from fpdf import FPDF
from fpdf.enums import XPos, YPos

from .config import get_settings


# =========================================================
# PDF FILE NAME
# =========================================================

def _slugify_title(title: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "_", title).strip("_")
    return text.lower() or "comic"


# =========================================================
# SAVE PDF
# =========================================================

def save_pdf(title: str, layout) -> str:
    settings = get_settings()

    settings.exports_dir.mkdir(parents=True, exist_ok=True)

    safe_title = _slugify_title(title)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_title}_{timestamp}.pdf"
    output_path = settings.exports_dir / filename

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(
        0,
        12,
        title,
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )
    pdf.ln(4)

    for panel in layout:
        pdf.set_font("Helvetica", "B", 12)
        pdf.multi_cell(
            0,
            8,
            f"Panel {panel.panel}: {panel.title}",
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )

        pdf.set_font("Helvetica", "", 11)
        if getattr(panel, "scene_description", None):
            pdf.multi_cell(
                0,
                7,
                panel.scene_description,
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
        if getattr(panel, "caption", None):
            pdf.multi_cell(
                0,
                7,
                f"Caption: {panel.caption}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
        if getattr(panel, "narration", None):
            pdf.multi_cell(
                0,
                7,
                f"Narration: {panel.narration}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )
        if getattr(panel, "dialogue", None):
            pdf.multi_cell(
                0,
                7,
                f"Dialogue: {panel.dialogue}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )

        pdf.ln(3)

    pdf.output(str(output_path))

    return f"/static/exports/{filename}"
