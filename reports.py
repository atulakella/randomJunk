from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
import io

def generate_pdf(name, age, relaxed_freq, stressed_freq, active_freq):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "TEST REPORTS")
    c.drawString(50, height - 80, "COGNILIFT.AI")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 120, f"Name: {name}")
    c.drawString(50, height - 140, f"Age: {age}")
    c.drawString(50, height - 160, f"Date and Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.drawString(50, height - 200, "Frequency Analysis:")
    y = height - 220
    for state, freq in [("Relaxed", relaxed_freq), ("Stressed", stressed_freq), ("Active", active_freq)]:
        c.drawString(70, y, f"{state} State:")
        y -= 20
        for band, value in freq.items():
            c.drawString(90, y, f"{band}: {value:.4f}")
            y -= 20
        y -= 10

    c.setFont("Helvetica-Bold", 18)
    c.drawString(50, y - 40, "cognilift")
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer