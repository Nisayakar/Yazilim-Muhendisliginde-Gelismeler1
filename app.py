from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

USERS_DB = {
    "user1": {"password": "pass123", "user_id": 101},
    "admin": {"password": "adminpass", "user_id": 100}
}

BOOKS_DB = {
    1: {"title": "Sefiller", "author": "Victor Hugo", "status": "Available"},
    2: {"title": "Suç ve Ceza", "author": "Fyodor Dostoyevski", "status": "Available"},
    3: {"title": "Karamazov Kardeşler", "author": "Fyodor Dostoyevski", "status": "Loaned", "loaned_to": 101},
    4: {"title": "Yabancı", "author": "Albert Camus", "status": "Available"}
}


active_sessions = {}
current_user_id = None



@app.route('/login', methods=['POST'])
def login():
    global current_user_id
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')


    if username in USERS_DB and USERS_DB[username]['password'] == password:
        
        user_id = USERS_DB[username]['user_id']
        active_sessions[username] = user_id 
        current_user_id = user_id
        return jsonify({
            "message": "Giriş Başarılı. Ana menü gösteriliyor.",
            "user_id": user_id,
            "status": "success"
        }), 200
    
 
    return jsonify({"message": "Geçersiz kullanıcı adı veya şifre."}), 401



@app.route('/search', methods=['GET'])
def search_books():
   
    keyword = request.args.get('keyword', '')
    
  
    results = []
    for book_id, book_info in BOOKS_DB.items():
        if keyword.lower() in book_info['title'].lower() or keyword.lower() in book_info['author'].lower():
            results.append({"id": book_id, **book_info})

    
    return jsonify({"books": results}), 200



@app.route('/borrow', methods=['POST'])
def borrow_book():
    global current_user_id
    if current_user_id is None:
        return jsonify({"message": "Önce giriş yapmalısınız."}), 401
        
    data = request.get_json()
    book_id = data.get('book_id')

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



@app.route('/logout', methods=['POST'])
def logout():
    global current_user_id
    active_sessions.pop(next((k for k, v in active_sessions.items() if v == current_user_id), None), None)
    current_user_id = None
    
   
    return jsonify({"message": "Çıkış başarılı. Giriş ekranına yönlendiriliyorsunuz."}), 200

if __name__ == '__main__':
    print("Flask Sunucusu Başlatılıyor...")
    app.run(debug=True)