import pymysql

try:
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="Motogna6624.",
        database="shop_warenwelt"
    )
    print("Verbindung erfolgreich!")
    conn.close()
except pymysql.Error as err:
    print(f"Fehler: {err}")