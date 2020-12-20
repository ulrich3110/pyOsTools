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


# Definition der ersten und der zweiten Struktur (Quelle und Ziel)
QUELLE = "."
ZIEL = "./tst"


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


def comparedirs(quell_liste, quell_info_verz, ziel_liste,
                ziel_info_verz):
    '''
    Vergleicht die Quell-Liste mit der Ziel-Liste und gibt die
    Unterschiede in einer Liste zurück.
    quell_liste = ['pfad/name',  ]
    quell_info_verz = {'pfad/name': ('datum', groesse),  }
    ziel_liste = ['pfad/name',  ]
    ziel_info_verz = {'pfad/name': ('datum', groesse),  }
    unterschiede = [
        (
            'quellpfad',
            'quellname',
            'quelldatum',
            quellgrösse,
            'zielpfad'
            'zielname',
            'zieldatum',
            zielgrösse
        ),
    ]
    '''
    unterschiede = []
    # die Qelle mit dem Ziel vergleichen
    for i in quell_liste:
        quell_name = os.path.basename(i)
        quell_pfad = os.path.dirname(i)
        ziel_namen_liste = []
        for j in ziel_liste:
            ziel_namen_liste.append(os.path.basename(j))
        if quell_name not in ziel_namen_liste:
            # Der Eintrag in der Quell Liste wurde nicht in der
            # Ziel-Liste gefunden: Zu Unterschiede hinzufügen
            if os.path.isfile(i):
                # Der Quell-Schlüssel repräsentiert eine Datei
                # Informationen von Quelle und Ziel lesen
                quell_datum = quell_info_verz[i][0]
                quell_groesse = quell_info_verz[i][1]
            else:
                quell_datum = ""
                quell_groesse = ""
            unterschiede.append((
                quell_pfad,
                quell_name,
                quell_datum,
                quell_groesse,
                "nicht vorhanden",
                "nicht vorhanden",
                "",
                0
            ))
        else:
            # Der Eintrag ist vorhanden
            quell_schluessel = i
            # Schlüssel in Ziel-Verzeichnis suchen
            for j in ziel_liste:
                ziel_name = os.path.basename(j)
                if quell_name == ziel_name:
                    # Ziel Schlüssel gefunden
                    ziel_schluessel = j
                    ziel_pfad = os.path.dirname(j)
                    break
            if os.path.isfile(quell_schluessel):
                # Der Quell-Schlüssel repräsentiert eine Datei
                # Informationen von Quelle und Ziel lesen
                quell_datum = quell_info_verz[quell_schluessel][0]
                quell_groesse = quell_info_verz[quell_schluessel][1]
                ziel_datum = ziel_info_verz[ziel_schluessel][0]
                ziel_groesse = ziel_info_verz[ziel_schluessel][1]
                # Datum & Grösse vergleichen
                if (quell_datum != ziel_datum or
                    quell_groesse != ziel_groesse):
                    # Anderes Datum oder anderer Grösse
                    unterschiede.append((
                        quell_pfad,
                        quell_name,
                        quell_datum,
                        quell_groesse,
                        ziel_pfad,
                        ziel_name,
                        ziel_datum,
                        ziel_groesse
                    ))
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
        if os.path.isfile(i):
            # Der Quell-Schlüssel repräsentiert eine Datei
            # Informationen von Quelle und Ziel lesen
            ziel_datum = quell_info_verz[i][0]
            ziel_groesse = quell_info_verz[i][1]
        else:
            ziel_datum = ""
            ziel_groesse = ""
        unterschiede.append((
            "nicht vorhanden",
            "nicht vorhanden",
            "",
            0,
            ziel_pfad,
            os.path.basename(i),
            ziel_datum[i][0],
            ziel_groesse[i][1]
        ))
    # Die Unterschiede zurückgeben
    return(unterschiede)


def getcomparetree(unterschiede):
    '''
    Erstellt eine Hierarchische Liste der Unterschiede mit Hilfe der
    Liste der Unterschiede
    unterschiede = [
        (
            'quellpfad',
            'quellname',
            'quelldatum',
            quellgrösse,
            'zielpfad'
            'zielname',
            'zieldatum',
            zielgrösse
        ),
    ]
    unerschied_list = [
        "Quell-Pfad",
        "Quell-Dateiname (Datum, Grösse)",
        "Ziel-Pfad",
        "Ziel-Dateiname (Datum, Grösse)",
        "",
    ]
    '''
    unterschied_liste = []
    # Einträge an Liste anfügen
    for u in unterschiede:
        # Werte auslesen
        quell_pfad = u[0]
        quell_name = u[1]
        quell_datum = u[2]
        quell_groesse = u[3]
        ziel_pfad = u[4]
        ziel_name = u[5]
        ziel_datum = u[6]
        ziel_groesse = u[7]
        # Einträge für Quelle und Ziel an Liste anfügen
        for i in (
            (quell_pfad, quell_name, quell_datum, quell_groesse),
            (ziel_pfad, ziel_name, ziel_datum, ziel_groesse)
        ):
            # Pfad einfügen
            text = "{}".format(i[0])
            unterschied_liste.append(text)
            if i[0] != "nicht vorhanden":
                # Pfad ist vorhanden, mit Datei-Namen beginnen
                text = "\t{}".format(i[1])
                if i[1] != "nicht vorhanden":
                    # Datei-Datum anhängen
                    if not i[2]:
                        # Kein Datum
                        text = "{} (--, ".format(text)
                    else:
                        # Datum vorhanden
                        text = "{0} ({1}, ".format(text, i[2])
                    # Datei Grösse anhängen
                    if not i[3]:
                        # Keine Grösse
                        text = "{}--)".format(text)
                    else:
                        # Mit Datei Grösse
                        text = "{0}{1:,} bytes)".format(text, i[3])
                # Datei-Infos anhängen
                unterschied_liste.append(text)
        # Leerzeile einfügen
        unterschied_liste.append("")
    return(unterschied_liste)


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
    # Unterschiede als Text-Datei speichern
    titel = "Unerschiede von\n<{0}>  und\n<{1}>\n\n".format(
        os.path.abspath(QUELLE),
        os.path.abspath(ZIEL)
    )
    if not unterschiede:
        strukt_text = "Keine"
    else:
        unerschied_list = getcomparetree(unterschiede)
        strukt_text = "\n".join(unerschied_list)
    log = "{0}{1}".format(titel, strukt_text)
    logname = "Vergleich_{}.txt".format(timetext())
    pfad = os.path.join(ZIEL, logname)
    savetext(log, pfad)
