def test_pridat_ukol_pozitivni(app_module, db_connection, monkeypatch, capsys):
    """Pozitivní test: ověří, že se platný úkol správně uloží do databáze."""
    vstupy = iter([
        "Nakoupit mléko",
        "Koupit dvě balení mléka"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(vstupy))

    app_module.pridat_ukol()

    vystup = capsys.readouterr().out

    assert "Úkol byl úspěšně přidán do databáze." in vystup

    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ukoly")
    ukoly = cursor.fetchall()
    cursor.close()

    assert len(ukoly) == 1
    assert ukoly[0]["nazev"] == "Nakoupit mléko"
    assert ukoly[0]["popis"] == "Koupit dvě balení mléka"
    assert ukoly[0]["stav"] == "Nezahájeno"


def test_pridat_ukol_negativni(app_module, db_connection, monkeypatch, capsys):
    """Negativní test: ověří reakci na prázdný název úkolu."""
    vstupy = iter([
        "",                        # neplatný název
        "Dokončit report",         # druhý pokus - platný název
        "Dopsat závěrečnou část"   # platný popis
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(vstupy))

    app_module.pridat_ukol()

    vystup = capsys.readouterr().out

    assert "Název úkolu nesmí být prázdný" in vystup

    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ukoly")
    ukoly = cursor.fetchall()
    cursor.close()

    assert len(ukoly) == 1
    assert ukoly[0]["nazev"] == "Dokončit report"
    assert ukoly[0]["popis"] == "Dopsat závěrečnou část"
    assert ukoly[0]["stav"] == "Nezahájeno"


def test_aktualizovat_ukol_pozitivni(app_module, db_connection, monkeypatch, capsys):
    """Pozitivní test: ověří, že se stav existujícího úkolu správně změní."""

    # 1. Příprava testovacích dat - vložení úkolu přímo do DB
    cursor = db_connection.cursor()
    cursor.execute(
        """
        INSERT INTO ukoly (nazev, popis, stav)
        VALUES (%s, %s, %s)
        """,
        ("Test aktualizace", "Ověření změny stavu", "Nezahájeno")
    )
    db_connection.commit()
    id_ukolu = cursor.lastrowid
    cursor.close()

    # 2. Simulace vstupů uživatele:
    #    nejprve zadá ID úkolu, potom zvolí nový stav
    #    Pro stav "Nezahájeno" bude volba:
    #    1 = "Probíhá"
    #    2 = "Hotovo"
    vstupy = iter([
        str(id_ukolu),
        "1"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(vstupy))

    # 3. Zavolání testované funkce
    app_module.aktualizovat_ukol()

    # 4. Zachycení výstupu
    vystup = capsys.readouterr().out

    # 5. Ověření hlášky
    assert "Stav úkolu byl úspěšně změněn" in vystup

    # 6. Ověření změny v databázi
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ukoly WHERE id = %s", (id_ukolu,))
    ukol = cursor.fetchone()
    cursor.close()

    assert ukol is not None
    assert ukol["id"] == id_ukolu
    assert ukol["nazev"] == "Test aktualizace"
    assert ukol["stav"] == "Probíhá"


def test_aktualizovat_ukol_negativni(app_module, db_connection, monkeypatch, capsys):
    """Negativní test: ověří reakci na zadání neexistujícího ID úkolu."""

    # 1. Příprava testovacích dat - vložení jednoho existujícího úkolu
    cursor = db_connection.cursor()
    cursor.execute(
        """
        INSERT INTO ukoly (nazev, popis, stav)
        VALUES (%s, %s, %s)
        """,
        ("Test negativní aktualizace", "Kontrola neexistujícího ID", "Nezahájeno")
    )
    db_connection.commit()
    id_existujiciho_ukolu = cursor.lastrowid
    cursor.close()

    # 2. Simulace vstupů:
    #    - nejprve neexistující ID
    #    - potom 0 pro návrat do hlavního menu
    vstupy = iter([
        "9999",
        "0"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(vstupy))

    # 3. Zavolání testované funkce
    app_module.aktualizovat_ukol()

    # 4. Zachycení výstupu
    vystup = capsys.readouterr().out

    # 5. Ověření správné reakce programu
    assert "Úkol s takovým ID neexistuje" in vystup
    assert "Návrat do hlavního menu bez změny stavu úkolu." in vystup

    # 6. Ověření, že existující úkol zůstal beze změny
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ukoly WHERE id = %s", (id_existujiciho_ukolu,))
    ukol = cursor.fetchone()
    cursor.close()

    assert ukol is not None
    assert ukol["id"] == id_existujiciho_ukolu
    assert ukol["nazev"] == "Test negativní aktualizace"
    assert ukol["stav"] == "Nezahájeno"


def test_odstranit_ukol_pozitivni(app_module, db_connection, monkeypatch, capsys):
    """Pozitivní test: ověří, že se existující úkol správně odstraní."""

    # 1. Příprava testovacích dat
    cursor = db_connection.cursor()
    cursor.execute(
        """
        INSERT INTO ukoly (nazev, popis, stav)
        VALUES (%s, %s, %s)
        """,
        ("Test mazání", "Ověření odstranění úkolu", "Nezahájeno")
    )
    db_connection.commit()
    id_ukolu = cursor.lastrowid
    cursor.close()

    # 2. Simulace vstupů uživatele:
    #    - zadání ID úkolu
    #    - potvrzení mazání "a"
    vstupy = iter([
        str(id_ukolu),
        "a"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(vstupy))

    # 3. Zavolání testované funkce
    app_module.odstranit_ukol()

    # 4. Zachycení výstupu
    vystup = capsys.readouterr().out

    # 5. Ověření hlášky
    assert "byl trvale odstraněn z databáze" in vystup

    # 6. Ověření, že úkol už v databázi není
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ukoly WHERE id = %s", (id_ukolu,))
    ukol = cursor.fetchone()
    cursor.close()

    assert ukol is None


def test_odstranit_ukol_negativni(app_module, db_connection, monkeypatch, capsys):
    """Negativní test: ověří reakci na neplatné potvrzení mazání a zrušení akce."""

    # 1. Příprava testovacích dat
    cursor = db_connection.cursor()
    cursor.execute(
        """
        INSERT INTO ukoly (nazev, popis, stav)
        VALUES (%s, %s, %s)
        """,
        ("Test negativního mazání", "Kontrola neplatného potvrzení", "Nezahájeno")
    )
    db_connection.commit()
    id_ukolu = cursor.lastrowid
    cursor.close()

    # 2. Simulace vstupů:
    #    - zadání ID úkolu
    #    - neplatné potvrzení "x"
    #    - následně zrušení mazání "n"
    vstupy = iter([
        str(id_ukolu),
        "x",
        "n"
    ])

    monkeypatch.setattr("builtins.input", lambda _: next(vstupy))

    # 3. Zavolání testované funkce
    app_module.odstranit_ukol()

    # 4. Zachycení výstupu
    vystup = capsys.readouterr().out

    # 5. Ověření správné reakce programu
    assert "Neplatná volba. Zadejte prosím 'a' pro ano nebo 'n' pro ne." in vystup
    assert "Úkol nebyl odstraněn." in vystup

    # 6. Ověření, že úkol stále existuje
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM ukoly WHERE id = %s", (id_ukolu,))
    ukol = cursor.fetchone()
    cursor.close()

    assert ukol is not None
    assert ukol["id"] == id_ukolu
    assert ukol["nazev"] == "Test negativního mazání"
    assert ukol["stav"] == "Nezahájeno"
