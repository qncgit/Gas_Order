# ==============================================================================
# File: GAS_ORDER/model/local_database.py
# ==============================================================================
import sqlite3
from config import APP_CONFIG
from .data_models import Transaction

class LocalDatabase:
    """
    Quản lý cơ sở dữ liệu SQLite cục bộ.
    Lưu trữ dữ liệu để hoạt động offline.
    """
    def __init__(self):
        # check_same_thread=False là cần thiết khi CSDL được truy cập từ nhiều thread (SyncManager)
        self.conn = sqlite3.connect(APP_CONFIG.DATABASE_PATH, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Tạo các bảng nếu chúng chưa tồn tại."""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS employees (id TEXT PRIMARY KEY, name TEXT NOT NULL, birth_date TEXT, department TEXT, status TEXT)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (id TEXT PRIMARY KEY, employee_id TEXT NOT NULL, rfid_card_id TEXT, username TEXT, role TEXT NOT NULL)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS transactions (id TEXT PRIMARY KEY, timestamp TEXT NOT NULL, seller_employee_id TEXT NOT NULL, buyer_employee_id TEXT NOT NULL, transaction_type TEXT NOT NULL, unit_price REAL NOT NULL, quantity REAL NOT NULL, total_amount REAL NOT NULL, payment_method TEXT NOT NULL, is_synced INTEGER DEFAULT 0)")
        # Bảng settings không còn được sử dụng, nhưng giữ lại để không làm hỏng CSDL cũ
        self.cursor.execute("CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)")
        self.conn.commit()

    def add_transaction(self, tx: Transaction):
        self.cursor.execute("INSERT INTO transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (tx.id, tx.timestamp, tx.seller_employee_id, tx.buyer_employee_id, tx.transaction_type, tx.unit_price, tx.quantity, tx.total_amount, tx.payment_method, tx.is_synced))
        self.conn.commit()

    def get_employee_by_short_id(self, short_id: str):
        self.cursor.execute("SELECT * FROM employees WHERE id LIKE ?", ('%' + short_id,))
        row = self.cursor.fetchone()
        return {'id': row[0], 'name': row[1], 'birth_date': row[2], 'department': row[3]} if row else None

    def get_user_by_rfid(self, rfid: str):
        self.cursor.execute("SELECT * FROM users WHERE rfid_card_id=?", (rfid,))
        row = self.cursor.fetchone()
        return {'id': row[0], 'employee_id': row[1], 'role': row[4]} if row else None

    def get_unsynced_transactions(self):
        self.cursor.execute("SELECT * FROM transactions WHERE is_synced = 0")
        rows = self.cursor.fetchall()
        transactions = [{"id": r[0], "timestamp": r[1], "seller_employee_id": r[2], "buyer_employee_id": r[3], "transaction_type": r[4], "unit_price": r[5], "quantity": r[6], "total_amount": r[7], "payment_method": r[8]} for r in rows]
        return transactions

    def mark_transaction_as_synced(self, tx_id: str):
        self.cursor.execute("UPDATE transactions SET is_synced = 1 WHERE id = ?", (tx_id,))
        self.conn.commit()

    def bulk_update_employees(self, employees: list):
        self.cursor.execute("DELETE FROM employees")
        self.cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?)", employees)
        self.conn.commit()
    
    def bulk_update_users(self, users: list):
        self.cursor.execute("DELETE FROM users")
        self.cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?)", users)
        self.conn.commit()

    def close(self):
        self.conn.close()