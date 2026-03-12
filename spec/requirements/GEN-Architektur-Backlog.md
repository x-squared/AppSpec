# Feature-of [GEN]: Architektur-Backlog

Dieses Dokument beschreibt den wiederkehrenden Architektur-Review-Prozess sowie die aktuell vorgeschlagenen Änderungsstories.

## Use Case: {architecture, process} Regelmäßiger Architektur-Review-Zyklus [Spec]

### Story: {process, architecture} Review wird in fester Taktung durchgeführt [Spec]

#### Item: {process} Der Architektur-Review erfolgt mindestens alle zwei Wochen oder vor größeren Releases. [Spec]

#### Item: {process} Der Review betrachtet die seit dem letzten Zyklus geänderten Flows in Backend, Frontend, Datenmodell, Seeds, Reports und Spezifikationen. [Spec]

#### Item: {architecture} Ergebnis eines Zyklus ist eine priorisierte Liste von Änderungsstories mit Aufwand, Risiko und erwartetem Architekturgewinn. [Spec]

## Use Case: {architecture, process} Entscheidungs- und Umsetzungsprozess [Spec]

### Story: {process} Änderungsstories werden vor der Umsetzung explizit freigegeben [Spec]

#### Item: {process} Jede vorgeschlagene Story wird mit `accept`, `defer` oder `reject` entschieden. [Spec]

#### Item: {process, architecture} Nur `accept`-Stories werden in Architekturartefakten dokumentiert (Regeln, Spezifikation, Manuals) und anschließend implementiert. [Spec]

#### Item: {architecture} Nach Umsetzung wird dokumentiert, welche Drift reduziert wurde und welche bewussten Restschulden verbleiben. [Spec]

## Use Case: {architecture, process} Erweiterter Trigger-Set für Architekturdenken [Spec]

### Story: {architecture} Review prüft nicht nur Strukturdrift, sondern auch Konzept-Fit [Spec]

#### Item: {architecture, process} Bei komplexen Abläufen wird geprüft, ob ein Prozess-Framework sinnvoll ist (z. B. BPMN/CMMN/DMN statt impliziter Logik). [Spec]

#### Item: {data, architecture} Bei medizinischen Daten wird geprüft, ob etablierte Standards besser passen (z. B. LOINC für Beobachtungstypen, UCUM für Einheiten). [Spec]

#### Item: {architecture, data} Bei fachlichen Zustandswechseln wird geprüft, ob explizite Zustands- oder Event-Modelle erforderlich sind. [Spec]

#### Item: {architecture} Bei wiederkehrenden Architekturregeln wird geprüft, ob automatisierbare Fitness-Checks in CI ergänzt werden sollen. [Spec]

#### Item: {architecture} Bei Bedarf werden externe Referenzrahmen kurz einbezogen und gegen die aktuelle TPL-Architektur abgeglichen. [Spec]

## Use Case: {architecture} Erste vorgeschlagene Review-Stories [Spec]

### Story: {architecture, process} Batch 2026-03 Architekturverbesserungen [Spec]

#### Item: {process, architecture} Story AR-001: Prozessrahmen für koordinationsnahe Mehrschritt-Abläufe definieren. [Done]
Ziel: Explizite Modellierung von Ablaufzuständen/Schritten statt impliziter Verteilung über Views/Hooks/Services.
Warum: Aktuell sind Prozessschritte über mehrere Schichten verteilt und dadurch schwer überprüfbar.
Zielzustand: Einheitliches Prozessmodell mit klaren Zuständen, Übergängen und Verantwortlichkeiten.
Akzeptanzkriterien: Mindestens ein priorisierter Mehrschritt-Flow ist explizit modelliert und durch Tests abgesichert.
Aufwand: M
Risiko: Mittel

