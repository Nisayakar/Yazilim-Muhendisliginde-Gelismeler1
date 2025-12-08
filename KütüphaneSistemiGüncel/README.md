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

🛡 Kimlik Doğrulama — JWT Authentication Flow
🔐 Login — POST /login
{
  "username": "admin",
  "password": "adminpass"
}


Başarılı olursa →

Authorization: Bearer <TOKEN>


📌 Token session’da tutulur
📌 API isteklerinde otomatik eklenir

📌 AUTH Kuralları
Durum	Erişim	Sonuç
Token yok	🔒	❌ 401 Unauthorized
Token var ama rol user	🔒 Admin	❌ 403 Forbidden
Token + admin	✔	Admin Panel erişimi

🧪 Backend REST API Endpointleri
Endpoint	Method	Auth	Açıklama
/login	POST	❌	Token üretir
/logout	POST	❌	Çıkış
/search	GET	❌	Kitap arama
/my_books	GET	✔	Kullanıcının kitapları
/borrow	POST	✔	Ödünç alma
/return	POST	✔	İade
/admin_info	GET	🛡 Admin	İstatistik
/admin/books	POST	🛡 Admin	Kitap ekleme
/admin/books/{id}	DELETE	🛡 Admin	Kitap silme

🖥 Kullanıcı Arayüzü
Özellik	Durum
Giriş ekranı	✔
Kitap listesi + görselller	✔
Arama + sonuç bulunamadı uyarısı	✔
Ödünç aldıklarım bölümü	✔
Admin kitap ekle / sil	✔
Sayfalama	✔
Responsive tasarım	✔

▶️ Çalıştırma (Run)
docker-compose down
docker-compose up --build

Tarayıcıdan Aç
Uygulama	Adres
UI	http://localhost:5001

API Test	http://localhost:5000/search?keyword=sefiller

👥 Test Kullanıcıları
Kullanıcı	Şifre	Rol
admin	adminpass	Admin
user1	pass123	Kullanıcı
Nisa	nisa94	Kullanıcı


Bu proje;

✔ Docker
✔ JWT Authentication
✔ Yetkilendirme yönetimi
✔ UI/UX
✔ API tasarımı
✔ Microservice Mimarisi

konularını başarılı şekilde uygulamaktadır.
