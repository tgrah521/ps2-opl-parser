#!/bin/sh

echo "Pfad zur ISO-Datei eingeben: "
read ISO

echo "Pfad zum Ausgabeverzeichnis (z.B. USB-Stick): "
read OUT

echo "Spielname (leer lassen für Standard): "
read NAME

if [ -z "$NAME" ]; then
    python ps2_opl_parser.py "$ISO" "$OUT"
else
    python ps2_opl_parser.py "$ISO" "$OUT" --name "$NAME"
fi

# Entspricht 'pause' in Batch (wartet auf Enter)
echo "Drücke Enter zum Beenden..."
read dummy
