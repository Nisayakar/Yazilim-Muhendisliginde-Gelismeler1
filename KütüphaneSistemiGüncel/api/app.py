from flask import Flask, request, jsonify
from datetime import datetime
import jwt
from functools import wraps

app = Flask(__name__)

SECRET_KEY = "super_secret_jwt_key"   # JWT Şifreleme Anahtarı


USERS_DB = {
    "user1": {"password": "pass123", "user_id": 101, "role": "user"},
    "Nisa": {"password": "nisa94", "user_id": 102, "role": "user"},
    "admin": {"password": "adminpass", "user_id": 100, "role": "admin"}
}


BOOKS_DB = {
    1: {
        "title": "Sefiller",
        "author": "Victor Hugo",
        "status": "Available",
        "cover_url": "https://covers.openlibrary.org/b/id/7222246-L.jpg"
    },
    2: {
        "title": "Suç ve Ceza",
        "author": "Fyodor Dostoyevski",
        "status": "Available",
        "cover_url": "https://covers.openlibrary.org/b/id/8231858-L.jpg"
    },
    3: {
        "title": "Karamazov Kardeşler",
        "author": "Fyodor Dostoyevski",
        "status": "Loaned",
        "loaned_to": 101,
        "cover_url": "https://covers.openlibrary.org/b/id/8235026-L.jpg"
    },
    4: {
        "title": "Yabancı",
        "author": "Albert Camus",
        "status": "Available",
        "cover_url": "https://covers.openlibrary.org/b/id/9250144-L.jpg"
    },
    5: {
        "title": "1984",
        "author": "George Orwell",
        "status": "Available",
        "cover_url": "https://covers.openlibrary.org/b/id/1535410-L.jpg"
    },
    6: {
        "title": "Hayvan Çiftliği",
        "author": "George Orwell",
        "status": "Available",
        "cover_url": "https://covers.openlibrary.org/b/id/9641666-L.jpg"
    },
    7: {
        "title": "Simyacı",
        "author": "Paulo Coelho",
        "status": "Available",
        "cover_url": "https://covers.openlibrary.org/b/id/13266540-L.jpg"
    },
    8: {
        "title": "Kürk Mantolu Madonna",
        "author": "Sabahattin Ali",
        "status": "Available",
        "cover_url": "https://covers.openlibrary.org/b/id/12771361-L.jpg"
    },
    9: {
        "title": "Tutunamayanlar",
        "author": "Oğuz Atay",
        "status": "Available",
        "cover_url": "https://covers.openlibrary.org/b/id/11187067-L.jpg"
    },
    10: {
        "title": "Şeker Portakalı",
        "author": "José Mauro de Vasconcelos",
        "status": "Available",
        "cover_url": "https://covers.openlibrary.org/b/id/10451860-L.jpg"
    }
}



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return jsonify({"message": "Token bulunamadı!"}), 401
        
        try:
            token = token.replace("Bearer ", "")
            decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.user = decoded
        except Exception:
            return jsonify({"message": "Token geçersiz veya süresi dolmuş!"}), 403

        return f(*args, **kwargs)
    return decorated



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    if username in USERS_DB and USERS_DB[username]['password'] == password:
        user_info = USERS_DB[username]

        token = jwt.encode(
            {"username": username, "role": user_info['role']},
            SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({
            "message": f"Giriş Başarılı. Rol: {user_info['role']}.",
            "token": token,
            "role": user_info['role']
        }), 200

    return jsonify({"message": "Geçersiz kullanıcı adı veya şifre."}), 401


@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Çıkış başarılı."}), 200



@app.route('/search', methods=['GET'])
def search_books():
    keyword = request.args.get('keyword', '').strip()
    
    results = []
    for book_id, book_info in BOOKS_DB.items():
        if keyword == "" or \
           keyword.lower() in book_info['title'].lower() or \
           keyword.lower() in book_info['author'].lower():
            results.append({
                "id": book_id,
                "title": book_info['title'],
                "author": book_info['author'],
                "status": book_info['status'],
                "cover_url": book_info.get("cover_url")
            })

    return jsonify({"books": results}), 200



@app.route('/my_books', methods=['GET'])
@token_required
def get_my_books():
    username = request.user['username']
    current_user_id = USERS_DB[username]['user_id']
    
    borrowed_books = [
        {
            "id": book_id,
            "title": book["title"],
            "author": book["author"],
            "cover_url": book.get("cover_url")
        }
        for book_id, book in BOOKS_DB.items()
        if book.get("status") == "Loaned" and book.get("loaned_to") == current_user_id
    ]

    return jsonify({"books": borrowed_books}), 200



@app.route('/borrow', methods=['POST'])
@token_required
def borrow_book():
    data = request.get_json() or {}
    book_id = data.get('book_id')
    username = request.user['username']
    current_user_id = USERS_DB[username]['user_id']

    if book_id not in BOOKS_DB:
        return jsonify({"message": f"Kitap ID {book_id} bulunamadı."}), 404

    book = BOOKS_DB[book_id]

    if book["status"] != "Available":
        return jsonify({"message": f"Kitap '{book['title']}' ödünç alınamaz!"}), 400

    book["status"] = "Loaned"
    book["loaned_to"] = current_user_id
    book["loan_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return jsonify({"message": "Kitap başarıyla ödünç alındı."}), 200



@app.route('/return', methods=['POST'])
@token_required
def return_book():
    data = request.get_json() or {}
    book_id = data.get('book_id')
    username = request.user['username']
    current_user_id = USERS_DB[username]['user_id']

    if book_id not in BOOKS_DB:
        return jsonify({"message": "Kitap bulunamadı!"}), 404

    book = BOOKS_DB[book_id]

    if book.get("loaned_to") != current_user_id:
        return jsonify({"message": "Bu kitap sizin değil!"}), 403

    book["status"] = "Available"
    book.pop("loaned_to", None)
    book.pop("loan_date", None)

    return jsonify({"message": "Kitap başarıyla iade edildi."}), 200



@app.route('/admin/books', methods=['POST'])
@token_required
def admin_add_book():
    if request.user['role'] != "admin":
        return jsonify({"message": "Yetkiniz yok!"}), 403

    data = request.get_json() or {}
    title = data.get("title")
    author = data.get("author")
    cover_url = data.get("cover_url")

    if not title or not author:
        return jsonify({"message": "Başlık ve yazar zorunludur."}), 400

    new_id = max(BOOKS_DB.keys()) + 1 if BOOKS_DB else 1
    BOOKS_DB[new_id] = {
        "title": title,
        "author": author,
        "status": "Available"
    }
    if cover_url:
        BOOKS_DB[new_id]["cover_url"] = cover_url

    return jsonify({
        "message": "Kitap başarıyla eklendi.",
        "book_id": new_id
    }), 201



@app.route('/admin/books/<int:book_id>', methods=['DELETE'])
@token_required
def admin_delete_book(book_id):
    if request.user['role'] != "admin":
        return jsonify({"message": "Yetkiniz yok!"}), 403

    if book_id not in BOOKS_DB:
        return jsonify({"message": "Kitap bulunamadı."}), 404

    if BOOKS_DB[book_id]["status"] == "Loaned":
        return jsonify({"message": "Ödünç verilmiş kitabı silemezsiniz."}), 400

    deleted = BOOKS_DB.pop(book_id)
    return jsonify({"message": f"'{deleted['title']}' başarıyla silindi."}), 200



@app.route('/admin_info', methods=['GET'])
@token_required
def admin_info():
    if request.user['role'] != "admin":
        return jsonify({"message": "Yetkiniz yok!"}), 403

    return jsonify({
        "message": "Yönetici paneline hoş geldiniz!",
        "total_users": len(USERS_DB),
        "total_books": len(BOOKS_DB)
    }), 200


if __name__ == '__main__':
    print("Flask API Çalışıyor...")
    app.run(host='0.0.0.0', port=5000)
