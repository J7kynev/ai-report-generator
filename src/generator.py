# generator.py
# Builds a structured PDF report from analysis output

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.colors import HexColor
from datetime import datetime

def generate_pdf(analysis: str, filename: str = None) -> str:
    """Generate a professional PDF report from the AI analysis."""
    os.makedirs("outputs", exist_ok=True)

    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"outputs/report_{timestamp}.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        fontSize=22,
        textColor=HexColor("#1a1a2e"),
        spaceAfter=12,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontSize=11,
        leading=18,
        textColor=HexColor("#2d2d2d"),
    )

    content = []
    content.append(Paragraph("AI Business Report", title_style))
    content.append(Paragraph(
        f"Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}",
        styles["Normal"]
    ))
    content.append(Spacer(1, 0.5*cm))

    for line in analysis.split("\n"):
        if line.strip():
            content.append(Paragraph(line.strip(), body_style))
            content.append(Spacer(1, 0.2*cm))

    doc.build(content)
    return filename