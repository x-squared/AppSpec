# Feature-of [GEN]: Spec-Spezifikation

Dieses Dokument beschreibt das Spezifikationssystem und dessen Regeln im Projekt.

## Use Case: Struktur und Mindestregeln [Ready]

## Use Case: Eine neue Spezifikation wird erstellt [Ready]

### Story: Die Hierarchie wird konsistent verwendet [Ready]

#### Item: Anforderungen werden in der Hierarchie `Feature -> Use Case -> Story -> Item` beschrieben. [Ready]

#### Item: Statuslabels sind `[Spec]`, `[Ready]`, `[Impl]`, `[QA]` oder `[Done]`. [Ready]

#### Item: Fehlt ein Statuslabel, wird standardmäßig `[Spec]` angenommen. [Ready]

#### Item: Formulierungen sind fachlich präzise und überprüfbar. [Ready]

## Use Case: Der Fortschritt wird über Status geführt [Ready]

### Story: Statushierarchie bleibt logisch konsistent [Ready]

#### Item: Ein Elternknoten darf nicht `[Done]` sein, solange untergeordnete Knoten nicht `[Done]` sind. [Ready]

#### Item: `Feature [Done]` ist nur zulässig, wenn alle enthaltenen Use Cases, Stories und Items `[Done]` sind. [Ready]

#### Item: `Use Case [Done]` ist nur zulässig, wenn alle enthaltenen Stories und Items `[Done]` sind. [Ready]

#### Item: `Story [Done]` ist nur zulässig, wenn alle enthaltenen Items `[Done]` sind. [Ready]

## Use Case: Änderungsmodus für bestehende Features [Ready]

## Use Case: Eine bereits implementierte Funktion wird fachlich nachgezogen [Ready]

### Story: Statusstart wird korrekt gesetzt [Ready]

#### Item: Bei normalen Spezifikationsupdates ist der Startstatus `[Spec]`. [Ready]

#### Item: Bei Reverse-Engineering aus bestehendem Code ist der Startstatus `[Impl]`. [Ready]

#### Item: Änderungen werden als neue Story oder klarer Änderungsblock dokumentiert, statt frühere Aussagen stillschweigend zu überschreiben. [Ready]

## Use Case: TODO-Markierung für offene Punkte [Ready]

## Use Case: Offene Diskussionen werden innerhalb der Spezifikation kenntlich gemacht [Ready]

### Story: TODO wird als Diskussionsmarker verwendet [Ready]

#### Item: Das Inline-Label `TODO` markiert Inhalte als noch zu diskutieren und nicht final entschieden. [Ready]

#### Item: Alles, was nach `TODO` auf derselben Zeile steht, gilt als offener Diskussionsinhalt. [Ready]

#### Item: Bei Zeilenumbruch gehört der visuell überlaufende Fortsetzungstext weiterhin zum selben TODO-Hinweis. [Ready]

## Use Case: Markierter Änderungsmodus für Implementierung [Ready]

## Use Case: Änderungen werden direkt im Spezifikationstext markiert [Ready]

### Story: Marker erlauben minimale Textänderungen mit sauberer Endfassung [Ready]

#### Item: Für Einfügungen wird `[[ADD]] ... [[/ADD]]` verwendet. [Ready]

#### Item: Für gezielte Ersetzungen wird `[[REPLACE: "<alter Ausschnitt>"]] ... [[/REPLACE]]` verwendet. [Ready]

#### Item: Für gezielte Löschungen wird `[[DELETE: "<alter Ausschnitt>"]]` verwendet. [Ready]

#### Item: Für temporäre Umsetzungshinweise wird `[[NOTE]] ... [[/NOTE]]` verwendet; dieser Hinweis bleibt nicht im finalen Spezifikationstext. [Ready]

#### Item: Nach Umsetzung werden alle Marker aufgelöst und entfernt, damit die Spezifikation nahtlos lesbar bleibt. [Ready]

#### Item: Außerhalb markierter Bereiche sind nur minimale Formulierungsanpassungen zulässig. [Ready]

