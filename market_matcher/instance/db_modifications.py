import sqlite3

conn = sqlite3.connect('market_matcher.db')
cursor = conn.cursor()

# Drop the existing table
cursor.execute('DROP TABLE IF EXISTS product')

# Create the new table with desired columns
cursor.execute('''
    CREATE TABLE product (
        id INTEGER PRIMARY KEY,
        product_name TEXT NOT NULL,
        brand TEXT,
        market TEXT NOT NULL,
        price REAL NOT NULL,
        category TEXT,
        market_group TEXT
    )
''')

conn.commit()
conn.close()