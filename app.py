import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="sql.tokyohost.eu",
            user="hfdoga",
            password="O2wdnXzwSBJCk",
            database="backenddolgozat"
        )
        if connection.is_connected():
            print("Sikeres csatlakozás az adatbázishoz!")
            return connection
    except Error as e:
        print("Hiba történt a csatlakozás során:", e)
        return None

def list_data(connection):
    cursor = connection.cursor()

    print("\n--- Mérések adatai ---")
    query = """
        select meres.id, allapot.homerseklet, allapot.paratartalom, helyiseg.helyiseg, idopont.idopont
        from meres
        join allapot on meres.allapot_id = allapot.id
        join helyiseg on allapot.id = helyiseg.id
        join idopont on meres.idopont_id = idopont.id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Hőmérséklet: {row[1]}°C, Páratartalom: {row[2]}%, Helyiség: {row[3]}, Időpont: {row[4]}")
    cursor.close()

def add_data(connection):
    homerseklet = input("Add meg a hőmérséklet értékét: ")
    paratartalom = input("Add meg a páratartalom értékét: ")
    helyiseg = input("Add meg a helyiséget: ")
    idopont = input("Add meg az időpontot (YYYY-MM-DD HH:MM:SS): ")

    cursor = connection.cursor()

    try:
        cursor.execute("insert into allapot (homerseklet, paratartalom) values (%s, %s)", (homerseklet, paratartalom))
        allapot_id = cursor.lastrowid

        cursor.execute("insert into helyiseg (id, helyiseg) values (%s, %s)", (allapot_id, helyiseg))

        cursor.execute("insert into idopont (idopont) values (%s)", (idopont,))
        idopont_id = cursor.lastrowid

        cursor.execute("insert into meres (allapot_id, idopont_id) values (%s, %s)", (allapot_id, idopont_id))

        connection.commit()
        print("Adatok sikeresen hozzáadva.")
    except Error as e:
        print("Hiba történt az adatok hozzáadása során:", e)
        connection.rollback()
    finally:
        cursor.close()

def edit_data(connection):
    record_id = input("Add meg a módosítandó rekord ID-ját: ")
    new_paratartalom = input("Add meg az új hőmérséklet értéket: ")
    new_homerseklet = input("Add meg az új páratartalom értéket: ")
    new_helyiseg = input("Add meg az új helyiséget: ")
    new_idopont = input("Add meg az új időpontot (YYYY-MM-DD HH:MM:SS): ")

    cursor = connection.cursor()
    try:
        cursor.execute("update allapot set homerseklet = %s, paratartalom = %s where id = %s", (new_homerseklet, new_paratartalom, record_id))
        cursor.execute("update helyiseg set helyiseg = %s where id = %s", (new_helyiseg, record_id))
        cursor.execute("update idopont set idopont = %s where id = (select idopont_id from meres where allapot_id = %s)", (new_idopont, record_id))
        connection.commit()
        print("Rekord módosítva.")
    except Error as e:
        print("Hiba történt az adatok módosítása során:", e)
        connection.rollback()
    finally:
        cursor.close()

def delete_data(connection):
    record_id = input("Add meg a törlendő rekord ID-ját: ")

    cursor = connection.cursor()
    try:
        cursor.execute("delete from meres where allapot_id = %s", (record_id,))
        cursor.execute("delete from helyiseg where id = %s", (record_id,))
        cursor.execute("delete from allapot where id = %s", (record_id,))
        connection.commit()
        print("Rekord törölve.")
    except Error as e:
        print("Hiba történt a rekord törlése során:", e)
        connection.rollback()
    finally:
        cursor.close()

def main():
    connection = create_connection()
    if connection is None:
        return
    
    while True:
        print("\n1. Adatok kilistázása")
        print("2. Adatok hozzáadása")
        print("3. Adatok szerkesztése")
        print("4. Adatok törlése")
        print("5. Kilépés")
        
        choice = input("Válassz egy lehetőséget (1-5): ")

        if choice == '1':
            list_data(connection)
        elif choice == '2':
            add_data(connection)
        elif choice == '3':
            edit_data(connection)
        elif choice == '4':
            delete_data(connection)
        elif choice == '5':
            print("Kilépés...")
            break
        else:
            print("Érvénytelen választás, próbáld újra.")

    connection.close()

if __name__ == "__main__":
    main()