## Use Case: Temporäre Fokusmarkierung für Assistenz [Ready]

## Use Case: Ein begrenzter Textbereich wird explizit zur Bearbeitung markiert [Ready]

### Story: Einfache Bereichsgrenzen mit temporären Delimitern [Ready]

#### Item: Der Marker `>>>>>` öffnet einen Bereich, den der Assistent betrachten oder bearbeiten soll. [Ready]

#### Item: Der Marker `<<<<<` schließt den zuvor geöffneten Bereich. [Ready]

#### Item: Diese Marker sind temporäre Arbeitsmarkierungen und gehören nicht zur finalen Spezifikation. [Ready]

#### Item: Nach Umsetzung werden die Marker wieder entfernt, sodass ein sauberer Spezifikationstext verbleibt. [Ready]

## Use Case: Übersetzungshinweise in Überschriften [Ready]

## Use Case: Sprachhinweise werden einheitlich notiert [Ready]

### Story: Optionales Hint-Format bleibt maschinen- und menschenlesbar [Ready]

#### Item: Übersetzungshinweise in Überschriften verwenden das Format `[<LANG>: <text>]`, z. B. `[EN: Coordination Protocol]`. [Ready]

#### Item: Der Übersetzungshinweis steht vor dem Statuslabel in derselben Überschrift. [Ready]

#### Item: Beispiel: `### Story: Koordinationsprotokoll [EN: Coordination Protocol] [Spec]`. [Ready]

## Use Case: Semantische Hinweislabels [Ready]

## Use Case: Label-Format zur Einordnung von Anforderungen [Ready]

### Story: Optionale Kontextlabels sind einheitlich und erweiterbar [Ready]

#### Item: Semantische Hinweislabels werden im Format `{name}` oder `{name1, name2, ...}` notiert. [Ready]

#### Item: Empfohlene Startlabels sind `{view}`, `{tab}`, `{panel}`, `{process}`, `{function}`, `{structure}`, `{design}`, `{architecture}`, `{data}`, `{quality}`, `{documentation}` und `{specification}`. [Ready]

#### Item: Zusätzliche lokale Labels sind erlaubt, wenn sie den Kontext klarer machen. [Ready]

#### Item: Labels sind Hinweise und keine harte Vorgabe für die Implementierung. [Ready]

#### Item: `{process}` deutet darauf hin, dass das Process-Framework in Betracht gezogen werden kann, aber nicht zwingend genutzt werden muss. [Ready]

#### Item: Empfohlene Reihenfolge in Überschriften: `<Titel> {label} [<LANG>: <text>] [Status]`. [Ready]

#### Item: Mehrere semantische Hints in einer Überschrift sind erlaubt, z. B. `{design, function}`. [Ready]

#### Item: Kurzbedeutung der Labels: `{view}` Seite/View, `{tab}` Tab-Kontext, `{panel}` Panel/Section, `{process}` Ablaufhinweis, `{function}` Funktionshinweis, `{structure}` Strukturhinweis, `{design}` visuelle/UX-Hinweise, `{architecture}` Architekturhinweise, `{data}` Datenhandling- und Seed-Hinweise, `{quality}` Qualitäts- und Testanforderungen inkl. Verifikationskriterien, `{documentation}` Dokumentations- und Manual-Anforderungen, `{specification}` Spezifikationsregeln und Strukturkonventionen. [Ready]

## Use Case: Feature-Label und Dateifamilie [Ready]

## Use Case: Feature und Teil-Spezifikationen sind eindeutig gekoppelt [Ready]

### Story: Label-basierte Dateikonvention [Ready]

#### Item: Jedes Feature definiert ein Label (z. B. `TPLK`) und genau eine Feature-Datei `<LABEL>-<Feature-Name>.md`. [Ready]

#### Item: Die Feature-Datei verwendet den Kopf `# Feature [<LABEL>]: <Feature-Name>`. [Ready]

