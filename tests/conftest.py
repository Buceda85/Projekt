import sys
from pathlib import Path

import pytest
import mysql.connector
from mysql.connector import Error


# zajistí, že pytest najde soubor projekt2.py v kořenu projektu
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


@pytest.fixture(scope="session")
def db_connection():
    """Připojení k testovací MySQL databázi pro celou testovací session."""
    connection = None

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Test123!",
            database="test_projekt2"
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
def app_module(db_connection, monkeypatch):
    """Napojí modul projekt2 na testovací databázi."""
    import taskmanager2

    monkeypatch.setattr(taskmanager2, "db_connection", db_connection)
    return taskmanager2
