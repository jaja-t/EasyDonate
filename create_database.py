import sqlite3

conn = sqlite3.connect('donor.db')


c = conn.cursor()

c.execute("""CREATE TABLE donor (
            org text NOT NULL,
            email text,
            address text,
            object text NOT NULL,
            description text,
            quantity integer NOT NULL
            )""")


conn.commit() #important

conn.close()