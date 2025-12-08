# 📚 Kütüphane Yönetim Sistemi — Library Management System  
*(JWT Authentication + Docker Compose Multi-Service Architecture)*

---

## 🇹🇷 Proje Amacı (Project Purpose)

Bu proje; Backend geliştiren öğrencilerin uygulamalarını Docker Compose ile **çok servisli mimari** şeklinde çalıştırdığı ve **JWT (Bearer Token) ile kimlik doğrulama & yetkilendirme** yaptığı örnek bir sistemdir.

This project demonstrates a **multi-service architecture** using Docker Compose and **JWT-based authentication & authorization**.

---

## ✔ Gereksinim Karşılama Tablosu — Requirements Status

| Özellik / Feature | Durum / Status |
|------------------|:--------------:|
| 2 ayrı servis (Frontend + Backend) | ✔ |
| Servislerin farklı portlarda çalışması | ✔ (5000 API – 5001 UI) |
| Dockerfile ve Docker Compose | ✔ |
| JWT Token Authentication | ✔ |
| Rol bazlı erişim (Admin / User) | ✔ |
| Ödünç alma / İade işlemleri | ✔ |
| Admin Panel — Kitap ekleme & silme | ✔ |
| Arama, sayfalama, hata mesajları | ✔ |
| Kapak görselleri ve modern UI | ✔ |
| Responsive Bootstrap arayüz | ✔ |

---

## 🧱 Proje Mimarisi — Project Architecture

project/
│
├─ api/ (Backend — Flask API)
│ ├─ app.py
│ ├─ requirements.txt
│ └─ Dockerfile
│
├─ client/ (Frontend — Flask Client UI)
│ ├─ client_app.py
│ ├─ client_requirements.txt
│ └─ Dockerfile
│
└─ docker-compose.yml



---

## 🔌 Servis Detayları — Services

| Servis | Port | Açıklama | Description |
|--------|-----:|----------|-------------|
| api_service | 5000 | JWT destekli Backend API | Backend with JWT Auth |
| client_service | 5001 | Web UI (Flask Client) | Authentication-aware client UI |

---

## 🛡 JWT Kimlik Doğrulama — Authentication Flow

### 🔑 Login — POST `/login`
```json
{
  "username": "admin",
  "password": "adminpass"
}
Başarılı olursa:

Authorization: Bearer <TOKEN>
Token session içinde saklanır ve API isteklerinde otomatik gönderilir.

Login olmadan → ❌ Korunan endpointlere erişilemez
Without login → ❌ Protected endpoints are blocked

📌 Endpoint Listesi — Backend REST Endpoints
Endpoint	Method	Auth	Açıklama / Description
/login	POST	❌	Login, returns JWT
/logout	POST	❌	Logout response
/search	GET	❌	Public book search
/my_books	GET	✔	Borrowed books
/borrow	POST	✔	Borrow a book
/return	POST	✔	Return borrowed
/admin_info	GET	✔(Admin)	Admin stats
/admin/books	POST	✔(Admin)	Add book
/admin/books/{id}	DELETE	✔(Admin)	Delete book

🎨 Kullanıcı Arayüzü Özellikleri — UI Features
Feature	Status
Login ekranı & yetkilendirme	✔
Kapak görselleri	✔
Kitap arama	✔
Sayfalama	✔
Ödünç aldıklarım	✔
Admin panel	✔
Bootstrap modern UI	✔

📌 Giriş yapmadan hiçbir işlem yapılamaz.

▶️ Çalıştırma — Run
docker-compose down
docker-compose up --build

📍 Tarayıcı adresleri:

Servis	URL
Web UI	http://localhost:5001
API Test	http://localhost:5000/search?keyword=yabancı

👥 Test Kullanıcıları — Test User Accounts
Kullanıcı	Şifre	Rol
admin	adminpass	admin
user1	pass123	user
Nisa	nisa94	user

Bu proje;

✔ Docker
✔ JWT Authentication
✔ Yetkilendirme yönetimi
✔ UI/UX
✔ API tasarımı
✔ Microservice Mimarisi

konularını başarılı şekilde uygulamaktadır.
