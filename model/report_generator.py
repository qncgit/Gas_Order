# ==============================================================================
# File: GAS_ORDER/model/report_generator.py
# ==============================================================================
import openpyxl
from PyQt5.QtWidgets import QFileDialog
from utils.helpers import show_info_message, show_error_message

class ReportGenerator:
    """Tạo và xuất báo cáo ra file Excel."""
    def export_to_excel(self, parent, data, headers):
        if not data:
            show_info_message(parent, "Thông báo", "Không có dữ liệu để xuất báo cáo.")
            return
        
        file_path, _ = QFileDialog.getSaveFileName(parent, "Lưu file báo cáo", "", "Excel Files (*.xlsx)")
        
        if not file_path:
            return # Người dùng đã hủy
            
        try:
            workbook = openpyxl.Workbook()
            sheet = workbook.active
            
            column_keys = list(headers.keys())
            sheet.append([headers[key] for key in column_keys])

            for row_data in data:
                sheet.append([row_data.get(key, "") for key in column_keys])

            workbook.save(file_path)
            show_info_message(parent, "Thành công", f"Đã xuất báo cáo thành công!\nĐường dẫn: {file_path}")
        except Exception as e:
            show_error_message(parent, "Lỗi xuất báo cáo", str(e))