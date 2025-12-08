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

## 🔌 Servis Detayları — Services

| Servis | Port | Açıklama | Description |
|--------|-----:|----------|-------------|
| api_service | 5000 | JWT destekli Backend API | Backend with JWT Auth |
| client_service | 5001 | Web UI (Flask Client) | Authentication-aware client UI |

---
🛡 JWT Authentication & Authorization Flow
🔐 Login — POST /login
{
  "username": "admin",
  "password": "adminpass"
}

Durum	Erişim	Sonuç
Token yok	❌	401 Unauthorized
User token ile Admin endpoint	❌	403 Forbidden
Admin token	✔	Admin Panel erişimi

📌 Token session içinde tutulur
📌 Authorization header ile otomatik gönderilir
→ Authorization: Bearer <TOKEN>

🧪 Backend REST API Endpoints
Endpoint	Method	Auth	Açıklama
/login	POST	❌	JWT Token üretir
/logout	POST	❌	Çıkış
/search	GET	❌	Kitap arama
/my_books	GET	✔	Kullanıcının kitapları
/borrow	POST	✔	Ödünç alma
/return	POST	✔	İade
/admin_info	GET	🛡 Admin	İstatistik
/admin/books	POST	🛡 Admin	Kitap ekleme
/admin/books/{id}	DELETE	🛡 Admin	Kitap silme
🖥 Kullanıcı Arayüzü — Frontend UI Features
Özellik	✓
Giriş ekranı	✔
Kitap listesi + kapak görselleri	✔
Arama ve “bulunamadı” uyarısı	✔
Sayfalama	✔
Ödünç aldıklarım listesi	✔
Admin kitap ekleme	✔
Admin kitap silme	✔
Modern Bootstrap & Responsive	✔
▶️ Çalıştırma — Run
docker-compose down
docker-compose up --build

Uygulama	Adres
UI	http://localhost:5001

API	http://localhost:5000/search?keyword=sefiller
👥 Test Kullanıcıları — Test Users
Kullanıcı	Şifre	Rol
admin	adminpass	Admin
user1	pass123	User
Nisa	nisa94	User
🏁 Sonuç — Conclusion

Bu proje başarıyla göstermektedir:

Teknoloji	✓
Docker & Containers	✔
Multi-Service Architecture	✔
JWT Authentication	✔
Role-based Authorization	✔
Microservice Deployment	✔
UI + API entegrasyonu	✔
