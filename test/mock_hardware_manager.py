# ==============================================================================
# File: GAS_ORDER/test/mock_hardware_manager.py (PHIÊN BẢN GIẢ LẬP)
# ==============================================================================
import threading
import time
import random
from PyQt5.QtCore import QObject, pyqtSignal
from utils.helpers import format_currency

class MockHardwareManager(QObject):
    """
    Lớp giả lập phần cứng để phát triển và kiểm thử mà không cần thiết bị thật.
    """
    rfid_scanned = pyqtSignal(str)

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.rfid_thread = None
        self.is_running = False

    def start_rfid_listener(self):
        """Bắt đầu giả lập việc quẹt thẻ trong một thread riêng."""
        print("Bắt đầu giả lập lắng nghe RFID (chế độ test)...")
        self.is_running = True
        self.rfid_thread = threading.Thread(target=self._simulate_rfid_scan)
        self.rfid_thread.daemon = True
        self.rfid_thread.start()
        
    def _simulate_rfid_scan(self):
        """Hàm giả lập việc quẹt thẻ sau một khoảng thời gian ngẫu nhiên."""
        cards = ["RFID001", "RFID002", "RFID003", "INVALID_CARD"]
        while self.is_running:
            sleep_time = random.randint(8, 20)
            time.sleep(sleep_time)
            card_id = random.choice(cards)
            print(f"[GIẢ LẬP] Đã quẹt thẻ: {card_id}")
            self.rfid_scanned.emit(card_id)

    def stop_rfid_listener(self):
        """Dừng việc giả lập lắng nghe RFID."""
        self.is_running = False
        print("Đã dừng giả lập lắng nghe RFID.")

    def print_receipt(self, transaction_data):
        """Giả lập việc in hóa đơn bằng cách in ra console."""
        print("\n--- [HÓA ĐƠN GIẢ LẬP] ---")
        print(f"  Mã GD: {transaction_data.get('id')}")
        print(f"  Thời gian: {transaction_data.get('timestamp')}")
        print(f"  NV Mua: {transaction_data.get('buyer_name', 'N/A')}")
        print("  -------------------------")
        print(f"  Số lượng: {transaction_data.get('quantity')} L")
        print(f"  Đơn giá: {format_currency(transaction_data.get('unit_price'))}/L")
        print(f"  Tổng tiền: {format_currency(transaction_data.get('total_amount'))}")
        print(f"  Hình thức: {transaction_data.get('payment_method')}")
        print("--- [KẾT THÚC HÓA ĐƠN] ---\n")
        return True # Luôn thành công