# Anleitung: SharePoint & Microsoft Power Automate Setup

Diese Anleitung führt dich Schritt für Schritt durch das Einrichten der SharePoint-Liste und das manuelle Erstellen des Flows in Power Automate (Microsoft Flow), basierend auf euren genauen Anforderungen und der hochgeladenen CSV-Struktur.

---

## 1. SharePoint-Liste "Report Processing Log" erstellen

Deine Liste soll exakt die Spaltennamen aus der Datei `src/report_template/Report Processing Log (1).csv` verwenden.

### Schritt-für-Schritt-Erstellung über CSV-Import:
1. Öffne deine SharePoint-Seite: [ISAAIDailyReportProcessing](https://studfrauasde.sharepoint.com/sites/ISAAIDailyReportProcessing).
2. Klicke auf **Neu** (New) -> **Liste** (List).
3. Wähle **Aus CSV** (From CSV) aus.
4. Klicke auf **Datei hochladen** und wähle die Datei `src/report_template/Report Processing Log (1).csv` aus deinem lokalen Git-Repository aus.
5. SharePoint liest die Spaltennamen automatisch ein. Überprüfe die Spaltentypen in der Vorschau:
   - **Titel**: Einzeiliger Text (Single line of text) - *Wird als Hauptspalte (Title) verwendet*.
   - **ReceivedDateTime**: Datum und Uhrzeit (Date and Time).
   - **SenderEmail**: Einzeiliger Text.
   - **ReportDate**: Datum und Uhrzeit (oder Nur Datum).
   - **ReportA_Status** & **ReportB_Status**: Choice (Auswahl) mit den Optionen: `Pass`, `Violation`, `Error`, `Pending`.
   - **ReportA_ViolationDetails** & **ReportB_ViolationDetails**: Mehrzeiliger Text (Multiple lines of text).
   - **OverallStatus**: Choice mit den Optionen: `Completed`, `Exception`, `Processing`, `Failed`.
   - **ExceptionFlag**: Ja/Nein (Yes/No) oder Einzeiliger Text.
   - **EvidenceA_Link**, **EvidenceB_Link**, **Presentation_Link**: Hyperlink.
6. Benenne die Liste **Report Processing Log** und klicke auf **Erstellen**.

---

## 2. SharePoint-Bibliothek für Dateien vorbereiten

Erstelle in SharePoint eine Dokumentenbibliothek namens **Evidence Archive** und lege folgende Ordnerstrukturen an:
- `Evidence Archive/Templates/` -> Lade hier deine PowerPoint-Vorlage `daily_run_template.pptx` hoch.
- `Evidence Archive/Presentations/` -> Hier speichert Power Automate die erstellten Präsentationen ab.
- `Evidence Archive/Evidence/` -> Hier werden die Excel-Nachweisdateien gespeichert.

---

## 3. Power Automate Flow manuell aufbauen

Da der Copilot-Import bei komplexen verzweigten Flows Fehler wirft, baue den Flow im Power Automate-Designer Schritt für Schritt wie folgt auf:

### Phase A: Trigger & Variablen initialisieren
1. **Trigger**: *Wenn eine neue E-Mail eintrifft (V3)* (Outlook).
   - **Ordner**: `Posteingang` (Inbox).
   - **Betreff-Filter**: `Financial Report`.
   - **Nur mit Anlagen**: `Ja`.
   - **Anlagen einschließen**: `Ja`.
2. **Aktion**: *Variable initialisieren* `LogItemID` (Typ: `Ganzzahl`).
3. **Aktion**: *Variable initialisieren* `ReportDate` (Typ: `Zeichenfolge`).
   - Wert (Expression): `substring(triggerOutputs()?['body/attachments'][0]['name'], 0, 8)`
4. **Aktion**: *Variable initialisieren* `ReportA_Result` (Typ: `Zeichenfolge`, Standard: `Pass`).
5. **Aktion**: *Variable initialisieren* `ReportB_Result` (Typ: `Zeichenfolge`, Standard: `Pass`).
6. **Aktion**: *Variable initialisieren* `ReportA_Details` (Typ: `Zeichenfolge`, Standard: `Keine Verletzung gefunden`).
7. **Aktion**: *Variable initialisieren* `ReportB_Details` (Typ: `Zeichenfolge`, Standard: `Keine Verletzung gefunden`).

### Phase B: Zeile in SharePoint-Liste anlegen
1. **Aktion**: *Element erstellen* (SharePoint -> `Report Processing Log`).
   - **Titel**: `@triggerOutputs()?['body/subject']`
   - **ReceivedDateTime**: `@triggerOutputs()?['body/receivedDateTime']`
   - **SenderEmail**: `@triggerOutputs()?['body/from']`
   - **OverallStatus**: `Processing`
   - **ExceptionFlag**: `No`
2. **Aktion**: *Variable festlegen* `LogItemID`.
   - **Wert**: `@outputs('Element_erstellen')?['body/ID']` (die ID der neu erstellten Tabellenzeile).

### Phase C: Zip-Anhang entpacken & XML auslesen
1. **Aktion**: *Auf alle anwenden* (Apply to each) -> Loop über E-Mail-Anhänge: `triggerOutputs()?['body/attachments']`.
2. **Aktion (im Loop)**: *Bedingung* -> Überprüfe, ob der Anhang eine ZIP-Datei ist (z. B. Dateiname endet auf `.zip`).
3. **Im Ja-Zweig**:
   - **Aktion**: *Archiv in Ordner extrahieren* (OneDrive für Business).
     - **Archivdatei-Inhalt**: `Anlage Inhalt` (Attachment Content).
     - **Zielordnerpfad**: `/Evidence Archive/Temp/`.
   - **Aktion**: *Dateiinhalte abrufen* (SharePoint oder OneDrive) für die extrahierten XML-Dateien:
     - Finde die Datei `*ReportTypeA.xml` und lies den Text in eine Compose-Aktion `XML_A_Inhalt`.
     - Finde die Datei `*ReportTypeB.xml` und lies den Text in eine Compose-Aktion `XML_B_Inhalt`.

### Phase D: Parallele Validierung
Erstelle eine **Parallele Verzweigung** (Parallel Branch) nach dem Schließen des Attachment-Loops:

#### Linker Ast (Report Type A)
1. **Aktion**: *Verfassen* (Compose) -> `MarkerA`.
   - Wert (Expression): `xpath(xml(outputs('XML_A_Inhalt')), 'string(/Report/Data/Row/ViolationMarker)')`
2. **Aktion**: *Bedingung* -> Prüfe, ob `MarkerA` gleich `V` ist.
3. **Im Ja-Zweig (Verletzungsprüfung)**:
   - Lies die vier Schwellenwerte aus (Threshold1 bis Threshold4) mit XPath-Konvertierungen zu Ganzzahlen. Beispiel für Threshold1:
     `int(xpath(xml(outputs('XML_A_Inhalt')), 'string(/Report/Data/Row/Threshold1)'))`
   - Wenn ein Wert **kleiner als 50** ist:
     - Setze Variable `ReportA_Result` = `Violation`.
     - Setze Variable `ReportA_Details` = *Details der Verletzung*.

#### Rechter Ast (Report Type B)
Führe dieselben Schritte analog für `XML_B_Inhalt` aus und setze `ReportB_Result` sowie `ReportB_Details`.

### Phase E: Excel-Nachweis & PowerPoint-Erstellung
Nachdem die parallelen Zweige zusammengeführt wurden:
1. **Aktion**: *Skript ausführen* (Excel Online).
   - Führe euer Office Script aus, um die Zeilen und Ergebnisse in `evidence_log.xlsx` zu schreiben.
2. **Aktion**: *Datei kopieren* (SharePoint).
   - **Quelle**: `/Evidence Archive/Templates/daily_run_template.pptx`
   - **Ziel**: `/Evidence Archive/Presentations/`
   - **Neuer Name**: `concat(variables('ReportDate'), '_Run_Summary.pptx')`
3. **Aktion**: *Präsentation aus Vorlage erstellen* (PowerPoint Online).
   - Wähle die kopierte Präsentation aus.
   - Trage die Variablen in die erkannten Tags ein:
     - `{{ReportDate}}` -> `variables('ReportDate')`
     - `{{ReportA_Status}}` -> `variables('ReportA_Result')`
     - `{{ReportB_Status}}` -> `variables('ReportB_Result')`
     - `{{ReportA_Details}}` -> `variables('ReportA_Details')`
     - `{{ReportB_Details}}` -> `variables('ReportB_Details')`

### Phase F: Exception Gate & Abschluss
1. **Aktion**: *Bedingung* -> Ist `ReportA_Result` gleich `Violation` ODER `ReportB_Result` gleich `Violation`?
2. **Im Ja-Zweig (Verstoß vorliegend)**:
   - **Aktion**: *Element aktualisieren* (SharePoint `Report Processing Log` mit `LogItemID`):
     - `OverallStatus`: `Exception`
     - `ExceptionFlag`: `Yes`
     - `EvidenceA_Link`, `EvidenceB_Link`, `Presentation_Link` -> Links zu den erstellten Dateien.
   - **Aktion**: *E-Mail senden (V2)* (An Supervisor, Wichtigkeit: Hoch) mit den Links zu den Excel- und PowerPoint-Dateien.
3. **Im Nein-Zweig (Keine Fehler)**:
   - **Aktion**: *Element aktualisieren* (SharePoint `Report Processing Log` mit `LogItemID`):
     - `OverallStatus`: `Completed`
     - `EvidenceA_Link`, `EvidenceB_Link`, `Presentation_Link` -> Links zu den Dateien.
   - **Aktion**: *E-Mail senden (V2)* (An Standard-Verteiler) mit Excel- und PowerPoint-Anlagen.
   - **Aktion**: E-Mail als `.eml` exportieren und in SharePoint sichern.
