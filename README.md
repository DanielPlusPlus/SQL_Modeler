# SQL Generator From Diagram Python
<b>PL:</b> To repozytorium zawiera projekt w języku Python stworzony podczas moich studiów na Politechnice Świętokrzyskiej.<br/> 
<b>ENG:</b> This repository contains project in Python language that was created during my studies at the Kielce University of Technology.

## Uruchomienie projektu / Project setup

1. Upewnij się, że używasz Pythona 3.12 lub nowszego:
   ```bash
   python --version
   ```
2. Utwórz wirtualne środowisko:
   ```bash
   python -m venv .venv
   ```
3. Aktywuj środowisko:
   ```bash
   # Linux/macOS
   source .venv/bin/activate

   # Windows (PowerShell)
   # If script execution is blocked, run:
   # Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
   .venv/Scripts/Activate.ps1

   # Windows (cmd)
   .venv\Scripts\activate.bat
   ```
4. Zainstaluj zależności z pliku `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
5. Uruchom aplikację (po aktywacji środowiska):
   ```bash
   python main.py
   ```
