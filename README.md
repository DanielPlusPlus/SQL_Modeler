# SQL Modeler

Projekt w Pythonie do generowania diagramów/struktur SQL. Repozytorium powstało podczas studiów na Politechnice Świętokrzyskiej.

## Wymagania

- Python 3.12

## Instalacja i uruchomienie

1. Utwórz i aktywuj wirtualne środowisko:

   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

   Na Windows:

   ```powershell
   py -3.12 -m venv .venv
   .venv\Scripts\activate
   ```

2. Zainstaluj zależności z pliku `requirements.txt`:

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