#### Item: {data, architecture} Story AR-002: LOINC/UCUM-Rollout auf vollständige medizinische Werteabdeckung mit klarer Migrationsstrategie abschließen. [Done]
Ziel: Einheitensichere Berechnungen, konsistente Interoperabilität und klare Betriebsmigration.
Warum: Teilabdeckung erhöht das Risiko semantischer und rechnerischer Inkonsistenzen.
Zielzustand: Relevante medizinische Werte nutzen einheitlich LOINC/UCUM inklusive Betriebs-Backfill.
Akzeptanzkriterien: Vollständige Scope-Liste, Backfill-Lauf, und Berichtsfelder auf kanonischen Werten.
Aufwand: M
Risiko: Mittel

#### Item: {architecture, structure} Story AR-003: Architekturentscheidungen als ADR-Muster in `doc/` ergänzen. [Done]
Ziel: Nachvollziehbarkeit wichtiger Strukturentscheidungen und reduzierter Wissensverlust.
Warum: Wichtige Entscheidungen sind derzeit verteilt und schwer rekonstruierbar.
Zielzustand: Wiederverwendbares ADR-Format mit Querverweisen aus Specs und Regeln.
Akzeptanzkriterien: ADR-Template vorhanden und mindestens ein aktueller Architekturentscheid dokumentiert.
Aufwand: S
Risiko: Niedrig

#### Item: {architecture} Story AR-004: Architektur-Fitness-Checks für Schichtgrenzen und Importregeln in QA-Pipeline ausbauen. [Done]
Ziel: Frühzeitige Drift-Erkennung als automatisierter Gate statt rein manueller Prüfung.
Warum: Manuelle Prüfungen erkennen Drift oft zu spät.
Zielzustand: CI-Checks validieren zentrale Schicht- und Abhängigkeitsregeln automatisiert.
Akzeptanzkriterien: Definierte Regelmenge läuft reproduzierbar in QA und blockiert bei Verstoß.
Aufwand: M
Risiko: Mittel

#### Item: {architecture, data} Story AR-005: Berichtsbuilder-Felder für kanonische statt uneinheitliche Rohwerte standardisieren. [Done]
Ziel: Vergleichbare Auswertungen und geringeres Fehlerrisiko durch semantisch uneinheitliche Daten.
Warum: Gemischte Rohwerte führen zu schwer vergleichbaren Ergebnissen.
Zielzustand: Report-Quellen bevorzugen kanonische Felder und dokumentieren Fallbacks explizit.
Akzeptanzkriterien: Betroffene Datenquellen umgestellt und im Report-Manual nachvollziehbar dokumentiert.
Aufwand: S
Risiko: Niedrig

#### Item: {architecture, process} Story AR-006: Invarianten für Kontext- und Sichtbarkeitslogik zentralisieren. [Done]
Ziel: Konsistente Berechtigungs- und Sichtbarkeitsregeln statt verteilter Sonderfälle.
Warum: Wiederholte Kontextlogik in mehreren Flows erhöht Fehler- und Regressionsrisiken.
Zielzustand: Kernregeln sind in fokussierten Services gekapselt und frontendseitig nur als UX-Gating gespiegelt.
Akzeptanzkriterien: Referenzflows nutzen zentrale Prüfpfade; Abweichungen sind dokumentiert.
Aufwand: M
Risiko: Mittel

#### Item: {architecture, data} Story AR-007: Migrations-Reliability-Framework für DEV/TEST/PROD ausbauen. [Done]
Ziel: Vorhersagbare, idempotente Migrationen über frische und bestehende Datenbanken.
Warum: Datenmigrationen sind aktuell teilweise manuell und ohne einheitliches Verifikations-Gate.
Zielzustand: Migrationen enthalten verpflichtende Nachverifikation, klare Exit-Codes und operator-taugliche Logs.
Akzeptanzkriterien: Neue/veränderte Migrationsmodi führen eine strikte Schema-/Integritätsprüfung aus und scheitern bei Drift reproduzierbar.
Aufwand: M
Risiko: Mittel

