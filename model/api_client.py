# ==============================================================================
# File: GAS_ORDER/model/api_client.py
# ==============================================================================
import requests
from config import APP_CONFIG

class ApiClient:
    def __init__(self):
        self.config = APP_CONFIG

    def get_data(self, table_key, view_key="default", params=None):
        headers, url_server, table_id, view_id = self.config.config_header_api(), self.config.config_url_server(), self.config.config_table_id(table_key), self.config.config_view_id(table_key, view_key)
        if not table_id: 
            print(f"Lỗi: Không tìm thấy table_id cho key '{table_key}'")
            return None
        try:
            url, all_records, offset, limit = f"http://{url_server}/api/v2/tables/{table_id}/records", [], 0, 100
            while True:
                querystring = {"offset": str(offset), "limit": str(limit), "where": params.get('where', '') if params else '', "viewId": view_id}
                response = requests.get(url, headers=headers, params=querystring, timeout=10)
                response.raise_for_status()
                records = response.json().get('list', [])
                all_records.extend(records)
                if len(records) < limit: break
                offset += limit
            return all_records
        except requests.exceptions.RequestException as e:
            print(f"Lỗi get_data từ API: {e}")
            return None

    def post_data(self, table_key, data):
        table_id = self.config.config_table_id(table_key)
        if not table_id: return None
        try:
            url = f"http://{self.config.config_url_server()}/api/v2/tables/{table_id}/records"
            response = requests.post(url, json=data, headers=self.config.config_header_api(), timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi gửi dữ liệu (POST): {e}")
            return None

    def patch_data(self, table_key, data):
        table_id = self.config.config_table_id(table_key)
        if not table_id: return None
        try:
            url = f"http://{self.config.config_url_server()}/api/v2/tables/{table_id}/records"
            response = requests.patch(url, json=data, headers=self.config.config_header_api(), timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Lỗi khi cập nhật dữ liệu (PATCH): {e}")
            return None

    def check_connection(self):
        try:
            response = requests.get(f"http://{self.config.config_url_server()}/api/v2/meta/bases", headers=self.config.config_header_api(), timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False