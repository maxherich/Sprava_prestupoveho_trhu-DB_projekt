class Majitel:
    def __init__(self,id, jmeno, prijmeni, email, rozpocet, aktivni):
        self.id = id
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.email = email
        self.rozpocet = rozpocet
        self.aktivni = aktivni

import csv
from database_connection import DatabaseConnection

conn = DatabaseConnection()
cursor = conn.connection.cursor()

class Majitel_Repository:

    def pridat(self, jmeno, prijmeni, email, rozpocet, aktivni):
        sql = f"INSERT INTO majitel (jmeno, prijmeni, email, rozpocet, aktivni) VALUES (%s, %s, %s, %s, %s)"
        values = (jmeno, prijmeni, email, rozpocet, aktivni)
        cursor.execute(sql, values)
        conn.connection.commit()

    def smazat(self, jmeno, prijmeni):
        sql = f"DELETE FROM majitel WHERE jmeno = %s AND prijmeni = %s "
        values = (jmeno, prijmeni)
        cursor.execute(sql, values)
        conn.connection.commit()

    def vyhledat(self, jmeno, prijmeni):
        sql = f"SELECT * FROM majitel WHERE jmeno = %s AND prijmeni = %s "
        values = (jmeno, prijmeni)
        cursor.execute(sql, values)
        conn.connection.commit()
        return cursor.fetch()

    def aktivni_majitele(self):
        sql = f"SELECT * FROM seznam_aktivnich_majitelu"
        cursor.execute(sql)
        conn.connection.commit()
        return cursor.fetchall()

    def import_z_csv(self):
        with open("csv_data/majitel.csv", "r", encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                self.pridat(row[1], row[2], row[3], row[4], row[5])