# ==============================================================================
# File: GAS_ORDER/model/sync_manager.py
# ==============================================================================
import threading
import time
from PyQt5.QtCore import QObject, pyqtSignal
from .api_client import ApiClient
from .local_database import LocalDatabase
from .data_models import Transaction
from utils.helpers import generate_unique_id, get_current_timestamp
from config_items import cfg

class SyncManager(QObject):
    """
    Điều phối việc đồng bộ dữ liệu giữa CSDL cục bộ và server.
    """
    connection_status_changed = pyqtSignal(bool)
    sync_finished = pyqtSignal(str)

    def __init__(self, config):
        super().__init__()
        self.config, self.api_client, self.local_db = config, ApiClient(), LocalDatabase()
        self.is_running, self.sync_thread, self.is_online = False, None, False

    def start(self):
        self.is_running = True
        self.sync_thread = threading.Thread(target=self._sync_loop)
        self.sync_thread.daemon = True
        self.sync_thread.start()

    def stop(self):
        self.is_running = False

    def _sync_loop(self):
        print("Tiến trình đồng bộ đã bắt đầu.")
        while self.is_running:
            was_online, self.is_online = self.is_online, self.api_client.check_connection()
            if self.is_online != was_online: self.connection_status_changed.emit(self.is_online)
            
            if self.is_online:
                print("Đang online. Bắt đầu đồng bộ...")
                self._sync_up()
                self._sync_down()
                self.sync_finished.emit("Đồng bộ hoàn tất.")
            else:
                print("Đang offline. Bỏ qua chu kỳ đồng bộ.")
            
            time.sleep(self.config.SYNC_INTERVAL_SECONDS)

    def _sync_up(self):
        unsynced_txs = self.local_db.get_unsynced_transactions()
        if not unsynced_txs: return
        print(f"Phát hiện {len(unsynced_txs)} giao dịch cần đẩy lên...")
        for tx_data in unsynced_txs:
            if self.api_client.post_data("transactions", tx_data):
                self.local_db.mark_transaction_as_synced(tx_data['id'])
            else: 
                print(f"Lỗi khi đẩy giao dịch {tx_data['id']}. Sẽ thử lại sau.")
                break 

    def _sync_down(self):
        print("Đang tải dữ liệu nhân viên và người dùng từ server...")
        employees_data = self.api_client.get_data("employees")
        if employees_data is not None:
            employees_to_save = [(e['Id'], e['Name'], e.get('BirthDate'), e.get('Department'), e.get('Status', 'Active')) for e in employees_data]
            self.local_db.bulk_update_employees(employees_to_save)
        
        users_data = self.api_client.get_data("users")
        if users_data is not None:
            users_to_save = [(u['Id'], u['EmployeeId'], u.get('RfidCardId'), u.get('Username'), u.get('Role', 'Seller')) for u in users_data]
            self.local_db.bulk_update_users(users_to_save)

    def create_transaction(self, seller_id, buyer_id, tx_type, unit_price, quantity, total, payment):
        new_tx = Transaction(id=generate_unique_id(), timestamp=get_current_timestamp(), seller_employee_id=seller_id, buyer_employee_id=buyer_id, transaction_type=tx_type, unit_price=float(unit_price), quantity=float(quantity), total_amount=float(total), payment_method=payment)
        self.local_db.add_transaction(new_tx)
        return new_tx.__dict__

    def find_employee(self, short_id):
        return self.local_db.get_employee_by_short_id(short_id)
        
    def find_user_by_rfid(self, rfid):
        return self.local_db.get_user_by_rfid(rfid)

    def get_current_price(self):
        """Lấy giá xăng hiện tại từ config."""
        try:
            return float(cfg.get(cfg.don_gia_xang))
        except (ValueError, TypeError):
            return 25000.0 # Giá trị mặc định an toàn

    def get_print_settings(self):
        """Lấy cài đặt in từ config."""
        return {
            'in_phieu_tien_mat': cfg.get(cfg.in_phieu_tien_mat),
            'in_phieu_ghi_no': cfg.get(cfg.in_phieu_ghi_no),
        }