#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os
import json

'''
remodirs.py - Verzeichnis-Strukturen als Json abspeichern
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


# Stammpfad von dem alle Quell Verzeichnisse eingelesen werden
QUELLSTAMM = "/home/andreas/Dropbox/1_Ich/2_Projekte/2020_pyOsTools/2018_Remote_Test/"
# Zielverzeichnis wo die JSON pro Verzeichnis gespeichert werden
JSONPATH = "./ziele"


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


if __name__ == '__main__':
    # Dateistrukturen anahnd einer Liste einlesen und die Datei-
    # Liste sowie das Info-Verzeichnis als JSON abspeichern.
    # Log-Nummer setzen
    log_nr = 0
    # Alle Verzeichnisse im Quellstamm lesen
    dir_liste = os.listdir(QUELLSTAMM)
    quell_liste = []
    for i in dir_liste:
        # Den Pfad aus Quellstamm und Eintrag zusammensetzen
        i_path = os.path.join(QUELLSTAMM, i)
        if os.path.isdir(i_path):
            # Der Eintrag ist ein Verzeichnis
            quell_liste.append(i)
            # Log-Meldung
            log_nr = logger(
                log_nr,
                "Verzeichnis im Quell-Stamm",
                i
            )
    # Die Verzeichnisse  abarbeiten
    for i in quell_liste:
        # Der Quell-Pfad setzt sich aus dem Quell-Stamm und dem
        # Quell-Namen zusammen
        quell_pfad = os.path.join(QUELLSTAMM, i)
        # Quell Verzeichnis und Informationen lesen
        quell_verzeich, quell_dateien = dirs(quell_pfad)
        quell_info_verz = datinfo(quell_dateien)
        # Log-Meldung
        log_nr = logger(
            log_nr,
            "Quell-Verzeichnis gelesen",
            quell_info_verz
        )
        # Verzeichnis für den JSON Export erzeugen
        # {'Datei-Liste': [  ], 'Info-Verz': {  }}
        json_verz = {
            'Stamm': quell_pfad,
            'Datei-Liste': quell_dateien,
            'Info-Verz': quell_info_verz
        }
        # Schreibe Informationen als JSON Datei
        name = "{}.json".format(i)
        datei_pfad = os.path.join(JSONPATH, name)
        with open(datei_pfad, 'w') as json_file:
            json.dump(json_verz, json_file)
        # Log-Meldung
        log_nr = logger(
            log_nr,
            "JSON geschrieben",
            datei_pfad
        )
