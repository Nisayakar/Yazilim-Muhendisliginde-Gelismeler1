import requests
from mcp.server.fastmcp import FastMCP

API_URL = "http://api_service:5000"

mcp = FastMCP("Library MCP Server")

def get_auth_token():
    """Admin girişi yapıp token alır."""
    try:
        resp = requests.post(f"{API_URL}/login", json={"username": "admin", "password": "adminpass"})
        if resp.status_code == 200:
            return resp.json().get("token")
    except:
        return None
    return None

@mcp.tool()
def search_library(keyword: str) -> str:
    """Kütüphanede kitap arar. Kitap adı veya yazar verilebilir."""
    try:
        # Arama endpointi token istemiyor
        resp = requests.get(f"{API_URL}/search", params={"keyword": keyword})
        data = resp.json()
        books = data.get("books", [])
        
        if not books:
            return "Kitap bulunamadı."
            
        result = f"'{keyword}' araması için bulunan kitaplar:\n"
        for b in books:
            result += f"- {b['title']} ({b['author']}) [Durum: {b['status']}]\n"
        return result
    except Exception as e:
        return f"Hata oluştu: {str(e)}"

@mcp.tool()
def get_system_stats() -> str:
    """Sistemdeki toplam kullanıcı ve kitap sayılarını getirir (Admin yetkisi gerektirir)."""
    token = get_auth_token()
    if not token:
        return "Giriş hatası: Admin token alınamadı."
        
    headers = {"Authorization": f"Bearer {token}"}
    try:
        resp = requests.get(f"{API_URL}/admin_info", headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            return (f"Sistem İstatistikleri:\n"
                    f"Toplam Kitap: {data.get('total_books')}\n"
                    f"Toplam Kullanıcı: {data.get('total_users')}")
        else:
            return f"Yetki Hatası: {resp.text}"
    except Exception as e:
        return f"Bağlantı Hatası: {str(e)}"

if __name__ == "__main__":
    mcp.run()