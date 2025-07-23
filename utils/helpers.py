# ==============================================================================
# File: GAS_ORDER/utils/helpers.py
# ==============================================================================
import uuid
from datetime import datetime

def generate_unique_id():
    """Tạo ra một mã định danh duy nhất toàn cầu (UUID)."""
    return str(uuid.uuid4())

def get_current_timestamp():
    """Lấy thời gian hiện tại dưới dạng chuỗi ISO 8601."""
    return datetime.now().isoformat()

def format_currency(value):
    """Định dạng số thành chuỗi tiền tệ VNĐ."""
    try:
        return "{:,.0f} VNĐ".format(float(value))
    except (ValueError, TypeError):
        return "0 VNĐ"

def show_info_message(parent, title, content):
    """Hiển thị hộp thoại thông báo thông tin."""
    from PyQt5.QtWidgets import QMessageBox
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Information)
    msg_box.setText(content)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()

def show_error_message(parent, title, content):
    """Hiển thị hộp thoại thông báo lỗi."""
    from PyQt5.QtWidgets import QMessageBox
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Critical)
    msg_box.setText(content)
    msg_box.setWindowTitle(title)
    msg_box.setStandardButtons(QMessageBox.Ok)
    msg_box.exec_()