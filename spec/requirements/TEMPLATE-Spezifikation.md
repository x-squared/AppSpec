# Feature [GEN]: TEMPLATE-Spezifikation

Kurzvorlage für neue fachliche Spezifikationen. Für die vollständigen Regeln siehe `GEN-Spec-Spezifikation.md`.

## Use Case: Feature-Label und Dateimuster festlegen [Spec]

### Story: Neues Feature ist eindeutig benannt [Spec]

#### Item: Jedes Feature hat ein Label (z. B. `TPLK`) und eine zentrale Feature-Datei `<LABEL>-<Feature-Name>.md`. [Spec]
Beispiel: `TPLK-Koordination-Transplantation.md` mit Kopf `# Feature [TPLK]: Koordination Transplantation`.

#### Item: Direkt unter dem Feature-Kopf steht die Section `## Spezifikationen` mit der Liste der Teil-Dateien. [Spec]
Beispiel: Unter `# Feature [TPLK]: ...` folgt unmittelbar `## Spezifikationen` und danach die Dateiliste.

#### Item: Teil-Spezifikationen verwenden dasselbe Label-Präfix und den Kopf `# Feature-of [<LABEL>]: <Feature-Name>`. [Spec]
Beispiel: `TPLK-Episode-Spezifikation.md` mit Kopf `# Feature-of [TPLK]: Koordination Transplantation`.

#### Item: Überschriften dürfen optionale Übersetzungshinweise im Format `[<LANG>: <text>]` tragen. [Spec]
Beispiel: `### Story: Koordinationsprotokoll [EN: Coordination Protocol] [Spec]`.

#### Item: Überschriften dürfen optionale semantische Hinweislabels im Format `{name}` oder `{name1, name2, ...}` tragen (z. B. `{view}`, `{tab}`, `{panel}`, `{process}`, `{function}`, `{structure}`, `{design}`, `{architecture}`, `{data}`, `{quality}`, `{documentation}`, `{specification}`). [Spec]
Beispiel: `### Story: Koordinationsprotokoll {process} [EN: Coordination Protocol] [Spec]`.
Beispiel mit mehreren Hints: `### Story: Koordinationsprotokoll {design, function} [EN: Coordination Protocol] [Spec]`.

#### Item: Hinweislabels werden kurz interpretiert: `{view}` Seite/View, `{tab}` Tab, `{panel}` Panel/Section, `{process}` Ablauf, `{function}` Funktionalität, `{structure}` Struktur, `{design}` visuelle Gestaltung/UX, `{architecture}` Architekturbelange, `{data}` Datenhandling/Seed-Daten, `{quality}` Qualitätsziele/Testbarkeit/Verifikation, `{documentation}` Dokumentationsumfang/Manual-Pflege, `{specification}` Regeln der Spezifikationssystematik. [Spec]

## Use Case: Neue Funktion wird beschrieben [Spec]

### Story: Ziel und fachlicher Ablauf sind klar [Spec]

#### Item: Zielbild der Funktion in 1-2 Sätzen beschreiben. [Spec]
Beispiel: Eine Koordination kann als abgeschlossen markiert werden und speichert eine Abschlussbemerkung.

#### Item: Fachliche Regeln und Grenzen explizit nennen. [Spec]
Beispiel: Abschluss ist nur erlaubt, wenn alle Pflichtdaten vorhanden sind.

#### Item: Sichtbares Verhalten im UI benennen. [Spec]
Beispiel: Der Abschlussstatus wird im Detailkopf angezeigt.

## Use Case: Akzeptanzkriterien werden prüfbar festgelegt [Spec]

### Story: Umsetzung ist testbar und eindeutig [Spec]

#### Item: Mindestens ein positiver Akzeptanzfall. [Spec]
Beispiel: Bei vollständigen Daten wird der Abschluss gespeichert.

#### Item: Mindestens ein negativer Akzeptanzfall. [Spec]
Beispiel: Bei fehlenden Pflichtdaten wird der Abschluss mit klarer Fehlermeldung abgelehnt.

## Use Case: Optionaler Änderungsmodus mit Markern [Spec]

### Story: Änderungen werden minimal-invasiv markiert [Spec]

#### Item: Einfügungen mit `[[ADD]] ... [[/ADD]]`, Ersetzungen mit `[[REPLACE: "..."]] ... [[/REPLACE]]`, Löschungen mit `[[DELETE: "..."]]`. [Spec]
