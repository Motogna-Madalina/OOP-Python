import mysql.connector

print("START")

conn = mysql.connector.connect(
    host="localhost",
    user="shopuser",
    password="Shop123!"
)

print("CONNECTED")

conn.close()

print("END")

