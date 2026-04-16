"""
Generador de PDF para tablas de amortización e inversión.
Utiliza ReportLab para crear PDFs profesionales con:
- Logo e información de la institución financiera
- Datos del cliente
- Tabla de pagos completa
- Resumen de totales
"""
import os
from io import BytesIO
from typing import Optional, List

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, HRFlowable, Image
)
from reportlab.lib.colors import HexColor


# Paleta de colores corporativos
PRIMARY = HexColor("#1a3c5e")
SECONDARY = HexColor("#2575bc")
ACCENT = HexColor("#e8f4fd")
HEADER_BG = HexColor("#1a3c5e")
HEADER_FG = colors.white
ROW_ALT = HexColor("#f0f7ff")
TOTAL_BG = HexColor("#2575bc")


def generar_pdf_amortizacion(
    schedule: List[dict],
    institution_name: str,
    institution_logo: Optional[str],
    credit_type_name: str,
    amount: float,
    term_months: int,
    nominal_rate: float,
    system: str,
    client_name: str,
    total_capital: float,
    total_interest: float,
    charge_names: List[str],
    total_charges_details: dict[str, float],
    total_payment: float,
) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    styles = getSampleStyleSheet()
    story = []

    # ── Encabezado ──────────────────────────────────────
    header_data = []
    logo_cell = ""
    if institution_logo and os.path.exists(institution_logo):
        try:
            img = Image(institution_logo, width=4 * cm, height=2 * cm)
            logo_cell = img
        except Exception:
            logo_cell = ""

    title_style = ParagraphStyle(
        "titulo", fontSize=16, fontName="Helvetica-Bold",
        textColor=PRIMARY, alignment=TA_LEFT
    )
    sub_style = ParagraphStyle(
        "sub", fontSize=9, fontName="Helvetica",
        textColor=colors.gray, alignment=TA_LEFT
    )

    header_data.append([
        logo_cell,
        [
            Paragraph(institution_name, title_style),
            Paragraph("Tabla de Amortización", sub_style),
        ]
    ])
    t = Table(header_data, colWidths=[5 * cm, 13 * cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (1, 0), "LEFT"),
    ]))
    story.append(t)
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY))
    story.append(Spacer(1, 0.3 * cm))

    # ── Info del crédito ─────────────────────────────────
    sistema_label = "Sistema Francés (Cuota Fija)" if system == "frances" else "Sistema Alemán (Capital Constante)"
    info_style = ParagraphStyle("info", fontSize=9, fontName="Helvetica")
    bold_style = ParagraphStyle("bold", fontSize=9, fontName="Helvetica-Bold")

    info_table = [
        [Paragraph("<b>Cliente:</b>", info_style), Paragraph(client_name, info_style),
         Paragraph("<b>Tipo de Crédito:</b>", info_style), Paragraph(credit_type_name, info_style)],
        [Paragraph("<b>Monto:</b>", info_style), Paragraph(f"$ {amount:,.2f}", info_style),
         Paragraph("<b>Plazo:</b>", info_style), Paragraph(f"{term_months} meses", info_style)],
        [Paragraph("<b>Tasa Nominal Anual:</b>", info_style), Paragraph(f"{nominal_rate:.2f}%", info_style),
         Paragraph("<b>Sistema:</b>", info_style), Paragraph(sistema_label, info_style)],
    ]
    t2 = Table(info_table, colWidths=[4 * cm, 5.5 * cm, 4 * cm, 5 * cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ACCENT),
        ("BOX", (0, 0), (-1, -1), 0.5, PRIMARY),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.lightgrey),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [ACCENT, colors.white]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t2)
    story.append(Spacer(1, 0.4 * cm))

    # ── Tabla de amortización ────────────────────────────
    col_headers = ["N°", "Saldo Inicial", "Capital", "Interés"] + charge_names + ["Cuota Total", "Saldo Final"]
    table_data = [col_headers]
    for row in schedule:
        row_data = [
            str(row["period"]),
            f"$ {row['initial_balance']:,.2f}",
            f"$ {row['capital']:,.2f}",
            f"$ {row['interest']:,.2f}"
        ]
        for name in charge_names:
            row_data.append(f"$ {row['indirect_charges'].get(name, 0.0):,.2f}")
        row_data.extend([
            f"$ {row['total_payment']:,.2f}",
            f"$ {row['final_balance']:,.2f}"
        ])
        table_data.append(row_data)

    # Fila de totales
    totals_row = ["TOTAL", "", f"$ {total_capital:,.2f}", f"$ {total_interest:,.2f}"]
    for name in charge_names:
        totals_row.append(f"$ {total_charges_details.get(name, 0.0):,.2f}")
    totals_row.extend([f"$ {total_payment:,.2f}", ""])
    table_data.append(totals_row)

    # Ancho de columnas dinámico
    dynamic_width = (8.8 / (2 + len(charge_names))) * cm
    col_widths = [1 * cm, 2.7 * cm, dynamic_width, dynamic_width]
    for _ in charge_names:
        col_widths.append(dynamic_width)
    col_widths.extend([2.8 * cm, 2.7 * cm])
    
    t3 = Table(table_data, colWidths=col_widths, repeatRows=1)
    row_count = len(table_data)
    total_row = row_count - 1

    font_size_header = 8
    font_size_data = 7.5
    if len(charge_names) >= 3:
        font_size_header = 7.5
        font_size_data = 6.5
    if len(charge_names) >= 5:
        font_size_header = 6.5
        font_size_data = 5.5

    t3.setStyle(TableStyle([
        # Encabezado
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), HEADER_FG),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), font_size_header),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        # Datos
        ("FONTSIZE", (0, 1), (-1, total_row - 1), font_size_data),
        ("ALIGN", (0, 1), (0, -1), "CENTER"),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("ROWBACKGROUNDS", (0, 1), (-1, total_row - 1), [colors.white, ROW_ALT]),
        # Fila total
        ("BACKGROUND", (0, total_row), (-1, total_row), TOTAL_BG),
        ("TEXTCOLOR", (0, total_row), (-1, total_row), colors.white),
        ("FONTNAME", (0, total_row), (-1, total_row), "Helvetica-Bold"),
        ("FONTSIZE", (0, total_row), (-1, total_row), font_size_header),
        # Bordes
        ("BOX", (0, 0), (-1, -1), 0.5, PRIMARY),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(t3)
    story.append(Spacer(1, 0.5 * cm))

    # ── Pie de página ────────────────────────────────────
    note_style = ParagraphStyle("nota", fontSize=7, textColor=colors.gray, alignment=TA_LEFT)
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.lightgrey))
    story.append(Paragraph(
        "* Los valores presentados son referenciales. Consulte con su asesor para condiciones definitivas.",
        note_style
    ))

    doc.build(story)
    return buffer.getvalue()


