#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os
import shutil

'''
strktlink.py - Eine Hierarchische Struktur mit Links erzeugen
Copyright (c) Nov. 2020: Andreas Ulrich
<http://erasand.ch>, <andreas@erasand.ch>

LIZENZ
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

DEUTSCHE ÜBERSETZUNG: <http://www.gnu.de/documents/gpl-3.0.de.html>
'''


# Mit welchem Befehl soll der Symlink erzeugt werden:
# "os.symlink", "(Bash) ln", "Shortcut.exe", "mklink /J", "bat"
SYMLINK = "os.symlink"
# Quell-Pfad mit den Original Verzeichnissen
QUELLE = "./Struktur_Test/Synchronisationen/"
# Zeil-Pfad für die struktur
ZIEL = "./Struktur_Test/Modell/"
# Archiv Verzeichnis für die bestehenden Strukturen
ARCHIV = "./Struktur_Test/Archiv/"
# Verzeichnisse welche direkt verlinkt werden können
DIREKT_LINK = {
    "erasand_MANAG_Organisation":
        "Management/1_Organisation",
    "erasand_MANAG_Strategie":
        "Management/2_Strategie",
    "erasand_MANAG_Ziele":
        "Management/3_Ziele",
    "erasand_SUPP_Linux__2018":
        "Support/1_Linux/Linux_2018",
    "erasand_SUPP_Linux__2019":
        "Support/1_Linux/Linux_2019",
    "erasand_SUPP_Mac__2018":
        "Support/2_Mac/Linux_2018",
    "erasand_SUPP_Mac__2019":
        "Support/2_Mac/Linux_2019",
    "erasand_SUPP_Windows__2018":
        "Support/3_Windows/Windows_2018",
    "erasand_SUPP_Windows__2019":
        "Support/3_Windows/Windows_2019",
    "erasand_WORK_erasand__2018":
        "Arbeiten/erasand/erasand_2018",
    "erasand_WORK_erasand__2019":
        "Arbeiten/erasand/erasand_2019",
    "erasand_WORK_Linux__2018":
        "Arbeiten/Linux/Linux_2018",
    "erasand_WORK_Linux__2019":
        "Arbeiten/Linux/Linux_2019",
    "erasand_WORK_Windows__2018":
        "Arbeiten/Windows/Windows_2018",
    "erasand_WORK_Windows__2019":
        "Arbeiten/Windows/Windows_2019",
    "erasand_PROJ_2019":
        "Projekte/Projekte_2019"
}
# Verzeichnisse welche Variabel, das heisst abhängig von der Endung
# Verlinkt werden sollen
VAR_LINK = {
    "erasand_PROJ_2018__":
        "Projekte/Projekte_2018",
    "erasand_PROJ_2020__":
        "Projekte/Projekte_2020",
}
# Verzeichnisse welche unbekannt sind und in einen separate Struktur
# verlinkt werden.
UNBEKANNT = "Unbekannt"


def logger(nummer, text, wert):
    '''
    Gibt auf dem Bildschirm eine Nachricht mit fortlaufender Nummer,
    einem Text und dem Wert aus. Am Ende wird die Nummer zurück gegeben.
    '''
    # Nummer hochzählen
    nummer += 1
    # Text mit vorangestellter Hex-Dez Nummber ausgeben
    wert_text = str(wert)
    if len(wert_text) > 40:
        wert_text = "{}..".format(wert_text[:39])
    print("# {0:X} - {1} - {2} #".format(
        nummer,
        text,
        str(wert_text)))
    # Nummer zurückgeben
    return(nummer)


def timetext():
    '''
    Erzeugt einen Text für Dateinmaen mit dem aktuellen Datum und
    akuteller Uhrzeit.
    '''
    text = time.strftime(
        '%Y-%m-%d_%H-%M-%S',
        time.localtime(time.time())
    )
    return(text)


def makelink(quell_pfad, ziel_pfad):
    '''
    Erzeugt eine Verknüpfung mit dem Pfad, je nach Betriebssystem.
    Falls der Ordner des Pfades nicht existiert, wird er erstellt.
    '''
    verz_pfad = os.path.dirname(ziel_pfad)
    # Prüfen ob Verzeichnis existiert
    if not os.path.isdir(verz_pfad):
        # Verzeichnis existiert nicht: Erzeugen
        os.makedirs(verz_pfad)
    # Verknüpfung erzeugen
    if SYMLINK == "os.symlink":
        # Python os.symlink Befehl verwenden
        os.symlink(
            os.path.abspath(quell_pfad),
            os.path.abspath(ziel_pfad)
        )
        rueck = "{0} erzeugt".format(SYMLINK)
    elif SYMLINK == "(Bash) ln":
        # Bash ln-Befehl verwenden
        # Befehlskette erzeugen
        befehl = "ln -s {0} {1}".format(
            os.path.abspath(quell_pfad),
            os.path.abspath(ziel_pfad)
        )
        rueck = os.system(befehl)
        rueck = "{0} erzeugt; {1}".format(SYMLINK, str(rueck))
    elif SYMLINK == "mklink /J":
        # Windows mklink /J Befehl verwenden
        # Befehlskette erzeugen
        befehl = 'mklink /J "{0}.lnk" "{1}"'.format(
            os.path.abspath(ziel_pfad),
            os.path.abspath(quell_pfad)
        )
        rueck = os.system(befehl)
        rueck = "{0} erzeugt; {1}".format(SYMLINK, str(rueck))
    elif SYMLINK == "Shortcut.exe":
        # Shortcut.exe verwenden
        # Befehlskette erzeugen
        befehl = 'shortcut.exe /F:"{0}.lnk" /A:C /T:"{1}"'.format(
            os.path.abspath(ziel_pfad),
            os.path.abspath(quell_pfad)
        )
        rueck = os.system(befehl)
        rueck = "{0} erzeugt; {1}".format(SYMLINK, str(rueck))
    elif SYMLINK == "bat":
        # Windows Batch Datei verwenden
        # Befehlskette erzeugen
        text = '@echo off\n'
        text = '{0}start explorer "{1}"\n'.format(
            text,
            os.path.abspath(quell_pfad)
        )
        # Batch Datei speichern
        datei_name = "{}.bat".format(ziel_pfad)
        try:
            fileObj = open(
                datei_name,
                'w',
                encoding='utf-8',
                errors='ignore'
            )
            fileObj.write(text)
            fileObj.close()
        except Exception:
            print('Fehler beim Speichern.')
        rueck = "{0} erzeugt {1}".format(SYMLINK, ziel_pfad)
    else:
        rueck = "Shortcut Befehl nicht definiert."
    return(rueck)


