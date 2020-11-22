#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os

'''
compdirs.py - 2 Verzeichnis-Strukturen vergleichen
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


# Definition der ersten und der zweiten Struktur (Quelle und Zeil)
QUELLE = "../2020_Rezepte"
ZIEL = "."


def lenlist(liste):
    '''
    Sucht die grösste Anzahl von Zeichen eines Textes in der liste und
    rückgabe der Länge
    '''
    max_anz = 0
    for i in liste:
        if len(i) > max_anz:
            max_anz = len(i)
    return(max_anz)


def savetext(text, pfad):
    '''
    Speichert den Text beim Pfad ab.
    text = "  "
    pfad = '/pfad'
    '''
    try:
        datei_objekt = open(pfad, 'w')
        datei_objekt.write(text)
        datei_objekt.close()
    except Exception:
        t = "Es gab einen Fehler beim Spechern.\n"
        t = "{0}Datei = {1}\nText = {2}\n".format(t, pfad, text)
        print(t)


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


def logger(nummer, text, wert):
    '''
    Gibt auf dem Bildschirm eine Nachricht mit fortlaufender Nummer,
    einem Text und dem Wert aus. Am Ende wird die Nummer zurück gegeben.
    '''
    # Nummer hochzählen
    nummer += 1
    # Text mit vorangestellter Hex-Dez Nummber ausgeben
    print("{0:X} # {1} # {2}".format(nummer, text, str(wert)))
    # Nummer zurückgeben
    return(nummer)


def dirs(pfad):
    '''
    Mit os.walk() das aktuelle Verzeichnis und alle Unterverzeichnisse
    durchsuchen. Das Ergbnis in der Verzeichnis-Liste und der
    Datei-Liste zurückgeben.
    pfad = 'pfad'
    verzeichnis_liste = ['pfad',  ]
    datei_liste = ['pfad/name',  ]
    '''
    datei_liste = []
    verzeichnis_liste = []
    for root, dirs, files in os.walk(pfad, topdown=False):
        for name in files:
            datei_liste.append(os.path.join(root, name))
        for name in dirs:
            verzeichnis_liste.append(os.path.join(root, name))
    return(verzeichnis_liste, datei_liste)


def datinfo(datei_liste):
    '''
    Erzeugt anhand der Datei-Liste eine Informationsverzeichns mit
    Datum und Grösse der Dateien
    datei_liste = ['pfad/name',  ]
    info_verzeichnis = {'pfad/name': ('datum', groesse),  }
    '''
    info_verzeichnis = {}
    # Lese jede Datei und hole Änderungsdatum & Dateigrösse
    for i in datei_liste:
        if os.path.isfile(i):
            # Das Element ist eine Datei
            datum = os.path.getmtime(i)
            datum_text = time.strftime(
                '%d.%m.%Y %H:%M:%S',
                time.localtime(datum)
            )
            groesse = os.path.getsize(i)
            info_verzeichnis[i] = (datum_text, groesse)
    # Info-Verzeichnis zurückgeben
    return(info_verzeichnis)


def comparedirs(quell_liste, quell_info_verz, ziel_liste,
                ziel_info_verz):
    '''
    Vergleicht die Quell-Liste mit der Ziel-Liste und gibt die
    Unterschiede in einer Liste zurück.
    quell_liste = ['pfad/name',  ]
    quell_info_verz = {'pfad/name': ('datum', groesse),  }
    ziel_liste = ['pfad/name',  ]
    ziel_info_verz = {'pfad/name': ('datum', groesse),  }
    unterschiede = [('quellpfad/name', 'zielpfad/name'),  ]
    '''
    unterschiede = []
    # die Qelle mit dem Ziel vergleichen
    for i in quell_liste:
        quell_name = os.path.basename(i)
        ziel_namen_liste = []
        for j in ziel_liste:
            ziel_namen_liste.append(os.path.basename(j))
        if quell_name not in ziel_namen_liste:
            # Der Eintrag in der Quell Liste wurde nicht in der
            # Ziel-Liste gefunden: Zu Unterschiede hinzufügen
            unterschiede.append((i, "nicht vorhanden"))
        else:
            # Der Eintrag ist vorhanden
            quell_schluessel = i
            # Schlüssel in Ziel-Verzeichnis suchen
            for j in ziel_liste:
                ziel_name = os.path.basename(j)
                if quell_name == ziel_name:
                    # Ziel Schlüssel gefunden
                    ziel_schluessel = j
                    break
            if os.path.isfile(quell_schluessel):
                # Der Quell-Schlüssel repräsentiert eine Datei
                # Informationen von Quelle und Ziel lesen
                quell_datum = quell_info_verz[quell_schluessel][0]
                quell_groesse = quell_info_verz[quell_schluessel][1]
                ziel_datum = ziel_info_verz[ziel_schluessel][0]
                ziel_groesse = ziel_info_verz[ziel_schluessel][1]
                # Datum vergleichen
                if quell_datum != ziel_datum:
                    # Anderes Datum, der Liste hinzufügen
                    quell_text = "{0}: {1}".format(i, quell_datum)
                    ziel_text = "{0}: {1}".format(i, ziel_datum)
                    unterschiede.append((quell_text, ziel_text))
                # Grösse vergleichen
                if quell_groesse != ziel_groesse:
                    # Anderes Datum, der Liste hinzufügen
                    quell_text = "{0}: {1:,} bytes".format(
                        i,
                        quell_groesse
                    )
                    ziel_text = "{0}: {1:,} bytes".format(
                        i,
                        ziel_groesse
                    )
                    unterschiede.append((quell_text, ziel_text))
            # Aus der Ziel-Liste löschen.
            index = 0
            for j in ziel_liste:
                ziel_name = os.path.basename(j)
                if ziel_name == quell_name:
                    # Eintrag gefunden und löschen, Suche abbrechen
                    del ziel_liste[index]
                    break
                else:
                    # Zähler hochzählen
                    index += 1
    # Die restlichen Einträge in der Ziel-Liste waren nicht in der
    # Quell-Liste vorhanden, den Unterschieden auch hinzufügen
    for i in ziel_liste:
        unterschiede.append(("nicht vorhanden", i))
    # Die Unterschiede zurückgeben
    return(unterschiede)


def logunterschiede(unterschiede, titel):
    '''
    Erstellt anhand der Unterschied-Liste einen Text für die Ausgabe
    am Bildschirm oder in eine Text-Datei.
    unterschied = [('quellpfad/name', 'zielpfad/name'),  ]
    titel = "  "
    text = "  \n  "
    '''
    # Benötigte Spaltenbreite ermitteln
    liste = []
    for i in unterschiede:
        liste.append(i[0])
    breite = lenlist(liste)
    # Ausgabe erzeugen
    # Titel
    titel_linie = len(titel) * "-"
    text = "\n{0}\n{1}\n".format(titel, titel_linie)
    # Zell Platzhalter erzeugen
    leer = breite * " "
    # Quelle und Ziel
    for i in unterschiede:
        # Text formatieren, die erste Spalte hat eine fixe Breite
        # text = "|{0:<50}|{1:<50}|".format(i[0], i[1])
        quell_text = "{0}{1}".format(i[0], leer)
        quell_text = quell_text[:breite]
        # Zeile
        text = "{0}{1} -> {2}\n".format(text, quell_text, i[1])
    # Text zurückgeben
    return(text)


if __name__ == '__main__':
    # 2 Dateistrukturen vergleichen und auf Namen, Grösse und Datum
    # prüfen. Ergebnis in die Ziel-Struktur als eine formatierte
    # Text-Datei schreiben.
    # Log-Nummer setzen
    log_nr = 0
    # Quell Verzeichnis und Informatieonen lesen
    quell_verzeich, quell_dateien = dirs(QUELLE)
    quell_info_verz = datinfo(quell_dateien)
    # Log-Meldung
    log_nr = logger(log_nr, "Quell-Verzeichnis gelesen", quell_info_verz)
    # Ziel Verzeichnis und Informatieonen lesen
    ziel_verzeich, ziel_dateien = dirs(ZIEL)
    ziel_info_verz = datinfo(ziel_dateien)
    # Log-Meldung
    log_nr = logger(log_nr, "Ziel-Verzeichnis gelesen", ziel_info_verz)
    # Unterschiede ermitteln
    unterschiede = comparedirs(
        quell_dateien,
        quell_info_verz,
        ziel_dateien,
        ziel_info_verz
    )
    # Log-Meldung
    log_nr = logger(log_nr, "Unterschiede ermittelt", unterschiede)
    # Unterschiede in einer Tabelleanzeigen
    titel = "Vergleich von   <{0}>   und   <{1}>".format(QUELLE, ZIEL)
    log = logunterschiede(unterschiede, titel)
    logname = "Vergleich_{}.txt".format(timetext())
    pfad = os.path.join(ZIEL, logname)
    savetext(log, pfad)
