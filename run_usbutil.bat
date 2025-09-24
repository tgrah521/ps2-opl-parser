@echo off
title PS2 OPL Parser

set /p ISO=Pfad zur ISO-Datei eingeben: 

set /p OUT=Pfad zum Ausgabeverzeichnis (z.B. USB-Stick): 

set /p NAME=Spielname (leer lassen für Standard): 

if "%NAME%"=="" (
    python ps2_opl_parser.py "%ISO%" "%OUT%"
) else (
    python ps2_opl_parser.py "%ISO%" "%OUT%" --name "%NAME%"
)

pause
