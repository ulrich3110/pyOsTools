#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

'''
pyren.py - Dateien des aktuellen Verzeichnisses umbenennen
Copyright (c) Feb. 2021: Andreas Ulrich
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

'''
Erklärung zu Kommandos und Werte im Rename Tupel
------------------------------------------------

"SCHLÜSSEL": Werte
Ersetzen am Anfang: "alt", "neu"
"START": ("Mu", "Te") = "Muster" >> "Tester"

Ersetzen am Ende: "alt", "neu"
"ENDE": ("ter", "e") = "Muster" >> "Muse"

Ersetzen: "alt", "neu"
"ERSATZ": (" ", "_") = "Mu ster" >> "Mu_ster"

Löschen: Position, Anzahl Zeichen
"LÖSCHEN": (2, 3) = "Muster" >> "Mer"

Einfügen: Position, Text
"EINFÜGEN": (3, "en") = "Muster" >> "Muenster"

An Anfang schieben: Position, Anzahl Zeichen
"ANFANG": (3, 2) = "Muster" >> "stMuer"

Ans Ende schieben: Position, Anzahl Zeichen
"SCHLUSS": (3, 2) = "Muster" >> "Muerst"

Am Anfang einfügen: Text
"EINFÜGENSTART": ("ein ") = "Muster" >> "ein Muster"

Am Ende einfügen: Text
"EINFÜGENENDE": ("schüler") = "Muster" >> "Musterschüler"

Nummerieren mit Zahlen: Startwert, Anzahl Stellen, "Trennzeichen"
"ZAHL": (3, 2, "_") = "Muster" >> "01_Muster a", "02_Muster b" ..

Nummerieren mit Buchstaben: Startbuchstabe, "Trennzeichen"
"BUCHSTABEN": ("c", "_") = "Muster" >> "c_Muster"

Alles klein Schreiben:
"KLEIN": 1 = "Muster" >> "muster"

Alles gross Schreiben:
"GROSS": 1 = "Muster" >> "MUSTER"

Gross wie Titel Schreiben:
"TITEL": 1 = "dieses muster" >> "Dieses Muster"

Gross wie Satzanfang schreiben:
"SATZ": 1 = "dieses muster" >> "Dieses muster"

Gross / Klein vertauschen:
"TAUSCHEN": 1 = "Muster" >> "mUSTER"

