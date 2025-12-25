import os
from flask import Flask, request, jsonify
from datetime import datetime
import jwt
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


SECRET_KEY = "super_secret_jwt_key"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)



class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default="user")

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default="Available")
    cover_url = db.Column(db.String(500))
    loan_date = db.Column(db.String(50))
    
    loaned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)


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


def seed_data():
    if User.query.first() is None:
        
        users = [
            User(username="user1", password="pass123", role="user"),
            User(username="Nisa", password="nisa94", role="user"),
            User(username="admin", password="adminpass", role="admin")
        ]
        db.session.add_all(users)
        
    
        books = [
            Book(title="Sefiller", author="Victor Hugo", cover_url="https://covers.openlibrary.org/b/id/7222246-L.jpg"),
            Book(title="Suç ve Ceza", author="Fyodor Dostoyevski", cover_url="https://covers.openlibrary.org/b/id/8231858-L.jpg"),
            Book(title="1984", author="George Orwell", cover_url="https://covers.openlibrary.org/b/id/1535410-L.jpg"),
            Book(title="Simyacı", author="Paulo Coelho", cover_url="https://covers.openlibrary.org/b/id/13266540-L.jpg"),
            Book(title="Hayvan Çiftliği", author="George Orwell", cover_url="https://covers.openlibrary.org/b/id/9641666-L.jpg")
        ]
        db.session.add_all(books)
        db.session.commit()
        print("--- Veritabanı başlangıç verileriyle dolduruldu ---")



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        token = jwt.encode(
            {"username": user.username, "role": user.role, "user_id": user.id},
            SECRET_KEY,
            algorithm="HS256"
        )
        return jsonify({
            "message": f"Giriş Başarılı. Rol: {user.role}.",
            "token": token,
            "role": user.role
        }), 200

    return jsonify({"message": "Geçersiz kullanıcı adı veya şifre."}), 401

@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Çıkış başarılı."}), 200

@app.route('/search', methods=['GET'])
def search_books():
    keyword = request.args.get('keyword', '').strip()
    
    query = Book.query
    if keyword:
        search = f"%{keyword}%"
        query = query.filter(
            (Book.title.ilike(search)) | (Book.author.ilike(search))
        )
    
    books = query.all()
    results = [{
        "id": b.id, "title": b.title, "author": b.author, 
        "status": b.status, "cover_url": b.cover_url
    } for b in books]

    return jsonify({"books": results}), 200

@app.route('/my_books', methods=['GET'])
@token_required
def get_my_books():
    current_user_id = request.user['user_id']
    books = Book.query.filter_by(loaned_to=current_user_id, status="Loaned").all()
    
    borrowed_books = [{
        "id": b.id, "title": b.title, "author": b.author, "cover_url": b.cover_url
    } for b in books]

    return jsonify({"books": borrowed_books}), 200

@app.route('/borrow', methods=['POST'])
@token_required
def borrow_book():
    data = request.get_json() or {}
    book_id = data.get('book_id')
    current_user_id = request.user['user_id']

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Kitap bulunamadı."}), 404

    if book.status != "Available":
        return jsonify({"message": "Bu kitap şu an müsait değil!"}), 400

    book.status = "Loaned"
    book.loaned_to = current_user_id
    book.loan_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db.session.commit()
    
    return jsonify({"message": "Kitap başarıyla ödünç alındı."}), 200

@app.route('/return', methods=['POST'])
@token_required
def return_book():
    data = request.get_json() or {}
    book_id = data.get('book_id')
    current_user_id = request.user['user_id']

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Kitap bulunamadı!"}), 404

    if book.loaned_to != current_user_id:
        return jsonify({"message": "Bu kitap sizin değil!"}), 403

    book.status = "Available"
    book.loaned_to = None
    book.loan_date = None
    db.session.commit()

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

    new_book = Book(title=title, author=author, cover_url=cover_url)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({"message": "Kitap başarıyla eklendi.", "book_id": new_book.id}), 201

@app.route('/admin/books/<int:book_id>', methods=['DELETE'])
@token_required
def admin_delete_book(book_id):
    if request.user['role'] != "admin":
        return jsonify({"message": "Yetkiniz yok!"}), 403

    book = Book.query.get(book_id)
    if not book:
        return jsonify({"message": "Kitap bulunamadı."}), 404

    if book.status == "Loaned":
        return jsonify({"message": "Ödünç verilmiş kitabı silemezsiniz."}), 400

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Kitap başarıyla silindi."}), 200

@app.route('/admin_info', methods=['GET'])
@token_required
def admin_info():
    if request.user['role'] != "admin":
        return jsonify({"message": "Yetkiniz yok!"}), 403

    user_count = User.query.count()
    book_count = Book.query.count()

    return jsonify({
        "message": "Yönetici paneline hoş geldiniz!",
        "total_users": user_count,
        "total_books": book_count
    }), 200

if __name__ == '__main__':
    with app.app_context():

        db.create_all()
        seed_data()
    print("Flask API (PostgreSQL Destekli) Çalışıyor...")
    app.run(host='0.0.0.0', port=5000)