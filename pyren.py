#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

'''
pyren.py - Dateien des aktuellen Verzeichnisses umbenennen
Copyright (c) Dez. 2020: Andreas Ulrich
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


if __name__ == '__main__':
    # Dateien anhand eines Musters umbenennen.
    # Aktuelles Verzeichnis lesen
    datei_liste = os.listdir()
    for e in datei_liste:
        # Jedes Element abarbeiten
        new_e = ""
        if e.endswith(" (B).json"):
            # " (B)" entfernen
            new_e = e.replace(" (B)", "")
        elif e.endswith(" (BS).json")
            new_e = e.replace(" (BS", "")
        if new_e:
            # Falls für new_e eine Zeichenfolge definiert wurde,
            # das Element umbenennen
            os.rename(e, new_e)
