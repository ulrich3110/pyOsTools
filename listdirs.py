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


def logverzeichnis(datei_verzeichnis, titel):
    '''
    Erstellt anhand des Datei-Verzeichnisses einen Text für die
    Ausgabe am Bildschirm oder in eine Text-Datei.
    datei_verzeichnis = {'pfad': ['name',  ],  }
    titel = "  "
    text = "  \n  "
    '''
    # Titel
    titel_linie = len(titel) * "-"
    text = "\n{0}\n{1}\n".format(titel, titel_linie)
    # Breite Verzeichnis Spalte ermitteln
    verz_liste = list(datei_verzeichnis.keys())
    verz_breite = lenlist(verz_liste)
    # Breite Namen und Datum Spalte ermitteln
    namen_liste = []
    datum_liste = []
    for dateien_pro_verz in datei_verzeichnis.values():
        for namen, datum, groesse in dateien_pro_verz:
            namen_liste.append(namen)
            datum_liste.append(datum)
    namen_breite = lenlist(namen_liste)
    datum_breite = lenlist(datum_liste)
    # Platzhalter für Spalten erzeugen
    verz_leer = verz_breite * " "
    namen_leer = namen_breite * " "
    datum_leer = datum_breite * " "
    # Verzeichnisse & Dateien
    for verzeichnis, dateien in datei_verzeichnis.items():
        # Verzeichnis-Spalte mit fixer Breite
        verz_text = "{0}{1}".format(verzeichnis, verz_leer)
        verz_text = verz_text[:verz_breite]
        # Dateien aufnehmen, die erse Datei steht in der gleichen Zeile
        # wie das Verzeichnis, die folgenden Dateien weden ohne
        # Verzeichnis aufgelistet.
        dateien.sort()
        # Prüfen ob das Verzeichnis leer ist:
        if not dateien:
            # Verzeichnis ist leer, nur den Verzeichnis Namen eintragem
            text = "{0}{1}\n\n".format(text, verz_text)
        else:
            # Verezichnis ist nich leer, alle Dateien abarbeiten
            for namen, datum, groesse in dateien:
                # Namenspalte mit fixer Breite
                namen_text = "{0}{1}".format(namen, namen_leer)
                namen_text = namen_text[:namen_breite]
                # Datumspalte mit fixer Breite
                datum_text = "{0}{1}".format(datum, datum_leer)
                datum_text = datum_text[:datum_breite]
                # Grösse mit Tausender Trennung und Rechtsbündig
                # 000'000'000'000 = 15 Zeichen
                groesse_text = "{0}{1:,}".format(15 * " ", groesse)
                groesse_text = groesse_text[-15:]
                # Zusammenfügen zum Text
                text = "{0}{1}   {2}   {3} {4} bytes\n".format(
                    text,
                    verz_text,
                    namen_text,
                    datum_text,
                    groesse_text
                )
                # Damit das Verzeichnis nur beim Ersten Eintrag angezeigt
                # wird, wird nach dem 1. Durchlauf (= 1. Eintrag) der
                # Verzeichnis Text mit dem Platzhalter der Verzeichnis
                # Spalte überschrieben.
                verz_text = verz_leer
            # Leerzeile am Ende des Verzeichnisses
            text = "{}\n".format(text)
    # Text zurückgeben
    return(text)


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
    # Inhalt pro Verzeichnis anzeigen
    titel = "Inhalt von   <{0}>".format(os.path.abspath(QUELLE))
    log = logverzeichnis(datei_verzeichnis, titel)
    logname = "Inhalt_{}.txt".format(timetext())
    pfad = os.path.join(QUELLE, logname)
    savetext(log, pfad)
