#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os

'''
listdirs.py - Alle Dateien und Verzeichnisse vom aktuellen Verzeichnis
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


QUELLE = "."


def savetext(text, pfad):
    '''
    Speichert den Text beim Pfad ab.
    text = "  "
    pfad = '/pfad'
    '''
    try:
        datei_objekt = open(
            pfad,
            'w',
            encoding='utf-8',
            errors='ignore'
        )
        datei_objekt.write(text)
        datei_objekt.close()
    except Exception as err:
        # Fehlermeldung erzeugen und als Error Text Datei speichern
        t = "Es gab einen Fehler in Funktion savetext.\n"
        t = "{0}Pfad = {1}\nError = {2}\n".format(t, pfad, str(err))
        err_pfad = "{}___error.txt".format(pfad)
        err_objekt = open(err_pfad, 'w')
        err_objekt.write(t)
        err_objekt.close()


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
    wert_text = str(wert)
    if len(wert_text) > 40:
        wert_text = "{}..".format(wert_text[:39])
    print("# {0:X} - {1} - {2} #".format(
        nummer,
        text,
        str(wert_text)))
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


def sortdirs(quell_pfad, verzeichnis_liste, datei_liste,
             info_verzeichnis):
    '''
    Die Datei-Liste anhand der Verzeichnisse sortieren und das
    Datei-Verzeichnis zurückgeben.
    quell_pfad = 'pfad'
    verzeichnis_liste = ['pfad',  ]
    datei_liste = ['pfad/name',  ]
    info_verzeichnis = {'pfad/name': ('datum', groesse),  }
    datei_verzeichnis = {'pfad': [('name', 'datum', groesse)  ],  }
    '''
    # Datei-Verzeichnis anhand der Verzeichnis-Liste vorbereiten
    datei_verzeichnis = {quell_pfad: []}
    for i in verzeichnis_liste:
        datei_verzeichnis[i] = []
    # Datei-Verzeichnis anhand der Datei-Liste abfüllen
    for i in datei_liste:
        if os.path.isfile(i):
            # Das Element is eine Datei
            verzeichnis = os.path.dirname(i)
            dateiname = os.path.basename(i)
            datum = info_verzeichnis[i][0]
            groesse = info_verzeichnis[i][1]
            datei_verzeichnis[verzeichnis].append(
                (dateiname, datum, groesse)
            )
    return(datei_verzeichnis)


def gettree(datei_verzeichnis):
    '''
    Erstellt eine Hierarchische Verzeichnis-Liste der Verzeichnisse
    mit Hilfe des Datei-Verzeichnisses
    datei_verzeichnis = {'pfad': [('name', 'datum', groesse)  ],  }
    verz_liste = ['pfad',  ]
    '''
    verz_liste = []
    for verzeichnis, dateien in datei_verzeichnis.items():
        verz_liste.append(verzeichnis)
    verz_liste.sort()
    return(verz_liste)


def getfiletree(datei_verzeichnis, verz_liste):
    '''
    Erstellt eine Hierarchische Text-Liste der Verzeichnisse und Dateien
    mit Hilfe de Datei-Verzeichnisses und einer Liste der Verzeichnisse
    datei_verzeichnis = {'pfad': [('name', 'datum', groesse)  ],  }
    verz_liste = ['pfad',  ]
    verz_datei_list = ["Pfad", "Dateiname (Datum, Grösse)", "", ]
    '''
    verz_datei_liste = []
    for verzeichnis in verz_liste:
        # Verzeichnis als Titel
        text = "{}".format(verzeichnis)
        verz_datei_liste.append(text)
        if not datei_verzeichnis[verzeichnis]:
            # Keine Dateien
            verz_datei_liste.append("   (keine Dateien)")
        else:
            for datei in datei_verzeichnis[verzeichnis]:
                # Dateien auflisten mit Name (Datum, Grösse)
                name = datei[0]
                datum = datei[1]
                grösse = datei[2]
                text = "\t{0} ({1}, {2:,} bytes)".format(
                    name,
                    datum,
                    grösse
                )
                verz_datei_liste.append(text)
        verz_datei_liste.append("")
    return(verz_datei_liste)


if __name__ == '__main__':
    # Verzeichnis Inhalt auflisten und formatiert in eine Text-Datei
    # schreiben.
    # Log-Nummer setzen
    log_nr = 0
    # Verzeichnisse lesen
    verzeichnis_liste, datei_liste = dirs(QUELLE)
    # Log-Meldung
    log_nr = logger(log_nr, "Verzeichnis gelesen", verzeichnis_liste)
    # Informationen lesen
    info_verzeichnis = datinfo(datei_liste)
    # Log-Meldung
    log_nr = logger(log_nr, "Informationen gelesen", info_verzeichnis)
    # Daten ordnen nach Verzeichnissen
    datei_verzeichnis = sortdirs(
        QUELLE,
        verzeichnis_liste,
        datei_liste,
        info_verzeichnis
    )
    # Log-Meldung
    log_nr = logger(log_nr, "Daten geordnet", datei_verzeichnis)
    # Inhalt in einer hierarchischen Struktur erzeugen
    verz_liste = gettree(datei_verzeichnis)
    verz_datei_liste = getfiletree(datei_verzeichnis, verz_liste)
    # Überschriften
    titel = "Struktur von  <{0}>".format(os.path.abspath(QUELLE))
    linie = "-" * len(titel)
    # Texte zusammenführen
    log = "{0}\n{1}".format(titel, linie)
    strukt_text = "\n".join(verz_datei_liste)
    log = "{0}\n{1}".format(log, strukt_text)
    # In Logdatei speichern
    logname = "Inhalt_{}.txt".format(timetext())
    pfad = os.path.join(QUELLE, logname)
    savetext(log, pfad)
