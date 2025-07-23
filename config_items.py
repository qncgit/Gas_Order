# config_items.py
from qfluentwidgets import QConfig, ConfigItem, BoolValidator

class Config(QConfig):
    don_gia_xang = ConfigItem("General", "DonGiaXang", "25000")
    in_phieu_tien_mat = ConfigItem("Print", "InPhieuTienMat", True, BoolValidator())
    in_phieu_ghi_no = ConfigItem("Print", "InPhieuGhiNo", False, BoolValidator())
    table_id_transactions = ConfigItem("NocoDB", "TableIdTransactions", "")
    view_id_transactions = ConfigItem("NocoDB", "ViewIdTransactions", "")

cfg = Config()