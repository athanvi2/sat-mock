@echo off
rem Windows: double-click this file
cd /d "%~dp0"
py -m pip install -q -r requirements.txt
py app.py
