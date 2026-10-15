




Dennis Part:





Fabians Part:




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