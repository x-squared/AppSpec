# Feature-of [TPLK]: Koordination von Organspenden

Feature-Datei: `TPLK-Koordination-Transplantation.md`

## Use Case: {process} Koordination [Spec]

### Story: {structure} Phasen einer Koordination [Spec]
Eine Koordination besteht aus diesen Phasen:
1. Koordination: Ein Organangebot wird auf Empfänger zugewiesen.
2. Abschluss [EN: Completion]: Nacharbeit bis zum Abschluss der Koordination.

### Story: {data} Daten der Koordination [Spec]

#### Item: {data, structure} Struktur des Datenmodells [Spec]
Das Datenmodell umfasst diese Aspekte:
- Koordination: Basis mit allen relevanten Daten der Koordination.
- Event Log: Alle Ereignisse, die zu dem Protokoll erfasst werden.
- Spender [EN: Donor]: Daten zum Spender.
- Join auf Episode: Für die Zuteilung der Organe auf Empfänger.
- Herkunft: Beschreibt die Spitäler, von denen der Spender kommt.
- Zeiterfassung: Zeiterfassung durch Koordinatoren, die an der Koordination arbeiten.
- Procurement Effekt: Beschreibt, wie mit dem Organ grundsätzlich verfahren wurde.
- Procurement (mehrere Entitäen): Informationen zu Explantationen und zu den angenommenen Organen.

#### Item: {data} Daten der Koordination [Spec]
TODO

#### Item: {data} Daten des Event Logs [Spec]
TODO

#### Item: {data} Zeiterfassung [Spec]
TODO

#### Item: {data} Daten des Spenders [Spec]
- INTERNAL_NR (string 12): Interner Identifikator.
- 

#### Item: {data} Zuordnung zu Episoden [Spec]
TODO

#### Item: {data} Herkunft der Spende [Spec]
TODO

#### Item: {data} Daten des Procurements [Spec]
TODO



### Story:{view} View Koordination [Spec]

#### Item: {view} Übersicht [Spec]
Die Übersicht zeigt alle laufenden Koordinationen. Nach Auswahl einer Koordination, wird diese mit allen relevanten Tabs angezeigt.

#### Item: {tab} Koordination [Spec]
Das Tab umfasst alle Grunddaten der Koordination und eine Übersicht über das Koordinationsprotokoll.

#### Item: {tab} Koordinationsprotokoll [Spec]
Das Tab enthält die Aufzeichnung aller Daten, die beieiner Koordination erfasst werden (ausser den Grunddaten auf im ersten Tab).

#### Item: {tab} Abschluss [Spec]
Das Tab umfasst alle Informationen zu den Abschlussarbeiten einer Koordination. Hier wird die Koordination auch defintiv als abgeschlossen erfasst.

#### Item: {tab} Zeiterfassung [EN: Time Log] [Spec]
Zeit die Übersicht über die Zeiterfassung.

### Story: Koordination starten [Spec]

#### Item: {function} Globaler Start-Button [Spec]
In der Navigation wird ein Button angezeigt, über den eine Koordination gestartet wird.
- Der Button soll visuell als "Emergency-Kopf" gestaltet sein.
- Bei Auswahl wird die Übersicht der Koordinationen angezeigt.
- Dort ist eine neue Koordination bereits angezeigt, der Cursor steht im Feld für den Namen des Spenders.

#### Item: {function} Koordination neu anlegen [Spec]
- Dies erfolgt in der Übersicht über alle Koordinationen.
- Der Nutzer muss keine Werte erfassen. Wenn der Name nicht erfasst wird, wird er ersetzt durch "TODO Name erfassen (Koordination <Zeitstempel der Eröffnung>)".
- Sobald der Nutzer in einem beliebeigen Feld auf 'Return' drückt, wird die Koordinatiuon als Datensatz angelegt.
- Die Sicht springt auf das erste Tab der Koordination.
- 
### Story: {tab} Übersicht [EN: Coordination] [Spec]

### Story: {tab} Protokoll [EN: Protocol] [Spec]

#### Item: {structure} Aufbau Koordinationsprotokoll [Spec]
Das Protokoll Tab hat folgenden Aufbau:
- Überschrift: Name und in Klammern SWTPL-Nummer des Spenders. Falls die Daten nicht bekannt sind, wird ein Default-Text angezeigt: "Name noch zu erfassen (-)". 
- Zeile-1/Links: Auswahl der Hintergrundfarbe.
- Zeile-1/Mitte: Übersicht aller laufenden Koordinationen, die der User gerade bearbeitet.
- Zeile-1/Rechts: Start-Stop der Zeiterfassung.
- Zeile-2: Auswahl der Organe (alle).
- Zeile-3: Tabelle mit allen Organen und Anzeige der Organzuordnung.
- Darunter: layout für die Erfassung der Protokolldaten (weiter unten spezifiziert).

#### Item: {panel} Übersicht über alle laufenden Koordinationen
- Zeigt in einfacher Weise (z.B. als Pills) alle laufenden Koordinationen an. 
- Die Koordination zu der das angezeigte Protokoll gehört, ist ausgegraut und kann nicht angewählt werden.
- Die anderen Koordinationen könen anegwählt werden. Wenn gewählt, springt die Ansicht zu dem Protokoll der gewählten Koordination.
- Wenn das angesprungene Protokoll bereits in einem anderen Fenster geöffnet ist, sollte dieses Fenster in den Vordergrund geholt werden. Wenn dies nicht möglich ist, genügt der Wechsel der Ansicht im aktuellen Fenster.

#### Item: {process} Prozess-Regeln Erfassung im Koordinationsprotokoll [Spec]
Die Erfassung der Daten im Koordinationsprotokoll ist ein komplexer Prozess und wird durch eine geeignete Prozesssteuerung geregelt.

### Story: {data} Daten der Perfusion [Spec]
Die folgednen Items geben an, wie Daten zur Perfursion von Organen erfasst werden. Angegeben wird:
- Organe: Die Organe, für die diese Art der Perfusion erfasst wird.
- Inhalte: Ein oder mehrere erfasste Werten (in Klammern: Angabe der Einheiten)

#### Item: {data} Einheiten [Spec]
Folgende Einheiten werden verwendet:
- Ja/Nein: Für reine Bestätigung
- Spezifische Wertlisten (werden jeweils angegeben)

#### Item: {data} Lifeport [Spec]
- Organe: Leber
- Lifeport (Werte: Home / Extern / Ohne)




