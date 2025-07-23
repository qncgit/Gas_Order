# ==============================================================================
# File: GAS_ORDER/config.py
# ==============================================================================
import os

class Config:
    """
    Lớp chứa toàn bộ cấu hình cho ứng dụng.
    Thay đổi các giá trị ở đây để phù hợp với môi trường của bạn.
    """
    # --- Chế độ Vận hành ---
    # Đặt là True để dùng code giả lập phần cứng trong thư mục /test
    # Đặt là False khi triển khai ra máy thật với phần cứng thật
    DEBUG_MODE = True

    # --- Cấu hình API NocoDB ---
    NOCODB_URL = "localhost:8080"  # Thay bằng địa chỉ IP và cổng của NocoDB server
    NOCODB_API_TOKEN = "YOUR_API_TOKEN_HERE" # Thay bằng API Token của bạn

    # --- Cấu hình CSDL Cục bộ (SQLite) ---
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATABASE_NAME = "gas_order_local.db"
    DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_NAME)

    # --- Cấu hình Bảng NocoDB ---
    # Hướng dẫn:
    # 1. Mở NocoDB trong trình duyệt.
    # 2. Đi đến bảng bạn muốn cấu hình (ví dụ: 'users').
    # 3. Nhìn vào thanh địa chỉ URL, bạn sẽ thấy một chuỗi tương tự như sau:
    #    /dashboard/#/nc/project_id/base_id/table/tbl_xxxxxxxxxxxx
    # 4. Copy phần `tbl_xxxxxxxxxxxx` và dán vào "table_id" tương ứng dưới đây.
    # 5. Để lấy View ID, hãy chọn một View (ví dụ: Grid) và làm tương tự, URL sẽ có dạng:
    #    .../view/viw_yyyyyyyyyyyy
    # 6. Copy phần `viw_yyyyyyyyyyyy` và dán vào "views" -> "default".
    NOCODB_TABLES = {
        "users": {
            "table_id": "tbl_xxxxxxxxxxxx",
            "views": {
                "default": "viw_yyyyyyyyyyyy"
            }
        },
        "employees": {
            "table_id": "tbl_aaaaaaaaaaaa",
            "views": {
                "default": "viw_bbbbbbbbbbbb"
            }
        },
        "transactions": {
            "table_id": "tbl_cccccccccccc",
            "views": {
                "default": "viw_dddddddddddd"
            }
        },
        "price_history": {
            "table_id": "tbl_eeeeeeeeeeee",
            "views": {
                "default": "viw_ffffffffffff"
            }
        }
    }

    # --- Cấu hình Phần cứng (CHỈ DÙNG KHI DEBUG_MODE = False) ---
    PRINTER_CONFIG = {
        "vendor_id": 0x04b8,
        "product_id": 0x0202,
        "profile": "TM-T88V"
    }
    RFID_READER_CONFIG = {
        "port": "COM3",
        "baudrate": 9600
    }

    # --- Cấu hình Đồng bộ ---
    SYNC_INTERVAL_SECONDS = 300  # Đồng bộ mỗi 5 phút

    def config_header_api(self):
        return {"xc-token": self.NOCODB_API_TOKEN}

    def config_url_server(self):
        return self.NOCODB_URL

    def config_table_id(self, table_key):
        """Lấy ID của bảng từ cấu trúc NOCODB_TABLES."""
        return self.NOCODB_TABLES.get(table_key, {}).get("table_id")

    def config_view_id(self, table_key, view_key="default"):
        """Lấy ID của view từ cấu trúc NOCODB_TABLES."""
        table_config = self.NOCODB_TABLES.get(table_key, {})
        return table_config.get("views", {}).get(view_key)

APP_CONFIG = Config()