import os, mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()

# funkce pro připojení programu k MySQL databázi
def pripojeni_db():
    """Vytvoří databázi, pokud neexistuje, a vrátí připojení k databázi."""

    db_host = os.getenv("DB_HOST")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    if db_host is None or db_user is None or db_password is None or db_name is None:
        print("Chybí údaje pro připojení k databázi v souboru .env.")
        return None

    server_connection = None
    cursor = None

    try:
        # 1) Připojení k MySQL serveru bez výběru konkrétní databáze
        server_connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )

        cursor = server_connection.cursor()

        # Ošetření názvu databáze pro použití v SQL příkazu
        safe_db_name = db_name.replace("`", "``")

        # 2) Vytvoření databáze, pokud ještě neexistuje
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{safe_db_name}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        server_connection.commit()

    except Error as e:
        print("Chyba při vytváření databáze:")
        print(e)
        return None

    finally:
        if cursor is not None:
            cursor.close()

        if server_connection is not None and server_connection.is_connected():
            server_connection.close()

    try:
        # 3) Připojení už přímo ke konkrétní databázi
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )

        if connection.is_connected():
            print("Připojení k databázi bylo úspěšné.")
            return connection

    except Error as e:
        print("Chyba při připojování k databázi:")
        print(e)
        return None

# funkce pro vytvoření SQL tabulky "ukoly"
def vytvoreni_tabulky(connection):
    """Vytvoří tabulku 'ukoly', pokud ještě neexistuje."""

    cursor = None

    try:
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
        print("Tabulka 'ukoly' byla ověřena nebo úspěšně vytvořena.")

    except mysql.connector.Error as e:
        print("Chyba při vytváření tabulky:", e)

    finally:
        if cursor is not None:
            cursor.close()

# funkce hlavního menu
def hlavni_menu(connection):
    while True:
        print("\nSprávce úkolů — Hlavní menu")
        print("1. Přidat nový úkol")
        print("2. Zobrazit všechny úkoly")
        print("3. Aktualizovat stav úkolu")
        print("4. Odstranit úkol")
        print("5. Konec programu")

        volba = input("Vyberte možnost (1–5): ").strip()

        # Validace vstupu
        if not volba:
            print("\nNezadali jste žádnou volbu. Zkuste to znovu.")
            continue
        if not volba.isdigit():
            print("\nVolba musí být číslo 1–5. Zkuste to znovu.")
            continue

        volba = int(volba)

        if volba == 1:
            pridat_ukol(connection)
        elif volba == 2:
            zobrazit_ukoly(connection)
        elif volba == 3:
            aktualizovat_ukol(connection)
        elif volba == 4:
            odstranit_ukol(connection)
        elif volba == 5:
            print("\nKonec programu.")
            break
        else:
            print("\nNeplatná volba. Zadejte číslo v rozmezí 1–5.")

# funkce pro přidání úkolu do seznamu úkolů
def pridat_ukol(connection):
    """Přidá nový úkol do databáze."""

    # kontrola připojení k databázi
    if connection is None or not connection.is_connected():
        print("\nNelze uložit úkol — není aktivní připojení k databázi.")
        return

    while True:
        print("\nPřidání nového úkolu")
        print("Zadejte 0 pro návrat do hlavního menu.")

        nazev_ukolu = input("Zadejte název úkolu: ").strip()

        if nazev_ukolu == "0":
            print("\nNávrat do hlavního menu bez přidání úkolu.")
            return

        if not nazev_ukolu:
            print("\nNázev úkolu nesmí být prázdný. Zkuste to prosím znovu.")
            continue

        popis_ukolu = input("Zadejte popis úkolu: ").strip()

        if popis_ukolu == "0":
            print("\nNávrat do hlavního menu bez přidání úkolu.")
            return

        if not popis_ukolu:
            print("\nPopis úkolu nesmí být prázdný. Zkuste to prosím znovu.")
            continue

        cursor = None

        try:
            cursor = connection.cursor()

            vychozi_stav = "Nezahájeno"

            sql = """
                INSERT INTO ukoly (nazev, popis, stav)
                VALUES (%s, %s, %s)
            """
            hodnoty = (nazev_ukolu, popis_ukolu, vychozi_stav)

            cursor.execute(sql, hodnoty)
            connection.commit()

            nove_id = cursor.lastrowid

            print("\nÚkol byl úspěšně přidán do databáze.")
            print(f"   ID: {nove_id}")
            print(f"   Název: {nazev_ukolu}")
            print(f"   Popis: {popis_ukolu}")
            print(f"   Stav: {vychozi_stav}")

            return

        except mysql.connector.Error as e:
            print("\nDošlo k chybě při ukládání úkolu do databáze:")
            print(e)
            return

        finally:
            if cursor is not None:
                cursor.close()

