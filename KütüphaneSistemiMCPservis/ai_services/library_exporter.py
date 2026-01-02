import time
import requests
from prometheus_client import start_http_server, Gauge

API_URL = "http://api_service:5000"

TOTAL_BOOKS = Gauge('library_total_books', 'Toplam Kitap Sayısı')
TOTAL_USERS = Gauge('library_total_users', 'Toplam Kullanıcı Sayısı')
API_STATUS = Gauge('library_api_status', 'API Erişilebilirliği (1: Up, 0: Down)')

def get_token():
    try:
        r = requests.post(f"{API_URL}/login", json={"username": "admin", "password": "adminpass"}, timeout=5)
        return r.json().get("token") if r.status_code == 200 else None
    except:
        return None

def update_metrics():
    token = get_token()
    if not token:
        API_STATUS.set(0)
        print("API Erişilemiyor veya Login Başarısız")
        return

    API_STATUS.set(1)
    try:
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(f"{API_URL}/admin_info", headers=headers, timeout=5)
        if r.status_code == 200:
            data = r.json()
            TOTAL_BOOKS.set(data.get('total_books', 0))
            TOTAL_USERS.set(data.get('total_users', 0))
            print(f"Metrikler Güncellendi: Kitap={data.get('total_books')}, User={data.get('total_users')}")
    except Exception as e:
        print(f"Veri çekme hatası: {e}")

if __name__ == "__main__":
    print("Library Exporter Başlatılıyor (Port 8000)...")
    start_http_server(8000)
    while True:
        update_metrics()
        time.sleep(15) 