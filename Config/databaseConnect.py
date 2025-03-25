import mysql.connector

# Connect to MySQL Database

def get_conn():
    conn = mysql.connector.connect(
        host="localhost",        # use 'localhost' for XAMPP
        user="root",             # Default XAMPP MySQL username
        password="",             # Default password
        database="water_management"        #remember to change name when using different database
    )
    
    # Check if connection was successful
    return conn