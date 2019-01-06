# -*- coding: utf-8 -*-

#Diese Hilfe wird vor dem Login auf der  Startseite angezeigt.
startseite = """\
<h1>Hilfe</h1>

<h3>Anmelden</h3>
<p>Um Dich auf auf unserer Seite anzumelden, benötigst Du Deine E-Mail-Adresse und Dein Passwort. Dies setzt eine einmalige
Registrierung voraus.</p>

<h3>Registrieren</h3>
<p>Um auf dieser Seite selbst verschiedene Aufgaben für Deine Schüler anzulegen und zu bearbeiten, benötigst Du ein gültiges Benutzerkonto. 
Bitte nutze den Button "Registrieren" um Dein Benutzerkonto anzulegen.
<p><strong>Sowohl die Registrierung als auch die Nutzung unserer Seite sind unentgeltlich.</strong></p>
"""


#Diese Hilfe wird nach dem Login bei der Auflistung der Aufgabenordner angezeigt.
meinordner = """\
<h1>Hilfe</h1>

<p>Mit Klick auf <span class="glyphicon glyphicon-plus"/> kannst Du Aufgabenordner hinzufügen.</p>

<p>In den <strong>Aufgabenordnern</strong> legst Du anschließend Übungen, Experimente und Arbeitsblätter für Deine Schüler an.</p>
"""


#Diese Hilfe wird innerhalb des Aufgabenordners angezeigt.
aufgabenliste = """\
<h1>Hilfe</h1>

<h3><span class="glyphicon glyphicon-plus"/> (Hinzufügen)</h3>
<p><strong>Mit Klick auf + kannst Du Deinem Aufgabenordner Übungen, Experimente, Arbeitsblätter und Bilder hinzufügen. Alle Aufgabentypen enthalten Pflichtfelder, die Du ausfüllen musst.
Dabei hast Du u.a. die Wahl, die Aufgabe als Selbsttest oder benotet an den Schüler weiterzugeben. Bei der benoteten Variante kannst Du Über einen QR-Code die Lösungen Deiner Schüler überprüfen.</p>

<h3>Zurück</h3>
<p>Bringt Dich in Deinen Ordner im Portal.</p>

<h3>Bearbeiten</h3>
<p>Bringt Dich in die Bearbeitungsmaske Deines aktuellen Aufgabenordners.</p>

<h3>Übung</h3>
<p><strong>Übungen</strong> dienen der Wissenskontrolle Deiner Schüler in Form von Freitext oder Multiple-Choice Antwortoptionen.</p>

<h3>Experiment</h3>
<p>Dieser Aufgabentyp eignet sich insbesondere für alle naturwissenschaftlichen Fächer. Mit diesem Aufgabentyp beschreibst Du den Versuchsaufbau
und die vom Schüler geforderten Versuchsreihen. Anhand Deiner Vorgaben kann der Schüler seine Messergebnisse selbständig überprüfen. Bei
benoteten Experimenten führst Du den Vergleich durch.

<h3>Arbeitsblatt</h3
<p>Für Deine digitalen <strong>Arbeitsblätter</strong> verwendest Du Deine Übungen und Experimente. Du kannst diese nach Deiner Wahl
auf dem Arbeitsblatt anordnen. Zusätzlich kannst Du Deinem Arbeitsblatt einen Prolog- und einen Epilog-Text hinzufügen.</p>
"""


#Diese Hilfe wird beim Hinzufügen und Bearbeiten des Aufgabenordners angezeigt.
aufgabenordner = """\
<h1>Hilfe</h1>

<p>Hier bearbeitest Du Deinen Aufgabenordner. Nachdem Du die Kurs-ID eingetragen hast, kannst Du Deine Eingaben speichern.
Optional besteht die Möglichkeit, eine Kurzbeschreibung sowie ein Bild hinzuzufügen. Nach dem Speichern kannst Du Deinen Ordner
mit verschiedenen Arten von Aufgaben (Übungen, Experimente) oder Materialen (Bilder) bestücken.</p>

<p>Auf Deiner Startseite siehst Du alle von Dir angelegten Aufgabenordner.</p>

<h3>Kurs-ID</h3>

<p>Hier vergibst Du die Identifikationsnummer (ID) des Kurses. Verwende entweder die ID aus dem dazugehörigen Kurs (iTunes U), oder vergib eine eigene
ID.</p>

<h3>Kurzbeschreibung</h3>

<p>In dieses Feld kannst Du eine genaue Bezeichnung oder Kurzbeschreibung eintragen. Diese wird auf Deiner Startseite zusätzlich
zur Kurs-ID angezeigt.</p>

<h3>Bild zum Aufgabenordner</h3>

<p>Jedem Aufgabenordner kannst Du optional ein kleines Vorschaubild hinzufügen. Dieses wird mit der Auflistung der
Aufgabenordner auf Deiner Startseite angezeigt.</p>
"""

