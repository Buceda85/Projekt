import os
import sys
from pathlib import Path

import pytest
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error


# zajistí, že pytest najde soubor taskmanager2.py v kořenu projektu
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


# načtení proměnných z .env.test, případně z .env
load_dotenv(ROOT_DIR / ".env.test")
load_dotenv(ROOT_DIR / ".env", override=False)


@pytest.fixture(scope="session")
def db_connection():
    """Připojení k testovací MySQL databázi pro celou testovací session."""
    server_connection = None
    connection = None
    cursor = None

    db_host = os.getenv("TEST_DB_HOST", os.getenv("DB_HOST"))
    db_user = os.getenv("TEST_DB_USER", os.getenv("DB_USER"))
    db_password = os.getenv("TEST_DB_PASSWORD", os.getenv("DB_PASSWORD"))
    db_name = os.getenv("TEST_DB_NAME", "test_projekt2")

    if db_host is None or db_user is None or db_password is None or db_name is None:
        pytest.fail(
            "Chybí přihlašovací údaje k testovací databázi. "
            "Zkontrolujte soubor .env.test nebo .env."
        )

    try:
        # 1) Připojení k MySQL serveru bez výběru databáze
        server_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )

        cursor = server_connection.cursor()
        safe_db_name = db_name.replace("`", "``")

        # 2) Vytvoření testovací databáze, pokud neexistuje
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{safe_db_name}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        server_connection.commit()

    except Error as e:
        pytest.fail(f"Nepodařilo se vytvořit testovací databázi: {e}")

    finally:
        if cursor is not None:
            cursor.close()

        if server_connection is not None and server_connection.is_connected():
            server_connection.close()

    try:
        # 3) Připojení už přímo k testovací databázi
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ukoly (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nazev VARCHAR(255) NOT NULL,
                popis TEXT NOT NULL,
                stav VARCHAR(50) NOT NULL DEFAULT 'Nezahájeno',
                datum_vytvoreni DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.commit()
        cursor.close()

        yield connection

    except Error as e:
        pytest.fail(f"Nepodařilo se připojit k testovací databázi: {e}")

    finally:
        if connection is not None and connection.is_connected():
            connection.close()


@pytest.fixture(autouse=True)
def clean_db(db_connection):
    """Vyčistí tabulku 'ukoly' před a po každém testu."""
    cursor = db_connection.cursor()

    try:
        cursor.execute("DELETE FROM ukoly")
        db_connection.commit()

        yield

        cursor.execute("DELETE FROM ukoly")
        db_connection.commit()

    finally:
        cursor.close()


@pytest.fixture
def app_module():
    """Vrátí modul taskmanager2 pro testování."""
    import taskmanager2
    return taskmanager2
