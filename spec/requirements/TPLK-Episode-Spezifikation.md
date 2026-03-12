# Feature-of [TPLK]: Episoden einer Transplantation

Feature-Datei: `TPLK-Koordination-Transplantation.md`

## Use Case: Episode [Spec]

### Story: Episode Prozess abbilden [Spec]

#### Item: Phasen einer Episode
Episoden haben folgende Phasen
1. Abklärung [EN: Evaluation]
2. Listung [EN: Listing]
3. Koordination [EN: Coordination]
   1. Allokation [EN: Allocation]
   2. Transplantation [EN: Transplantation]
4. Nachbetreuung [EN: Follow-Up]
5. Abgeschlossen (EN: Closed]

#### Item: Start- und Endtermine der Phasen
Jede Phase hat einen Start- und Endtermin. Dies gilt jedoch nicht für die Subphasen wie Allokation. Die Start- und Endtermine werden je nach Kontext erfasst.
Wenn die Episode auf irgend eine Weise abgeschlossen wird, dann ist dies der Endtermin der gesamten Episode.

#### Item: Bearbeitung während der Phasen
Es könne stets nur die Daten einer Episode bearbeitet werden, die der Phase zugehören, die gerade aktiv ist. Das gilt nicht für übergeordnete und von der Phase unabhängig Daten.

Regeln:
- Organe können ausschliesslich in der Phase Abklärung hinzugefügt werden.

##### Item: Phase Abklärung starten
Mit dem Anlegen der Episode wird die Phase Abklärung eröffnet.

Regeln:
- Der Starttermin wird durch den User angegeben.
- Der Endtermin ist gleich dem Starttermin der nächsten Phase.

#### Item: Phase Listung starten
Der User entscheidet, wann die Phase Listung gestartet wird. Dies erfolgt durch eine explizite Auslösung dieser Phase in der GUI.

Regeln:
- Der Starttermin wird durch den User angegeben. Dies erfolgt durch explizite Erfassung der angaben zur Listung (siehe separates Item).
- Der Endtermin ist gleich dem Starttermin der nächsten Phase.

#### Item: Phase Koordination/Allokation starten
Die Phase Koordination/Allokation und damit die Gesamtphase Koordination wird im Rahmen des Use Case Koordination gestartet: Sobald eine Episode einer Koordination zugeordnet wird, wechselt die Episode in die Phase Koordination/Allokation.

Regeln:
- Der Starttermin der gesamten Koordination erfolgt durch das Datum der zugeordneten Koordination.

#### Item: Phase Koordination/Transplantation starten
Die Phase Koordination/Transplantation wird im Rahmen des Use Case Koordination gestartet: im Protocol vermerkt ist, dass alle Organe der Episode transplantiert wurden, wechselt die Phase.

Regeln:
- Der Endtermin der gesamten Koordination ist gleich dem Start der Nachbetreuung.
- 
#### Item: Phase Nachbetreuung starten
Die Phase Nachbetreuung startet, sobald die  Koordination, aus der heraus diese Phase entstand, als abgeschlossen markiert wird.

Regeln:
- Der Starttermin ist gleich dem Abschluss der Koordination und wird aus diesem Prozess heraus gesetzt.
- Der Endtermin ist wird durch due User im Rahmen des Abschlusses der Episode gesetzt.
- Die Episode ist dann abgeschlossen und kann nicht mehr geändert werden.

#### Item: Phase Abgeschlossen starten
Eine Episode kann aus diesen Gründen abgeschlossen werden:
- Die Episode wird explizit aus der Nachbetreuung heraus abgeschlossen.
- Die Episode wird abgelehnt (siehe folgende Items).
- Die Episode wird storniert (siehe folgende Items)

Der Abschluss wird aus dem jeweiligen Kontext heraus ausgelöst.

Regeln:
- Das Abschlussdatum ist das letzte Datum im Prozess.

##### Item: Episode ablehnen
Episoden können aus medizinischen oder anderen Gründen abgelehnt werden. Die Ablehnung kann erfolgen, solange die Phase Koordination nicht gestartet wurde.
Die Erfassung der Tatsache erfolgt im Kontext der Übersicht der Episoden.

##### Item: Episode stornieren
Episoden können storniert werden. Sie gelten dann als in dem Zustand beendet, in dem sie sich gerade befinden. Das System führt alle allenfalls notwendigen Abschlussarbeiten durch.

#### Story: Episode Übersicht anzeigen [Spec]

#### Item: Filtern auf Episoden
In der Übersicht kann wie folgt gefiltert werden:
- Nur offene Episoden anzeigen (Default)
- Zusätzlich abgeschlossene Episoden anzeigen
- Zusätzlich stornierte Episoden anzeigen

## Use Case: Episoden GUI [Spec]
Der Use case ist Teil der Gesamtstory Patienten als Empfänger.

### Story: Episoden Tab
Das Tab für Episoden beseht aus diesen Teilen:
- Liste aller Episoden eines Patienten
- Pro ausgewählter Episode werden alle Details der episode angezeigt
Details werden in der Folge angegeben.
