# ==============================================================================
# File: GAS_ORDER/view/login_window.py
# ==============================================================================
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt
from qfluentwidgets.components import LineEdit, PasswordLineEdit, PrimaryPushButton, TitleLabel, SubtitleLabel
from qfluentwidgets.common import setFont

class LoginWindow(QWidget):
    """Giao diện cửa sổ đăng nhập."""
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Đăng nhập - Hệ thống Bán xăng")
        self.setFixedSize(400, 500)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = TitleLabel("GAS_ORDER", self)
        subtitle = SubtitleLabel("Vui lòng đăng nhập để tiếp tục", self)
        setFont(title, 36)
        
        layout.addStretch()
        layout.addWidget(title, 0, Qt.AlignCenter)
        layout.addWidget(subtitle, 0, Qt.AlignCenter)
        layout.addSpacing(40)

        self.username_input = LineEdit(self)
        self.username_input.setPlaceholderText("Tên đăng nhập")
        self.password_input = PasswordLineEdit(self)
        self.password_input.setPlaceholderText("Mật khẩu")
        self.login_button = PrimaryPushButton("Đăng nhập", self)

        layout.addWidget(QLabel("Dành cho Admin / Thống kê:"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addSpacing(30)

        self.rfid_label = SubtitleLabel("Hoặc quẹt thẻ để đăng nhập", self)
        self.rfid_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.rfid_label)
        layout.addStretch()

    def get_credentials(self):
        return {
            "username": self.username_input.text(),
            "password": self.password_input.text()
        }

    def clear_form(self):
        self.username_input.clear()
        self.password_input.clear()