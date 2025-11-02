# seznam všech úkolů
ukoly = []

# funkce hlavního menu
def hlavni_menu():
    while True:
        print("\nSprávce úkolů — Hlavní menu")
        print("1. Přidat nový úkol")
        print("2. Zobrazit všechny úkoly")
        print("3. Odstranit úkol")
        print("4. Konec programu")

        volba = input("Vyberte možnost (1–4): ").strip()

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
            odstranit_ukol()
        elif volba == 4:
            print("\nKonec programu.")
            break
        else:
            print("\nNeplatná volba. Zadejte číslo v rozmezí 1–4.")

# funkce pro přidání úkolu do seznamu úkolů
def pridat_ukol():
    # použití cyklu pro možnost opakovaného zadávání názvu a popisu úkolu.
    while True:
        # proměnná, do které se ukládá název úkolu zadaný uživatelem - nesmí být prázdný vstup.
        nazev_ukolu = input("\nZadejte název úkolu: ").strip()
        if not nazev_ukolu:
            print("\nNázev úkolu nesmí být prázdný. Zkuste to prosím znovu.")
            continue  # vrátí se na začátek cyklu a zeptá se znovu

        popis_ukolu = input("Zadejte popis úkolu: ").strip()
        if not popis_ukolu:
            print("\nPopis úkolu nesmí být prázdný. Zkuste to prosím znovu.")
            continue  # vrátí se na začátek cyklu a zeptá se znovu

        # Pokud jsou oba vstupy vyplněné, úkol se uloží
        ukol = {"nazev": nazev_ukolu, "popis": popis_ukolu}
        ukoly.append(ukol)
        print(f"\nÚkol '{nazev_ukolu}' byl úspěšně přidán.")
        break  # ukončí cyklus

# funkce pro zobrazení všech přidaných úkolů uživatelem
def zobrazit_ukoly():
    if not ukoly:
        print("\nSeznam úkolů je prázdný.")
        return
    print("\nSeznam úkolů:")
    for i, u in enumerate(ukoly, start=1):
        print(f"{i}. {u['nazev']} – {u['popis']}")
    print()

# funkce pro odebrání konkrétního úkolu zadáním čísla úkolu v seznamu
def odstranit_ukol():
    while True:
        # pokud je seznam prázdný, informuj uživatele a vrať se do hlavního menu
        if not ukoly:
            print("\nSeznam úkolů je prázdný. Není co mazat.")
            input("Stiskněte Enter pro návrat do hlavního menu...")
            return  # ← opustí funkci a vrátí se zpět do hlavního menu

        zobrazit_ukoly()
        vstup = input("Zadejte číslo úkolu, který chcete odstranit: ").strip()

        # ošetření pokud uživatel zadá prázdný vstup
        if not vstup:
            print("\nNezadali jste číslo úkolu, který si přejete smazat. Zkuste to prosím znovu.")
            continue
    
        # ošetření pokud uživatel zadá jiné znaky než číselné
        if not vstup.isdigit():
            print("\nNezadali jste celé kladné číslo. Zkuste to prosím znovu.")
            continue

        # uživatel vidí pořadí úkolu od "1.", ale indexy začínají v Pythonu od "0"
        index = int(vstup) - 1

        # podmínka pro zadání jiného vstupu než reálného čísla úkolu v seznamu
        if index < 0 or index >= len(ukoly):
            print("\nTakové číslo úkolu v seznamu není. Zkuste to prosím znovu.")
            continue

        # odebrání konkrétního úkolu ze sezmamu úkolů za pomocí indexu úkolu
        odebrany_ukol = ukoly.pop(index)
        print(f"\nÚkol '{odebrany_ukol['nazev']}' byl odstraněn.")
        break

if __name__ == "__main__":
    hlavni_menu()
