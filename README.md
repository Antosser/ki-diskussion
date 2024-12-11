# KI-Diskussion-Generator

Dieses Projekt ermöglicht es, ein Gespräch zwischen zwei Positionen (Pro und Contra) zu einem gegebenen Thema mit der GPT-4 API von OpenAI zu generieren und dieses Gespräch anschließend mit der Google Cloud Text-to-Speech API in Sprache umzuwandeln. Das Projekt besteht aus zwei Hauptskripten: `text.py` und `voice.py`, sowie einer `.env`-Datei, die API-Schlüssel sicher speichert.

## Dateien

- `text.py`: Dieses Skript erzeugt ein Gespräch zwischen zwei Positionen (Pro und Contra) mithilfe der GPT-4 API von OpenAI. Das Gespräch wird als Textdatei im Verzeichnis `generated_text` gespeichert.
- `voice.py`: Dieses Skript liest das erzeugte Gespräch, wandelt es mit der Google Cloud Text-to-Speech API in Sprache um und kombiniert die Audiodateien mit einer 2-Sekunden-Pause zwischen jedem Segment.
- `.env`: Diese Datei speichert sensible Umgebungsvariablen wie den OpenAI API-Schlüssel und Google Cloud Service Account-Anmeldeinformationen.

## Anforderungen

- Python 3.x
- Python-Pakete: `openai`, `gtts`, `google-cloud-texttospeech`, `pydub`, `dotenv`
- Google Cloud Text-to-Speech API-Anmeldeinformationen (Service Account-Datei)

### Installiere die benötigten Pakete

Installiere die benötigten Abhängigkeiten, indem du den folgenden Befehl ausführst:

```bash
pip install -r requirements.txt
```

### Setup der `.env`-Datei

Erstelle eine `.env`-Datei im Projektstammverzeichnis mit folgendem Inhalt:

```
OPENAI_API_KEY=dein_openai_api_schluessel_hier
GOOGLE_APPLICATION_CREDENTIALS=pfad_zu_deiner_google_service_account_json
```

Stelle sicher, dass du die Platzhalter mit deinem tatsächlichen OpenAI API-Schlüssel und dem Pfad zu deiner Google Cloud Service Account JSON-Datei ersetzt.

## Verwendung

### 1. Generiere das Gespräch (`text.py`)

Führe das Skript `text.py` aus, um ein Gespräch zwischen zwei Positionen zu einem bestimmten Thema zu generieren.

```bash
python text.py
```

#### Eingaben

- `Thema`: Gib das Thema des Gesprächs ein (z. B. "Künstliche Intelligenz").
- `Iterationen`: Gib die Anzahl der Iterationen ein, um das Gespräch zu generieren. Das Gespräch wechselt abwechselnd zwischen den Positionen "Pro" und "Contra".

Das Gespräch wird als `.txt`-Datei im Verzeichnis `generated_text` gespeichert.

### 2. Konvertiere das Gespräch in Sprache (`voice.py`)

Nachdem das Gespräch generiert und gespeichert wurde, kannst du es mit `voice.py` in Sprache umwandeln.

```bash
python voice.py <pfad_zur_generierten_textdatei>
```

Die generierte Sprache wird als einzelne MP3-Dateien für jeden Dialog im Verzeichnis `generated_audio` gespeichert, gefolgt von einer kombinierten Audiodatei (`combined_output.mp3`), bei der zwischen den Segmenten eine 2-Sekunden-Pause eingefügt wird.

### Beispielablauf

1. Führe `text.py` aus und gib die erforderlichen Eingaben für das Thema und die Iterationen ein.
2. Überprüfe das Verzeichnis `generated_text` auf die ausgegebene `.txt`-Datei mit dem Gespräch.
3. Führe `voice.py` mit dem Pfad zur Gesprächs-Textdatei aus, um die entsprechende Sprachdatei zu generieren.
4. Überprüfe das Verzeichnis `generated_audio` auf die einzelnen und kombinierten Audiodateien.

## Fehlerbehandlung

Beide Skripte beinhalten eine Fehlerbehandlung für häufige Probleme wie fehlende API-Schlüssel, nicht gefundene Dateien oder Berechtigungsprobleme. Achte darauf, etwaige Fehlermeldungen, die im Terminal ausgegeben werden, zur Fehlerbehebung zu überprüfen.

## Lizenz

Dieses Projekt ist unter der GPLv3-Lizenz lizenziert. Siehe die [LICENSE](LICENSE)-Datei für Details.

---

Du kannst dieses Projekt nach Belieben anpassen und erweitern. Wenn du auf Probleme stößt oder Fragen hast, eröffne ein Issue auf GitHub!
