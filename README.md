




Dennis Part:





Fabians Part:

## Branches und ihre Nutzung, Umgang mit Merge-Konflikten

Wenn mehrere Leute gleichzeitig an einem Projekt arbeiten, will man nicht aus Versehen den funktionierenden Code der anderen kaputtmachen. Genau dafür nutzt man in Git sogenannte Branches (Zweige).

### Was sind Branches und wozu braucht man sie?

Der Hauptzweig eines Projekts heißt meistens `main`. Dort sollte immer nur Code liegen, der auch wirklich funktioniert. 

Wenn man nun an einer neuen Aufgabe oder einem eigenen Abschnitt arbeitet, erstellt man sich einen eigenen Branch. Das ist im Prinzip eine eigene Arbeitskopie vom Projekt. 

**Vorteile von Branches:**
- Man kann in Ruhe Dinge ausprobieren, ohne die Arbeit des Teams zu stören.
- Alle im Team können gleichzeitig an ihren eigenen Themen arbeiten.
- Wenn der eigene Teil fertig ist, lässt man kurz jemanden über einen Pull Request drüberschauen und fügt ihn erst dann wieder mit dem `main`-Branch zusammen (Merge).

### Typischer Ablauf beim Arbeiten mit Branches

**1. Neuen Branch erstellen und wechseln**
- Bevor man anfängt zu tippen, legt man einen neuen Branch an (in PyCharm unten rechts auf den aktuellen Branch klicken oder im Terminal mit `git switch -c branch-name`).
- Danach arbeitet man komplett unabhängig vom Hauptprojekt.

**2. Änderungen zwischenspeichern (Commits)**
- Man bearbeitet seine Dateien ganz normal.
- Zwischendurch speichert man seine Fortschritte regelmäßig mit einem Commit und einer kurzen Info-Nachricht ab (`git add .` und `git commit -m "Nachricht"`).

**3. Branch hochladen und zusammenführen**
- Mit `git push` lädt man seinen Branch auf GitHub hoch.
- Auf GitHub erstellt man dann einen Pull Request.
- Nachdem ein Teammitglied kurz drübergeschaut hat, wird der Branch in den `main`-Branch gemerged.

---

## Umgang mit Merge-Konflikten

Normalerweise führt Git Änderungen von verschiedenen Leuten automatisch zusammen. Ein **Merge-Konflikt** passiert nur dann, wenn zwei Personen zur selben Zeit **genau dieselbe Zeile** in einer Datei geändert haben. Git weiß dann nicht, welche Version die richtige ist, und fragt nach.

### Konflikte in PyCharm oder IntelliJ lösen (einfachster Weg)

Wenn es beim Zusammenführen einen Konflikt gibt, öffnet die IDE automatisch ein kleines Fenster.

1. Auf **„Merge...“** klicken.
2. Es öffnet sich eine Ansicht mit drei Spalten:
   - **Links:** Die eigenen Änderungen.
   - **Rechts:** Die Änderungen vom anderen Branch / von GitHub.
   - **Mitte:** Das fertige Ergebnis.
3. Mit den kleinen Pfeilen (`>>` und `<<`) klickt man sich einfach zusammen, welche Zeilen in die Mitte übernommen werden sollen. Man kann in der Mitte auch direkt Text anpassen.
4. Wenn alles passt, unten rechts auf **„Apply“** klicken. Damit ist der Konflikt gelöst.

### Konflikte manuell im Editor lösen

Falls man kein Tool nutzt, schreibt Git solche Markierungen direkt in den Text:

```text
<<<<<<< HEAD
Hier steht meine eigene Version vom Satz.
=======
Hier steht die Version von meinem Teammitglied.
>>>>>>> anderer-branch
```

Mareis Part:

## Git mit IntelliJ IDEA und PyCharm benutzen

IntelliJ IDEA und PyCharm sind Entwicklungsumgebungen (IDEs) von JetBrains. Beide Programme unterstützen Git direkt. Dadurch kann man viele Git-Funktionen verwenden, ohne alle Befehle im Terminal eingeben zu müssen. Direkt über Reiter im Hauptmenu.

### Local Repository und Remote Repository

**Local Repository:**

