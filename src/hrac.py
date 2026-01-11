class Hrac:
    def __init__(self,id, jmeno, prijmeni, cislo_dresu, pozice, klub_id):
        self.id = id
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.cislo_dresu = cislo_dresu
        self.pozice = pozice
        self.klub_id = klub_id

import csv
from database_connection import DatabaseConnection

conn = DatabaseConnection()
cursor = conn.connection.cursor()

class Hrac_Repository:

    def pridat(self, jmeno, prijmeni, cislo_dresu, pozice, klub_id):
        sql = f"INSERT INTO hrac (jmeno, prijmeni, cislo_dresu, pozice, klub_id) VALUES (%s, %s, %s, %s, %s)"
        values = (jmeno, prijmeni, cislo_dresu, pozice, klub_id)
        cursor.execute(sql, values)
        conn.connection.commit()

    def smazat(self, jmeno, prijmeni):
        sql = f"DELETE FROM hrac WHERE jmeno = %s AND prijmeni = %s "
        values = (jmeno, prijmeni)
        cursor.execute(sql, values)
        conn.connection.commit()

    def seznam_hracu(self):
        sql = "SELECT * FROM hraci_tymu"
        cursor.execute(sql)
        return cursor.fetchall()

    def import_z_csv(self, cesta_k_souboru):
        with open(cesta_k_souboru, "r", encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                self.pridat(row[0], row[1], row[2], row[3], row[4])
