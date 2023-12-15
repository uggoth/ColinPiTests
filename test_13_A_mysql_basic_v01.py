import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="dbuser",
        password="Bankal0re*",
        host="localhost",
        port=3306,
        database="robotdb"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
