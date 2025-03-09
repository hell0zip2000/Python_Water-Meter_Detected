from Config.databaseConnect import conn
from BUS.KhachHangBUS import KhachHangBUS

def test_database_connection():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM khachhang")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()

if __name__ == "__main__":  #test ground
    BUS = KhachHangBUS()
    lists = BUS.get_all()
    for user in lists:
        print(user)
    #testing the database function