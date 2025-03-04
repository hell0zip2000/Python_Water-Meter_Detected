import mysql.connector

# Connect to MySQL Database
conn = mysql.connector.connect(
    host="localhost",        # use 'localhost' for XAMPP
    user="root",             # Default XAMPP MySQL username
    password="",             # Default password
    database="qlnuoc" #database name
)

# Check if connection was successful
if conn.is_connected():
    print("Connected to MySQL database!")

