# Feature [PAT]: Patient

## Spezifikationen
- `PAT-Patient-Spezifikation.md` (Basis-Spezifikation für Patient-Kernlogik)


------------------------------------------------

## Use Case: {data, architecture, view} Patient-Kerndaten und Stammdatenführung [Spec]

### Story: {panel, function} Stammdaten sind strukturiert ediwork now,.Does this need an update to reflect tierbar [Spec]

#### Item: Patienten-ID (`pid`) ist systemweit eindeutig und Pflichtfeld. [Spec]
Die Patienten-ID identifiziert den Patienten fachlich eindeutig und darf nicht mit Episode- oder Koordinations-IDs vermischt werden.

#### Item: Personenstammdaten werden als patient-zentrierte Basisattribute geführt. [Spec]
Mindestens Name, Vorname und Geburtsdatum sind als Kernattribute zu behandeln.

#### Item: Änderungen an Stammdaten erfolgen nachvollziehbar und konsistent. [Spec]
Bearbeitung folgt einem klaren Edit/Save/Cancel-Verhalten; unbestätigte Änderungen dürfen persistierte Daten nicht überschreiben.

## Use Case: {data} Patient-bezogene Basisreferenzen verwalten [Spec]

### Story: {function, data} Referenzwerte für den Patienten werden standardisiert genutzt [Spec]

#### Item: Referenzwerte wie Geschlecht oder Sprache werden über zentrale Referenzquellen aufgelöst. [Spec]
Für stabile, systemweite Konstanten sind Codes zu verwenden; frei definierbare lokale Listen bleiben klar getrennt.

#### Item: Sichtbare Benennungen werden i18n-fähig geführt. [Spec]
Die Anzeige patientbezogener Referenzwerte muss sprachabhängig konsistent aufgelöst werden.

## Use Case: {architecture, process} Klare Domänengrenze für Patient [Spec]

### Story: {architecture} Patient bleibt von Episode und Koordination fachlich getrennt [Spec]

#### Item: Diese Spezifikation umfasst nur patient-zentrierte Kern- und Stammdaten. [Spec]
Workflow- und Prozesslogik aus Episode oder Koordination ist explizit ausgeschlossen.

#### Item: Erweiterungen in Episode/Koordination werden in eigenen Feature-of-Spezifikationen beschrieben. [Spec]
Abhängigkeiten dürfen referenziert werden, die fachliche Detailregelung bleibt jedoch in den jeweiligen Domänendokumenten.
