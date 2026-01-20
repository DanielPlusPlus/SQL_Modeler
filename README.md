# SQL Modeler

Projekt w Pythonie do generowania diagramów/struktur SQL. Repozytorium powstało podczas studiów na Politechnice Świętokrzyskiej.

## Wymagania

- Python 3.12 (wymagana wersja; jeśli nie masz 3.12, pobierz ją z https://www.python.org/downloads/ lub użyj menedżera pakietów systemu)

## Instalacja i uruchomienie

1. Utwórz i aktywuj wirtualne środowisko (użyj Pythona 3.12):

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

   Jeśli `python3.12` nie jest dostępny, użyj `python3` wskazującego na 3.12 (np. `python3 --version`) lub zainstaluj Pythona 3.12.

   Na Windows:

   ```powershell
   py -3.12 -m venv .venv
   .venv\Scripts\activate
   ```

   Upewnij się, że `py -3.12` wskazuje na wersję 3.12 (np. `py -3.12 --version`).

2. Zainstaluj zależności z pliku `requirements.txt` (plik znajduje się w katalogu głównym repozytorium):

   ```bash
   python -m pip install -r requirements.txt
   ```

3. Uruchom aplikację:

   ```bash
   python main.py
   ```

## Testy (opcjonalnie)

```bash
python -m unittest discover tests/
```
