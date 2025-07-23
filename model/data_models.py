# ==============================================================================
# File: GAS_ORDER/model/data_models.py
# ==============================================================================
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Employee:
    """Đại diện cho một nhân viên mua xăng."""
    id: str
    name: str
    birth_date: str
    department: str
    status: Optional[str] = "Active"

@dataclass
class User:
    """Đại diện cho một người dùng hệ thống (NV Bán xăng, Admin, Thống kê)."""
    id: str
    employee_id: str
    rfid_card_id: Optional[str] = None
    username: Optional[str] = None
    role: str = "Seller" # Các vai trò: Seller, Admin, Statistician

@dataclass
class Transaction:
    """Đại diện cho một giao dịch bán xăng."""
    id: str # UUID, tạo ở client
    timestamp: str
    seller_employee_id: str
    buyer_employee_id: str
    transaction_type: str # 'Lít' hoặc 'Tiền'
    unit_price: float
    quantity: float
    total_amount: float
    payment_method: str # 'Tiền mặt' hoặc 'Ghi nợ'
    is_synced: int = 0 # 0 = chưa đồng bộ, 1 = đã đồng bộ