from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

def generate_report(filename, score, strength, matched, missing, suggestions):

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>Resume Analysis Report</b>", styles["Title"]))

    story.append(Paragraph(f"<b>Match Score:</b> {score}%", styles["BodyText"]))
    story.append(Paragraph(f"<b>Resume Strength:</b> {strength}", styles["BodyText"]))

    story.append(Paragraph("<br/><b>Matched Skills</b>", styles["Heading2"]))
    for skill in matched:
        story.append(Paragraph(f"• {skill}", styles["BodyText"]))

    story.append(Paragraph("<br/><b>Missing Skills</b>", styles["Heading2"]))
    for skill in missing:
        story.append(Paragraph(f"• {skill}", styles["BodyText"]))

    story.append(Paragraph("<br/><b>Suggestions</b>", styles["Heading2"]))
    for suggestion in suggestions:
        story.append(Paragraph(f"• {suggestion}", styles["BodyText"]))

    doc.build(story)