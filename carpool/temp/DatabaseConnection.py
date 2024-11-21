import sqlite3

# Connect to SQLite database
conn = sqlite3.connect(r'D:\04_Hackothon\carpool_updated_new\carpool_updated\carpool_updated\carpool\db.sqlite3')
cursor = conn.cursor()

cursor.execute(f"PRAGMA table_info({'rider_ride'});")
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Execute SQL query to fetch all rows from a table
# cursor.execute("SELECT * FROM rider_ride")

# Fetch all rows
rows = cursor.fetchall()

# Print each row
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
