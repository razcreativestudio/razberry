@echo off
rem ==============================================================================
rem Metadata & Header File
rem Proyek        : RAZBerry Browser
rem File          : RAZBerry.bat
rem Dibuat Pada   : 2026-11-24
rem Author        : RAZ Creative Studio
rem Deskripsi     : Batch launcher untuk menjalankan RAZBerry Browser standalone
rem ==============================================================================
cd /d "%~dp0dist\RAZBerry"
start "" "razberry.exe" -app browser\application.ini %*