# funkce pro zobrazení všech přidaných úkolů uživatelem
def zobrazit_ukoly(connection):
    """Zobrazí úkoly z databáze se stavem 'Nezahájeno' nebo 'Probíhá'."""

    if connection is None or not connection.is_connected():
        print("\nNelze zobrazit úkoly — není aktivní připojení k databázi.")
        return

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("""
            SELECT id, nazev, popis, stav
            FROM ukoly
            WHERE stav IN ('Nezahájeno', 'Probíhá')
            ORDER BY id
        """)
        ukoly = cursor.fetchall()

        if not ukoly:
            print("\nSeznam úkolů je prázdný (žádné úkoly ve stavu 'Nezahájeno' nebo 'Probíhá').")
            return

        print("\nSeznam úkolů:")
        print("-" * 80)
        for u in ukoly:
            print(f"ID: {u['id']}")
            print(f"Název: {u['nazev']}")
            print(f"Popis: {u['popis']}")
            print(f"Stav: {u['stav']}")
            print("-" * 80)

    except mysql.connector.Error as e:
        print("\nDošlo k chybě při načítání úkolů z databáze:")
        print(e)

# funkce pro aktualizování úkolu v databázi
def aktualizovat_ukol(connection):
    """Změna stavu úkolu v databázi."""

    # kontrola připojení k databázi
    if connection is None or not connection.is_connected():
        print("\nNelze pracovat s úkoly — není aktivní připojení k databázi.")
        return

    try:
        cursor = connection.cursor(dictionary=True)

        while True:
            # 1) Načtení seznamu úkolů
            cursor.execute("SELECT id, nazev, stav FROM ukoly ORDER BY id")
            ukoly = cursor.fetchall()

            if not ukoly:
                print("\nSeznam úkolů je prázdný. Není co aktualizovat.")
                return

            # 2) Vypsání seznamu úkolů
            print("\nSeznam úkolů:")
            for u in ukoly:
                print(f"ID: {u['id']} | Název: {u['nazev']} | Stav: {u['stav']}")

            # 3) Výběr úkolu podle ID (s možností návratu)
            print("\nZadejte ID úkolu, jehož stav chcete změnit.")
            print("Nebo zadejte 0 pro návrat do hlavního menu.")
            vstup = input("Vaše volba: ").strip()

            if not vstup:
                print("\nNezadali jste žádné ID. Zkuste to prosím znovu.")
                continue

            if not vstup.isdigit():
                print("\nID musí být celé kladné číslo. Zkuste to prosím znovu.")
                continue

            id_ukolu = int(vstup)

            # možnost návratu do hlavního menu bez změny
            if id_ukolu == 0:
                print("\nNávrat do hlavního menu bez změny stavu úkolu.")
                return

            # 4) Ověření, zda úkol s daným ID existuje
            cursor.execute(
                "SELECT id, nazev, stav FROM ukoly WHERE id = %s",
                (id_ukolu,)
            )
            vybrany = cursor.fetchone()

            if vybrany is None:
                print("\nÚkol s takovým ID neexistuje. Zkuste to prosím znovu.")
                continue

            print(f"\nVybrali jste úkol:")
            print(f"ID: {vybrany['id']}")
            print(f"Název: {vybrany['nazev']}")
            print(f"Aktuální stav: {vybrany['stav']}")

            # 5) Příprava nabídky stavů
            vsechny_stavy = ["Nezahájeno", "Probíhá", "Hotovo"]
            # vyfiltrujeme jen ty dva, které nejsou aktuální
            dostupne_stavy = [s for s in vsechny_stavy if s != vybrany['stav']]

            # 6) Volba nového stavu (s možností návratu na výběr úkolu)
            while True:
                print("\nVyberte nový stav úkolu:")
                print("0. Vrátit se na výběr úkolu")
                print(f"1. {dostupne_stavy[0]}")
                print(f"2. {dostupne_stavy[1]}")
                volba_stavu = input("Vaše volba (0–2): ").strip()

                if volba_stavu == "0":
                    print("\nVracíme se zpět na výběr úkolu.")
                    # vyskočíme z výběru stavu a vrátíme se na začátek vnějšího while,
                    # kde se znovu vypíše seznam úkolů
                    break

                if volba_stavu in ("1", "2"):
                    novy_stav = dostupne_stavy[int(volba_stavu) - 1]

                    # 7) Aktualizace v databázi
                    cursor.execute(
                        "UPDATE ukoly SET stav = %s WHERE id = %s",
                        (novy_stav, id_ukolu)
                    )
                    connection.commit()

                    print(f"\nStav úkolu byl úspěšně změněn z '{vybrany['stav']}' na '{novy_stav}'.")
                    return  # po úspěšné změně končíme funkci

                print("\nNeplatná volba. Zadejte 0, 1 nebo 2.")

            # pokud se ve vnitřním while zvolila 0, vnější while pokračuje znovu:
            # znovu se vypíšou úkoly a vybírá se jiné ID

    except mysql.connector.Error as e:
        print("\nDošlo k chybě při aktualizaci úkolu v databázi:")
        print(e)

