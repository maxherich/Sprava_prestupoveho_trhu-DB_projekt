class Hrac:
    def __init__(self,id, jmeno, prijmeni, cislo_dresu, pozice, klub_id):
        self.id = id
        self.jmeno = jmeno
        self.prijmeni = prijmeni
        self.cislo_dresu = cislo_dresu
        self.pozice = pozice
        self.klub_id = klub_id

from database_connection import DatabaseConnection

conn = DatabaseConnection()
cursor = conn.connection.cursor()

class Hrac_Repository:

    def import_z_csv(self):
        sql = f"LOAD DATA LOCAL INFILE 'csv_data/hrac.csv' INTO TABLE hrac FIELDS TERMINATED BY ',' IGNORE 1 ROWS;"
        cursor.execute(sql)
        conn.connection.commit()

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

    def vyhledat(self, jmeno, prijmeni):
        sql = f"SELECT * FROM hrac WHERE jmeno = %s AND prijmeni = %s "
        values = (jmeno, prijmeni)
        cursor.execute(sql, values)
        conn.connection.commit()
        return cursor.fetch()