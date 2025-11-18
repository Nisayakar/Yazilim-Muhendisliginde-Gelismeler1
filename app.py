from flask import Flask, request, jsonify
from datetime import datetime

# --- Veritabanları ---
app = Flask(__name__)

USERS_DB = {
    # YÖNETİCİ ROLÜ TANIMLANDI
    "user1": {"password": "pass123", "user_id": 101, "role": "user"},
    "Nisa": {"password": "nisa94", "user_id": 102, "role": "user"},
    "admin": {"password": "adminpass", "user_id": 100, "role": "admin"} 
}

BOOKS_DB = {
    1: {"title": "Sefiller", "author": "Victor Hugo", "status": "Available"},
    2: {"title": "Suç ve Ceza", "author": "Fyodor Dostoyevski", "status": "Available"},
    3: {"title": "Karamazov Kardeşler", "author": "Fyodor Dostoyevski", "status": "Loaned", "loaned_to": 101},
    4: {"title": "Yabancı", "author": "Albert Camus", "status": "Available"}
}

# --- Oturum Yönetimi ---
# active_sessions artık kullanıcı ID'si ve ROL bilgisini tutar.
active_sessions = {}

# --- API Endpoints ---

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in USERS_DB and USERS_DB[username]['password'] == password:
        user_info = USERS_DB[username]
        
        # Oturumda kullanıcı adı, ID ve ROL bilgisini sakla
        active_sessions[username] = {
            "user_id": user_info['user_id'],
            "role": user_info['role']
        }
        
        return jsonify({
            "message": f"Giriş Başarılı. Rol: {user_info['role']}.",
            "user_id": user_info['user_id'],
            "role": user_info['role'], # ROL bilgisini Client'a gönder
            "status": "success"
        }), 200
    
    return jsonify({"message": "Geçersiz kullanıcı adı veya şifre."}), 401

@app.route('/logout', methods=['POST'])
def logout():
    active_sessions.clear()
    return jsonify({"message": "Çıkış başarılı."}), 200


@app.route('/search', methods=['GET'])
def search_books():
    keyword = request.args.get('keyword', '')
    
    results = []
    for book_id, book_info in BOOKS_DB.items():
        if keyword.lower() in book_info['title'].lower() or keyword.lower() in book_info['author'].lower():
            display_info = {
                "id": book_id, 
                "title": book_info['title'],
                "author": book_info['author'],
                "status": book_info['status']
            }
            results.append(display_info)
    
    return jsonify({"books": results}), 200

# --- Ödünç Alınan Kitapları Listeleme ---
@app.route('/my_books', methods=['GET'])
def get_my_books():
    username = request.args.get('username')
    
    if username not in active_sessions:
        return jsonify({"message": "Lütfen oturum açın."}), 401
        
    current_user_id = active_sessions[username]['user_id']
    
    borrowed_books = []
    for book_id, book in BOOKS_DB.items():
        if book.get("status") == "Loaned" and book.get("loaned_to") == current_user_id:
            borrowed_books.append({
                "id": book_id,
                "title": book["title"],
                "author": book["author"]
            })

    return jsonify({"books": borrowed_books}), 200


@app.route('/borrow', methods=['POST'])
def borrow_book():
    data = request.get_json()
    book_id = data.get('book_id')
    username = data.get('username')
    
    if username not in active_sessions:
        return jsonify({"message": "Önce giriş yapmalısınız."}), 401
    
    current_user_id = active_sessions[username]['user_id']

    if book_id not in BOOKS_DB:
        return jsonify({"message": f"Kitap ID {book_id} bulunamadı."}), 404

    book = BOOKS_DB[book_id]
    
    if book["status"] != "Available":
        return jsonify({"message": f"Kitap '{book['title']}' şu anda ödünç alınamaz durumda."}), 400

    book["status"] = "Loaned"
    book["loaned_to"] = current_user_id
    book["loan_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    return jsonify({
        "message": f"Kitap (ID: {book_id}, Başlık: {book['title']}) başarıyla ödünç alındı.",
        "status": "success"
    }), 200

# --- Kitap İade Etme ---
@app.route('/return', methods=['POST'])
def return_book():
    data = request.get_json()
    book_id = data.get('book_id')
    username = data.get('username')
    
    if username not in active_sessions:
        return jsonify({"message": "Önce giriş yapmalısınız."}), 401
    
    current_user_id = active_sessions[username]['user_id']

    if book_id not in BOOKS_DB:
        return jsonify({"message": f"Kitap ID {book_id} bulunamadı."}), 404

    book = BOOKS_DB[book_id]
    
    if book.get("status") != "Loaned":
        return jsonify({"message": f"Kitap '{book['title']}' zaten müsait durumda."}), 400
        
    if book.get("loaned_to") != current_user_id:
        return jsonify({"message": "Bu kitap sizin tarafınızdan ödünç alınmamış."}), 403

    book["status"] = "Available"
    book.pop("loaned_to", None)
    book.pop("loan_date", None)
    
    return jsonify({
        "message": f"Kitap (ID: {book_id}, Başlık: {book['title']}) başarıyla iade edildi.",
        "status": "success"
    }), 200


# --- Yöneticilere Özel Yetkilendirme Örneği ---
@app.route('/admin_info', methods=['GET'])
def admin_info():
    username = request.args.get('username')
    
    # 1. Oturum kontrolü
    if username not in active_sessions:
        return jsonify({"message": "Lütfen oturum açın."}), 401
        
    user_session = active_sessions[username]
    
    # 2. Rol kontrolü (Sadece 'admin' rolüne izin ver)
    if user_session['role'] != 'admin':
        return jsonify({"message": "Yetkiniz yok. Bu sayfa sadece yöneticilere açıktır."}), 403
        
    # Yöneticiye özel bilgi
    return jsonify({
        "message": f"Hoş geldiniz, Yönetici ({username}).",
        "total_users": len(USERS_DB),
        "total_books": len(BOOKS_DB)
    }), 200


if __name__ == '__main__':
    print("Flask Sunucusu Başlatılıyor...")
    app.run(host='0.0.0.0', port=5000)
