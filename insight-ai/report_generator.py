from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf_report(result: dict) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("Insight AI - Public Document Analysis Report", styles["Title"]))
    story.append(Spacer(1, 12))

    story.append(Paragraph("Simple Summary", styles["Heading2"]))
    story.append(Paragraph(result.get("simple_summary", ""), styles["Normal"]))
    story.append(Spacer(1, 12))

    def add_list_section(title, items):
        story.append(Paragraph(title, styles["Heading2"]))
        if items:
            story.append(ListFlowable([
                ListItem(Paragraph(str(item), styles["Normal"])) for item in items
            ]))
        else:
            story.append(Paragraph("No items identified.", styles["Normal"]))
        story.append(Spacer(1, 12))

    add_list_section("Key Decisions", result.get("key_decisions", []))
    add_list_section("Risks", result.get("risks", []))

    story.append(Paragraph("Public Impact", styles["Heading2"]))
    story.append(Paragraph(result.get("public_impact", ""), styles["Normal"]))
    story.append(Spacer(1, 12))

    add_list_section("What It Means for Residents", result.get("what_it_means_for_residents", []))
    add_list_section("Recommended Actions", result.get("recommended_actions", []))

    doc.build(story)
    buffer.seek(0)

    return buffer