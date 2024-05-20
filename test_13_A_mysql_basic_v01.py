#import mariadb
import mysql.connector
import sys

# Connect to MariaDB Platform
try:
    conn = mysql.connector.connect(
        user="dbuser",
        password="bankalore",
        host="localhost",
        port=3306,
        database="robotdb"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()
print ('Got cursor')
