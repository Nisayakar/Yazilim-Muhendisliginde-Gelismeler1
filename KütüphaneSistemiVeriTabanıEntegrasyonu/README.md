# 📚 Kütüphane Yönetim Sistemi — Library Management System  
*(JWT Authentication + Docker Compose Multi-Service Architecture)*

---

## Proje Amacı (Project Purpose)

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

| Servis Adı         | Port | Açıklama                 | Description                     |
| ------------------ | ---- | ------------------------ | ------------------------------- |
| library_db     | 5432 | PostgreSQL Veritabanı    | Persistent Data Storage         |
| api_service    | 5000 | JWT destekli Backend API | Backend with JWT Authentication |
| client_service | 5001 | Web UI (Flask Client)    | Authentication-aware Client UI  |


---
🛡 JWT Authentication & Authorization Flow
🔐 Login — POST /login

Request Body

{
  "username": "admin",
  "password": "adminpass"
}

✅ Yetkilendirme Senaryoları
Durum (Condition)	Erişim Hedefi (Target)	Sonuç (Result)
Token yok	🔒 Korumalı Alanlar	❌ 401 Unauthorized
Token var ama rol user	🔒 Admin Paneli	❌ 403 Forbidden
Token + admin rolü	✔ Admin Paneli	✅ Erişim Başarılı

📌 Token session içinde tutulur
📌 Her istekte otomatik gönderilir

Authorization: Bearer <TOKEN>

🧪 Backend REST API Endpointleri
| Endpoint            | Method | Auth     | Açıklama (Description)             |
| ------------------- | ------ | -------- | ---------------------------------- |
| `/login`            | POST   | ❌        | Token üretir                       |
| `/logout`           | POST   | ❌        | Çıkış işlemi                       |
| `/search`           | GET    | ❌        | Kitap arama                        |
| `/my_books`         | GET    | ✔        | Kullanıcının ödünç aldığı kitaplar |
| `/borrow`           | POST   | ✔        | Kitap ödünç alma                   |
| `/return`           | POST   | ✔        | Kitap iade etme                    |
| `/admin_info`       | GET    | 🛡 Admin | Sistem istatistikleri              |
| `/admin/books`      | POST   | 🛡 Admin | Yeni kitap ekleme                  |
| `/admin/books/{id}` | DELETE | 🛡 Admin | Kitap silme                        |


🖥 Kullanıcı Arayüzü — Frontend UI Features
| Özellik (Feature)                | Durum (Status) |
| -------------------------------- | -------------- |
| Giriş Ekranı (Login Page)        | ✔              |
| Kitap Listesi + Görseller        | ✔              |
| Arama + Sonuç Bulunamadı Uyarısı | ✔              |
| Ödünç Aldıklarım Bölümü          | ✔              |
| Admin: Kitap Ekle / Sil          | ✔              |
| Sayfalama (Pagination)           | ✔              |
| Responsive Tasarım               | ✔              |


▶️ Çalıştırma — Run
docker-compose down
docker-compose up --build

🌐 Uygulama Adresleri — Application Addresses
| Uygulama (Application) | Adres (Address)                                                                                |
| ---------------------- | ---------------------------------------------------------------------------------------------- |
| Web UI (Arayüz)        | [http://localhost:5001](http://localhost:5001)                                                 |
| API Test               | [http://localhost:5000/search?keyword=sefiller](http://localhost:5000/search?keyword=sefiller) |

👥 Test Kullanıcıları — Test Users
| Kullanıcı Adı | Şifre     | Rol (Role)        |
| ------------- | --------- | ----------------- |
| admin         | adminpass | Admin (Tam Yetki) |
| user1         | pass123   | User (Standart)   |
| Nisa          | nisa94    | User (Standart)   |


🏁 Sonuç — Technology Stack & Capabilities
| Teknoloji / Feature        | Durum |
| -------------------------- | ----- |
| Docker & Containers        | ✔     |
| Multi-Service Architecture | ✔     |
| PostgreSQL & SQLAlchemy    | ✔     |
| JWT Authentication         | ✔     |
| Role-based Authorization   | ✔     |
| Microservice Deployment    | ✔     |
| UI + API Entegrasyonu      | ✔     |






