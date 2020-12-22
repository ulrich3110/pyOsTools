#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import os
import json

'''
compremo.py - Verzeichnis-Strukturen anhand von JSON vergleichen
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


# Verzeichnis der ersten und zweiten JSON Struktur (Quelle und Ziel)
QUELLE = "./quellen"
ZIEL = "./ziele"
# Verzeichnis in dem die Vergleiche abgelegt werden
VERGLEICH = "./vergleiche"
# Ausnahmeliste mit Dateinamen, welche ignoriert werden
AUSNAHMEN = ["Thumbs.db", ".DS_Store"]
# Ausnahme mit Dateinamen Anfang a, welche ebenfalls ignoriert wird
AUSN_STARTa = "~$"


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


def remocomparedirs(quell_stamm, quell_liste, quell_info_verz,
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
            # Ausnahme mit a, nichts machen
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
            # Ausnahme mit a, nichts machen
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


def comparejson(quell_liste, ziel_liste):
    '''
    Eine Quell-Liste von Json Dateien mit einer Ziel-liste vergleichen
    und die Unterschiede als Verzeichnis zurückgeben:
    gleich = ['.json',  ]
    unterschiede = {'quelle': ['.json',  ], 'ziel': ['.json',  ]}
    '''
    gleich = []
    unterschiede = {'quelle': [], 'ziel': []}
    identisch = []
    for i in quell_liste:
        if i not in ziel_liste:
            # Die Json Datei von der Quelle ist im Ziel nicht vorhanden
            unterschiede['ziel'].append(i)
        else:
            if i not in gleich:
                # Die Json Datei von der Quelle ist im Ziel vorhanden
                # aber noch nicht om der Gleich-Liste
                gleich.append(i)
    for i in ziel_liste:
        if i not in quell_liste:
            # Die json Datei vom Ziel ist in der Quelle nicht vorhanden
            unterschiede['quelle'].append(i)
        else:
            if i not in gleich:
                # Die Json Datei vom Ziel ist in der Quelle vorhanden
                # aber noch nicht om der Gleich-Liste
                gleich.append(i)
    # Gleich & Unterschiede zurückgeben
    return(gleich, unterschiede)


def logjsonuntersch(gleich, unterschiede):
    '''
    Erstellt anhand den Listen einen Text für die Ausgabe
    am Bildschirm oder in eine Text-Datei.
    gleich = ['.json',  ]
    unterschiede = {'quelle': ['.json',  ], 'ziel': ['.json']}
    titel = "  "
    text = "  \n  "
    '''
    # Ausgabe erzeugen
    # Vergiglechene Json anzeigen
    text = "Überprüfte Json\n"
    text = "{0}---------------\n".format(text)
    for i in gleich:
        text = "{0}{1}\n".format(text, i)
    # Quell Unerschiede anzeigen
    text = "{0}\n".format(text)
    text = "{0}Nicht überprüfte Json der Quellen\n".format(text)
    text = "{0}---------------------------------\n".format(text)
    for i in unterschiede['quelle']:
        text = "{0}{1}\n".format(text, i)
    # Ziel Unterschiede anzteigen
    text = "{0}\n".format(text)
    text = "\n{0}Nicht überprüfte Json im Ziel\n".format(text)
    text = "{0}-------------------------------\n".format(text)
    for i in unterschiede['ziel']:
        text = "{0}{1}\n".format(text, i)
    return(text)


if __name__ == '__main__':
    # JSON Dateistrukturen vergleichen und auf Namen, Grösse und Datum
    # prüfen. Ergebnis in die Ziel-Struktur als eine formatierte
    # Text-Datei schreiben.
    # Wenn im Quell- und im Zeilverzeichnis JSON mit identisehem
    # Namen vorhanden sind, werden diese miteinander verglichen und
    # das Ergebnis in das Vergleich Verzeichnis geschrieben.
    # Die in der Quelle und im Ziel unterschiedlich vorhandenen JSON
    # wrden ebenalls im Vergleich Verzeichnis aufgeführt.
    # Log-Nummer setzen
    log_nr = 0
    # Quellverzeichnis json lesen
    quell_json = []
    quell_liste = os.listdir(QUELLE)
    for i in quell_liste:
        quell_pfad = os.path.join(QUELLE, i)
        if os.path.isfile(quell_pfad) and i.endswith(".json"):
            # Json Datei
            quell_json.append(i)
            # Log-Meldung
            log_nr = logger(
                log_nr,
                "Quell Json",
                i
            )
    # Zielverzeichnis json lesen
    ziel_json = []
    ziel_liste = os.listdir(ZIEL)
    for i in ziel_liste:
        ziel_pfad = os.path.join(ZIEL, i)
        if os.path.isfile(ziel_pfad) and i.endswith(".json"):
            # Json Datei
            ziel_json.append(i)
            # Log-Meldung
            log_nr = logger(
                log_nr,
                "Ziel Json",
                i
            )
    # Json Dateien in Quelle und Ziel vergleichen
    json_gleich, json_unterschiede = comparejson(quell_json, ziel_json)
    # Log-Meldung
    log_nr = logger(log_nr, "Gleiche Json", json_gleich)
    log_nr = logger(log_nr, "Unterschiedliche Json", json_unterschiede)
    # Gleiche Json Verzeichnisse miteinander vergleichen
    for i in json_gleich:
        # Json Quelle lesen
        quell_pfad = os.path.join(QUELLE, i)
        with open(quell_pfad) as f:
            quell_json_verz = json.load(f)
        # Log-Meldung
        log_nr = logger(log_nr, "Quell-Json gelesen", quell_json_verz)
        # Json Ziel lesen
        ziel_pfad = os.path.join(ZIEL, i)
        with open(ziel_pfad) as f:
            ziel_json_verz = json.load(f)
        # Log-Meldung
        log_nr = logger(log_nr, "Ziel-Json gelesen", ziel_json_verz)
        # Unterschiede ermitteln
        # {'Datei-Liste': [  ], 'Info-Verz': {  }}
        unterschiede = remocomparedirs(
            quell_json_verz['Stamm'],
            quell_json_verz['Datei-Liste'],
            quell_json_verz['Info-Verz'],
            ziel_json_verz['Stamm'],
            ziel_json_verz['Datei-Liste'],
            ziel_json_verz['Info-Verz']
        )
        # Log-Meldung
        log_nr = logger(log_nr, "Unterschiede ermittelt", unterschiede)
        # Unterschiede als Text-Datei speichern im Ziel
        titel = "Unerschiede von\n<{0}>  und\n<{1}>\n\n".format(
            os.path.abspath(quell_pfad),
            os.path.abspath(ziel_pfad)
        )
        if not unterschiede:
            strukt_text = "Keine"
        else:
            unerschied_list = getcomparetree(unterschiede)
            strukt_text = "\n".join(unerschied_list)
        log = "{0}{1}".format(titel, strukt_text)
        logname = "Vergleich_{0}_{1}.txt".format(i, timetext())
        pfad = os.path.join(VERGLEICH, logname)
        savetext(log, pfad)
    # Unterschiede in Json in einer Liste anzeigen
    json_log = logjsonuntersch(json_gleich, json_unterschiede)
    json_titel = "Unerschiede von   <{0}>   und   <{1}>".format(
        os.path.abspath(QUELLE),
        os.path.abspath(ZIEL)
    )
    json_logname = "Vergleich_Quelle_Ziel_{}.txt".format(timetext())
    json_pfad = os.path.join(VERGLEICH, json_logname)
    savetext(json_log, json_pfad)
