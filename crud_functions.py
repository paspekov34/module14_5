import sqlite3

def initiate_db():
  """Создает таблицы Products и Users, если они еще не созданы."""
  # Подключение к базе данных products.db
  conn_products = sqlite3.connect('products.db')
  cursor_products = conn_products.cursor()

  # Создание таблицы Products
  cursor_products.execute('''
  CREATE TABLE IF NOT EXISTS Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
  )
  ''')

  # Подключение к базе данных users.db
  conn_users = sqlite3.connect('users.db')
  cursor_users = conn_users.cursor()

  # Создание таблицы Users
  cursor_users.execute("""
  CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL,
    age INTEGER NOT NULL,
    balance INTEGER NOT NULL
  )
  """)

  # Добавление тестовых товаров в Products
  for i in range(1, 5):
    cursor_products.execute('INSERT INTO Products (title, description, price) VALUES (?,?,?)',
                (f'title{i}', f'description{i}', i * 100))

  # Сохранение изменений
  conn_products.commit()
  conn_users.commit()

  # Закрытие соединений
  conn_products.close()
  conn_users.close()

def add_user(username, email, age, db_path='users.db'):
  """Добавляет пользователя в таблицу Users."""
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, 1000)",
          (username, email, age))
  conn.commit()
  conn.close()

def is_included(username, db_path='users.db'):
  """Проверяет, существует ли пользователь в таблице Users."""
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()
  cursor.execute("SELECT 1 FROM Users WHERE username = ?", (username,))
  result = cursor.fetchone()
  conn.close()
  return bool(result)

def get_all_products():
  """Возвращает все записи из таблицы Products."""
  conn = sqlite3.connect('products.db')
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM Products")
  products = cursor.fetchall()
  conn.close()
  return products