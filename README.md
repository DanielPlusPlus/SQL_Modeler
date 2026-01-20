# SQL Modeler

Projekt w Pythonie do generowania diagramów/struktur SQL. Repozytorium powstało podczas studiów na Politechnice Świętokrzyskiej.

## Wymagania

- Python 3.12 (jeśli nie masz zainstalowanej wersji 3.12, pobierz ją z https://www.python.org/downloads/ lub użyj menedżera pakietów systemu)

## Instalacja i uruchomienie

1. Utwórz i aktywuj wirtualne środowisko:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   Upewnij się, że polecenie `python3` wskazuje na wersję 3.12 (np. `python3 --version`).

   Na Windows:

   ```powershell
   py -3.12 -m venv .venv
   .venv\Scripts\activate
   ```

   Upewnij się, że `py -3.12` wskazuje na wersję 3.12 (np. `py -3.12 --version`).

2. Zainstaluj zależności z pliku `requirements.txt` (plik znajduje się w katalogu głównym repozytorium):

   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. Uruchom aplikację:

   ```bash
   python3 main.py
   ```

## Testy (opcjonalnie)

```bash
python3 -m unittest discover tests/
```
