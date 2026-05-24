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

MySQL Server musí být spuštěný a uživatel uvedený v souboru `.env` musí mít oprávnění pro vytvoření databáze.

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

## Nastavení připojení k databázi

Projekt používá soubor `.env`, který obsahuje lokální přihlašovací údaje k MySQL databázi.

Soubor `.env` není součástí repozitáře, protože může obsahovat citlivé údaje, například heslo k databázi.

V repozitáři je přiložený vzorový soubor:

```text
.env.example
```

Podle tohoto souboru je potřeba vytvořit vlastní lokální soubor:

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

## Nastavení testovací databáze

Testy mohou používat samostatný soubor:

```text
.env.test
```

Soubor `.env.test` není součástí repozitáře, protože může obsahovat citlivé údaje.

Příklad obsahu souboru `.env.test`:

```env
TEST_DB_HOST=localhost
TEST_DB_USER=root
TEST_DB_PASSWORD=your_mysql_password
TEST_DB_NAME=test_projekt2
```

Testovací databáze je oddělená od hlavní databáze aplikace, aby testy nemazaly běžná data.

Pokud soubor `.env.test` neexistuje, testy mohou využít hodnoty ze souboru `.env`.

---

## Nastavení databáze

Aplikace vytváří databázi automaticky při spuštění.

Při spuštění se aplikace nejprve připojí k MySQL serveru bez výběru konkrétní databáze a následně provede vytvoření databáze, pokud ještě neexistuje.

Používaná databáze pro běžný běh aplikace:

```text
projekt2
```

Název databáze je možné změnit v souboru `.env` pomocí proměnné:

```env
DB_NAME=projekt2
```

Tabulka `ukoly` se také vytvoří automaticky při spuštění aplikace, pokud ještě neexistuje.

Soubor `database.sql` je v projektu ponechán pouze jako volitelný pomocný přehled databázové struktury. Pro spuštění aplikace není nutné tento soubor ručně spouštět.

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
tests/
```

Testy používají samostatnou testovací databázi:

```text
test_projekt2
```

Testovací databáze i tabulka se vytvoří automaticky, pokud ještě neexistují.

---

## Struktura projektu

```text
projekt/
├── tests/
│   ├── conftest.py
│   └── test_ukoly.py
├── .env.example
├── .gitignore
├── database.sql
├── pytest.ini
├── README.md
├── requirements.txt
└── taskmanager2.py
```

Lokální soubory `.env` a `.env.test` nejsou součástí repozitáře, protože mohou obsahovat citlivé údaje.

---

## Soubor database.sql

Soubor `database.sql` slouží pouze jako volitelný pomocný soubor s SQL strukturou databáze.

Aplikace pro své spuštění nevyžaduje ruční spuštění tohoto souboru.

Databáze i tabulka se vytváří automaticky přímo v aplikaci při spuštění programu.

---

## Poznámka k databázi

Databáze ani data nejsou součástí repozitáře.

Aplikace si databázi i tabulku vytvoří automaticky při spuštění podle údajů uvedených v lokálním souboru `.env`.

Testy si samostatnou testovací databázi vytvoří automaticky podle údajů v `.env.test` nebo podle záložních hodnot v `.env`.

---

## Poznámka k citlivým údajům

Soubor `.env` a případně také `.env.test` jsou záměrně uvedeny v `.gitignore`, aby se nenahrávaly na GitHub.

Do repozitáře patří pouze vzorový soubor `.env.example`, který neobsahuje skutečné heslo k databázi.

---

## requirements.txt

Projekt používá tyto Python knihovny:

```text
mysql-connector-python
python-dotenv
pytest
```

Instalace všech závislostí probíhá pomocí:

```bash
python3 -m pip install -r requirements.txt
```
