# Image Captioning für Webseiten mit Gemini Flash Lite

Dieses Projekt extrahiert Bilder von einer Webseite und generiert automatische Bildbeschreibungen (Captions) mit Google Gemini Flash Lite.

## Voraussetzungen
- Python 3.10+
- Abhängigkeiten: siehe `requirements.txt`
- Ein Gemini API Key (siehe `https://ai.google.dev`)

## Installation
```bash
# 1) Virtuelle Umgebung (optional)
python -m venv myvenv
source myvenv/bin/activate  # Windows: myvenv\\Scripts\\activate

# 2) Abhängigkeiten installieren
pip install -r requirements.txt

# 3) Umgebungsvariable setzen (oder .env nutzen)
export GEMINI_API_KEY=dein_api_key
# Alternativ: .env anlegen (siehe .env.example) und z.B. mit deinem Shell-Profil laden
```

## Nutzung
```bash
python image_captioning_gemini.py
```
- Ergebnisse werden in `captions.txt` gespeichert.
- Standard-URL ist Wikipedia/IBM. Die URL kannst du im Skript anpassen (Variable `url`).

## Hinweise zu Rate Limits
Die Free‑Tier Gemini API ist auf ca. 15 Requests/Minute limitiert. Bei `429 RESOURCE_EXHAUSTED`:
- kurz warten und erneut ausführen,
- Requests drosseln,
- oder auf einen höheren Plan upgraden.