Beispiel zum kopieren:
TP_REN = ("START", "alt", "neu")
TP_REN = ("ENDE", "alt", "neu")
TP_REN = ("ERSATZ", "alt", "neu")
TP_REN = ("LÖSCHEN", 2, 3)
TP_REN = ("EINFÜGEN", 3, "en")
TP_REN = ("ANFANG", 3, 2)
TP_REN = ("SCHLUSS", 3, 2)
TP_REN = ("EINFÜGENSTART", "ein ", None)
TP_REN = ("EINFÜGENENDE", "schüler", None)
TP_REN = ("ZAHL", 3, 2, "_")
TP_REN = ("BUCHSTABEN", "c", "_")
TP_REN = ("KLEIN", 1)
TP_REN = ("GROSS", 1)
TP_REN = ("TITEL", 1)
TP_REN = ("SATZ", 1)
TP_REN = ("TAUSCHEN", 1)
'''

TP_REN = ("TITEL", 1)

if __name__ == '__main__':
    # Dateien anhand des Tupels TP_REN umbenennen
    # Aktuelles Datei-Verzeichnis lesen
    ls_datei = os.listdir()
    # Index für die Datei
    in_datei_id = 0
    # Liste für die Umbenennungen
    ls_rename = []
    for tx_datei in ls_datei:
        # Jede Datei abarbeiten
        tx_neu = ""
        # Aktionen und Werte auslesen
        if tx_datei == "pyren.py":
            # Nichts machen, darum Index 1 herunterzählen
            in_datei_id -= 1
        elif TP_REN[0] == "START":
            # Am Dateianfang ersetzen
            if tx_datei.startswith(TP_REN[1]):
                # Beginnt mit Suchtext, Anfang abschneiden
                # Muster
                # 012345
                in_id = len(TP_REN[1])
                tx_neu = tx_datei[in_id:]
                # Neuer Anfang voranstellen
                tx_neu = "{0}{1}".format(TP_REN[2], tx_neu)
        elif TP_REN[0] == "ENDE":
            # An Dateiende ersetzen
            if tx_datei.endswith(TP_REN[1]):
                # Endet mit Suchtext, Schluss abschneiden
                # Muster
                # 012345
                in_id = len(tx_neu) - len(TP_REN[1])
                tx_neu = tx_datei[:in_id]
                # Neues Ende anfügen
                tx_neu = "{0}{1}".format(tx_neu, TP_REN[2])
        elif TP_REN[0] == "ERSATZ":
            # Zeichen ersetzen
            tx_neu = tx_datei.replace(TP_REN[1], TP_REN[2])
        elif TP_REN[0] == "LÖSCHEN":
            # Ab Position Anzahl Zeichen löschen
            # Muster
            # 012345
            # Linker und rechter Text auslesen
            in_links = TP_REN[1] - 1
            in_rechts = TP_REN[1] + TP_REN[2] - 1
            tx_links = tx_datei[:in_links]
            tx_rechts = tx_datei[in_rechts:]
            # Zusammenfügen
            tx_neu = "{0}{1}".format(tx_links, tx_rechts)
        elif TP_REN[0] == "EINFÜGEN":
            # Ab Position Anzahl Zeichen löschen
            # Muster
            # 012345
            # Linker und rechter Text auslesen
            in_id = TP_REN[1] - 1
            tx_links = tx_datei[:in_id]
            tx_rechts = tx_datei[in_id:]
            # Zusammenfügen
            tx_neu = "{0}{1}{2}".format(
                tx_links,
                TP_REN[2],
                tx_rechts
            )
        elif TP_REN[0] == "ANFANG":
            # Ab Position Anzahl Zeichen an den Anfang stellen
            # Muster
            # 012345
            # Linker, mittlerer und rechter Text auslesen
            in_links = TP_REN[1] - 1
            in_rechts = TP_REN[1] + TP_REN[2] - 1
            tx_links = tx_datei[:in_links]
            tx_rechts = tx_datei[in_rechts:]
            tx_mitte = tx_datei[in_links:in_rechts]
            # Mittlerer Text an den Anfang
            tx_neu = "{0}{1}{2}".format(
                tx_mitte,
                tx_links,
                tx_rechts
            )
        elif TP_REN[0] == "SCHLUSS":
            # Ab Position Anzahl Zeichen an den Anfang stellen
            # Muster
            # 012345
            # Linker, mittlerer und rechter Text auslesen
            in_links = TP_REN[1] - 1
            in_rechts = TP_REN[1] + TP_REN[2] - 1
            tx_links = tx_datei[:in_links]
            tx_rechts = tx_datei[in_rechts:]
            tx_mitte = tx_datei[in_links:in_rechts]
            # Mittlerer Text an den Anfang
            tx_neu = "{0}{1}{2}".format(
                tx_links,
                tx_rechts,
                tx_mitte
            )
        elif TP_REN[0] == "EINFÜGENSTART":
            # Am Anfang einfügen
            tx_neu = "{0}{1}".format(TP_REN[1], tx_datei)
        elif TP_REN[0] == "EINFÜGENENDE":
            # Am Ende einfügen
            tx_neu = "{0}{1}".format(tx_datei, TP_REN[1])
        elif TP_REN[0] == "ZAHL":
            # Neu nummerieren mit Zahlen und Trennzeichen
            # Zahl generieren
            tx_zahl = str(in_datei_id + TP_REN[1])
            tx_zahl = tx_zahl.zfill(TP_REN[2])
            # Dateinamen mit Zahl und Trennzeichen bilden
            tx_neu = "{0}{1}{2}".format(
                tx_zahl,
                TP_REN[3],
                tx_datei
            )
        elif TP_REN[0] == "BUCHSTABEN":
            # Neu nummerieren mit Zahlen und Trennzeichen
            # Bucstaben generieren
            ls_abc_kl = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                         'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                         'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                         'y', 'z']
            ls_abc_gr = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                         'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
                         'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                         'Y', 'Z']
            # Startbuchstabe und Startwert suchen
            if TP_REN[1] in ls_abc_kl:
                # Der Startwerte entspricht a - z
                # Start suchen
                tx_id_klgr = "klein"
                # Such-ID mit 1 beginnen, Start-ID auf 0
                in_suchid = 0
                in_startid = 0
                for tx_buchstabe in ls_abc_kl:
                    if TP_REN[1] == tx_buchstabe:
                        # Buchstabe gefunden
                        in_startid = in_suchid
                        break
                    in_suchid += 1
                print("startid", in_startid)
            elif TP_REN[1] in ls_abc_gr:
                # Der Startwerte entspricht A-Z
                # Start suchen
                tx_id_klgr = "gross"
                # Such-ID mit 1 beginnne, Start-ID auf 0
                in_suchid = 0
                in_startid = 0
                for tx_buchstabe in ls_abc_gr:
                    if TP_REN[1] == tx_buchstabe:
                        # Buchstabe gefunden
                        in_startid = in_suchid
                        break
                    in_suchid += 1
                print("STARTID", in_startid)
            # Buchstaben anhand Typ (gross/klein) und ID bilden
            in_buchstid = in_datei_id + in_suchid
            # Buchstaben Index kann von 0 - 25 sein, solange
            # durchlaufen, bis der Wert 0-25 ist.
            while in_buchstid > 25:
                in_buchstid -= 26
            if tx_id_klgr == "klein":
                tx_buchstabe = ls_abc_kl[in_buchstid]
            elif tx_id_klgr == "gross":
                tx_buchstabe = ls_abc_gr[in_buchstid]
            # Dateinamen mit Zahl und Trennzeichen bilden
            tx_neu = "{0}{1}{2}".format(
                tx_buchstabe,
                TP_REN[2],
                tx_datei
            )
        elif TP_REN[0] == "KLEIN":
            # Alles mit Klein buchstaben
            tx_neu = tx_datei.lower()
        elif TP_REN[0] == "GROSS":
            # Alles mit GROSS BUCHSTABEN
            tx_neu = tx_datei.upper()
        elif TP_REN[0] == "TITEL":
            # Alles mit Titel Gross Buchstaben
            tx_neu = tx_datei.title()
        elif TP_REN[0] == "SATZ":
            # Alles mit Satz gross buchstaben
            tx_neu = tx_datei.capitalize()
        elif TP_REN[0] == "TAUSCHEN":
            # Alles mit vERTAUSCHTEN gROSS bUCHSTABEN
            tx_neu = tx_datei.swapcase()
        if tx_neu:
            # Es wurde eine Änderung gemacht, in Liste aufnehmen
            ls_rename.append((tx_datei, tx_neu))
        # Datei Id hochzählen
        in_datei_id += 1
    if ls_rename:
        # Liste enthält Umbenennungen, linke Spaltenbreite ermitteln
        in_anzlinks = 0
        for tx_alt, tx_neu in ls_rename:
            if len(tx_alt) > in_anzlinks:
                in_anzlinks = len(tx_alt)
        # Erbebnis präsentieren
        print("Dateien umbenennen")
        print("------------------")
        for tx_alt, tx_neu in ls_rename:
            tx_t = "{0}  >  {1}".format(
                tx_alt.ljust(in_anzlinks),
                tx_neu
            )
            print(tx_t)
        # Abfrage
        print("")
        tx_input = input("Möchten Sie die Dateien umbenennen (j/n)? ")
        tx_input = tx_input.lower()
        if tx_input == "j":
            # die Elemente umbenennen
            for tx_alt, tx_neu in ls_rename:
                os.rename(tx_alt, tx_neu)
    else:
        print("Keine Dateien zum umbenennen ..")
        tx_input = input("Bitte bestätigen um fortzufahren ..")
