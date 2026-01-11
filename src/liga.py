class Liga:
    def __init__(self,id, nazev, zeme, uroven):
        self.id = id
        self.nazev = nazev
        self.zeme = zeme
        self.uroven = uroven

import csv
from database_connection import DatabaseConnection

conn = DatabaseConnection()
cursor = conn.connection.cursor()

class LigaRepository:

    def pridat(self, nazev, zeme, uroven):
        sql = f"INSERT INTO liga (nazev, zeme, uroven) VALUES (%s, %s, %s)"
        values = (nazev, zeme, uroven)
        cursor.execute(sql, values,)
        conn.connection.commit()

    def smazat(self, nazev):
        sql = f"DELETE FROM liga WHERE nazev = %s"
        values = (nazev,)
        cursor.execute(sql, values,)
        conn.connection.commit()

    def seznam_lig(self):
        sql = f"SELECT * FROM liga"
        cursor.execute(sql)
        return cursor.fetchall()

    def import_z_csv(self, cesta_k_souboru):
        with open(cesta_k_souboru, "r", encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader, None)
            for row in reader:
                self.pridat(row[0], row[1], row[2])