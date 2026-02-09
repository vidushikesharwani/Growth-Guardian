import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

print("\n📋 CHILDREN TABLE:")
for row in cursor.execute("SELECT * FROM children"):
    print(row)

print("\n📋 MILESTONES TABLE:")
for row in cursor.execute("SELECT * FROM milestones"):
    print(row)

conn.close()
