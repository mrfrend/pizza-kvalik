import pymysql
import datetime
from pages.order_item_widget import OrderItem


class Database:
    def __init__(self) -> None:
        self.conn = pymysql.connect(
            host="localhost",
            password="",
            user="root",
            database="pizzeria_db",
            cursorclass=pymysql.cursors.DictCursor,
        )

    def cursor(self):
        return self.conn.cursor()

    def authorize(self, login: str, password: str):
        with self.cursor() as cur:
            cur.execute(
                "SELECT * FROM users WHERE username = %s AND password_hash = %s",
                [login, password],
            )
            result = cur.fetchone()
            return result

    def get_menu(self):
        with self.cursor() as cur:
            cur.execute("SELECT * FROM menu_items")
            return cur.fetchall()

    def create_order(
        self,
        user_id: int,
        items: list[OrderItem],
        order_date=datetime.datetime.now(),
        total_amount=0,
        status="Ожидает приготовления",
    ):
        with self.cursor() as cur:
            print(f"{user_id=}")
            create_order = """
                INSERT INTO orders(user_id) VALUES (%s)
            """
            cur.execute(create_order, [user_id])
            order_id = cur.lastrowid

            for item in items:
                item_id = item.product["item_id"]
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
            if order_total:
                cur.execute(update_order_total, [order_total["total"], order_id])

            self.conn.commit()

    def get_orders_of_user(self, user_id: int):
        with self.cursor() as cur:
            query = """
                SELECT order_id, total_amount, status
                FROM orders WHERE user_id = %s
            """
            cur.execute(query, [user_id])
            return cur.fetchall()

    def get_orders(self, status=None):
        with self.cursor() as cur:
            query = """
                SELECT order_id, order_date, total_amount, status
                FROM orders
                WHERE 1=1
            """
            params = []
            if status is not None:
                query += " AND status = %s"
                params.append(status)
            query += " ORDER BY order_id"
            cur.execute(query, params)
            return cur.fetchall()

    def get_order_composition(self, order_id: int):
        with self.cursor() as cur:
            query = """
                    SELECT CONCAT_WS(' ', name, 'x', quantity) as composition
                    FROM order_items
                    JOIN menu_items
                    ON order_items.item_id = menu_items.item_id
                    WHERE order_id = %s
                """
            cur.execute(query, [order_id])
            return cur.fetchall()

    def delete_menu_item(self, menu_item_id: int):
        with self.cursor() as cur:
            statement = """DELETE FROM menu_items WHERE item_id = %s"""
            cur.execute(statement, [menu_item_id])
            self.conn.commit()

    def get_categories(self):
        with self.cursor() as cur:
            query = "select DISTINCT category from menu_items"
            cur.execute(query)
            return cur.fetchall()

    def get_statuses(self):
        with self.cursor() as cur:
            query = "select DISTINCT status from orders"
            cur.execute(query)
            return cur.fetchall()

    def update_order_status(self, order_id: int, status: str):
        with self.cursor() as cur:
            statment = """
                UPDATE orders
                set status = %s
                where order_id = %s
            """
            cur.execute(statment, [status, order_id])
            self.conn.commit()

    def insert_menu_item(
        self, name: str, description: str, price: float, category: str, image_path: str
    ):
        with self.cursor() as cur:
            statement = "INSERT INTO menu_items(name, description, price, category, image) VALUES (%s, %s, %s , %s, %s)"
            cur.execute(statement, [name, description, price, category, image_path])
            self.conn.commit()

    def update_menu_item(
        self,
        menu_item_id: int,
        name: str,
        description: str,
        price: float,
        category: str,
        image_path: str,
    ):
        with self.cursor() as cur:
            statement = """
            UPDATE menu_items
            SET name = %s, 
            description = %s, 
            price = %s,  
            category = %s,
            image = %s
            WHERE item_id = %s
            """
            cur.execute(
                statement,
                [name, description, price, category, image_path, menu_item_id],
            )
            self.conn.commit()


dao = Database()
