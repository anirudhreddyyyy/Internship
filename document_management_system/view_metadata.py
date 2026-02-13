import sqlite3

# Connect to database
conn = sqlite3.connect("instance/documents.db")
cursor = conn.cursor()

# Show all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

print("\nMetadata Rows:\n")

# Fetch metadata
cursor.execute("SELECT id, filename, category FROM document;")

rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
