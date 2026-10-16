

# Was ist Git?
Git ist ein freies und quelloffenes Versionskontrollsystem, das ursprünglich von Linus Torvalds im Jahr 2005 entwickelt wurde. Es dient dazu, Änderungen an Dateien innerhalb eines Projekts zu erfassen, zu speichern und zu verwalten. Obwohl Git vor allem in der Softwareentwicklung eingesetzt wird, kann es grundsätzlich auch für die Versionsverwaltung anderer textbasierter Dateien verwendet werden.
Ein wesentliches Merkmal von Git ist seine dezentrale Architektur. Im Gegensatz zu zentralisierten Versionskontrollsystemen verfügt jede lokale Arbeitskopie eines Projekts in der Regel über eine vollständige Kopie der Versionshistorie. Dadurch können Änderungen unabhängig von einem zentralen Server vorgenommen und dokumentiert werden. Der Austausch von Änderungen zwischen verschiedenen Entwicklerinnen und Entwicklern erfolgt bei Bedarf über sogenannte Remote-Repositories, also entfernte Projektarchive.
Die Verwaltung der Änderungen basiert auf sogenannten Commits. Ein Commit repräsentiert einen dokumentierten Zustand des Projekts und enthält Informationen über die vorgenommenen Änderungen sowie Metadaten, beispielsweise eine Zeitangabe und die Identität der verantwortlichen Person. Auf diese Weise entsteht eine nachvollziehbare Entwicklungshistorie, anhand derer frühere Projektzustände untersucht und bei Bedarf wiederhergestellt werden können.

# Warum sollte Git verwendet werden?
Der Einsatz von Git bietet mehrere Vorteile, die sowohl für individuelle Entwicklungsprojekte als auch für die kollaborative Softwareentwicklung relevant sind.

	## Nachvollziehbarkeit und Versionshistorie
	Ein wesentlicher Vorteil von Git besteht in der systematischen Dokumentation von Änderungen. Durch die Speicherung einzelner Commits lässt sich nachvollziehen, welche Anpassungen zu welchem Zeitpunkt vorgenommen wurden. Dies erleichtert insbesondere die Fehlersuche, da Änderungen identifiziert werden können, die möglicherweise zu unerwartetem Verhalten oder Fehlern in einer Anwendung geführt haben.
	Darüber hinaus ermöglicht Git die Wiederherstellung früherer Projektzustände. Dadurch wird das Risiko reduziert, dass funktionierende Implementierungen durch spätere Änderungen dauerhaft verloren gehen.
	
	## Unterstützung der Zusammenarbeit
	Bei größeren Softwareprojekten arbeiten häufig mehrere Personen parallel an unterschiedlichen Komponenten desselben Systems. Ohne eine geeignete Versionsverwaltung kann dies zu Konflikten führen, beispielsweise wenn mehrere Personen dieselbe Datei bearbeiten.
	Git ermöglicht es, Änderungen verschiedener Beteiligter zusammenzuführen. Treten dabei widersprüchliche Änderungen auf, sogenannte Merge-Konflikte, können diese gezielt analysiert und aufgelöst werden. Somit unterstützt Git eine strukturierte Zusammenarbeit und verbessert die Nachvollziehbarkeit gemeinsamer Entwicklungsprozesse.
	
	## Parallele Entwicklung durch Branches
	Ein weiteres zentrales Konzept von Git ist die Verwendung von Branches (Entwicklungszweigen). Diese ermöglichen es, neue Funktionen zu implementieren, Fehler zu beheben oder experimentelle Änderungen vorzunehmen, ohne unmittelbar den Hauptentwicklungsstand zu verändern.
	Nach Abschluss und Überprüfung der jeweiligen Arbeiten können die Änderungen in einen anderen Entwicklungszweig integriert werden. Dadurch lassen sich unterschiedliche Entwicklungsaufgaben voneinander trennen, was insbesondere bei umfangreichen Projekten zur Strukturierung des Entwicklungsprozesses beiträgt.
	
	## Dezentrale Arbeitsweise und Ausfallsicherheit
	Da Git-Repositories üblicherweise die vollständige Versionshistorie enthalten, können viele Operationen lokal und ohne permanente Internetverbindung durchgeführt werden. Dazu gehören beispielsweise das Erstellen von Commits, das Vergleichen von Versionen und das Wechseln zwischen Entwicklungszweigen.
	Diese dezentrale Architektur reduziert die Abhängigkeit von einem ständig verfügbaren zentralen Server. Zudem kann eine vorhandene Repository-Kopie unter bestimmten Voraussetzungen zur Wiederherstellung der Versionshistorie beitragen. Git ersetzt jedoch keine vollständige Backup-Strategie, da beispielsweise ungesicherte lokale Änderungen oder der Verlust sämtlicher Repository-Kopien weiterhin zu Datenverlust führen können.
	
	## Integration in moderne Entwicklungsprozesse
	Git bildet eine wichtige Grundlage für zahlreiche moderne Werkzeuge und Arbeitsabläufe der Softwareentwicklung. Plattformen wie GitHub und GitLab nutzen Git beispielsweise zur Verwaltung von Quellcode, zur Durchführung von Code-Reviews und zur Organisation gemeinsamer Entwicklungsarbeit.
	Darüber hinaus lässt sich Git mit automatisierten Test- und Bereitstellungsprozessen kombinieren. Im Rahmen von Continuous Integration und Continuous Delivery (CI/CD) können Änderungen beispielsweise automatisch getestet werden, sobald sie in ein Repository übertragen werden. Dadurch unterstützt Git die Standardisierung und Automatisierung von Entwicklungsabläufen.
	