# funkce pro odebrání konkrétního úkolu zadáním čísla úkolu v seznamu
def odstranit_ukol(connection):
    """Odstraní úkol z databáze podle ID."""

    # kontrola připojení k databázi
    if connection is None or not connection.is_connected():
        print("\nNelze pracovat s úkoly — není aktivní připojení k databázi.")
        return

    try:
        cursor = connection.cursor(dictionary=True)

        while True:
            # 1) Načtení seznamu úkolů
            cursor.execute("SELECT id, nazev, stav FROM ukoly ORDER BY id")
            ukoly = cursor.fetchall()

            if not ukoly:
                print("\nSeznam úkolů je prázdný. Není co mazat.")
                return

            # 2) Vypsání seznamu úkolů
            print("\nSeznam úkolů:")
            for u in ukoly:
                print(f"ID: {u['id']} | Název: {u['nazev']} | Stav: {u['stav']}")

            # 3) Výběr ID úkolu (s možností návratu)
            print("\nZadejte ID úkolu, který chcete odstranit.")
            print("Nebo zadejte 0 pro návrat do hlavního menu.")
            vstup = input("Vaše volba: ").strip()

            if not vstup:
                print("\nNezadali jste žádné ID. Zkuste to prosím znovu.")
                continue

            if not vstup.isdigit():
                print("\nID musí být celé kladné číslo. Zkuste to prosím znovu.")
                continue

            id_ukolu = int(vstup)

            # možnost návratu
            if id_ukolu == 0:
                print("\nNávrat do hlavního menu bez odstranění úkolu.")
                return

            # 4) Ověření, zda úkol s daným ID existuje
            cursor.execute(
                "SELECT id, nazev, popis, stav FROM ukoly WHERE id = %s",
                (id_ukolu,)
            )
            vybrany = cursor.fetchone()

            if vybrany is None:
                print("\nÚkol s takovým ID neexistuje. Zkuste to prosím znovu.")
                continue

            print("\nVybrali jste k odstranění tento úkol:")
            print(f"ID: {vybrany['id']}")
            print(f"Název: {vybrany['nazev']}")
            print(f"Popis: {vybrany['popis']}")
            print(f"Stav: {vybrany['stav']}")

            # 5) Potvrzení smazání
            while True:
                potvrzeni = input("\nOpravdu chcete tento úkol trvale odstranit? (a/n): ").strip().lower()
                if potvrzeni in ("a", "n"):
                    break
                print("Neplatná volba. Zadejte prosím 'a' pro ano nebo 'n' pro ne.")

            if potvrzeni == "n":
                print("\nÚkol nebyl odstraněn.")
                return

            # 6) Odstranění z databáze
            cursor.execute("DELETE FROM ukoly WHERE id = %s", (id_ukolu,))
            connection.commit()

            print(f"\nÚkol s ID {id_ukolu} a názvem '{vybrany['nazev']}' byl trvale odstraněn z databáze.")
            return # úspěšné smazání, ukončíme cyklus

    except mysql.connector.Error as e:
        print("\nDošlo k chybě při odstraňování úkolu z databáze:")
        print(e)

if __name__ == "__main__":
    conn = pripojeni_db()

    if conn is not None:
        try:
            # připojení proběhlo v pořádku = program se spustí
            vytvoreni_tabulky(conn)
            hlavni_menu(conn)

        finally:
            if conn.is_connected():
                conn.close()
                print("\nPřipojení k databázi bylo ukončeno.")
    else:
        # připojení selhalo = program se ukončí
        print("\nProgram bude ukončen z důvodu chyby připojení k databázi.")
