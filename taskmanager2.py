import mysql.connector, datetime
from mysql.connector import Error

db_connection = None

# funkce pro připojení programu k MySQL databázi
def pripojeni_db():
    """Pokusí se připojit k MySQL databázi.
       Při úspěchu vrátí connection objekt, při neúspěchu None.
    """
    global db_connection

    try:
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Test123!",
            database="sys"
        )

        if db_connection.is_connected():
            print("\nPřipojení k databázi bylo úspěšné.")
            return db_connection
        else:
            print("\nNepodařilo se připojit k databázi.")
            return None

    except Error as e:
        print("\nChyba při připojování k databázi:")
        print(e)
        return None

# funkce pro vytvoření SQL tabulky "ukoly"
def vytvoreni_tabulky(connection):
    """Vytvoří tabulku 'ukoly', pokud ještě neexistuje."""
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

# funkce hlavního menu
def hlavni_menu():
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
            print("\nVolba musí být číslo 1–4. Zkuste to znovu.")
            continue

        volba = int(volba)

        if volba == 1:
            pridat_ukol()
        elif volba == 2:
            zobrazit_ukoly()
        elif volba == 3:
            aktualizovat_ukol()
        elif volba == 4:
            odstranit_ukol()
        elif volba == 5:
            print("\nKonec programu.")
            break
        else:
            print("\nNeplatná volba. Zadejte číslo v rozmezí 1–4.")

# funkce pro přidání úkolu do seznamu úkolů
def pridat_ukol():
    # použití cyklu pro možnost opakovaného zadávání názvu a popisu úkolu.
    while True:
        nazev_ukolu = input("\nZadejte název úkolu: ").strip()
        if not nazev_ukolu:
            print("\nNázev úkolu nesmí být prázdný. Zkuste to prosím znovu.")
            continue

        popis_ukolu = input("Zadejte popis úkolu: ").strip()
        if not popis_ukolu:
            print("\nPopis úkolu nesmí být prázdný. Zkuste to prosím znovu.")
            continue

        if db_connection is None or not db_connection.is_connected():
            print("\nNelze uložit úkol — není aktivní připojení k databázi.")
            return
        try:
            cursor = db_connection.cursor()

            vychozi_stav = "Nezahájeno"

            sql = """
                INSERT INTO ukoly (nazev, popis, stav)
                VALUES (%s, %s, %s)
            """
            hodnoty = (nazev_ukolu, popis_ukolu, vychozi_stav)

            cursor.execute(sql, hodnoty)
            db_connection.commit()

            nove_id = cursor.lastrowid

            print(f"\nÚkol byl úspěšně přidán do databáze.")
            print(f"   ID: {nove_id}")
            print(f"   Název: {nazev_ukolu}")
            print(f"   Popis: {popis_ukolu}")
            print(f"   Stav: {vychozi_stav}")

            break

        except mysql.connector.Error as e:
            print("\nDošlo k chybě při ukládání úkolu do databáze:")
            print(e)
            break

