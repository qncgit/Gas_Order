import sys
import os
from config import APP_CONFIG
from controller.app_controller import AppController
from qfluentwidgets.common import qconfig
from config_items import cfg

if __name__ == "__main__":
    print("Khởi chạy ứng dụng GAS_ORDER...")

    # Đảm bảo thư mục config tồn tại
    config_dir = 'config'
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        print(f"Đã tạo thư mục '{config_dir}'.")
        
    # Tải file cài đặt. Nếu file không tồn tại, nó sẽ được tạo với giá trị mặc định.
    qconfig.load(os.path.join(config_dir, 'settings.json'), cfg)
    
    # Khởi tạo controller chính
    main_controller = AppController(APP_CONFIG)
    
    # Chạy ứng dụng
    sys.exit(main_controller.run())
