# ==============================================================================
# File: GAS_ORDER/model/hardware_manager.py (PHIÊN BẢN SẢN PHẨM)
# ==============================================================================
import threading
from PyQt5.QtCore import QObject, pyqtSignal

# Bỏ comment các dòng import này khi triển khai thực tế
# import serial
# from escpos.printer import Usb

class HardwareManager(QObject):
    """
    Quản lý phần cứng THẬT.
    File này không chứa logic giả lập.
    """
    rfid_scanned = pyqtSignal(str)

    def __init__(self, config):
        super().__init__()
        self.config = config
        self.rfid_thread = None
        self.is_running = False
        # self.serial_port = None # Dùng cho pyserial

    def start_rfid_listener(self):
        """Bắt đầu lắng nghe tín hiệu từ cổng COM trong một thread riêng."""
        print("Khởi động trình lắng nghe RFID (chế độ sản phẩm)...")
        # --- CODE THỰC TẾ (BỎ COMMENT KHI DÙNG) ---
        # try:
        #     self.serial_port = serial.Serial(
        #         port=self.config.RFID_READER_CONFIG['port'],
        #         baudrate=self.config.RFID_READER_CONFIG['baudrate'],
        #         timeout=1
        #     )
        #     self.is_running = True
        #     self.rfid_thread = threading.Thread(target=self._listen_to_rfid_port)
        #     self.rfid_thread.daemon = True
        #     self.rfid_thread.start()
        # except serial.SerialException as e:
        #     print(f"LỖI: Không thể mở cổng COM '{self.config.RFID_READER_CONFIG['port']}'. Lỗi: {e}")

    def _listen_to_rfid_port(self):
        """Vòng lặp đọc dữ liệu từ cổng serial."""
        # --- CODE THỰC TẾ (BỎ COMMENT KHI DÙNG) ---
        # print("Đang lắng nghe trên cổng " + self.config.RFID_READER_CONFIG['port'])
        # while self.is_running and self.serial_port.is_open:
        #     try:
        #         line = self.serial_port.readline().decode('utf-8').strip()
        #         if line:
        #             print(f"Dữ liệu RFID nhận được: {line}")
        #             self.rfid_scanned.emit(line)
        #     except Exception as e:
        #         print(f"Lỗi khi đọc từ cổng serial: {e}")
        #         break
        # print("Đã dừng lắng nghe cổng serial.")
        pass

    def stop_rfid_listener(self):
        """Dừng việc lắng nghe RFID."""
        self.is_running = False
        # --- CODE THỰC TẾ (BỎ COMMENT KHI DÙNG) ---
        # if self.serial_port and self.serial_port.is_open:
        #     self.serial_port.close()
        print("Đã dừng trình lắng nghe RFID (chế độ sản phẩm).")

    def print_receipt(self, transaction_data):
        """In hóa đơn ra máy in nhiệt thật."""
        print(f"[IN HÓA ĐƠN] Đang in cho giao dịch: {transaction_data['id']}")
        # --- CODE THỰC TẾ (BỎ COMMENT KHI DÙNG) ---
        # try:
        #     p = Usb(self.config.PRINTER_CONFIG['vendor_id'], 
        #             self.config.PRINTER_CONFIG['product_id'], 
        #             profile=self.config.PRINTER_CONFIG['profile'])
        #     p.set(align='center', text_type='B')
        #     p.text("HOA DON BAN XANG\n")
        #     # ... (thêm các dòng in khác) ...
        #     p.cut()
        #     return True
        # except Exception as e:
        #     print(f"Lỗi khi in hóa đơn: {e}")
        #     return str(e)
        return "Chức năng in thật chưa được kích hoạt."