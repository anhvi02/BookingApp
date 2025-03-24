import sqlite3
# Path to SQLite database
db_path = 'bookings.db'

# Connect to SQLite database (it will create the database if it doesn't exist)
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Create the table (if not already created)
# cur.execute('''
#     CREATE TABLE IF NOT EXISTS bookings (
#         name TEXT NOT NULL,
#         numberofpeople INTEGER NOT NULL, 
#         phone TEXT NOT NULL,
#         time TEXT NOT NULL,
#         service TEXT NOT NULL
#     )
# ''')

cur.execute('DELETE FROM bookings;')
conn.commit()

conn.close()