# funkce pro zobrazení všech přidaných úkolů uživatelem
def zobrazit_ukoly():
    """Zobrazí úkoly z databáze se stavem 'Nezahájeno' nebo 'Probíhá'."""

    # kontrola připojení k databázi
    if db_connection is None or not db_connection.is_connected():
        print("\nNelze zobrazit úkoly — není aktivní připojení k databázi.")
        return

    try:
        cursor = db_connection.cursor(dictionary=True)

        # Načtení úkolů s požadovaným stavem
        cursor.execute("""
            SELECT id, nazev, popis, stav, datum_vytvoreni
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
            dv = u['datum_vytvoreni']
            # Naformátování datumu (pokud je to datetime objekt)
            if isinstance(dv, datetime.datetime):
                dv_str = dv.strftime("%d.%m.%Y %H:%M")
            else:
                dv_str = str(dv)

            print(f"ID: {u['id']}")
            print(f"Název: {u['nazev']}")
            print(f"Popis: {u['popis']}")
            print(f"Stav: {u['stav']}")
            print(f"Vytvořeno: {dv_str}")
            print("-" * 80)

    except mysql.connector.Error as e:
        print("\nDošlo k chybě při načítání úkolů z databáze:")
        print(e)

# funkce pro aktualizování úkolu v databázi
def aktualizovat_ukol():
    """Změna stavu úkolu v databázi."""

    # kontrola připojení k databázi
    if db_connection is None or not db_connection.is_connected():
        print("\nNelze pracovat s úkoly — není aktivní připojení k databázi.")
        return

    try:
        cursor = db_connection.cursor(dictionary=True)

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
                    db_connection.commit()

                    print(f"\nStav úkolu byl úspěšně změněn z '{vybrany['stav']}' na '{novy_stav}'.")
                    return  # po úspěšné změně končíme funkci

                print("\nNeplatná volba. Zadejte 0, 1 nebo 2.")

            # pokud se ve vnitřním while zvolila 0, vnější while pokračuje znovu:
            # znovu se vypíšou úkoly a vybírá se jiné ID

    except mysql.connector.Error as e:
        print("\nDošlo k chybě při aktualizaci úkolu v databázi:")
        print(e)

# funkce pro odebrání konkrétního úkolu zadáním čísla úkolu v seznamu
def odstranit_ukol():
    """Odstraní úkol z databáze podle ID."""

    # kontrola připojení k databázi
    if db_connection is None or not db_connection.is_connected():
        print("\nNelze pracovat s úkoly — není aktivní připojení k databázi.")
        return

    try:
        cursor = db_connection.cursor(dictionary=True)

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
            db_connection.commit()

            print(f"\nÚkol s ID {id_ukolu} a názvem '{vybrany['nazev']}' byl trvale odstraněn z databáze.")
            return # úspěšné smazání, ukončíme cyklus

    except mysql.connector.Error as e:
        print("\nDošlo k chybě při odstraňování úkolu z databáze:")
        print(e)

    while True:
        # pokud je seznam prázdný, informuj uživatele a vrať se do hlavního menu
        if not ukoly:
            print("\nSeznam úkolů je prázdný. Není co mazat.")
            input("Stiskněte Enter pro návrat do hlavního menu...")
            return

        zobrazit_ukoly()
        vstup = input("Zadejte číslo úkolu, který chcete odstranit (nebo 0 pro návrat do hlavního menu): ").strip()

        # ošetření pokud uživatel zadá prázdný vstup
        if not vstup:
            print("\nNezadali jste číslo úkolu, který si přejete smazat. Zkuste to prosím znovu.")
            continue
    
        # ošetření pokud uživatel zadá jiné znaky než číselné
        if not vstup.isdigit():
            print("\nNezadali jste celé kladné číslo. Zkuste to prosím znovu.")
            continue

        cislo = int(vstup)

        if cislo == 0:
            print("\nNávrat do hlavního menu.")
            return
        
         # uživatel vidí pořadí úkolu od "1.", ale indexy začínají v Pythonu od "0"
        index = cislo - 1

        # podmínka pro zadání jiného vstupu než reálného čísla úkolu v seznamu
        if index < 0 or index >= len(ukoly):
            print("\nTakové číslo úkolu v seznamu není. Zkuste to prosím znovu.")
            continue

        # odebrání konkrétního úkolu ze sezmamu úkolů za pomocí indexu úkolu
        odebrany_ukol = ukoly.pop(index)
        print(f"\nÚkol '{odebrany_ukol['nazev']}' byl odstraněn.")
        break

if __name__ == "__main__":
    conn = pripojeni_db()

    if conn is not None:
        # připojení proběhlo v pořádku = program se spustí
        vytvoreni_tabulky(conn)
        hlavni_menu()
    else:
        # připojení selhalo = program se ukončí
        print("\nProgram bude ukončen z důvodu chyby připojení k databázi.")
