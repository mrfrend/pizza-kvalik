import pymysql
import datetime
from pages.order_item_widget import OrderItem
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
    
    def create_order(self, user_id: int, items: list[OrderItem], order_date=datetime.datetime.now(), total_amount=0, status="Ожидает приготовления"):
        with self.cursor() as cur:
            print(f"{user_id=}")
            create_order = """
                INSERT INTO orders(user_id) VALUES (%s)
            """
            cur.execute(create_order, [user_id])
            order_id = cur.lastrowid

            for item in items:
                item_id = item.product['item_id']
                quantity = item.count

                insert_order_item = """
                    INSERT INTO order_items(order_id, item_id, quantity)
                    VALUES (%s, %s, %s)
                """
                cur.execute(insert_order_item, [order_id, item_id, quantity])
            
            cur.execute("SELECT get_order_sum(%s) as total", [order_id])
            order_total = cur.fetchone()
            print(order_total)

            update_order_total = """
                UPDATE orders
                SET total_amount = %s
                WHERE order_id = %s
            """

            cur.execute(update_order_total, [order_total['total'], order_id])

            self.conn.commit()









dao = Database()

