import sqlite3

conn = sqlite3.connect('rural.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
email TEXT,
password TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS feedback(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
email TEXT,
message TEXT
)
''')

conn.commit()
conn.close()

print("Database Created Successfully")