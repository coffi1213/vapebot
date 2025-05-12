import sqlite3
from datetime import datetime
from config import DATABASE_PATH

conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
cur = conn.cursor()

# Инициализация таблиц
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    points INTEGER DEFAULT 0,
    ref_id INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT,
    price INTEGER,
    photo TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    date TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    product_id INTEGER,
    text TEXT,
    date TEXT,
)
""")

conn.commit()

# Пользователи
def add_user(user_id, ref_id=None):
    cur.execute("INSERT OR IGNORE INTO user (user_id, ref_id) VALUES (?, ?)", (user_id, ref_id))
    conn.commit()

def get_user_points(user_id):
    row = cur.execute("SELECT points FROM users WHERE user_id=?", (user_id,)).fetchone()
    return row[0] if row else 0

def set_user_points(user_id, points):
    cur.execute("UPDATE users SET points=? WHERE user_id=?", (points, user_id))
    conn.commit()

def get_all_users():
    return cur.execute("SELECT user_id, points FROM users").fetchall()

# Товары
def add_product(name, description, price, photo=None):
    cur.execute("INSERT INTO products (name, description, price, photo) VALUES (?, ?, ?, ?)", 
                (name, description, price, photo))
    conn.commit()

def get_all_products():
    return cur.execute("SELECT * FROM products").fetchall()

def get_product(product_id):
    return cur.execute("SELECT * FROM products WHERE id=?", (produst_id,)).fetchone()

# Корзина
def add_to_cart(user_id, product_id):
    cur.execute("INSERT INTO cart (user_id, product_id) VALUES (?, ?)", (user_id, product_id))
    conn.commit()

def get_cart(user_id):
    return cur.execute("SELECT p.id, p.name, p.price FROM cart c JOIN product_id = p.id WHERE c.user_id=?", (user_id,)).fetchall()

def clear_cart(user_id):
    cur.execute("DELETE FROM cart WHERE user_id=?", (user_id,))
    conn.commit()

# Заказы
def record_order(user_id, product_id):
    cur.execute("INSERT INTO orders (user_id, product_id, date) VALUES (?, ?, ?)",
                (user_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

def get_user_orders(user_id):
    return cur.execute("SELECT p.name, o.date FROM orders o JOIN products p ON o.product_id = p.id WHERE o.user_id=?", (user_id,)).fetchall()

def get_total_orders():
    return cur.execute("SELECT COUNT(*) FROM orders").fetchone()[0]

def get_top_products(limit=3):
    return cur.execute("""
        SELECT product_id, COUNT(*) as total FROM orders
        GROUP BY produst_id
        ORDER BY total DESC
        LIMIT ?
    """, (limit,)).fetchall()

# Отзывы 
def add_review(user_id, product_id, text):
    cur.execute("INSERT INTO reviews (user_id, product_id, text, date) VALUES (?, ?, ?, ?)",
                (user_id, product_id, text, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

def get_reviews(product_id):
    return cur.execute("SELECT text, date FROM reviews WHERE product_id=?", (product_id,)).fetchall()
    