#Grundlegende Funktionsweise von Git
Die praktische Anwendung von Git basiert auf mehreren grundlegenden Arbeitsschritten:
	1.  Repository erstellen oder klonen: Ein Repository bildet den zentralen Verwaltungsbereich eines Projekts und enthält dessen Versionshistorie.
	2.  Dateien bearbeiten: Änderungen werden zunächst im lokalen Arbeitsverzeichnis vorgenommen.
	3.  Änderungen vormerken: Mit git add werden ausgewählte Änderungen für den nächsten Commit vorbereitet.
	4.  Änderungen speichern: Der Befehl git commit dokumentiert die vorgemerkten Änderungen als neuen Eintrag in der Versionshistorie.
	5.  Änderungen austauschen: Mit git push können lokale Commits an ein entferntes Repository übertragen werden. git pull dient dazu, Änderungen aus einem entfernten Repository abzurufen und in den lokalen Entwicklungsstand zu integrieren.
	
Dabei ist zu beachten, dass Git nicht automatisch jede Änderung dauerhaft speichert. Änderungen müssen bewusst vorgemerkt und committet werden, damit sie Bestandteil der Versionshistorie werden.





# Grundlegende Git-Befehle

## Einleitung

Git ist ein verteiltes Versionskontrollsystem, mit dem Änderungen an Dateien und Projekten verfolgt werden können. Es wird häufig in der Softwareentwicklung eingesetzt, um gemeinsam an Projekten zu arbeiten und frühere Versionen wiederherzustellen.

In diesem README werden die wichtigsten Git-Befehle vorgestellt und anhand von Beispielen erklärt.

## 1\. Repository erstellen – `git init`

Mit `git init` wird ein neues Git-Repository im aktuellen Verzeichnis erstellt. Dadurch kann Git die Änderungen an den Dateien verfolgen.

```
git init
```

**Beispiel:** Ein neues Projekt soll mit Git verwaltet werden. Dazu wird im Projektverzeichnis der Befehl ausgeführt.

## 2\. Dateien zum Staging-Bereich hinzufügen – `git add`

Mit `git add` werden Änderungen für den nächsten Commit vorgemerkt.

```
git add datei.txt
```

Um alle Änderungen im aktuellen Verzeichnis hinzuzufügen, kann folgender Befehl verwendet werden:

```
git add .
```

**Beispiel:** Eine geänderte Datei wird mit `git add` für den nächsten Commit vorbereitet.

## 3\. Änderungen speichern – `git commit`

Mit `git commit` werden die vorgemerkten Änderungen als neuer Versionsstand im lokalen Repository gespeichert. Jeder Commit sollte eine aussagekräftige Nachricht enthalten.

```
git commit -m "Erste Version erstellt"
```

Die Option `-m` ermöglicht es, direkt eine Commit-Nachricht anzugeben.

**Beispiel:** Nach dem Hinzufügen einer neuen Datei wird ein Commit erstellt, um den aktuellen Stand des Projekts zu speichern.

## 4\. Änderungen überprüfen – `git status`

Mit `git status` kann überprüft werden, welche Dateien geändert wurden, welche Dateien neu sind und welche Änderungen bereits für einen Commit vorgemerkt wurden.

```
git status
```

Dieser Befehl ist besonders hilfreich, um vor einem Commit den aktuellen Zustand des Repositorys zu kontrollieren.

## 5\. Änderungen anzeigen – `git diff`

Mit `git diff` werden Änderungen zwischen dem aktuellen Arbeitsverzeichnis und dem letzten gespeicherten Stand angezeigt.

