# Feature-of [GEN]: Architektur

## Spezifikationen

- [GEN-Architektur-Backlog](./GEN-Architektur-Backlog.md)
- [GEN-Medical-Values-Spezifikation](./GEN-Medical-Values-Spezifikation.md)

Dieses Feature macht die Vorgaben an die Architektur der App.

## Use Case: {architecture} Die fachliche Architektur ist in Domänen aufgeteilt. [Spec]
 
### Story: {architecture} Domänen folgen Prinzipien [Spec]

#### Item: {architecture, specification} Die Spezifikation ist gemäss der Domänen aufgeteilt [Spec]

### Story: {architecture} Domäne: GEN Grundlagen [Spec]

### Story: {architecture} Domäne: PAT Patient [Spec]

### Story: {architecture} Domäne: TPLK Transplantationskoordination [Spec]

#### Item: {architecture} Subdomäne: TPLK Episoden: TPL-Episoden der Patienten [Spec]

#### Item: {architecture} Subdomäne: TPLK Koordination: Zuweisungen der Organe von Spendern auf Empänger [Spec]

### Story: {architecture} Domäne: LTPL Lebenspende [Spec]

### Story: {architecture} Domäne: KOLL Kolloquien [Spec]

### Story: {architecture} Domäne: STCS Transplant-Kohortenstudie [Spec]

### Story: {architecture} Domäne: CROSS Querschnitt [Spec]

## Use Case: {architecture} Datenarchitektur [Spec]

### Story: {architecture} Datenobjekte folgen grundsätzlichen Vorgaben [Spec]

#### Item: {architecture} Bewegungsdaten haben Standardattribute [Spec]
Alle Bewegungsdaten enthalten Standardattribute.
- CREATED_BY_ID (ID eines Users): Der Nutzer, der den Datensatz angelegt hat.
- CREATED_AT (Timestamp): Zeitpunkt der ersten Erstellung.
- CHANGED_BY_ID (ID eines Users): Der Nutzer, der die letzte Änderung gemacht hat.
- CHANGED_AT (Timestamp): Zeitpunkt der letzten Änderung.
- ROW_VERSION (Integer): Wird für Optimistic-Locking verwendet.

## Use Case: {architecture, process} Prozesssteuerung [Spec]

### Story: {architecture, process} UI-Prozesse werden in komplexen Fällen durch das Backend gesteuert [Spec]
UI-Prozesse werden durch das Backend gesteuert. Folgende Regeln beschreiben die Erwartungen.

#### Item: {architecture, process} Prozesslogik wird nur in einfachen Fällen in der GUI abgebildet [Spec]
Prozessschritte sollten nur in sehr einfachen Fällen in der GUI abgebildet werden. Komplexere Abläufe werden ausschließlich über eine Backend-Steuerung umgesetzt.



-------------------------------



## Use Case: {architecture, structure} Umfang der Architektur-Spezifikation [Spec]

### Story: {architecture} Architektur-Spezifikation beschreibt Leitplanken statt Feature-Details [Spec]

#### Item: {architecture} Schichten und Verantwortungen sind explizit festgelegt. [Spec]
Die Spezifikation soll die Trennung zwischen Router, Service, Modell/Schema und Frontend-Orchestrierung definieren sowie Anti-Pattern benennen (z. B. Business-Logik in Routern oder UI).

#### Item: {architecture, data} Domänengrenzen und Ownership sind dokumentiert. [Spec]
Für jede zentrale Domäne wird festgelegt, welche Datenobjekte und Prozesse dort verankert sind und wo Übergänge zu anderen Domänen erfolgen.

#### Item: {architecture, process} Prozesssteuerung wird als serverseitige Zustandslogik beschrieben. [Spec]
Für relevante Workflows werden erlaubte Zustände, Transitionen, Guard-Regeln und Fehlersemantik (z. B. 409 bei Konflikt) spezifiziert.

### Story: {architecture, data} Architektur regelt technische Querschnittsbelange [Spec]

#### Item: {architecture, data} Audit-, Versionierungs- und Konsistenzregeln sind einheitlich definiert. [Spec]
Die Spezifikation soll verbindlich regeln, wann `created_by/created_at`, `changed_by/changed_at` und `row_version` gesetzt und geprüft werden.

#### Item: {architecture, data} Referenzdatenstrategie ist klar abgegrenzt. [Spec]
Es wird definiert, wann `CODE` (stabile systemweite Konstanten) und wann `CATALOGUE` (lokal pflegbare Listen) zu verwenden ist.

#### Item: {architecture, data} Datenmodelländerungen haben ein verbindliches Impact-Protokoll. [Spec]
Bei Modelländerungen sind betroffene Schichten (Modelle, Schemas, Services, Seed, Frontend, Reports, Doku) systematisch mitzupflegen.

### Story: {architecture, process} Operative Verifikation ist Teil der Architektur [Spec]

#### Item: {architecture, process} Für kritische Migrationspfade existieren Verify-Modi mit klaren Qualitätszielen. [Spec]
Architekturrelevante Migrationen sind erst abgeschlossen, wenn die zugehörigen Verifikationen erfolgreich sind (z. B. `issue_count = 0` bei definierten Quality Gates).

#### Item: {architecture, structure} Architekturentscheidungen und Begriffe werden nachvollziehbar gehalten. [Spec]
Die Spezifikation verweist auf ADRs, Glossar und Architektur-Backlog, damit Entscheidungen, Begriffe und offene Architekturstories konsistent bleiben.

