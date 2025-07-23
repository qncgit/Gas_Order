# ==============================================================================
# File: GAS_ORDER/controller/main_controller.py
# ==============================================================================
from view.main_window import MainWindow

class MainController:
    """Controller cho cửa sổ chính của Admin/Thống kê."""
    def __init__(self, model, app_controller):
        self.model = model # SyncManager
        self.app_controller = app_controller
        self.view = None # Sẽ được tạo khi cần
        self.current_user = None

    def show_view(self, user_info):
        """Hiển thị cửa sổ chính."""
        self.current_user = user_info
        # Truyền vai trò của người dùng vào MainWindow để nó có thể hiển thị đúng các mục cài đặt
        self.view = MainWindow(self, self.current_user.get('role', 'Statistician'))
        self.view.show()

    def handle_logout(self):
        """Xử lý sự kiện nhấn nút Đăng xuất."""
        self.view.close()
        self.app_controller.show_login_window()