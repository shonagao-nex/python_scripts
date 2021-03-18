#!/bin/sh

pyinstaller controlGUI.py --onefile
cp -f dist/controlGUI .
