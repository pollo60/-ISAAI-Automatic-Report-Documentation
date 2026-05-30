Bericht: Validierung täglicher Finanzberichte (IST-Prozess)

1. Management Summary

Der aktuelle Prozess zur Validierung der Finanzberichte (Report A und Report B) ist ein rein manueller, zeitkritischer Ablauf mit hoher repetitiver Last. Die Bearbeitung erfolgt sequenziell durch einen Operations Analysten und umfasst den Datentransfer zwischen heterogenen Systemen (Outlook, Excel, SharePoint, DMS). Aufgrund der manuellen Dateneingabe und der komplexen Datei-Nomenklatur besteht eine erhöhte Anfälligkeit für Übertragungsfehler und Verzögerungen bei der Archivierung.

2. Detaillierter Prozessablauf (Schritt-für-Schritt)

Phase 1: Input & Datenextraktion

Eingangsprüfung: Der Prozess startet im Company Mail System (Outlook). Täglich wird der Eingang einer E-Mail der Abteilung Compliance Operations verifiziert, die die Berichte Report A (DailyViol) und Report B (MonthlyViol) als ZIP-Anhänge enthält.

Download: Die ZIP-Dateien werden lokal auf die Arbeitsstation heruntergeladen.

Extraktion: Aus den ZIP-Archiven wird jeweils eine XML-Datei extrahiert. Diese Dateien tragen einen alphanumerischen Code als Namen, der kryptisch aufgebaut ist, aber das Berichtsdatum enthält.

Phase 2: Aufbereitung & Validierung (Excel)

Datenimport: Die extrahierten XML-Dateien werden manuell via Drag-and-Drop in Microsoft Excel importiert, um die Rohdaten in eine tabellarische Struktur zu transformieren.

Business Logic Check: Innerhalb der Excel-Tabellen führt der Analyst eine manuelle Sichtprüfung spezifischer Spalten durch:

Prüfung auf Violations (gekennzeichnet durch einen Marker "V").

Verifizierung, ob Grenzwerte (z. B. Werte < 90) unterschritten werden.

Bericht-Typ-Trennung: Dieser Schritt wird für Report A (täglich) und Report B (monatlich) identisch durchgeführt, wobei die Berichte aufgrund der unterschiedlichen Regelwerke nacheinander bearbeitet werden.

Phase 3: Dokumentation & Kommunikation (SharePoint)

Sicherung der Evidence: Die validierten Daten werden als .xlsx-Dateien im SharePoint-Ordner REPORTING gespeichert.

Nomenklatur-Regel: Der Dateiname wird manuell auf das Datum des letzten Werktages angepasst (Format: YYYYMMDD_Typ).

Distribution: Eine Zusammenfassungs-E-Mail mit beiden Excel-Tabellen im Anhang wird an die Kontaktpersonen im Bereich Investment, Finance, Germany versendet.

Mailing-Archiv: Die versendete Mail wird manuell als .msg-Datei im SharePoint-Ordner MAILING abgelegt.

Phase 4: Governance & Archivierung (DMS)

System-Login: Zugriff auf das unternehmensweite Database Management System (DMS).

Navigation: Navigieren zum Bereich Supervisor Reviews -> Monatstafel -> Zeile Regulatory -> Sponsor Review.

Identifikation: Der Analyst hinterlegt sein individuelles Kürzel für den aktuellen Bearbeitungstag.

Upload & Verknüpfung: Innerhalb der Tageskachel werden zwei Dokumente hochgeladen:

Die zuvor im SharePoint gespeicherte .msg-Datei der Berichte.

Der Bericht der Opening Quotas (ebenfalls als .msg-Datei aus dem MAILING-Ordner).

Sign-Off: Nach vollständigem Upload erfolgt der finale "Sign-Off" (unwiderruflich).

Terminierung: Logout aus dem DMS und Beendigung der Session.

3. Architectural Reasoning (Unit Mapping)

Unit 1 (Analysis Modeling): Die manuelle Kopplung von SharePoint (Dateisystem) und DMS (Datenbank) stellt einen Medienbruch dar, der die Prozessintegrität gefährdet.

Unit 2 (API States): Der Übergang von Schritt 13 zu 14 (Upload zu Sign-Off) ist ein kritischer State-Change. Im IST-Zustand ist dieser nicht durch System-Constraints abgesichert, sondern beruht auf menschlicher Sorgfalt.

Unit 13 (Technical Hygiene): Der hohe Anteil an manueller Nomenklatur-Anpassung ("Naming Convention Friction") bietet das größte Potenzial für eine Automatisierung durch den "Automated Reporting Service".

4. Risiken & Schwachstellen

Fehlerquelle Nomenklatur: Manuelle Datumsanpassungen bei Dateinamen führen häufig zu Inkonsistenzen im Archiv.

Single Point of Failure: Der Prozess ist stark personenabhängig (Kürzel-Eingabe).

Archivierungs-Gap: Die Zeitspanne zwischen E-Mail-Versand und DMS-Upload ist eine Phase ungesicherter Datenintegrität.