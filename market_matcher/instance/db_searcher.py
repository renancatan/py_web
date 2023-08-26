import sqlite3

conn = sqlite3.connect('market_matcher.db')
cursor = conn.cursor()

# Get table information
cursor.execute('PRAGMA table_info(product)')
columns = cursor.fetchall()

# Print column names and types
for column in columns:
    print(column[1], "-", column[2])

# Fetch and print rows
cursor.execute('SELECT * FROM product')
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close the connection
conn.close()
