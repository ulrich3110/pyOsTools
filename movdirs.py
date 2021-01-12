#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os

'''
movdirs.py - Dateien aus einer Struktur in ein Verzeichnis verschieben
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
QUELLE = "."
ZIEL = "./Test"
NAME = "_"
ERWEITERUNG = "*"


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


def movefiles(datei_liste, namen, erweiterung,
              ziel_verzeichnis):
    '''
    Dateien anhand der Datei-Liste im Datei-Namen und in der Datei-
    Erweierung suchen und in das Ziel-Verzeichnis verschieben.
    Ein leerer Name/Erweiterung oder ein * bedeutet alles
    datei_liste = ['pfad/name',  ]
    name = '  '
    erweiterung = '  '
    ziel_verzeichnis = 'pfad'
    '''
    gefunden_liste = []
    # Dateien suchen und in der Gefunden-Liste speichern
    for i in datei_liste:
        gefunden = ['', '']
        # Dateinamen mit Erweiterung aufsplitten in eine Liste,
        # [0] = Namen, [1] = Erweiterung
        if os.path.isfile(i):
            # Operationen nur durchführen, falls es eine Datei sit.
            n = os.path.basename(i)
            name_erw = n.split('.')
            # Zuerst Im Namen suchen
            if namen and namen != '*':
                # Zeichenfolge im Namen suchen
                if name_erw[0].find(namen) != -1:
                    # Gefunden
                    gefunden[0] = name_erw[0]
            else:
                # Alle Namen
                gefunden[0] = name_erw[0]
            # Wenn im Namen gefunden, dann in der Erweiterung suchen
            if gefunden[0]:
                if erweiterung and erweiterung != '*':
                    # Zeichenfolge in Erweiterung suchen
                    if name_erw[1].find(erweiterung) != -1:
                        # Gefunden
                        gefunden[1] = name_erw[1]
                else:
                    # Alle Erweiterungen
                    gefunden[1] = name_erw[1]
            # Wenn im Namen und Erweiterung gefunden, zur Gefunden-Liste
            # hinzufügen
            if gefunden[0] and gefunden[1]:
                gefunden_liste.append(i)
    # Falls Dateien gefunden wurden, diese verschieben
    if gefunden_liste:
        # Prüfen ob das Ziel-Verzeihnis existiert
        if not os.path.isdir(ziel_verzeichnis):
            # Ziel Verzeichnis erstellen
            os.mkdir(ziel_verzeichnis)
        for i in gefunden_liste:
            # Pfade bilden, für Quelle und Ziel
            n = os.path.basename(i)
            quell_pfad = i
            ziel_pfad = os.path.join(ziel_verzeichnis, n)
            # Prüfen, ob die Datei im Ziel existiert.
            # Falls ja, den Dateinamen um ein '_' erweitern
            while os.path.isfile(ziel_pfad):
                # Dateinamen.Erweiterung auslesen
                n = os.path.basename(ziel_pfad)
                n_e = n.split('.')
                # Erweitern und Dateinamen.Erweiterung bilden
                if len(n_e) == 1:
                    # Datei ohne Erweiterung
                    n = "{0}_".format(n_e[0])
                else:
                    # Datei mit Erweiterung
                    n = "{0}_.{1}".format(n_e[0], n_e[1])
                # Ziel-Pfad mit neuem Namen bilden
                ziel_pfad = os.path.join(ziel_verzeichnis, n)
            # Datei verschieben
            os.rename(quell_pfad, ziel_pfad)


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
        verzeichnis = os.path.dirname(i)
        dateiname = os.path.basename(i)
        datum = info_verzeichnis[i][0]
        groesse = info_verzeichnis[i][1]
        datei_verzeichnis[verzeichnis].append(
            (dateiname, datum, groesse)
        )
    return(datei_verzeichnis)


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
        datum = os.path.getmtime(i)
        datum_text = time.strftime(
            '%d.%m.%Y %H:%M:%S',
            time.localtime(datum)
        )
        groesse = os.path.getsize(i)
        info_verzeichnis[i] = (datum_text, groesse)
    # Info-Verzeichnis zurückgeben
    return(info_verzeichnis)


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
    # Dateien nach Spezifikationen suchen und in ein Verzeichnis
    # verschieben
    # Log-Nummer setzen
    log_nr = 0
    # Verzeichnisse lesen
    verzeichnis_liste, datei_liste = dirs(QUELLE)
    # Log-Meldung
    log_nr = logger(
        log_nr,
        "Quell-Verzeichnis gelesen",
        verzeichnis_liste
    )
    # Namen, Erweiterung und Ziel festlegen
    # Verschieben
    movefiles(datei_liste, NAME, ERWEITERUNG, ZIEL)
    # Log-Meldung
    log_nr = logger(log_nr, "Daeien verschoben", "")
    # Im Ziel den Inhalt anzeigen
    dir2_liste, dat2_liste = dirs(ZIEL)
    inf2_verzeichnis = datinfo(dat2_liste)
    # Log-Meldung
    log_nr = logger(
        log_nr,
        "Ziel-Verzeichnis gelesen",
        inf2_verzeichnis
    )
    # Daten ordnen nach Verzeichnissen
    dat2_verzeichnis = sortdirs(
        ZIEL,
        dir2_liste,
        dat2_liste,
        inf2_verzeichnis
    )
    # Log-Meldung
    log_nr = logger(log_nr, "Zeiel-Daten geordnet", dat2_verzeichnis)
    # Inhalt anzeigen
    titel = "Inhalt von   <{0}>".format(os.path.abspath(ZIEL))
    log = logverzeichnis(dat2_verzeichnis, titel)
    logname = "Inhalt_{}.txt".format(timetext())
    pfad = os.path.join(ZIEL, logname)
    savetext(log, pfad)
