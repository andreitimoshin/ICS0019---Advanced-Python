import csv
import sqlite3

conn = sqlite3.connect('DINERS.db')
c = conn.cursor()


c.execute("""CREATE TABLE IF NOT EXISTS CANTEEN (
             ID INTEGER PRIMARY KEY,
             Name TEXT NOT NULL,
             Location  TEXT NOT NULL,
             time_open TEXT NOT NULL,
             time_closed TEXT NOT NULL
             )""")

csv_file = 'Canteens.csv'


with open(csv_file, 'r', encoding="UTF-8") as scvFile:
    reader = csv.reader(scvFile, delimiter=';')
    next(reader)
    for row in reader:
        time_open, time_closed = row[3].split('-')
        c.execute("INSERT INTO CANTEEN (Name, Location, time_open, time_closed) VALUES (?, ?, ?, ?)", (row[0], row[1], time_open.strip(), time_closed.strip()))

conn.commit()
conn.close()

print('Success!')
