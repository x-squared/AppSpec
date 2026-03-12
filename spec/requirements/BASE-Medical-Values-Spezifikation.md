# Feature-of [BASE]: Basis

Feature-Datei: `GEN-Architektur-Spezifikation.md`

## Use Case: {data} Medizinische Werte [Spec]

### Story: {data} Typen von Einheiten [Spec]

#### Item: {data} Numerische Einheiten [Spec]
- Ganzzahl (optional: Minimum, Maximum)
- Dezimalzahl (optional: Minimum, Maximum)
- Boolsch
- Datum
- Zeitstempel

#### Item: {data} Metrische Einheiten [Spec]
- Gewicht (Einheit: kg)
- Länge-cm (Einheit: cm)

#### Item: {data} Listen-Einheiten [Spec]
Dies sind Einheiten, die durch Listen beschreiben werden. Die Listen können entweder fix sein (als Codes abzubilden), oder sie können variabel sein (als Kataloge abzubilden),

### Story: {data} Medizinische Einheiten [Spec]

#### Item: {data} Listentyp: Testergebnis [Spec]
- Positiv [EN: Positive]
- Negativ [EN: Negative]
- Grenzwertig [EN: Bordercase]

### Story: {data} Leber [Spec]

#### Item: {data} MELD-Werte [Spec]
Es werden drei MELD-Werte erfasst. Dies sind alles ganzzahlige Werte zwischen 0 und 40 (inklusive). Dabei kennzeichnet der Wert 40 die höchste Kritikalität.
- MELD: Errechneter MELD-Wert.
- Upgrade MELD: Schrittweise Erhöhung über die Zeit.
- SE MELD: Standard MELD-Wert.


----------------------------------------------------

## Use Case: {data, architecture} Systematik des Medical-Values-Systems mit UCUM und LOINC [Spec]

### Story: {data, structure} Trennung von Fachbedeutung, Datentyp und Werteinstanz [Spec]

#### Item: {architecture, data} Die fachliche Bedeutung eines Messwerts wird über eine Medical-Value-Template-Definition beschrieben. [Spec]
Die Template-Definition enthält fachliche Schlüssel (z. B. LAB-/KIS-Schlüssel), eine fachliche Bezeichnung und die Zuordnung zu einer Gruppe.

#### Item: {architecture, data} Der technische Datentyp wird separat als Datatype-Definition geführt. [Spec]
Die Datatype-Definition beschreibt Primitive (z. B. number, catalogue, date), Formatregeln, Präzision sowie Einheitenspezifika.

#### Item: {architecture, data} Eine konkrete Werteinstanz wird patienten- und kontextbezogen gespeichert. [Spec]
Kontexte sind mindestens STATIC, ORGAN und DONOR; die Kontexte werden als Datenbeziehung modelliert und nicht als fest codierte Einzelfelder.

### Story: {data, function} Einheitensicherheit und Berechnungsfähigkeit über UCUM [Spec]

#### Item: {data} Für numerische Datentypen wird eine kanonische UCUM-Einheit definiert. [Spec]
Beispiele: Gewicht mit kanonischer Einheit `kg`, Länge mit kanonischer Einheit `cm`.

#### Item: {data, function} Zulässige Eingabeeinheiten werden als UCUM-Liste definiert und serverseitig validiert. [Spec]
Eine Eingabe mit nicht erlaubter Einheit wird fachlich abgelehnt.

#### Item: {data, process} Eingegebene Werte werden in die kanonische Einheit normalisiert und für Berechnungen verwendet. [Spec]
Dabei werden sowohl Eingabewert/-einheit als auch normalisierter kanonischer Wert persistiert.

#### Item: {data, process} Berechnungen, Ableitungen und Auswertungen basieren ausschließlich auf kanonischen Werten. [Spec]
Dies verhindert Rechenfehler durch vermischte Einheiten.

### Story: {data, structure} Interoperabilität über LOINC [Spec]

#### Item: {data} Medizinische Templates können optional einen LOINC-Code tragen. [Spec]
Der LOINC-Code beschreibt fachlich, *was* gemessen wird, unabhängig von der Einheit.

#### Item: {data} LOINC und UCUM werden kombiniert eingesetzt. [Spec]
LOINC beschreibt den Beobachtungstyp, UCUM beschreibt die Einheit; beide Informationen sind gemeinsam erforderlich für sichere, interoperable Nutzung.

#### Item: {data} Fehlt ein LOINC-Code, bleibt der Wert intern nutzbar, ist aber eingeschränkt interoperabel. [Spec]
Für zentrale und häufig getauschte Werte wird die schrittweise Ergänzung von LOINC-Codes vorgesehen.

## Use Case: {data} Beschreibung der verwendeten medizinischen Werte [Spec]

### Story: {data} Basiswerte und Anthropometrie [Spec]

#### Item: {data} Blutgruppe wird als codebasierter Basiswert geführt. [Spec]
Die Blutgruppe ist ein statischer Basiswert und wird typischerweise über eine stabile Codeliste erfasst.

#### Item: {data} Größe und Gewicht werden als metrische Werte geführt. [Spec]
Größe ist eine Längeneinheit (kanonisch `cm`), Gewicht eine Masseneinheit (kanonisch `kg`).

#### Item: {data} BMI ist ein abgeleiteter numerischer Wert. [Spec]
BMI wird als Dezimalwert geführt; sofern berechnet, erfolgt die Berechnung auf Basis kanonischer Werte.

### Story: {data} Infektions- und Serologiewerte [Spec]

#### Item: {data} Serologische Testergebnisse werden als Listentyp „Testergebnis“ geführt. [Spec]
Zulässige Werte sind:
- Positiv [EN: Positive]
- Negativ [EN: Negative]
- Grenzwertig [EN: Borderline]

#### Item: {data} Typische serologische Felder umfassen u. a. CMV, EBV, Hepatitis- und HIV-bezogene Marker. [Spec]
Diese Werte werden templatebasiert gepflegt und je nach Organ-/Donor-Kontext angewendet.

### Story: {data} Organspezifische Leberwerte [Spec]

#### Item: {data} MELD-bezogene Werte werden als ganzzahlige Werte im Bereich 0 bis 40 (inklusive) geführt. [Spec]
Der Wert 40 kennzeichnet die höchste Kritikalität.

#### Item: {data} Es werden mindestens drei MELD-Felder unterschieden. [Spec]
- MELD: Errechneter MELD-Wert.
- Upgrade MELD: Zeitabhängige Priorisierungserhöhung.
- SE MELD: Standard-Exception-bezogener MELD-Wert.

### Story: {data, process} Pflege und Erweiterung des Wertesets [Spec]

#### Item: {data} Neue medizinische Werte werden primär über Template-/Datatype-Definitionen ergänzt, nicht durch ad-hoc Sonderfelder. [Spec]
Dadurch bleiben Validierung, Darstellung und Berechnung einheitlich.

#### Item: {data, quality} Bei Einführung neuer numerischer Werte sind kanonische Einheit, erlaubte UCUM-Einheiten und Konversionsregeln verpflichtend zu definieren. [Spec]
Damit bleibt die rechnerische Sicherheit auch bei zukünftigen Erweiterungen erhalten.
