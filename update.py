import sqlite3

conn = sqlite3.connect("app.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE users ADD COLUMN name TEXT")
except:
    print("name column already exists")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN notifications INTEGER DEFAULT 1")
except:
    print("notifications column already exists")

try:
    cursor.execute("ALTER TABLE users ADD COLUMN dark_mode INTEGER DEFAULT 0")
except:
    print("dark_mode column already exists")

conn.commit()
conn.close()

print("Database updated successfully!")