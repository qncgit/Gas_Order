# main_window.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QDesktopWidget
from PyQt5.QtCore import Qt
from qfluentwidgets import FluentWindow, ScrollArea, ExpandLayout, SettingCardGroup, LineEdit, SwitchSettingCard, TitleLabel, SubtitleLabel
from qfluentwidgets import FluentIcon as FIF, NavigationItemPosition
from config_items import cfg

class SettingsWidget(ScrollArea):
    def __init__(self, user_role, parent=None):
        super().__init__(parent)
        self.setObjectName("settings_widget")
        self.user_role = user_role
        
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # --- Nhóm Cài đặt chung ---
        self.settingGroup = SettingCardGroup("Cài đặt chung", self.scrollWidget)
        
        self.priceEdit = LineEdit(self)
        self.priceEdit.setText(cfg.get(cfg.don_gia_xang))
        self.priceCard = self.settingGroup.addSettingCard(
            self.priceEdit, FIF.PRICE, "Đơn giá xăng", "Cập nhật đơn giá bán xăng (VNĐ/Lít)"
        )
        self.priceEdit.textChanged.connect(lambda t: cfg.set(cfg.don_gia_xang, t))

        # --- Nhóm Cấu hình in phiếu ---
        self.printGroup = SettingCardGroup("Cấu hình in phiếu", self.scrollWidget)
        self.cashReceiptCard = SwitchSettingCard(
            cfg.in_phieu_tien_mat,
            FIF.PRINT,
            "In phiếu Tiền mặt",
            "Cho phép in hóa đơn cho các giao dịch thanh toán bằng tiền mặt.",
            parent=self.printGroup
        )
        self.debtReceiptCard = SwitchSettingCard(
            cfg.in_phieu_ghi_no,
            FIF.PRINT,
            "In phiếu Ghi nợ",
            "Cho phép in hóa đơn cho các giao dịch ghi nợ.",
            parent=self.printGroup
        )
        self.printGroup.addSettingCard(self.cashReceiptCard)
        self.printGroup.addSettingCard(self.debtReceiptCard)

        # --- Nhóm Cài đặt Admin ---
        if self.user_role == "Admin":
            self.adminGroup = SettingCardGroup("Cấu hình NocoDB (Admin)", self.scrollWidget)
            self.tableIdEdit = LineEdit(self)
            self.tableIdEdit.setText(cfg.get(cfg.table_id_transactions))
            self.viewIdEdit = LineEdit(self)
            self.viewIdEdit.setText(cfg.get(cfg.view_id_transactions))
            
            self.tableIdCard = self.adminGroup.addSettingCard(
                self.tableIdEdit, FIF.DATABASE, "ID Bảng Giao dịch", "Table ID cho bảng transactions"
            )
            self.viewIdCard = self.adminGroup.addSettingCard(
                self.viewIdEdit, FIF.GRID, "ID View Giao dịch", "View ID cho bảng transactions"
            )
            self.tableIdEdit.textChanged.connect(lambda t: cfg.set(cfg.table_id_transactions, t))
            self.viewIdEdit.textChanged.connect(lambda t: cfg.set(cfg.view_id_transactions, t))

        self.expandLayout.addWidget(self.settingGroup)
        self.expandLayout.addWidget(self.printGroup)
        if self.user_role == "Admin":
            self.expandLayout.addWidget(self.adminGroup)

        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

class ReportWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("report_widget")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(TitleLabel("Báo cáo & Thống kê", self))
        layout.addWidget(SubtitleLabel("Chức năng đang được phát triển", self))

class UserManagementWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("user_mgmt_widget")
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.addWidget(TitleLabel("Quản lý Người dùng", self))
        layout.addWidget(SubtitleLabel("Chức năng đang được phát triển", self))

class MainWindow(FluentWindow):
    def __init__(self, controller, user_role):
        super().__init__()
        self.controller = controller
        self.user_role = user_role if user_role in ["Admin", "User"] else "User"
        self.init_ui()

    def init_ui(self):
        from PyQt5.QtWidgets import QDesktopWidget
        
        self.setWindowTitle("Hệ thống Bán xăng - Bảng điều khiển")
        self.resize(1100, 800)
        self.center_window()

        try:
            self.report_interface = ReportWidget(self)
            self.user_mgmt_interface = UserManagementWidget(self)
            self.settings_interface = SettingsWidget(self.user_role, self)
        except Exception as e:
            print(f"Lỗi khi khởi tạo giao diện: {e}")
            return

        self.addSubInterface(self.report_interface, FIF.REPORT, "Báo cáo", selectable=False)
        if self.user_role == "Admin":
            self.addSubInterface(self.user_mgmt_interface, FIF.PEOPLE, "Quản lý Người dùng", selectable=False)
        self.addSubInterface(self.settings_interface, FIF.SETTING, "Cài đặt")

        self.navigationInterface.addItem(
            routeKey='logout',
            icon=FIF.POWER_BUTTON,
            text='Đăng xuất',
            onClick=self.controller.handle_logout,
            position=NavigationItemPosition.BOTTOM
        )

    def center_window(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())