# Modellierung in Archi oeffnen und importieren

Diese Abgabe enthaelt zwei empfohlene Hauptdateien fuer Archi:

- `report-processing-ist.archimate`
- `report-processing-soll.archimate`

Dazu kommen CSV-Snapshots fuer IST und SOLL:

- `report-processing-ist-elements.csv`
- `report-processing-ist-relations.csv`
- `report-processing-soll-elements.csv`
- `report-processing-soll-relations.csv`

## Empfohlener Weg: native `.archimate`-Dateien oeffnen

Das ist der beste Weg, wenn du die fertigen Views, das Layout und die saubere Diagrammstruktur direkt sehen willst.

1. Starte `Archi`.
2. Gehe auf `File > Open...`.
3. Waehle zuerst `report-processing-ist.archimate` im Projektordner aus.
4. Nach dem Oeffnen findest du links im Modellbaum den Ordner `Views`.
5. Oeffne die IST-Views per Doppelklick.
6. Wiederhole denselben Schritt fuer `report-processing-soll.archimate`.
7. Im SOLL-Modell oeffnest du ebenfalls die Views im Ordner `Views`.

Wichtig:

- Fuer `.archimate` nutzt du in Archi `Open`, nicht `Import`.
- Die nativen Dateien enthalten bereits Modellstruktur, Relationen und vorbereitete Diagramm-Views.

## Alternativer Weg: CSV in ein neues Archi-Modell importieren

Das ist nur dann sinnvoll, wenn du das Modell aus CSV selbst in Archi rekonstruieren oder pruefen willst.

### IST per CSV importieren

1. Starte `Archi`.
2. Gehe auf `File > New Model` und lege ein leeres Modell an.
3. Speichere das leere Modell optional zuerst unter einem Namen wie `Report-IST-CSV.archimate`.
4. Gehe auf `File > Import > CSV...`.
5. Waehle als Elements-Datei `report-processing-ist-elements.csv`.
6. Waehle als Relations-Datei `report-processing-ist-relations.csv`.
7. Falls Archi nach einer Properties-Datei fragt und diese optional ist, lasse sie leer oder ueberspringe sie.
8. Fuehre den Import aus.
9. Pruefe danach im Modellbaum, ob die Elemente in den Layer-Ordnern und die Beziehungen unter `Relations` sichtbar sind.

### SOLL per CSV importieren

1. Erstelle wieder ein neues leeres Modell.
2. Gehe auf `File > Import > CSV...`.
3. Waehle `report-processing-soll-elements.csv` als Elements-Datei.
4. Waehle `report-processing-soll-relations.csv` als Relations-Datei.
5. Fuehre den Import aus.
6. Pruefe anschliessend den Modellbaum.

Wichtig bei CSV:

- Der CSV-Import bringt dir Modellinhalte und Beziehungen, aber nicht automatisch dieselben fertig gestalteten Views wie die nativen `.archimate`-Dateien.
- Wenn du ueber CSV importierst, musst du die Views in Archi selbst anlegen oder die nativen `.archimate`-Dateien als visuelle Referenz benutzen.

## Nach dem Oeffnen in Archi pruefst du am besten diese Punkte

1. Links im Modellbaum sind `Business`, `Application`, `Technology & Physical`, `Relations` und `Views` sichtbar.
2. In den nativen Modellen lassen sich die Views per Doppelklick oeffnen.
3. Im IST-Modell ist der manuelle Ablauf mit Mail, ZIP, Excel, SharePoint und DMS sichtbar.
4. Im SOLL-Modell sind Automation Engine, Scheduler, Rule Evaluator, SharePoint Connector, DMS UI-Scraper und Exception Governance sichtbar.
5. Der DMS UI-Scraper ist im SOLL-Modell explizit vorhanden. Das ist fuer die Seminaranforderung zentral.

## Wenn in Archi etwas nicht sichtbar ist

1. Wenn das Modell geoeffnet ist, aber kein Diagramm sichtbar wird, oeffne den Ordner `Views` im Modellbaum und starte die View manuell per Doppelklick.
2. Wenn beim CSV-Import nur Elemente erscheinen, ist das normal. CSV importiert kein fertiges Diagrammlayout wie die nativen `.archimate`-Dateien.
3. Wenn Archi einen Header-Fehler meldet, wurde wahrscheinlich nicht die passende Elements- oder Relations-Datei gewaehlt.
4. Wenn Beziehungen fehlen, pruefe zuerst, ob die richtige CSV-Datei zum richtigen Zustand gehoert, also IST zu IST und SOLL zu SOLL.

## Empfehlung fuer die Abgabe

Fuer Vorfuehrung, Review und Bewertung solltest du primaer die beiden nativen `.archimate`-Dateien verwenden. Die CSV-Dateien sind ideal als technische Nachweise und fuer einen zusaetzlichen Import-Check, aber nicht die beste Primaersicht fuer die Praesentation.