Ein lokales Repository befindet sich auf dem eigenen Computer. Hier kann man Dateien bearbeiten, Änderungen speichern und Commits erstellen. Dafür ist keine Internetverbindung erforderlich. Hier ist Arbeit im Team eher schwierig.

**Remote Repository:**

Ein Remote Repository befindet sich beispielsweise auf GitHub. Es ermöglicht, Änderungen mit anderen Teammitgliedern zu teilen und gemeinsam an einem Projekt zu arbeiten.

**Unterschied:**

- Local Repository = Projekt und Git-Versionsverlauf auf dem eigenen Computer
- Remote Repository = Gemeinsames Repository auf einem Server (Github, Gitlab(...))

### Git in IntelliJ IDEA oder PyCharm verwenden (ohne Konsole)

**1. Du musst ein Repository klonen**

- IntelliJ IDEA oder PyCharm öffnen.
- „Get from VCS“ beziehungsweise „Clone Repository“ auswählen.
- Die URL des GitHub-Repositories einfügen oder nach Einloggen und Verifizierung mit Github Repository aus Liste auswählen.
- Auf „Clone“ klicken.

Das Projekt wird nun lokal auf dem Computer gespeichert.

**2. Einen Branch erstellen**

- Unten rechts auf den aktuellen Branch-Namen klicken. Oder auf dem Reiter im Menu Git 
- „New Branch“ auswählen.
- Einen Namen für den Branch eingeben.
- Den neuen Branch erstellen und zu ihm wechseln. (Überprüfe zur Sicherheit, dass oben links in der Leiste wirklich der Name steht)

Branches ermöglichen es, unabhängig vom Hauptprojekt an Änderungen zu arbeiten.

**3. Änderungen committen**

- Eine Datei im Projekt bearbeiten.
- Das Commit-Fenster über die IDE öffnen.
- Die gewünschten Änderungen auswählen.
- Eine passende Commit-Nachricht eingeben und nachvollziehbar für dein Team kommentieren.
- Auf „Commit“ klicken.

Der Commit speichert die Änderungen im lokalen Git-Verlauf.

**4. Änderungen auf GitHub hochladen**

- Im Git-Menü „Push“ auswählen.
- Die hochzuladenden Commits überprüfen.
- Auf „Push“ klicken.

Dadurch werden die Commits an das Remote Repository übertragen.

**5. Änderungen herunterladen**

Über „Git → Pull“ können Änderungen vom Remote Repository heruntergeladen und in den aktuellen lokalen Branch integriert werden.

---

## Nützliche Git-Tools und Plattformen

Neben Git gibt es verschiedene Programme und Plattformen, die die Arbeit mit Versionskontrolle erleichtern.

### GitHub

GitHub ist eine Online-Plattform zum Speichern und Verwalten von Git-Repositories.

Wichtige Funktionen:

- **Repositories:** Projekte online speichern und gemeinsam bearbeiten.
- **Pull Requests:** Änderungen überprüfen lassen, bevor sie in den Haupt-Branch übernommen werden.
- **Issues:** Aufgaben, Fehler und Verbesserungsvorschläge dokumentieren.
- **Code Reviews:** Änderungen anderer Teammitglieder kontrollieren und kommentieren.

Im Berufsalltag wird Github oft für Bewerbungen genutzt

### GitLab

GitLab ist eine weitere Plattform zur Verwaltung von Git-Repositories. Ähnlich wie GitHub unterstützt GitLab die Zusammenarbeit im Team, Code Reviews und die Automatisierung von Entwicklungsprozessen.

### GitHub Desktop

GitHub Desktop ist ein Programm, mit dem Git über eine grafische Benutzeroberfläche bedient werden kann.

Damit lassen sich beispielsweise Commits erstellen, Branches wechseln und Änderungen hochladen, ohne Git-Befehle im Terminal eingeben zu müssen.
Es soll die Arbeit mit Git übersichtlicher erleichtern. 

### IntelliJ IDEA und PyCharm

Beide Entwicklungsumgebungen verfügen über integrierte Git-Werkzeuge. Dadurch können Entwickler direkt beim Programmieren Änderungen verfolgen, Commits erstellen und mit Remote Repositories arbeiten.




Wer war wofür zuständig Doku: