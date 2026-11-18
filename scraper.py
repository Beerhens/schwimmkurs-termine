import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests

# HIER DIE URL DER SCHWIMMSCHULE EINTRAGEN
URL = "https://beispiel-schwimmschule.de/termine"


def scrape_termine():
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(URL, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # WICHTIG: Hier muss der CSS-Selektor der Schwimmschule rein!
    # Beispiel: Wenn die Termine in einer Tabelle oder einem bestimmten <div> stehen.
    # Aktuell zieht das Skript zum Testen alle Absätze (<p>) mit dem Wort "Schwimm" oder "Termin".
    gefundene_texte = []
    for element in soup.find_all(["p", "li", "td", "h2", "h3"]):
        text = element.get_text(strip=True)
        if text and len(text) > 10:  # Filtert leere oder zu kurze Schnipsel
            gefundene_texte.append(text)

    # Zeitstempel der letzten Prüfung
    jetzt = datetime.now().strftime("%d.%m.%Y um %H:%M Uhr")

    daten = {
        "letztes_update": jetzt,
        "quelle": URL,
        "inhalte": gefundene_texte[:30],  # Begrenzt auf die ersten 30 Treffer
    }

    with open("daten.json", "w", encoding="utf-8") as f:
        json.dump(daten, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    scrape_termine()
