from reportlab.pdfgen import canvas
import os

def fetch_case_details(case_type, case_number, year):
    # Dummy data for testing
    return {
        "parties": "Party A vs Party B",
        "filing_date": "2023-01-01",
        "next_hearing_date": "2023-12-01",
        "status": "Pending"
    }

def download_judgement(case_type, case_number, year):
    filename = f"judgement_{case_type}{case_number}{year}.pdf"
    filepath = os.path.abspath(filename)
    c = canvas.Canvas(filepath)
    c.drawString(100, 750, f"Judgement for {case_type}-{case_number}/{year}")
    c.drawString(100, 730, "Status: Pending")
    c.save()
    return filepath
