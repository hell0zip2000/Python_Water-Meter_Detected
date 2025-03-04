from Config.databaseConnect import conn

def test_database_connection():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM khachhang")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()

if __name__ == "__main__":
    test_database_connection()