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
QUELLE = "2018_Remote_Test"
ZIEL = "2018_transfer_test"
# Ausnahmeliste mit Dateinamen, welche ignoriert werden
AUSNAHMEN = ["Thumbs.db", ".DS_Store"]
# Ausnahme mit Dateinamen Anfängen, welche ignoriert werden
AUSN_STARTa = "~$"
# Ausnahmen mit Dateinamen Enden, welche ignoriert werden
AUSN_ENDa = ".tmp"
# Vergleichsart: Detail, Resume
ART = "Resume"


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


def comparedirs(quell_stamm, quell_liste, quell_info_verz,
                ziel_stamm, ziel_liste, ziel_info_verz):
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
    # Liste mit Unterschieden
    unterschiede = []
    # Liste für ungeprüfte Dateien im Ziel
    ziel_nicht_gepr = ziel_liste.copy()
    # die Qelle mit dem Ziel vergleichen
    for i in quell_liste:
        quell_name = os.path.basename(i)
        # Ausnahmen prüfen
        if quell_name in AUSNAHMEN:
            # Ausnahme, nichts machen
            pass
        elif quell_name.startswith(AUSN_STARTa):
            # Ausnahme Anfang mit a, nichts machen
            pass
        elif quell_name.endswith(AUSN_ENDa):
            # Ausnahme Ende mit a, nichts machen
            pass
        else:
            # Keine Ausnahme
            quell_pfad = os.path.dirname(i)
            # Quell- und Ziel-Schlüssel
            quell_schluessel = i
            ziel_schluessel = ""
            # Quell-Pfad ohne Stammverzeichnis
            quell_pn = i.replace(quell_stamm, "")
            # Den gleichen Eintrag von der Quelle im Ziel suchen
            # nach Abzug des Stamm Verzeichnisses
            for j in ziel_liste:
                # Pfad ohne Stammverzeichnis des Ziels
                j_pn = j.replace(ziel_stamm, "")
                if quell_pn == j_pn:
                    # Nach Abzug des Stamm Verzeichnisses
                    # sind die Einträge Quelle und Ziel identisch
                    ziel_schluessel = j
            # Quell Informationen lesen
            if quell_schluessel in quell_info_verz.keys():
                # Der Quell-Schlüssel ist in den Informationen vorhanden
                # Informationen von Quelle und Ziel lesen
                quell_datum = quell_info_verz[quell_schluessel][0]
                quell_groesse = quell_info_verz[quell_schluessel][1]
            else:
                quell_datum = ""
                quell_groesse = 0
            # Ziel Informationen lesen
            if ziel_schluessel:
                # Bei Übereinstimmung
                ziel_name = os.path.basename(ziel_schluessel)
                ziel_pfad = os.path.dirname(ziel_schluessel)
                if ziel_schluessel in ziel_info_verz.keys():
                    # Die Datei ist in den Informationen vorhanden
                    # Informationen von Quelle und Ziel lesen
                    ziel_datum = ziel_info_verz[ziel_schluessel][0]
                    ziel_groesse = ziel_info_verz[ziel_schluessel][1]
                else:
                    ziel_datum = ""
                    ziel_groesse = 0
            else:
                ziel_name = "nicht vorhanden"
                ziel_pfad = "nicht vorhanden"
                ziel_datum = ""
                ziel_groesse = 0
            # Vergleich
            if quell_datum != ziel_datum:
                # Anderes Datum
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
            # Aus den ungeprüften Ziel-Dateien löschen.
            index = 0
            for j in ziel_nicht_gepr:
                if j == ziel_schluessel:
                    # Eintrag gefunden und löschen, Suche abbrechen
                    del ziel_nicht_gepr[index]
                    break
                else:
                    # Zähler hochzählen
                    index += 1
    # Die restlichen Einträge wurden nicht geprüft,
    # zu den Unterschieden auch hinzufügen
    for i in ziel_nicht_gepr:
        ziel_name = os.path.basename(i)
        ziel_pfad = os.path.dirname(i)
        # Ausnahmen prüfen
        if ziel_name in AUSNAHMEN:
            # Ausnahme, nichts machen
            pass
        elif ziel_name.startswith(AUSN_STARTa):
            # Ausnahme Anfang mit a, nichts machen
            pass
        elif ziel_name.endswith(AUSN_ENDa):
            # Ausnahme Ende mit a, nichts machen
            pass
        else:
            # Keine Ausnahme
            if i in ziel_info_verz.keys():
                # Die Datei ist in den Informationen vorhanden
                # Informationen von Quelle und Ziel lesen
                ziel_datum = ziel_info_verz[i][0]
                ziel_groesse = ziel_info_verz[i][1]
            else:
                ziel_datum = ""
                ziel_groesse = ""
            # Zu Unterschiede hinzufügen
            unterschiede.append((
                "nicht vorhanden",
                "nicht vorhanden",
                "",
                0,
                ziel_pfad,
                ziel_name,
                ziel_datum,
                ziel_groesse
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
            (
                "Quelle",
                quell_pfad,
                quell_name,
                quell_datum,
                quell_groesse
            ),
            (
                "Ziel",
                ziel_pfad,
                ziel_name,
                ziel_datum,
                ziel_groesse
            )
        ):
            # Werte auslesen
            titel, pfad, name, datum, groesse = i
            # Pfad einfügen
            text = "{0}: {1}".format(titel, pfad)
            unterschied_liste.append(text)
            if pfad != "nicht vorhanden":
                # Pfad ist vorhanden, mit Datei-Namen beginnen
                text = "\t{}".format(name)
                if name != "nicht vorhanden":
                    # Datei-Datum anhängen
                    if not datum:
                        # Kein Datum
                        text = "{} (--, ".format(text)
                    else:
                        # Datum vorhanden
                        text = "{0} ({1}, ".format(text, datum)
                    # Datei Grösse anhängen
                    if not groesse:
                        # Keine Grösse
                        text = "{}--)".format(text)
                    else:
                        # Mit Datei Grösse
                        text = "{0}{1:,} bytes)".format(text, groesse)
                # Datei-Infos anhängen
                unterschied_liste.append(text)
        # Leerzeile einfügen
        unterschied_liste.append("")
    return(unterschied_liste)


def getcomresume(unterschiede, quell_stamm, ziel_stamm):
    '''
    Erstellt eine Zusammenfassung der Unterschiede mit Hilfe der
    Liste der Unterschiede, des Quell- und Ziel-Stammes
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
    quell_stamm = ""
    ziel_stamm = ""
    nicht_verz = {"Quell-Verzeichnis": ["Dateien", ], }
    zuviel_verz = {"Ziel-Verzeichnis": ["Dateien", ], }
    info_verz = {"reduziertes Verzeichnis":
                  [("Datei", "Quell-Datum", "Ziel-Datum",
                    Quell-Grösse, Ziel-Grösse), ], }
    fehler_liste = [(quell-pfad, quell-name, ziel-pfad, ziel-name), ]
    '''
    # Verzeichnisse definieren
    nicht_verz = {}
    zuviel_verz = {}
    info_verz = {}
    fehler_liste = []
    # Unterschiede abarbeiten
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
        # Im Ziel-Verzeichnis nicht vorhanden
        if ziel_name == "nicht vorhanden":
            if quell_pfad in nicht_verz.keys():
                # Quell-Pfad bereits vorhanden
                nicht_verz[quell_pfad].append(quell_name)
            else:
                # Quell-Pfad nocht nicht vorhanden
                nicht_verz[quell_pfad] = [quell_name]
        # Im Quell-Verzeichnis nicht vorhanden
        if quell_name == "nicht vorhanden":
            if ziel_pfad in nicht_verz.keys():
                # Quell-Pfad bereits vorhanden
                zuviel_verz[ziel_pfad].append(ziel_name)
            else:
                # Quell-Pfad nocht nicht vorhanden
                zuviel_verz[ziel_pfad] = [ziel_name]
        # Unterschiedlichde Datei-Informationen
        if (quell_name != "nicht vorhanden" and
           ziel_name != "nicht vorhanden"):
            # Von den Quell- und Zielpfaden die Stammpfade wegnehmen
            red_ziel_pfad = ziel_pfad.replace(ziel_stamm, "")
            red_quell_pfad = quell_pfad.replace(quell_stamm, "")
            if (red_ziel_pfad == red_quell_pfad and
               ziel_name == quell_name):
                # Bei Übereinstimmung von Pfaden und Namen die Infos
                # aufnehmen
                if red_ziel_pfad in info_verz.keys():
                    # Reduzierter Ziel-Pfad bereits vorhanden
                    info_verz[red_ziel_pfad].append((
                        ziel_name,
                        quell_datum,
                        ziel_datum,
                        quell_groesse,
                        ziel_groesse
                    ))
                else:
                    # Quell-Pfad nocht nicht vorhanden
                    info_verz[red_ziel_pfad] = [(
                        ziel_name,
                        quell_datum,
                        ziel_datum,
                        quell_groesse,
                        ziel_groesse
                    )]
            else:
                # Keine Übereinstimmung von Pfaden oder Namen
                # In Fehler Liste aufnehmen
                fehler_liste.append(
                    quell_pfad,
                    quell_name,
                    ziel_pfad,
                    ziel_name
                )
    # Zusammenfassung in eine Text-Datei ausgeben
    text = "QUELLE: {0}\n".format(quell_stamm)
    text = "{0}ZIEL : {1}\n".format(text, ziel_stamm)
    # Nicht vorhandene Dateien ausgeben
    text = "{0}\nNICHT VORHANDENE DATEIEN IM ZIEL\n".format(text)
    for pfad, dateien in nicht_verz.items():
        # Überprüfen ob Unterschiede vorhanden sind
        if pfad != "" and dateien != []:
            # Pfad
            text = "{0}{1}\n".format(text, pfad)
            # Dateien
            for d in dateien:
                text = "{0}  -{1}\n".format(text, d)
    # Zuviel vorhandene Dateien ausgeben
    text = "{0}\nZUVIEL VORHANDENE DATEIEN IM ZIEL\n".format(text)
    for pfad, dateien in zuviel_verz.items():
        # Pfad
        text = "{0}{1}\n".format(text, pfad)
        # Dateien
        for d in dateien:
            text = "{0}  -{1}\n".format(text, d)
    # Unterschiedliche Datei-Informationen
    text = "{0}\nUNTERSCHIEDLICHE INFORMATIONEN\n".format(text)
    for pfad, dateien in info_verz.items():
        # Pfad
        text = "{0}..{1}\n".format(text, pfad)
        text = "{0}   name / quell-datum / ziel-datum / ".format(text)
        text = "{0}quell-grösse / ziel-grösse\n".format(text)
        # Dateien & Informationen
        for d in dateien:
            text = "{0}  -{1} / {2} / {3} / ".format(
                text,
                d[0],
                d[1],
                d[2]
            )
            text = "{0}{1}bytes / {2}bytes\n".format(text, d[3], d[4])
    # Fehlerhafte Informationen
    text = "{0}\nFEHLER BEIM VERGLEICH\n".format(text)
    for f in fehler_liste:
        text = "{0}  -{1}: {2}  /  {3}: {4}".format(
                text,
                f[0],
                f[1],
                f[2],
                f[3]
            )
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
        QUELLE,
        quell_dateien,
        quell_info_verz,
        ZIEL,
        ziel_dateien,
        ziel_info_verz
    )
    # Log-Meldung
    log_nr = logger(log_nr, "Unterschiede ermittelt", unterschiede)
    if ART == "Detail":
        # Detaillierte Unterschiede als Text-Datei speichern
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
        logname = "Vergleich_{0}.txt".format(timetext())
        pfad = os.path.join(ZIEL, logname)
        savetext(log, pfad)
    elif ART == "Resume":
        # Zusammenfassung der Unerschiede als Text-Datei speichern
        text = getcomresume(
            unterschiede,
            QUELLE,
            ZIEL
        )
        logname = "Resume_{0}.txt".format(timetext())
        pfad = os.path.join(ZIEL, logname)
        savetext(text, pfad)
