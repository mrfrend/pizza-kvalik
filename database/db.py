import pymysql

class Database:
    def __init__(self) -> None:
        self.conn = pymysql.connect(host="localhost", password='pass1', user='root', database='pizzeria_db',cursorclass=pymysql.cursors.DictCursor)
    
    def cursor(self):
        return self.conn.cursor()

    def authorize(self, login: str, password: str):
        with self.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE username = %s AND password_hash = %s", [login, password])
            result = cur.fetchone()
            return result

    def get_menu(self):
        with self.cursor() as cur:
            cur.execute("SELECT * FROM menu_items")
            return cur.fetchall()


dao = Database()

