import  mysql.connector as mariadb
import sys
from pprint import pprint

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
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
print (mariadb.__version__)
sql = ("SELECT * FROM serial_nos")
result = cur.execute(sql)
print (result)
rows = result.fetchall()
pprint (rows)
cur.close()
conn.close()
