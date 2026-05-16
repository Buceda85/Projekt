# Task Manager

Konzolová aplikace v Pythonu pro správu úkolů s využitím lokální MySQL databáze.

Aplikace umožňuje:

- přidat nový úkol,
- zobrazit existující úkoly,
- aktualizovat stav úkolu,
- odstranit úkol,
- ukládat data do lokální MySQL databáze.

---

## Použité technologie

- Python 3
- MySQL
- mysql-connector-python
- python-dotenv
- pytest

---

## Požadavky před spuštěním

Před spuštěním projektu je potřeba mít nainstalované:

- Python 3
- MySQL Server
- pip

---

## Instalace projektu

Nejprve si naklonujte repozitář:

```bash
git clone URL_REPOZITARE
cd NAZEV_SLOZKY_PROJEKTU
```

Poté nainstalujte potřebné Python knihovny:

```bash
python3 -m pip install -r requirements.txt
```

Pokud používáte místo `python3` příkaz `python`, můžete použít:

```bash
python -m pip install -r requirements.txt
```

---

## Nastavení databáze

Projekt používá lokální MySQL databázi s názvem:

```text
projekt2
```

Databázi je možné vytvořit pomocí přiloženého souboru:

```text
database.sql
```

Soubor obsahuje příkaz:

```sql
CREATE DATABASE IF NOT EXISTS projekt2
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

Tento SQL příkaz lze spustit například v aplikaci MySQL Workbench.

Tabulka `ukoly` se vytvoří automaticky při spuštění aplikace, pokud ještě neexistuje.

---

## Nastavení připojení k databázi

Projekt používá soubor `.env`, který obsahuje lokální přihlašovací údaje k databázi.

Soubor `.env` není součástí repozitáře, protože může obsahovat citlivé údaje, například heslo k databázi.

V repozitáři je přiložený vzorový soubor:

```text
.env.example
```

Podle tohoto souboru je potřeba vytvořit vlastní soubor:

```text
.env
```

Příklad obsahu souboru `.env`:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=projekt2
```

Hodnotu `DB_PASSWORD` je potřeba upravit podle vlastního hesla k MySQL.

---

## Spuštění aplikace

Aplikaci lze spustit příkazem:

```bash
python3 taskmanager2.py
```

Případně:

```bash
python taskmanager2.py
```

Po spuštění se zobrazí konzolové menu pro práci s úkoly.

---

## Spuštění testů

Testy lze spustit příkazem:

```bash
python3 -m pytest
```

Případně:

```bash
python -m pytest
```

Testy se nachází ve složce:

```text
Tests/
```

---

## Struktura projektu

```text
projekt/
├── tests/
│   ├── conftest.py
│   └── test_ukoly.py
├── .env
├── .env.example
├── .gitignore
├── database.sql
├── pytest.ini
├── README.md
├── requirements.txt
└── taskmanager2.py
```

---

## Poznámka k databázi

Databáze samotná není součástí repozitáře.

Každý uživatel si ji vytvoří lokálně pomocí souboru `database.sql`.

Aplikace se následně připojí k databázi podle údajů uvedených v lokálním souboru `.env`.

Tabulka `ukoly` je vytvářena automaticky samotnou aplikací.

---

## Poznámka k citlivým údajům

Soubor `.env` je záměrně uvedený v `.gitignore`, aby se nenahrával na GitHub.

Do repozitáře patří pouze vzorový soubor `.env.example`, který neobsahuje skutečné heslo k databázi.
