import io
import json
from datetime import datetime
import pypdf
import requests

# Deine genaue PDF-URL vom Kinder Spiel und Sportverein
URL = "https://www.kinder-spiel-sport.de/_files/ugd/31658f_2b15e23129c54e288026535582d71e44.pdf"


def scrape_pdf_termine():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    # PDF aus dem Binärstrom im Arbeitsspeicher lesen
    pdf_file = io.BytesIO(response.content)
    reader = pypdf.PdfReader(pdf_file)

    alle_zeilen = []

    # Jede Seite des PDFs durchgehen
    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            # Zeilenweise auftrennen und leere Zeilen filtern
            for line in text.split("\n"):
                clean_line = line.strip()
                if clean_line:
                    alle_zeilen.append(clean_line)

    jetzt = datetime.now().strftime("%d.%m.%Y um %H:%M Uhr")

    daten = {
        "letztes_update": jetzt,
        "quelle": URL,
        "inhalte": alle_zeilen,  # Enthält den gesamten Text des PDF-Terminplans
    }

    with open("daten.json", "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    scrape_pdf_termine()