#### Item: {architecture, process} Story AR-008: Prozess- und Zustandsbegriffe als gemeinsames Vokabular verankern. [Done]
Ziel: Einheitliche Begriffswelt zwischen Spezifikation, Code und UI.
Warum: Uneinheitliche Terminologie erschwert Architekturreviews und Änderungsdiskussionen.
Zielzustand: Definierte Kernbegriffe mit referenzierbaren Definitionen in den relevanten Artefakten.
Akzeptanzkriterien: Glossar/Referenzliste vorhanden und in neuen Stories verwendet.
Aufwand: S
Risiko: Niedrig

#### Item: {architecture, structure} Story AR-009: Prozess- und Datenflüsse visualisiert quer über zentrale Domänen dokumentieren. [Done]
Ziel: Schnelleres Onboarding und bessere Änderungsfolgenabschätzung.
Warum: Reine Textbeschreibungen machen Cross-Domain-Abhängigkeiten schwer sichtbar.
Zielzustand: Ergänzende Visualisierungen für zentrale Flows und Übergänge sind versioniert verfügbar.
Akzeptanzkriterien: Mindestens ein priorisierter End-to-End-Flow ist als Diagramm dokumentiert und referenziert.
Aufwand: M
Risiko: Niedrig

#### Item: {architecture} Story AR-010: Governance-Artefakte auf ein konsistentes Struktur- und Referenzmuster bringen. [Done]
Ziel: Einheitliche Navigierbarkeit und weniger Meta-Drift zwischen Regeln, Spezifikationen und Manuals.
Warum: Inkonsistente Hierarchien und fehlende Querverweise erzeugen Reibung im laufenden Architekturprozess.
Zielzustand: Zentrale Architektur-/Spec-Artefakte folgen derselben Heading- und Link-Konvention.
Akzeptanzkriterien: Definierte Kernartefakte enthalten konsistente Hierarchie und gegenseitige Referenzen.
Aufwand: S
Risiko: Niedrig

#### Item: {architecture, process} Story AR-011: Transition-Map-Pattern auf Koordinations-Lifecycle ausrollen. [Spec]
Ziel: Explizite, testbare Zustandsübergänge für koordinationsnahe Workflow-Aktionen.
Warum: Übergangslogik ist teilweise verteilt und dadurch schwerer regressionssicher zu ändern.
Zielzustand: Zentraler Transition-Map-Service mit erlaubten Aktionen pro Phase/Status für Koordinationen.
Akzeptanzkriterien: Definierte Transition-Map inkl. Negativtests; Router delegieren nur noch an Service-Aktionen.
Aufwand: M
Risiko: Mittel

#### Item: {architecture, process} Story AR-012: Transition-Map-Pattern auf Colloquium-/Agenda-Workflow ausrollen. [Spec]
Ziel: Einheitliche Prozesssteuerung für Agenda-Statuswechsel und abhängige Folgeaktionen.
Warum: Agenda-/Task-nahe Übergänge sind fachlich gekoppelt und profitieren von expliziten Guards.
Zielzustand: Klar definierte erlaubte Übergänge inkl. Validierungsfehlern mit konsistenter 422-Semantik.
Akzeptanzkriterien: Übergangsregeln zentralisiert, bestehendes Verhalten erhalten, kritische Pfade durch Tests abgesichert.
Aufwand: M
Risiko: Mittel

#### Item: {architecture, process} Story AR-013: Transition-Map-Pattern auf TaskGroup/Task-Statusmodell vereinheitlichen. [Spec]
Ziel: Konsistente Statusübergänge für TaskGroup/Task über alle Erstellungs- und Bearbeitungswege.
Warum: Verteilte Statuslogik erhöht Risiko für inkonsistente Zustände zwischen UI, Services und Seeds.
Zielzustand: Gemeinsame Status-Transition-Definition mit wiederverwendbarer Validierung in Task-Services.
Akzeptanzkriterien: Erlaubte Übergänge dokumentiert, verbotene Übergänge liefern klare Fehler, Regressionstests vorhanden.
Aufwand: M
Risiko: Mittel