def generar_pdf_inversion(
    institution_name: str,
    institution_logo: Optional[str],
    investment_type_name: str,
    client_name: str,
    amount: float,
    term_days: int,
    annual_rate: float,
    gross_interest: float,
    ir_retention: float,
    net_interest: float,
    total_at_maturity: float,
) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2 * cm, leftMargin=2 * cm,
                            topMargin=2 * cm, bottomMargin=2 * cm)
    styles = getSampleStyleSheet()
    story = []

    title_style = ParagraphStyle("t", fontSize=18, fontName="Helvetica-Bold",
                                 textColor=PRIMARY, alignment=TA_CENTER)
    sub_style = ParagraphStyle("s", fontSize=10, textColor=colors.gray, alignment=TA_CENTER)

    story.append(Paragraph(institution_name, title_style))
    story.append(Paragraph("Resumen de Simulación de Inversión", sub_style))
    story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY))
    story.append(Spacer(1, 0.5 * cm))

    data = [
        ["Detalle", "Valor"],
        ["Cliente", client_name],
        ["Tipo de Inversión", investment_type_name],
        ["Capital Invertido", f"$ {amount:,.2f}"],
        ["Plazo", f"{term_days} días"],
        ["Tasa Anual", f"{annual_rate:.2f}%"],
        ["Interés Bruto", f"$ {gross_interest:,.2f}"],
        ["Retención IR", f"$ {ir_retention:,.2f}"],
        ["Interés Neto", f"$ {net_interest:,.2f}"],
        ["Total al Vencimiento", f"$ {total_at_maturity:,.2f}"],
    ]

    t = Table(data, colWidths=[9 * cm, 8 * cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [colors.white, ACCENT]),
        ("BACKGROUND", (0, -1), (-1, -1), SECONDARY),
        ("TEXTCOLOR", (0, -1), (-1, -1), colors.white),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BOX", (0, 0), (-1, -1), 1, PRIMARY),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(t)

    doc.build(story)
    return buffer.getvalue()
