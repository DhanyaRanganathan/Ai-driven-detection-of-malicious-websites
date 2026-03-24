import sqlite3

# Connect to the database
conn = sqlite3.connect("app.db")  # or full path if needed
cursor = conn.cursor()
print("Connected successfully!")

# Example: fetch all users
cursor.execute("SELECT * FROM users;")
users = cursor.fetchall()
print("Users:", users)

# Example: fetch all history
cursor.execute("SELECT user, site, risk, date FROM history ORDER BY date DESC;")
history = cursor.fetchall()
print("History:", history)

# Close the connection
conn.close()
print("Connection closed!")