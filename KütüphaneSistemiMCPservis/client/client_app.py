import requests
from datetime import datetime
import math
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

API_BASE_URL = os.environ.get("API_BASE_URL", "http://api_service:5000")

app = Flask(__name__)
app.secret_key = 'super_secret_client_key'

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>Kütüphane Sistemi</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">

<style>
body {
    background: linear-gradient(to right, #243949, #517fa4);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}
.card-box {
    width: 900px;
    background: rgba(255,255,255,0.98);
    border-radius: 14px;
    padding: 25px;
    box-shadow: 0 0 18px rgba(0,0,0,0.25);
    position: relative;
}
.btn-primary {
    background-color: #1b4d89;
    border: none;
}
.btn-primary:hover {
    background-color: #12385f;
}
.logout {
    position: absolute;
    right: 20px;
    top: 20px;
}
.book-card {
    background: #ebf3fa;
    border-radius: 10px;
    margin-bottom: 10px;
    padding: 10px;
}
.book-cover {
    width: 48px;
    height: 64px;
    object-fit: cover; 
    border-radius: 5px;
}
.section-title {
    color: #1b4d89;
    font-weight: 700;
}
</style>
</head>

<body>

<div class="card-box">
{% with messages = get_flashed_messages(with_categories=True) %}
  {% if messages %}
    {% for category, message in messages %}
      <div class="alert alert-{{ 'success' if category == 'success' else 'danger' }} mt-1">
        {{ message }}
      </div>
    {% endfor %}
  {% endif %}
{% endwith %}

{% if not session.get('logged_in') %}
    <h4 class="text-center mb-3">📚 Giriş Yap</h4>
    <div class="text-center mb-2">{{ current_date }}</div>

    <form action="/login_client" method="POST">
        <input class="form-control mb-2" type="text" name="username" placeholder="Kullanıcı adı" required>
        <input class="form-control mb-2" type="password" name="password" placeholder="Parola" required>
        <button class="btn btn-primary w-100">Giriş Yap</button>
    </form>

{% else %}
<form class="logout" action="/logout_client" method="POST">
    <button class="btn btn-danger btn-sm">Çıkış</button>
</form>

<h5 class="text-center">📚 Kütüphane Paneli</h5>
<p class="text-center"><b>{{ session.get('username') }}</b> — {{ current_date }}</p>

<form method="GET" action="/" class="mb-3">
    <div class="input-group">
        <input type="text" name="keyword" class="form-control" placeholder="Kitap ara..." value="{{ keyword }}">
        <button class="btn btn-success">Ara</button>
    </div>
</form>

{% if keyword and books|length == 0 %}
<div class="alert alert-warning">❌ Aradığınız kitap bulunamadı!</div>
{% endif %}

{% if books %}
<h6 class="section-title">🔍 Kitaplar</h6>
{% for book in books %}
<div class="book-card d-flex gap-2 align-items-center">
    {% if book.cover_url %}
    <img src="{{ book.cover_url }}" class="book-cover">
    {% endif %}
    <div class="flex-grow-1">
        <strong>{{ book.title }}</strong> — {{ book.author }}<br>
        <small>Durum: 
            {% if book.status == "Available" %}
                <b class="text-success">Müsait</b>
            {% else %}
                <b class="text-danger">Ödünçte</b>
            {% endif %}
        </small>

        <div class="mt-1 d-flex gap-1">
            {% if book.status == "Available" %}
            <form method="POST" action="/borrow_book">
                <input type="hidden" name="book_id" value="{{ book.id }}">
                <button class="btn btn-primary btn-sm">📖 Ödünç Al</button>
            </form>
            {% endif %}

            {% if session.get('role') == "admin" %}
            <form method="POST" action="/admin_delete_book"
                  onsubmit="return confirm('Silinsin mi?');">
                <input type="hidden" name="book_id" value="{{ book.id }}">
                <button class="btn btn-outline-danger btn-sm">🗑 Sil</button>
            </form>
            {% endif %}
        </div>
    </div>
</div>
{% endfor %}
{% endif %}

{% if my_books %}
<h6 class="section-title mt-3">📌 Ödünç Aldıklarım</h6>
{% for book in my_books %}
<div class="book-card d-flex gap-2 align-items-center">
    {% if book.cover_url %}
    <img src="{{ book.cover_url }}" class="book-cover">
    {% endif %}
    <div class="flex-grow-1">
        <strong>{{ book.title }}</strong><br>
        <form method="POST" action="/return_book" class="mt-1">
            <input type="hidden" name="book_id" value="{{ book.id }}">
            <button class="btn btn-warning btn-sm">↩️ İade Et</button>
        </form>
    </div>
</div>
{% endfor %}
{% endif %}

{% if session.get('role') == "admin" %}
<hr>
<h6 class="section-title">🛠 Admin Panel</h6>

<form action="/admin_add_book" method="POST" class="mb-3">
    <div class="row g-2">
        <div class="col-4"><input class="form-control" name="title" placeholder="Kitap adı"></div>
        <div class="col-4"><input class="form-control" name="author" placeholder="Yazar"></div>
        <div class="col-4"><input class="form-control" name="cover_url" placeholder="Kapak URL"></div>
    </div>
    <button class="btn btn-dark w-100 mt-2">➕ Kitap Ekle</button>
</form>

{% if admin_info %}
<div class="alert alert-info mt-1">
    Kullanıcı: {{ admin_info.total_users }} <br>
    Kitap: {{ admin_info.total_books }}
</div>
{% endif %}
{% endif %}

{% endif %}

</div>
</body>
</html>
"""

def call_api(method, endpoint, json_data=None, requires_auth=False):
    url = f"{API_BASE_URL}{endpoint}"
    headers = {}
    if requires_auth and session.get("token"):
        headers["Authorization"] = f"Bearer {session['token']}"
    try:
        if method == 'GET':
            response = requests.get(url, params=json_data, headers=headers)
        elif method == 'POST':
            response = requests.post(url, json=json_data, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, json=json_data, headers=headers)
        else:
            return {"message": "Method desteklenmiyor"}, 405

        return response.json(), response.status_code
    except Exception as e:
        return {"message": f"API Hatası: {str(e)}"}, 500

def get_my_borrowed_books():
    if not session.get('logged_in'):
        return []
    data, status = call_api('GET', "/my_books", None, True)
    return data.get('books', []) if status == 200 else []

@app.route('/', methods=['GET'])
def index():
    keyword = request.args.get('keyword', '')
    books, my_books = [], []

    if session.get('logged_in'):
        my_books = get_my_borrowed_books()

        data, status = call_api('GET', f"/search?keyword={keyword}")
        books = data.get('books', []) if status == 200 else []

    current_date = datetime.now().strftime("%d %B %Y")
    return render_template_string(HTML_TEMPLATE,
                                 books=books, keyword=keyword,
                                 my_books=my_books,
                                 admin_info=session.pop('admin_info', None),
                                 current_date=current_date)

@app.route('/login_client', methods=['POST'])
def login_client():
    username = request.form.get('username')
    password = request.form.get('password')
    data, status = call_api('POST', '/login',
                            {"username": username, "password": password})
    if status == 200:
        session.update({
            "logged_in": True, "username": username,
            "role": data.get('role'), "token": data.get('token')
        })
        flash("Giriş başarılı!", "success")
    else:
        flash(data.get('message'), "error")
    return redirect(url_for('index'))

@app.route('/logout_client', methods=['POST'])
def logout_client():
    session.clear()
    flash("Çıkış Yapıldı!", "success")
    return redirect(url_for('index'))

@app.route('/borrow_book', methods=['POST'])
def borrow():
    book_id = request.form.get('book_id', type=int)
    data, status = call_api('POST', "/borrow",
                            {"book_id": book_id}, True)
    flash(data.get('message'), "success" if status == 200 else "error")
    return redirect(url_for('index'))

@app.route('/return_book', methods=['POST'])
def return_book():
    book_id = request.form.get('book_id', type=int)
    data, status = call_api('POST', "/return",
                            {"book_id": book_id}, True)
    flash(data.get('message'), "success" if status == 200 else "error")
    return redirect(url_for('index'))

@app.route('/admin_add_book', methods=['POST'])
def admin_add():
    if session.get("role") != "admin":
        flash("Yetki yok!", "error")
        return redirect(url_for('index'))
    title = request.form.get('title')
    author = request.form.get('author')
    cover_url = request.form.get('cover_url')

    data, status = call_api('POST', "/admin/books",
                            {"title": title, "author": author, "cover_url": cover_url}, True)
    flash(data.get('message'), "success" if status in (200, 201) else "error")
    return redirect(url_for('index'))

@app.route('/admin_delete_book', methods=['POST'])
def admin_delete():
    if session.get("role") != "admin":
        flash("Yetki yok!", "error")
        return redirect(url_for('index'))
    book_id = request.form.get('book_id', type=int)
    data, status = call_api('DELETE', f"/admin/books/{book_id}", None, True)
    flash(data.get('message'), "success" if status == 200 else "error")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
