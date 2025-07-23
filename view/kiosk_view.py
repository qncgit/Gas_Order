# ==============================================================================
# File: GAS_ORDER/view/kiosk_view.py
# ==============================================================================
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
from qfluentwidgets.components import (LineEdit, PrimaryPushButton, TitleLabel, 
                                       SubtitleLabel, CardWidget, PushButton)
from qfluentwidgets.common import setFont, FluentIcon

class KioskWindow(QWidget):
    """Giao diện chính cho nhân viên bán xăng."""
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Kiosk Bán xăng")
        self.setGeometry(100, 100, 800, 600)
        main_layout = QHBoxLayout(self)

        left_panel = CardWidget(self)
        left_layout = QVBoxLayout(left_panel)
        
        title = TitleLabel("Giao dịch mới", self)
        left_layout.addWidget(title)
        
        search_layout = QHBoxLayout()
        self.employee_search_input = LineEdit(self)
        self.employee_search_input.setPlaceholderText("Nhập 4 số cuối mã NV...")
        self.search_button = PrimaryPushButton("Tìm", self)
        search_layout.addWidget(self.employee_search_input)
        search_layout.addWidget(self.search_button)
        left_layout.addLayout(search_layout)

        self.buyer_info_card = CardWidget(self)
        self.buyer_info_card.setVisible(False)
        buyer_layout = QVBoxLayout(self.buyer_info_card)
        self.buyer_name_label = QLabel("Tên: ", self)
        self.buyer_dept_label = QLabel("Phòng ban: ", self)
        buyer_layout.addWidget(self.buyer_name_label)
        buyer_layout.addWidget(self.buyer_dept_label)
        left_layout.addWidget(self.buyer_info_card)

        type_layout = QHBoxLayout()
        self.type_money_button = QPushButton("Theo Tiền", self)
        self.type_liter_button = QPushButton("Theo Lít", self)
        self.type_money_button.setCheckable(True)
        self.type_liter_button.setCheckable(True)
        self.type_liter_button.setChecked(True)
        type_layout.addWidget(self.type_money_button)
        type_layout.addWidget(self.type_liter_button)
        left_layout.addLayout(type_layout)

        self.quantity_input = LineEdit(self)
        self.quantity_input.setPlaceholderText("Nhập số lít...")
        left_layout.addWidget(self.quantity_input)

        suggestion_layout = QGridLayout()
        self.suggestion_buttons = []
        suggestions = ["50000", "100000", "200000", "Đầy bình"]
        for i, text in enumerate(suggestions):
            btn = QPushButton(text, self)
            self.suggestion_buttons.append(btn)
            suggestion_layout.addWidget(btn, i // 2, i % 2)
        left_layout.addLayout(suggestion_layout)

        self.complete_button = PrimaryPushButton("Hoàn thành", self)
        setFont(self.complete_button, 18)
        left_layout.addWidget(self.complete_button)
        
        left_layout.addStretch()
        main_layout.addWidget(left_panel, 1)

        right_panel = QVBoxLayout()
        
        seller_card = CardWidget(self)
        seller_layout = QVBoxLayout(seller_card)
        self.seller_name_label = SubtitleLabel("NV Bán: ", self)
        self.connection_status_label = QLabel("Trạng thái: ", self)
        seller_layout.addWidget(self.seller_name_label)
        seller_layout.addWidget(self.connection_status_label)
        right_panel.addWidget(seller_card)

        info_card = CardWidget(self)
        info_layout = QVBoxLayout(info_card)
        self.current_price_label = QLabel("Đơn giá: ", self)
        self.total_amount_label = TitleLabel("Tổng tiền: 0 VNĐ", self)
        info_layout.addWidget(self.current_price_label)
        info_layout.addWidget(self.total_amount_label)
        right_panel.addWidget(info_card)
        
        right_panel.addStretch()

        self.settings_button = PushButton(text=" Cài đặt", parent=self, icon=FluentIcon.SETTING)
        self.history_button = PushButton(text=" Lịch sử", parent=self, icon=FluentIcon.HISTORY)
        self.logout_button = PushButton(text=" Đăng xuất", parent=self, icon=FluentIcon.POWER)
        right_panel.addWidget(self.settings_button)
        right_panel.addWidget(self.history_button)
        right_panel.addWidget(self.logout_button)
        
        main_layout.addLayout(right_panel, 1)
        
    def update_buyer_info(self, employee_data):
        if employee_data:
            self.buyer_name_label.setText(f"<b>Tên:</b> {employee_data['name']}")
            self.buyer_dept_label.setText(f"<b>Phòng ban:</b> {employee_data['department']}")
            self.buyer_info_card.setVisible(True)
        else:
            self.buyer_info_card.setVisible(False)
            
    def update_seller_info(self, seller_name):
        self.seller_name_label.setText(f"NV Bán: <b>{seller_name}</b>")
        
    def update_connection_status(self, is_online):
        text = "Online" if is_online else "Offline"
        color = "green" if is_online else "red"
        self.connection_status_label.setText(f"Trạng thái: <b style='color:{color};'>{text}</b>")

    def reset_transaction_form(self):
        self.employee_search_input.clear()
        self.quantity_input.clear()
        self.buyer_info_card.setVisible(False)
        self.total_amount_label.setText("Tổng tiền: 0 VNĐ")