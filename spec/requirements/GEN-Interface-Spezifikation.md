# Feature [GEN]: Schnittstellen

Dieses Dokument beschreibt fachliche und technische Anforderungen für externe Schnittstellen in TPL-App.

## Status-Legende [Ready]

- Spec = laufende Spezifikation
- Ready = bereit für Implementierung
- Impl = in Umsetzung
- QA = Testdefinition/Ausführung offen
- Done = abgeschlossen

## Use Case: Schnittstellen-Architektur [Spec]

### Use Case: Externes System anbinden [Ready]

#### Story: Klare Modulgrenzen pro Schnittstelle [Ready]

##### Item: Jede externe Schnittstelle wird als eigenes Feature-Modul unter `backend/app/features/interfaces/<interface_key>/` umgesetzt. [Ready]

##### Item: Router enthalten nur HTTP-Orchestrierung; Transport, Mapping und Fachlogik liegen in der Schnittstellen-Feature-Schicht. [Ready]

##### Item: SQLAlchemy-Modelle werden nicht direkt auf externe Payload-Strukturen gemappt; die Transformation erfolgt explizit in Mappern. [Ready]

### Use Case: Schnittstellen-Operationen bereitstellen [Spec]

#### Story: Operationen sind explizit und nachvollziehbar [Spec]

##### Item: Schnittstellen bieten fachlich benannte Operationen wie `preview`, `validate`, `import`, `export` und `sync-status`. [Spec]

##### Item: Undurchsichtige Sammel-Endpunkte ("do-all") werden vermieden. [Spec]

##### Item: Wiederholte Imports sind idempotent ausführbar (z. B. via idempotency key oder fachlichem Duplikatsschutz). [Spec]

## Use Case: Daten- und Fehlerverhalten [Spec]

### Use Case: Externe Daten sicher übernehmen [Spec]

#### Story: Konsistente Feldabbildung [Spec]

##### Item: Externe Feldnamen werden nicht ungeprüft in interne API-Responses übernommen. [Spec]

##### Item: Pflichtfelder, Typen und Domänenwerte werden vor Persistierung validiert. [Spec]

##### Item: Fachliche Inkonsistenzen erzeugen klare, reproduzierbare Fehlermeldungen. [Spec]

### Use Case: Betriebsrobustheit sicherstellen [Spec]

#### Story: Observability und Fehlerisolation [Spec]

##### Item: Anfrage, Antwortstatus, Mapping-Schritte und Persistierung werden strukturiert geloggt. [Spec]

##### Item: Schnittstellen-spezifische Fehler werden in dedizierten Fehlertypen gekapselt. [Spec]

##### Item: Teilfehler führen nicht zu stillen Datenverlusten; der Verarbeitungsstatus bleibt nachvollziehbar. [Spec]

## Use Case: Konfiguration und Sicherheit [Spec]

### Use Case: Laufzeitkonfiguration verwalten [Ready]

#### Story: Konfiguration ohne Hardcoding [Ready]

##### Item: Zugangsdaten und Zielendpunkte werden über Konfiguration (Umgebung/Config-Module) bezogen. [Ready]

##### Item: Geheimnisse werden nicht im Quellcode oder Seed-Datensätzen gespeichert. [Ready]

### Use Case: Berechtigter Zugriff auf Schnittstellen [Spec]

#### Story: Rechte- und Rollenprüfung [Spec]

##### Item: Schnittstellen-Endpunkte sind über bestehende Berechtigungsmechanismen geschützt. [Spec]

##### Item: Schreiboperationen erfordern strengere Rechte als Lese-/Vorschauoperationen. [Spec]

## Use Case: Qualitätssicherung [Spec]

### Use Case: Schnittstellenänderungen verifizieren [Spec]

#### Story: Testabdeckung für Verträge und Flows [Spec]

##### Item: Pro Schnittstelle existiert mindestens ein Vertragstest für Mapping und Validierung. [Spec]

##### Item: Pro Schnittstelle existiert mindestens ein Integrationsfluss-Test für einen typischen End-to-End-Ablauf. [Spec]

##### Item: Fehlerpfade (z. B. Timeout, 4xx/5xx, ungültige Payload) sind explizit testbar und dokumentiert. [Spec]