#### Item: Direkt unter dem Feature-Kopf folgt die Section `## Spezifikationen` mit der Liste der Teil-Dateien. [Ready]

#### Item: Teil-Spezifikationen eines Features nutzen das gleiche Label-Präfix im Dateinamen. [Ready]

#### Item: Teil-Spezifikationen verwenden den Kopf `# Feature-of [<LABEL>]: <Feature-Name>`. [Ready]

#### Item: Die Feature-Datei listet alle zugehörigen Teil-Spezifikationen. [Ready]

## Use Case: Beispiel A - Fachliche Entitäten definieren [Spec]

## Use Case: Eine Spezifikation beschreibt neue Business-Entitäten [Spec]

### Story: Das Domänenmodell wird verständlich und konsistent beschrieben [Spec]

#### Item: Entität mit Zweck, Schlüsseln und Beziehungen definieren. [Spec]
Beispiel: Die Entität `Perfusionsprotokoll` wird über `ID` eindeutig identifiziert, gehört genau zu einer `Koordination` und referenziert optional ein `Organ`.

#### Item: Attribute mit Datentyp, Pflichtgrad und Bedeutung definieren. [Spec]
Beispiel: `perfusionsart` (Enum, Pflicht), `startzeit` (Zeitstempel, optional), `kommentar` (Text, optional).

#### Item: Lebenszyklus und Änderungsregeln der Entität definieren. [Spec]
Beispiel: Ein `Perfusionsprotokoll` darf nur im Status `offen` geändert werden; nach `abgeschlossen` nur über einen expliziten Korrekturprozess.

## Use Case: Beispiel B - Komplexe Logik mit Verzweigungen definieren [Spec]

## Use Case: Eine Spezifikation beschreibt regelbasierte Entscheidungen [Spec]

### Story: Fachliche Bedingungen werden deterministisch dokumentiert [Spec]

#### Item: Verzweigungslogik mit klaren Wenn-Dann-Regeln definieren. [Spec]
Beispiel: Wenn `Organ = Lunge`, dann ist `perfusionsart` aus `{EVLP, keine}` wählbar; wenn `Organ = Leber`, dann aus `{HOPE, NMP, keine}`.

#### Item: Prioritäten und Konfliktauflösung bei mehreren Regeln definieren. [Spec]
Beispiel: Eine organspezifische Regel hat Vorrang vor einer allgemeinen Regel.

#### Item: Fehler- und Grenzfälle explizit beschreiben. [Spec]
Beispiel: Bei fehlenden Pflichtangaben wird der Vorgang fachlich abgelehnt.

#### Item: Verzweigungen zusätzlich als Bullet-Layout darstellen, wenn dies die Lesbarkeit erhöht. [Spec]
Beispiel-Layout:
- Eingangszustand: `Organ`, `Status`, `Pflichtfelder`
- Wenn `Organ = Lunge`: erlaube `EVLP`
- Wenn `Organ = Leber`: erlaube `HOPE` oder `NMP`
- Wenn `is_rejected = true`: stoppe weitere Empfängerzuordnung
- Sonst: fahre mit Standardprozess fort

## Use Case: Beispiel C - Architekturelle Anforderungen definieren [Spec]

## Use Case: Eine Spezifikation legt technische Leitplanken fest [Spec]

### Story: Die Umsetzung bleibt über Module hinweg konsistent [Spec]

#### Item: Verantwortlichkeiten pro Schicht festlegen. [Spec]
Beispiel: Router-Schicht validiert Transport und Rechte, Service-Schicht enthält Geschäftslogik, Persistenzschicht verwaltet Integrität und Beziehungen.

#### Item: Integrations- und Schnittstellenregeln festlegen. [Spec]
Beispiel: Externe Systeme werden über dedizierte Adapter-Module angebunden; externe Feldnamen werden nicht ungeprüft in interne API-Verträge übernommen.

#### Item: Qualitäts- und Nachweisanforderungen festlegen. [Spec]
Beispiel: Für jede neue fachliche Regel werden mindestens ein positiver und ein negativer Testfall spezifiziert.
