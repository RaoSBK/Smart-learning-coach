from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from datetime import datetime


class PDFExporter:
    
    @staticmethod
    def export_summary_to_pdf(summary_json: dict, metadata: dict, filename="video_summary.pdf"):
        """
        Save AI summary (JSON) + metadata into a clean PDF.
        """

        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        x = 50
        y = height - 50

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(x, y, f"Video Summary: {metadata.get('title', 'Unknown Title')}")
        y -= 30

        # Date
        c.setFont("Helvetica", 10)
        c.drawString(x, y, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        y -= 20

        # Section function
        def draw_section(title, text, spacing=14):
            nonlocal y
            if y < 80:  # new page
                c.showPage()
                y = height - 50

            c.setFont("Helvetica-Bold", 13)
            c.drawString(x, y, title)
            y -= 18

            c.setFont("Helvetica", 11)
            wrapped = simpleSplit(text, "Helvetica", 11, width - 100)
            for line in wrapped:
                if y < 50:
                    c.showPage()
                    y = height - 50
                c.drawString(x, y, line)
                y -= spacing

            y -= 10  # extra spacing

        # Add sections
        draw_section("Short Summary:", summary_json.get("short_summary", ""))
        draw_section("Detailed Summary:", summary_json.get("detailed_summary", ""))

        # Key Points
        key_points = "\n".join([f"- {kp}" for kp in summary_json.get("key_points", [])])
        draw_section("Key Points:", key_points)

        # Study Notes
        study_notes = "\n".join([f"- {n}" for n in summary_json.get("study_notes", [])])
        draw_section("Study Notes:", study_notes)

        # Chapters
        chapters = "\n".join([f"- {ch}" for ch in summary_json.get("chapters", [])])
        draw_section("Chapters:", chapters)

        # Tags
        tags = ", ".join(summary_json.get("tags", []))
        draw_section("Tags:", tags)

        # Save PDF
        c.save()
        return filename
