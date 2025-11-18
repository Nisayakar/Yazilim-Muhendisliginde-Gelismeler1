import requests
import os
from flask import (
    Flask,
    request,
    render_template_string,
    redirect,
    url_for,
    flash,
    session
)

# API sunucusunun adresi (Port 5000)
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:5000")

# --- Client Uygulamasını Başlatma ---
app = Flask(__name__)
app.secret_key = 'super_secret_client_key'

# --- HTML Şablonu (Yönetici Paneli Eklendi) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Kitap Arama Motoru (Client App)</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 40px; background: #eef2f7; color: #333; }
        .container { max-width: 800px; margin: auto; background: #fff; border-radius: 10px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1); padding: 30px; }
        h1 { color: #007bff; border-bottom: 2px solid #007bff; padding-bottom: 10px; margin-bottom: 20px; text-align: center; }
        h2 { color: #5a5a5a; border-bottom: 1px dashed #ccc; padding-bottom: 5px; margin-top: 30px; }
        .auth-status { background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #dee2e6; }
        .search-form { display: flex; margin-bottom: 30px; }
        .search-form input { flex-grow: 1; padding: 12px; border: 1px solid #ccc; border-radius: 6px 0 0 6px; font-size: 16px; }
        .search-form button { padding: 12px 20px; background: #28a745; color: white; border: none; border-radius: 0 6px 6px 0; cursor: pointer; transition: background 0.3s; }
        .search-form button:hover { background: #218838; }
        .book-list { list-style: none; padding: 0; }
        .book-item { background: #f8f9fa; border: 1px solid #eee; margin-bottom: 15px; padding: 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center; }
        .book-item strong { display: block; font-size: 1.1em; color: #333; }
        .status-available { color: #28a745; font-weight: bold; }
        .status-loaned { color: #dc3545; font-weight: bold; }
        .borrow-btn { background: #ffc107; color: #333; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; }
        .borrow-btn:hover { background: #e0a800; }
        .return-btn { background: #007bff; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; }
        .return-btn:hover { background: #0056b3; }
        .logout-btn { background: #dc3545; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; }
        .login-input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
        .login-btn { background: #007bff; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; }
        .flash-msg { padding: 10px; background-color: #d4edda; color: #155724; border-radius: 5px; margin-bottom: 15px; }
        .flash-error { background-color: #f8d7da; color: #721c24; }
        .login-form-container { display: flex; justify-content: space-between; align-items: center; }
        .login-form { display: flex; gap: 10px; }
        .logged-in-status { display: flex; justify-content: space-between; align-items: center; width: 100%; }
        .my-books-list { background: #fff3cd; border: 1px solid #ffeeba; }
        .admin-panel { background: #dc3545; color: white; padding: 10px; border-radius: 8px; margin-bottom: 15px; }
        .admin-btn { background: #fff; color: #dc3545; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer; margin-left: 10px; }
        .admin-btn:hover { background: #f0f0f0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Kütüphane Kitap Arama Arayüzü (Port 5001)</h1>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <p class="flash-msg {% if category == 'error' %}flash-error{% endif %}">{{ message }}</p>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <div class="auth-status">
            {% if session['logged_in'] %}
                <div class="logged-in-status">
                    <p style="color: green;">
                        ✔ Giriş Yapıldı. Kullanıcı: <strong>{{ session['username'] }}</strong> 
                        (Rol: <strong>{{ session['role'] | default('user') }}</strong>) 
                    </p>
                    <form method="POST" action="/logout_client">
                        <button type="submit" class="logout-btn">Çıkış Yap</button>
                    </form>
                </div>
            {% else %}
                <div class="login-form-container">
                    <p style="color: orange;">⚠ Giriş Yapılmadı. Arama ve ödünç alma işlemleri için giriş yapın.</p>
                    <form class="login-form" method="POST" action="/login_client">
                        <input type="text" name="username" placeholder="Kullanıcı Adı" required class="login-input">
                        <input type="password" name="password" placeholder="Şifre" required class="login-input">
                        <button type="submit" class="login-btn">Giriş Yap</button>
                    </form>
                </div>
            {% endif %}
        </div>
        
        {% if session['logged_in'] %}
        
            {% if session['role'] == 'admin' %}
            <div class="admin-panel">
                <p>Yönetici Paneli Erişimi Aktif</p>
                <form method="GET" action="/view_admin_info" style="display: inline;">
                    <button type="submit" class="admin-btn">Yönetici Bilgilerini Gör</button>
                </form>
                {% if admin_info %}
                    <div style="margin-top: 10px; padding: 10px; background: #fff; color: #333; border-radius: 5px;">
                        <p><strong>API Bilgisi:</strong> {{ admin_info.message }}</p>
                        <p>Toplam Kullanıcı: {{ admin_info.total_users }}</p>
                        <p>Toplam Kitap: {{ admin_info.total_books }}</p>
                    </div>
                {% endif %}
            </div>
            {% endif %}
        
            <h2>Ödünç Aldığım Kitaplar</h2>
            <ul class="book-list">
                {% if my_books %}
                    {% for book in my_books %}
                    <li class="book-item my-books-list">
                        <div>
                            <strong>{{ book.title }}</strong>
                            <p>Yazar: {{ book.author }}</p>
                        </div>
                        <form method="POST" action="/return_book">
                            <input type="hidden" name="book_id" value="{{ book.id }}">
                            <button type="submit" class="return-btn">İade Et</button>
                        </form>
                    </li>
                    {% endfor %}
                {% else %}
                    <p>Henüz ödünç aldığınız bir kitap bulunmamaktadır.</p>
                {% endif %}
            </ul>
            ---

            <h2>Kitap Ara</h2>
            <form class="search-form" action="/" method="GET">
                <input type="text" name="keyword" placeholder="Başlık veya yazar girin (örn: Dostoyevski)" required value="{{ keyword or '' }}">
                <button type="submit">Kitap Ara</button>
            </form>

            {% if error_message %}
                <p class="status-info" style="color: red; font-weight: bold;">Hata: {{ error_message }}</p>
            {% endif %}

            {% if books %}
                <h2>Arama Sonuçları ({{ books | length }})</h2>
                <ul class="book-list">
                    {% for book in books %}
                    <li class="book-item">
                        <div>
                            <strong>{{ book.title }}</strong>
                            <p>Yazar: {{ book.author }}</p>
                            <p class="{% if book.status == 'Available' %}status-available{% else %}status-loaned{% endif %}">
                                Durum: {{ book.status }}
                            </p>
                        </div>
                        {% if book.status == 'Available' and session['logged_in'] %}
                            <form method="POST" action="/borrow_book">
                                <input type="hidden" name="book_id" value="{{ book.id }}">
                                <button type="submit" class="borrow-btn">Ödünç Al</button>
                            </form>
                        {% elif book.status == 'Available' %}
                                <button type="button" class="borrow-btn" disabled style="background: #ccc;">Ödünç Al (Giriş Yap)</button>
                        {% endif %}
                    </li>
                    {% endfor %}
                </ul>
            {% endif %}

        {% else %}
            <p style="text-align: center; margin-top: 30px; padding: 20px; background: #f0f0f0; border-radius: 8px;">
                Lütfen giriş yapınız. Giriş yaptıktan sonra arama sonuçları ve diğer işlemler burada görünecektir.
            </p>
        {% endif %}
    </div>
</body>
</html>
"""

# --- Yardımcı Fonksiyon: API Çağrısı ---
def call_api(method, endpoint, json_data=None):
    url = f"{API_BASE_URL}{endpoint}"
    
    try:
        if method == 'GET':
            response = requests.get(url, params=json_data)
        elif method == 'POST':
            response = requests.post(url, json=json_data)
        else:
            return None, 405

        if response.status_code in (200, 201):
            if response.content:
                return response.json(), response.status_code
            return {}, 200

        data = response.json() if response.content else {"message": f"API'den yanıt alınamadı. Durum: {response.status_code}"}
        return data, response.status_code

    except requests.ConnectionError:
        return {"error_message": f"API Bağlantı Hatası! {API_BASE_URL} adresi çalışmıyor."}, 503
    except requests.exceptions.JSONDecodeError:
        return {"error_message": "API'den geçerli bir JSON yanıtı alınamadı (API'yi kontrol edin)."}, 500
    except Exception as e:
        return {"error_message": f"Client'ta Bilinmeyen bir hata oluştu: {e}"}, 500

# --- Yardımcı Fonksiyonlar (Kısaltıldı) ---
def get_my_borrowed_books():
    if not session.get('logged_in'):
        return None
    username = session.get('username')
    data, status = call_api('GET', "/my_books", json_data={"username": username})
    if status == 200 and 'books' in data: return data['books']
    return None

# --- Ana Sayfa Route ---
@app.route('/', methods=['GET'])
def index():
    error_message = None
    keyword = request.args.get('keyword', '')
    books = None
    my_books = None
    admin_info = session.pop('admin_info', None) # Yönetici bilgisini oturumdan al
    
    if session.get('logged_in'):
        my_books = get_my_borrowed_books() 
        
        if keyword:
            data, status = call_api('GET', f"/search?keyword={keyword}")
            if status == 200 and 'books' in data:
                books = data['books']
            elif 'error_message' in data:
                error_message = data['error_message']
            
    return render_template_string(
        HTML_TEMPLATE, 
        books=books, 
        keyword=keyword, 
        error_message=error_message,
        my_books=my_books,
        admin_info=admin_info # HTML'e gönder
    )

# --- Login İşlemi ---
@app.route('/login_client', methods=['POST'])
def login_client():
    username = request.form.get('username')
    password = request.form.get('password')
    
    login_payload = {"username": username, "password": password}
    
    data, status = call_api('POST', '/login', json_data=login_payload)
    
    if status == 200:
        session['logged_in'] = True
        session['username'] = username
        session['role'] = data.get('role', 'user') 
        flash(f"Giriş başarılı! Hoş geldiniz, {username}.", "success")
    elif 'message' in data:
        session['logged_in'] = False
        flash(f"Giriş başarısız: {data['message']}", "error")
    else:
        session['logged_in'] = False
        flash("Giriş başarısız oldu. API bağlantı/hata sorunu.", "error")
        
    return redirect(url_for('index'))

# --- Yönetici Bilgisini Çekme Route'u (YENİ) ---
@app.route('/view_admin_info', methods=['GET'])
def view_admin_info():
    if session.get('role') != 'admin':
        flash("Hata: Bu işlemi yapmak için Yönetici yetkiniz yok.", "error")
        return redirect(url_for('index'))
        
    username = session.get('username')
    # NOT: API'ye GET isteği atarken json_data yerine params kullanmalıyız. call_api bunu zaten hallediyor.
    data, status = call_api('GET', "/admin_info", json_data={"username": username}) 
    
    if status == 200:
        session['admin_info'] = data
        flash("Yönetici bilgileri başarıyla çekildi.", "success")
    elif 'message' in data:
        flash(f"Yönetici Bilgi Hatası: {data['message']}", "error")
    else:
        flash("Hata: Yönetici bilgisi çekilirken sorun oluştu.", "error")
        
    return redirect(url_for('index'))

# --- Diğer Route'lar (Kısaltıldı) ---
@app.route('/logout_client', methods=['POST'])
def logout_client():
    call_api('POST', '/logout')
    session.pop('logged_in', None)
    session.pop('username', None)
    session.pop('role', None) 
    session.pop('admin_info', None)
    flash("Çıkış yapıldı. Giriş ekranına yönlendiriliyorsunuz.", "success")
    return redirect(url_for('index'))

@app.route('/borrow_book', methods=['POST'])
def perform_borrow():
    if not session.get('logged_in'):
        flash("Hata: Ödünç alma işlemi için giriş yapmalısınız.", "error"); return redirect(url_for('index'))
    book_id = request.form.get('book_id', type=int)
    borrow_payload = {"book_id": book_id, "username": session.get('username')}
    data, status = call_api('POST', '/borrow', json_data=borrow_payload)
    if status == 200: flash(data.get('message', 'Kitap başarıyla ödünç alındı!'), "success")
    else: flash(f"Hata: {data.get('message', 'Bilinmeyen bir sorun oluştu')}", "error")
    return redirect(url_for('index'))

@app.route('/return_book', methods=['POST'])
def perform_return():
    if not session.get('logged_in'):
        flash("Hata: İade işlemi için giriş yapmalısınız.", "error"); return redirect(url_for('index'))
    book_id = request.form.get('book_id', type=int)
    return_payload = {"book_id": book_id, "username": session.get('username')}
    data, status = call_api('POST', '/return', json_data=return_payload)
    if status == 200: flash(data.get('message', 'Kitap başarıyla iade edildi!'), "success")
    else: flash(f"Hata: {data.get('message', 'Bilinmeyen bir sorun oluştu')}", "error")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)