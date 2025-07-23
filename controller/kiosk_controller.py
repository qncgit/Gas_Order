# ==============================================================================
# File: GAS_ORDER/controller/kiosk_controller.py
# ==============================================================================
from view.kiosk_view import KioskWindow
from view.dialogs import PaymentDialog, SettingsDialog
from utils.helpers import show_error_message, show_info_message, format_currency

class KioskController:
    def __init__(self, model, app_controller):
        self.model = model
        self.app_controller = app_controller
        self.view = KioskWindow(self)
        
        self.current_seller = None
        self.current_buyer = None
        self.current_transaction_type = 'Lít'
        
        self._connect_signals()

    def _connect_signals(self):
        self.view.search_button.clicked.connect(self.find_employee)
        self.view.complete_button.clicked.connect(self.process_transaction)
        self.view.logout_button.clicked.connect(self.logout)
        self.view.settings_button.clicked.connect(self.show_settings)
        self.view.type_liter_button.clicked.connect(lambda: self.set_transaction_type('Lít'))
        self.view.type_money_button.clicked.connect(lambda: self.set_transaction_type('Tiền'))
        self.model.connection_status_changed.connect(self.view.update_connection_status)

    def show_view(self, user_info):
        self.current_seller = user_info
        self.view.update_seller_info(user_info.get('employee_name', 'Chưa rõ'))
        self.view.update_connection_status(self.model.is_online)
        self.view.current_price_label.setText(f"Đơn giá: {format_currency(self.model.get_current_price())}")
        self.view.showMaximized()

    def find_employee(self):
        short_id = self.view.employee_search_input.text()
        if not short_id or len(short_id) != 4:
            show_error_message(self.view, "Lỗi", "Vui lòng nhập đúng 4 số cuối mã nhân viên.")
            return
        employee_data = self.model.find_employee(short_id)
        self.current_buyer = employee_data
        self.view.update_buyer_info(employee_data)
        if not employee_data:
            show_info_message(self.view, "Thông báo", "Không tìm thấy nhân viên.")

    def set_transaction_type(self, tx_type):
        self.current_transaction_type = tx_type
        is_liter = tx_type == 'Lít'
        self.view.type_liter_button.setChecked(is_liter)
        self.view.type_money_button.setChecked(not is_liter)
        self.view.quantity_input.setPlaceholderText("Nhập số lít..." if is_liter else "Nhập số tiền (VNĐ)...")
    
    def process_transaction(self):
        if not self.current_buyer:
            show_error_message(self.view, "Lỗi", "Vui lòng chọn một nhân viên mua hàng."); return
        
        quantity_str = self.view.quantity_input.text()
        if not quantity_str:
            show_error_message(self.view, "Lỗi", "Vui lòng nhập số lượng."); return
        
        try: input_value = float(quantity_str)
        except ValueError:
            show_error_message(self.view, "Lỗi", "Số lượng không hợp lệ."); return
            
        unit_price = self.model.get_current_price()
        quantity_liters = input_value if self.current_transaction_type == 'Lít' else (input_value / unit_price)
        total_amount = (quantity_liters * unit_price) if self.current_transaction_type == 'Lít' else input_value
            
        payment_dialog = PaymentDialog(self.view)
        if payment_dialog.exec_():
            payment_method = payment_dialog.selected_method
            tx_data = self.model.create_transaction(self.current_seller['employee_id'], self.current_buyer['id'], self.current_transaction_type, unit_price, round(quantity_liters, 2), round(total_amount), payment_method)
            show_info_message(self.view, "Thành công", "Đã lưu giao dịch thành công!")
            self.handle_printing(tx_data)
            self.view.reset_transaction_form()
            self.current_buyer = None
        
    def handle_printing(self, tx_data):
        settings = self.model.get_print_settings()
        should_print = (tx_data['payment_method'] == 'Tiền mặt' and settings.get('in_phieu_tien_mat', False)) or \
                       (tx_data['payment_method'] == 'Ghi nợ' and settings.get('in_phieu_ghi_no', False))
        
        if should_print:
            tx_data['buyer_name'] = self.current_buyer.get('name', '')
            result = self.app_controller.hardware_manager.print_receipt(tx_data)
            if result is not True:
                show_error_message(self.view, "Lỗi in phiếu", f"Không thể in hóa đơn. Lỗi: {result}")

    def show_settings(self):
        """Hiển thị hộp thoại cài đặt cho Kiosk."""
        is_admin = self.current_seller.get('role') == 'Admin'
        
        dialog = SettingsDialog(is_admin, self.view)
        if dialog.exec_():
            show_info_message(self.view, "Thành công", "Đã lưu cài đặt.")
            # Cập nhật lại giá trên giao diện chính
            self.view.current_price_label.setText(f"Đơn giá: {format_currency(self.model.get_current_price())}")

    def logout(self):
        self.view.close()
        self.app_controller.show_login_window()