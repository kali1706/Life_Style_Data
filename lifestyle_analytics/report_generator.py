from __future__ import annotations

from datetime import date
from io import BytesIO
from typing import Tuple

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from openpyxl import Workbook


def generate_pdf_report(title: str = "Lifestyle Report", summary_lines: Tuple[str, ...] = ()) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(72, height - 72, title)

    pdf.setFont("Helvetica", 11)
    y = height - 108
    for line in summary_lines:
        pdf.drawString(72, y, line)
        y -= 18
        if y < 72:
            pdf.showPage()
            y = height - 72

    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return buffer.read()


def generate_excel_report() -> bytes:
    wb = Workbook()
    ws = wb.active
    ws.title = "Summary"
    ws.append(["Metric", "Value"])
    ws.append(["Example", 100])

    bio = BytesIO()
    wb.save(bio)
    bio.seek(0)
    return bio.read()
