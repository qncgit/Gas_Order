# ==============================================================================
# File: GAS_ORDER/controller/app_controller.py
# ==============================================================================
from PyQt5.QtWidgets import QApplication
from config import APP_CONFIG
from model.sync_manager import SyncManager
from view.login_window import LoginWindow
from .kiosk_controller import KioskController
from .main_controller import MainController
from utils.helpers import show_error_message

# --- Lựa chọn HardwareManager dựa trên cờ DEBUG_MODE ---
if APP_CONFIG.DEBUG_MODE:
    from test.mock_hardware_manager import MockHardwareManager as HardwareManager
    print("!!! CHÚ Ý: ỨNG DỤNG ĐANG CHẠY Ở CHẾ ĐỘ GIẢ LẬP PHẦN CỨNG (DEBUG MODE) !!!")
else:
    from model.hardware_manager import HardwareManager
    print("--- Ứng dụng đang chạy ở chế độ sản phẩm (Production Mode) ---")


class AppController:
    """
    Controller chính của ứng dụng.
    Quản lý các controller con và luồng chính (đăng nhập, điều hướng).
    """
    def __init__(self, config):
        self.config = config
        self.app = QApplication([])
        
        self.sync_manager = SyncManager(config)
        self.hardware_manager = HardwareManager(config)

        self.kiosk_controller = KioskController(self.sync_manager, self)
        self.main_controller = MainController(self.sync_manager, self)
        
        self.login_view = LoginWindow(self)
        
        self._connect_signals()
        
    def _connect_signals(self):
        """Kết nối các tín hiệu toàn cục."""
        self.login_view.login_button.clicked.connect(self.handle_login_with_password)
        self.hardware_manager.rfid_scanned.connect(self.handle_login_with_rfid)

    def run(self):
        """Bắt đầu ứng dụng."""
        self.show_login_window()
        self.sync_manager.start()
        self.hardware_manager.start_rfid_listener()
        
        exit_code = self.app.exec_()
        
        # Dọn dẹp trước khi thoát
        self.sync_manager.stop()
        self.hardware_manager.stop_rfid_listener()
        return exit_code

    def show_login_window(self):
        """Hiển thị cửa sổ đăng nhập."""
        self.login_view.clear_form()
        self.login_view.show()

    def handle_login_with_rfid(self, rfid_card_id):
        """Xử lý đăng nhập bằng thẻ RFID."""
        if not self.login_view.isVisible(): return
            
        user_info = self.sync_manager.find_user_by_rfid(rfid_card_id)
        if user_info:
            employee_info = self.sync_manager.find_employee(user_info['employee_id'][-4:])
            user_info['employee_name'] = employee_info.get('name', 'N/A') if employee_info else 'N/A'

            self.login_view.hide()
            self.kiosk_controller.show_view(user_info)
        else:
            show_error_message(self.login_view, "Lỗi", "Thẻ không hợp lệ hoặc chưa được đăng ký.")

    def handle_login_with_password(self):
        """Xử lý đăng nhập bằng tài khoản/mật khẩu."""
        credentials = self.login_view.get_credentials()
        username, password = credentials['username'], credentials['password']

        # TODO: Thay thế bằng logic xác thực API thật
        if username == "admin" and password == "admin":
            user_info = {'role': 'Admin', 'employee_name': 'Quản trị viên'}
            self.login_view.hide()
            self.main_controller.show_view(user_info)
        elif username == "thongke" and password == "thongke":
            user_info = {'role': 'Statistician', 'employee_name': 'Nhân viên Thống kê'}
            self.login_view.hide()
            self.main_controller.show_view(user_info)
        else:
            show_error_message(self.login_view, "Lỗi", "Tên đăng nhập hoặc mật khẩu không đúng.")