```
git diff
```

Damit lässt sich nachvollziehen, welche Zeilen in Dateien hinzugefügt, geändert oder entfernt wurden.

## 6\. Repository herunterladen oder klonen – `git clone`

Mit `git clone` wird ein vorhandenes Repository kopiert. Dabei werden auch die Versionshistorie und die zugehörigen Git-Daten übernommen.

```
git clone https://github.com/benutzer/projekt.git
```

Die URL muss durch die tatsächliche Adresse des gewünschten Repositorys ersetzt werden.

## 7\. Änderungen auf einen Remote-Server übertragen – `git push`

Mit `git push` werden lokale Commits in ein entferntes Repository übertragen, beispielsweise zu GitHub oder GitLab.

```
git push origin main
```

Dabei steht `origin` normalerweise für das entfernte Repository und `main` für den Branch, in den die Änderungen übertragen werden sollen.

## 8\. Änderungen herunterladen – `git pull`

Mit `git pull` werden neue Änderungen aus einem entfernten Repository abgerufen und in den aktuellen Branch integriert.

```
git pull origin main
```

Dieser Befehl ist besonders wichtig, wenn mehrere Personen gemeinsam an einem Projekt arbeiten.

## 9\. Branches verwalten – `git branch` und `git switch`

Branches ermöglichen es, unabhängig voneinander an neuen Funktionen oder Änderungen zu arbeiten.

Alle lokalen Branches anzeigen:

```
git branch
```

Einen neuen Branch erstellen:

```
git branch neuer-branch
```

Zu einem bestehenden Branch wechseln:

```
git switch neuer-branch
```

Einen neuen Branch erstellen und direkt zu ihm wechseln:

```
git switch -c neuer-branch
```

## Typischer Arbeitsablauf

Ein einfacher Git-Arbeitsablauf sieht folgendermaßen aus:

```
# 1. Repository initialisieren
git init

# 2. Dateien zum Staging-Bereich hinzufügen
git add .

# 3. Änderungen lokal speichern
git commit -m "Erste Version erstellt"

# 4. Änderungen auf den Remote-Server übertragen
git push origin main
```

**Hinweis:** Für den letzten Schritt muss bereits ein Remote-Repository eingerichtet sein. Bei einem neu erstellten Repository muss gegebenenfalls zuerst ein Remote hinzugefügt werden:

```
git remote add origin https://github.com/benutzer/projekt.git
```

Falls der lokale Branch noch keinen Upstream-Branch besitzt, kann der erste Push so erfolgen:

```
git push -u origin main
```

## Zusammenfassung

Die grundlegenden Git-Befehle helfen dabei, Projekte übersichtlich zu verwalten und Änderungen nachvollziehbar zu speichern.

| Befehl | Funktion |
| --- | --- |
| `git init` | Erstellt ein neues Repository |
| `git add` | Bereitet Änderungen für einen Commit vor |
| `git commit` | Speichert Änderungen lokal |
| `git status` | Zeigt den aktuellen Repository-Status |
| `git diff` | Zeigt Dateiänderungen an |
| `git clone` | Kopiert ein vorhandenes Repository |
| `git push` | Überträgt Commits zum Remote-Repository |
| `git pull` | Holt Änderungen aus einem Remote-Repository |
| `git branch` | Zeigt oder verwaltet Branches |
| `git switch` | Wechselt den Branch |

Mit diesen Befehlen lassen sich die wichtigsten Aufgaben der Versionsverwaltung mit Git erledigen. Sie bilden die Grundlage für die strukturierte Entwicklung und die Zusammenarbeit in Softwareprojekten.



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





## Dokumentation der Zusammenarbeit:

* **Dennis Schmelzet:** Erstellung des GitHub-Repositories, Anlegen der leeren README.md-Datei, Ausarbeitung der Abschnitte „Was ist Git und warum sollte es verwendet werden?“ sowie „Grundlegende Git-Befehle (git init, git add, git commit, git push)“.
* **Fabian Scholl:** Ausarbeitung des Abschnitts „Branches und ihre Nutzung, Umgang mit Merge-Konflikten“, Durchführung des finalen Merges in den Haupt-Branch, Ergänzung dieser Notiz zur Teamarbeit und Hochladen des Repository-Links auf Moodle.
* **Marei Wiesehan:** Ausarbeitung der Abschnitte zur Bedienung von IntelliJ IDEA und PyCharm (Local vs. Remote Repository) sowie Vorstellung nützlicher Git-Tools und Plattformen (GitHub, GitLab, GitHub Desktop).