#Diese Hilfe wird beim Anlegen oder bei Bearbeitung einer Übung angezeigt
uebung = """\
<h1>Hilfe</h1>

<p><strong>Übungen</strong> dienen der Wissenskontrolle Deiner Schüler in Form von Multiple-Choice Antwortoptionen.
Du kannst zwischen Selbsttest oder benoteter Aufgaben (Vergabe von Punkten) wählen. Außerdem ist es möglich, Lösungshinweise und Lernempfehlungen in Form von Text, Bildern oder Videos zu geben.</p>
"""

#Diese Hilfe wird bei der Einzelansicht einer Übung angezeigt
uebungsansicht = """\
<h1>Hilfe</h1>

<p><strong>Übungen</strong> dienen der Wissenskontrolle Deiner Schüler in Form von Multiple-Choice Antwortoptionen.
Du kannst zwischen Selbsttest oder benoteter Aufgaben (Vergabe von Punkten) wählen. Außerdem ist es möglich, Lösungshinweise und Lernempfehlungen 
in Form von Text, Bildern oder Videos zu geben.</p>

<h3>Link für iTunes U</h3>
<p>Den hier angegebenen Link musst Du mit Deinen Schülern teilen, um sie zur Bearbeitung der Übung aufzufordern. Du kannst diesen Link als Aufgabe in Deinen iTunes U Kurs einbinden. Bei benoteten Übungen wird ein Barcode generiert, den Dein Schüler mit Dir teilen muss, um Dir eine Bewertung zu
ermöglichen. Wenn Du iTunes U verwendest, können Deine Schüler den Barcode bei Dir einreichen (Upload).</p>
<p class="callout">Bitte teste den Link bevor Du ihn an Deine Schüler weitergibst.</p>
"""

#Diese Hilfe wird beim Anlegen oder bei Bearbeitung eines Experiments angezeigt
experiment = """\
<h1>Hilfe</h1>

<p><strong>Experimente</strong> dienen der Beschreibung des Versuchsaufbaus und der Definition von Versuchsreihen mit den von Dir erwarteten Ergebnissen. Bei Selbsttest-Experimenten können die Schüler selbständig ihre Messergebnisse überprüfen. Bei benoteten Experimenten wird ein Barcode
zum Download für den Schüler erzeugt. Wenn der Schüler den Barcode mit Dir teilt kannst Du die Messergebnisse prüfen und bewerten. Bei 
benoteten Experimenten kannst Du den Schüler außerdem auffordern, selbständig ein Fazit aus den Messergebnissen abzuleiten.</p>
"""

#Diese Hilfe wird bei der Einzelansicht eines Experiments angezeigt
experimentansicht = """\
<h1>Hilfe</h1>

<p><strong>Experimente</strong> dienen der Beschreibung des Versuchsaufbaus und der Definition von Versuchsreihen mit den von Dir erwarteten Ergebnissen. Bei Selbsttest-Experimenten können die Schüler selbständig ihre Messergebnisse überprüfen. Bei benoteten Experimenten wird ein Barcode
zum Download für den Schüler erzeugt. Wenn der Schüler den Barcode mit Dir teilt kannst Du die Messergebnisse prüfen und bewerten. Bei 
benoteten Experimenten kannst Du den Schüler außerdem auffordern, selbständig ein Fazit aus den Messergebnissen abzuleiten.</p>

<h3>Link für iTunes U</h3>
<p>Den hier angegebenen Link musst Du mit Deinen Schülern teilen, um sie zur Bearbeitung des Experiments aufzufordern. Du kannst diesen Link als Aufgabe in Deinen iTunes U Kurs einbinden. Bei benoteten Experimenten wird ein Barcode generiert, den Dein Schüler mit Dir teilen muss, um Dir 
eine Bewertung zu ermöglichen. Wenn Du iTunes U verwendest, können Deine Schüler den Barcode bei Dir einreichen (Upload).</p>
<p class="callout">Bitte teste den Link bevor Du ihn an Deine Schüler weitergibst.</p>
"""

#Diese Hilfe wird beim Anlegen oder bei Bearbeitung eines Arbeitsblatts angezeigt
arbeitsblatt = """\
<h1>Hilfe</h1>

<p><strong>Arbeitsblätter</strong> erlauben Dir die Kombination von Text, Übungen und Experimenten zu komplexen Aufgabenstellungen.</p>
"""

#Diese Hilfe wird bei der Einzelansicht eines Arbeitsblattes angezeigt
arbeitsblattansicht = """\
<h1>Hilfe</h1>

<p><strong>Arbeitsblätter</strong> erlauben Dir die Kombination von Text, Übungen und Experimenten zu komplexen Aufgabenstellungen.</p>

<h3>Link für iTunes U</h3>
<p>Den hier angegebenen Link musst Du mit Deinen Schülern teilen, um sie zur Bearbeitung des Arbeitsblattes aufzufordern. Du kannst diesen Link als Aufgabe in Deinen iTunes U Kurs einbinden. Bei benoteten Arbeitsblättern wird ein Barcode generiert, den Dein Schüler mit Dir teilen muss, um Dir 
eine Bewertung zu ermöglichen. Wenn Du iTunes U verwendest, können Deine Schüler den Barcode bei Dir einreichen (Upload).</p>
<p class="callout">Bitte teste den Link bevor Du ihn an Deine Schüler weitergibst.</p>
"""
