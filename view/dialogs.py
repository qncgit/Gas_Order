# ==============================================================================
# File: GAS_ORDER/view/dialogs.py
# ==============================================================================
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QPushButton, QRadioButton, QButtonGroup, QLabel, QCheckBox, QDialogButtonBox, QFormLayout
from qfluentwidgets.components import PrimaryPushButton, LineEdit, SwitchButton
from config_items import cfg

class PaymentDialog(QDialog):
    """Hộp thoại chọn hình thức thanh toán."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chọn hình thức thanh toán")
        self.layout = QVBoxLayout(self)
        
        self.label = QLabel("Vui lòng chọn hình thức thanh toán:", self)
        self.layout.addWidget(self.label)

        self.radio_cash = QRadioButton("Tiền mặt", self)
        self.radio_debt = QRadioButton("Ghi nợ", self)
        self.radio_cash.setChecked(True)

        self.button_group = QButtonGroup(self)
        self.button_group.addButton(self.radio_cash)
        self.button_group.addButton(self.radio_debt)

        self.layout.addWidget(self.radio_cash)
        self.layout.addWidget(self.radio_debt)

        self.ok_button = PrimaryPushButton("Xác nhận", self)
        self.ok_button.clicked.connect(self.accept)
        self.layout.addWidget(self.ok_button)

        self.selected_method = "Tiền mặt"

    def accept(self):
        self.selected_method = "Tiền mặt" if self.radio_cash.isChecked() else "Ghi nợ"
        super().accept()

class SettingsDialog(QDialog):
    """Hộp thoại cài đặt ứng dụng cho Kiosk, sử dụng QConfig."""
    def __init__(self, is_admin=False, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cài đặt Nhanh")
        self.is_admin = is_admin
        
        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        # Đơn giá xăng
        self.price_edit = LineEdit(self)
        self.price_edit.setText(cfg.get(cfg.don_gia_xang))
        self.form_layout.addRow("Đơn giá xăng:", self.price_edit)

        # In phiếu tiền mặt
        self.cash_receipt_switch = SwitchButton("Tiền mặt", self)
        self.cash_receipt_switch.setChecked(cfg.get(cfg.in_phieu_tien_mat))
        self.form_layout.addRow("Cho phép in phiếu:", self.cash_receipt_switch)
        
        # In phiếu ghi nợ
        self.debt_receipt_switch = SwitchButton("Ghi nợ", self)
        self.debt_receipt_switch.setChecked(cfg.get(cfg.in_phieu_ghi_no))
        self.form_layout.addRow("", self.debt_receipt_switch)

        self.layout.addLayout(self.form_layout)

        # Nút bấm
        self.button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def accept(self):
        """Lưu các thay đổi vào config."""
        cfg.set(cfg.don_gia_xang, self.price_edit.text())
        cfg.set(cfg.in_phieu_tien_mat, self.cash_receipt_switch.isChecked())
        cfg.set(cfg.in_phieu_ghi_no, self.debt_receipt_switch.isChecked())
        super().accept()