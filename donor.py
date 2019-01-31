import sqlite3

conn = sqlite3.connect('donor.db')

c = conn.cursor()

c.execute("""CREATE TABLE donors(
			user_id integer,
			first_name text,
            last_name text,
			object text,
			quantity integer,
			image text
			)""")

c.execute("INSERT INTO donor")

conn.commit()
conn.close()