if __name__ == '__main__':
    #
    # Eine Vielzahl von Verzeichnissen mit Verknüpfungen
    # hierarchisch abbilden.
    # 2 Methoden zur Erzeugung der Hierarchie:
    # - Vergleiche von Namensanfang mit Namensende mit einem
    #   Verzeichnis ergeben die Speicherorte der Verknüpfungen
    # - Bei bestimmten Verzeichnissen wird der Namensanfang genommen
    #   und anhand des Endes wird der Wert erzeugt, z.B. fortlaufende
    #   Nummern, eindutige ID's etc.
    # Log-Nummer setzen
    log_nr = 0
    # Vorhandene Hierarchie prüfen
    if os.path.isdir(ZIEL):
        # Vorhandene Hierarchie sichern, Namen des Verzeichnisses auslesen
        archiv_pfadliste = ZIEL.split(os.sep)
        archiv_name = archiv_pfadliste[len(archiv_pfadliste) - 1]
        archiv_name = "{0}_{1}".format(archiv_name, timetext())
        archiv_pfad = os.path.join(ARCHIV, archiv_name)
        # Ins Archiv verschieben
        shutil.move(ZIEL, archiv_pfad)
        # Log-Meldung
        log_nr = logger(log_nr, "Archiv erstellt", archiv_pfad)
    else:
        # Keine vorhandene Struktur_Test
        # Log-Meldung
        log_nr = logger(log_nr, "Keine vorhandene Struktur", "")
    # Verzeichnis einlesen
    inhalt = os.listdir(QUELLE)
    # jeder Eintrag abarbeiten
    for i in inhalt:
        # Status der Verknüpfung, False = nicht erzeugt, True = erzeugt
        link_status = False
        if os.path.isdir(os.path.join(QUELLE, i)):
            # Der Eintrag ist ein Verzeichnis
            # Log-Meldung
            log_nr = logger(log_nr, "Verzeichnis", i)
            # Direkt Verlinkungen prüfen
            if not link_status:
                for j in DIREKT_LINK.keys():
                    if i.startswith(j):
                        # Verzeichnis gefunden, Link erzeugen
                        quell_pfad = os.path.join(QUELLE, i)
                        ziel_pfad = os.path.join(ZIEL, DIREKT_LINK[j])
                        rueck = makelink(quell_pfad, ziel_pfad)
                        # Log-Meldung
                        log_nr = logger(
                            log_nr,
                            "Verknüpfung erstellt",
                            "{0} / {1}".format(
                                ziel_pfad,
                                str(rueck)
                            )
                        )
                        # Status auf erzeugt setzen
                        link_status = True
            if not link_status:
                for j in VAR_LINK.keys():
                    if i.startswith(j):
                        # Verzeichnis gefunden, Link erzeugen
                        quell_pfad = os.path.join(QUELLE, i)
                        ziel_verz = os.path.join(ZIEL, VAR_LINK[j])
                        # Verknüpfungsname wird aus dem Quell Namen
                        # erzeugt, indem der Schlüsselbegriff (j)
                        # abgetrennt wird (mittels Indexierung).
                        ziel_name = i[len(j):]
                        ziel_pfad = os.path.join(ziel_verz, ziel_name)
                        rueck = makelink(quell_pfad, ziel_pfad)
                        # Log-Meldung
                        log_nr = logger(
                            log_nr,
                            "Verknüpfung erstellt",
                            "{0} / {1}".format(
                                ziel_pfad,
                                str(rueck)
                            )
                        )
                        # Status auf erzeugt setzen
                        link_status = True
            if not link_status:
                # Verzeicnis gefunden, Verknüpfung im Unbekannt
                # Verzeichnis erstellen, Link erzeugen
                quell_pfad = os.path.join(QUELLE, i)
                ziel_pfad = os.path.join(ZIEL, UNBEKANNT, i)
                rueck = makelink(quell_pfad, ziel_pfad)
                # Log-Meldung
                log_nr = logger(
                    log_nr,
                    "Verknüpfung erstellt",
                    "{0} / {1}".format(ziel_pfad, str(rueck))
                )
                # Status auf erzeugt setzen
                link_status = True
        else:
            # Kein Verzeichnis
            # Log-Meldung
            log_nr = logger(log_nr, "Kein Verzeichnis", i)
    log_nr = logger(log_nr, "Programm Ende, Anzahl Logs", log_nr)
