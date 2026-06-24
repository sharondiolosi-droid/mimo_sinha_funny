import os
import sqlite3
from datetime import datetime, timedelta
import json

# Detecta se está no Railway (com DATABASE_URL)
DATABASE_URL = os.environ.get('DATABASE_URL')

class Database:
    def __init__(self):
        self.is_postgres = False
        if DATABASE_URL:
            try:
                import psycopg2
                self.conn = psycopg2.connect(DATABASE_URL)
                self.cursor = self.conn.cursor()
                self.is_postgres = True
                print("✅ Conectado ao PostgreSQL no Railway")
            except Exception as e:
                print(f"⚠️ Erro no PostgreSQL: {e}. Usando SQLite.")
                self._connect_sqlite()
        else:
            self._connect_sqlite()
        
        self.create_tables()

    def _connect_sqlite(self):
        self.conn = sqlite3.connect('mimo_sinha.db')
        self.cursor = self.conn.cursor()
        print("✅ Conectado ao SQLite (local)")

    # ... (mantenha o resto dos seus métodos, mas adapte para PostgreSQL se necessário)


import sqlite3
from datetime import datetime, timedelta
import json

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('mimo_sinha.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Users table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                last_name TEXT,
                subscription TEXT,
                subscription_end DATE,
                created_at DATE,
                is_admin INTEGER DEFAULT 0
            )
        ''')

        # Subscriptions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                plan TEXT,
                package TEXT,
                payment_id TEXT,
                status TEXT,
                amount REAL,
                created_at DATE,
                expires_at DATE,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')

        # Models table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS models (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                category TEXT,
                description TEXT,
                price REAL,
                is_active INTEGER DEFAULT 1
            )
        ''')

        # Promotions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS promotions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                discount_percent INTEGER,
                code TEXT,
                valid_until DATE,
                is_active INTEGER DEFAULT 1
            )
        ''')

        # Content table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS content (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT,
                title TEXT,
                description TEXT,
                file_id TEXT,
                content_type TEXT,
                created_at DATE,
                is_active INTEGER DEFAULT 1
            )
        ''')

        # Payments table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                transaction_id TEXT,
                amount REAL,
                method TEXT,
                status TEXT,
                created_at DATE,
                FOREIGN KEY(user_id) REFERENCES users(user_id)
            )
        ''')

        self.conn.commit()

    # User methods
    def add_user(self, user_id, username, first_name, last_name):
        try:
            self.cursor.execute('''
                INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, created_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, username, first_name, last_name, datetime.now().date()))
            self.conn.commit()
            return True
        except:
            return False

    def get_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        return self.cursor.fetchone()

    def update_subscription(self, user_id, plan, days=30):
        end_date = datetime.now().date() + timedelta(days=days)
        self.cursor.execute('''
            UPDATE users SET subscription = ?, subscription_end = ?
            WHERE user_id = ?
        ''', (plan, end_date, user_id))
        self.conn.commit()

    def check_subscription(self, user_id):
        self.cursor.execute('''
            SELECT subscription_end FROM users WHERE user_id = ?
        ''', (user_id,))
        result = self.cursor.fetchone()
        if result and result[0]:
            end_date = datetime.strptime(result[0], '%Y-%m-%d').date()
            return end_date > datetime.now().date()
        return False

    # Model methods
    def add_model(self, name, category, description, price):
        self.cursor.execute('''
            INSERT INTO models (name, category, description, price)
            VALUES (?, ?, ?, ?)
        ''', (name, category, description, price))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_models(self, category=None):
        if category:
            self.cursor.execute('SELECT * FROM models WHERE category = ? AND is_active = 1', (category,))
        else:
            self.cursor.execute('SELECT * FROM models WHERE is_active = 1')
        return self.cursor.fetchall()

    def delete_model(self, model_id):
        self.cursor.execute('UPDATE models SET is_active = 0 WHERE id = ?', (model_id,))
        self.conn.commit()

    # Content methods
    def add_content(self, category, title, description, file_id, content_type):
        self.cursor.execute('''
            INSERT INTO content (category, title, description, file_id, content_type, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (category, title, description, file_id, content_type, datetime.now().date()))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_content(self, category=None):
        if category:
            self.cursor.execute('SELECT * FROM content WHERE category = ? AND is_active = 1', (category,))
        else:
            self.cursor.execute('SELECT * FROM content WHERE is_active = 1')
        return self.cursor.fetchall()

    # Promotion methods
    def add_promotion(self, title, description, discount, code, valid_until):
        self.cursor.execute('''
            INSERT INTO promotions (title, description, discount_percent, code, valid_until)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, description, discount, code, valid_until))
        self.conn.commit()
        return self.cursor.lastrowid

    def validate_promo(self, code):
        self.cursor.execute('''
            SELECT * FROM promotions WHERE code = ? AND is_active = 1
            AND valid_until >= date('now')
        ''', (code,))
        return self.cursor.fetchone()

    def __del__(self):
        self.conn.close()