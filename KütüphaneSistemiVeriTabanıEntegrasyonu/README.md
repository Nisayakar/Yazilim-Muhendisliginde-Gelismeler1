Ödev Teslim Raporu — Kütüphane Yönetim Sistemi
🎯 Projenin Amacı

Bu proje, çok servisli mimariye sahip bir web uygulamasının
Docker Compose ile yönetilmesi ve JWT tabanlı kimlik doğrulama uygulanması üzerine geliştirilmiştir.

Aşağıdaki gereksinimler tam olarak karşılanmıştır:

Gereksinim	Durum
İki ayrı servis (Frontend + Backend)	✔
Servislerin farklı portlarda yayınlanması	✔ (API: 5000, UI: 5001)
Dockerfile + Docker Compose kullanımı	✔
JWT veya Bearer Token ile korunan endpointler	✔
Login zorunlu → tüm kritik işlemler	✔
Admin / Kullanıcı rol ayrımı	✔
Kitap ödünç alma / iade etme	✔
Admin panel → kitap ekle/sil	✔
Arama, sayfalama, kitap bulunamadı bildirimi	✔
Bootstrap ile modern arayüz	✔
🧱 Proje Yapısı
project/
│
├─ api/
│  ├─ app.py                 → Backend API
│  ├─ requirements.txt
│  └─ Dockerfile
│
├─ client/
│  ├─ client_app.py          → Flask UI (Token Client)
│  ├─ client_requirements.txt
│  └─ Dockerfile
│
└─ docker-compose.yml        → Çoklu Servis Yönetimi

🔌 Servis Yapısı
Servis	Port	Görevi
api_service	5000	JWT Authentication + Book API
client_service	5001	Web UI – Kullanıcı arayüzü

Arayüz isteği API’ye token ile gider → Güvenli işlem sağlanır.

🛡 Kimlik Doğrulama

✔ JWT üretimi → /login
✔ Token header’da taşınır:

Authorization: Bearer <TOKEN>

Endpoint	Auth	Açıklama
POST /login	❌	Token üretir
GET /search	❌	Herkes görüntüleyebilir
GET /my_books	✔	Token şart
POST /borrow	✔	Ödünç alma
POST /return	✔	İade
GET /admin_info	✔ (Admin)	İstatistik
POST /admin/books	✔ (Admin)	Kitap ekle
DELETE /admin/books/{id}	✔ (Admin)	Kitap sil

Rol kontrolü yapılmazsa → 403 Forbidden
Token yok/yanlış → 401 Unauthorized

🌍 Kullanıcı Arayüzü (Frontend)

✔ Bootstrap temalı modern tasarım
✔ Kapak görselli kitap listesi
✔ Arama + sayfalama
✔ Admin panel → Kitap ekleme / silme

Arayüz Özellikleri (Özet)
Özellik	Durum
Login ekranı	✔
Tüm kitapların listelenmesi	✔
Ödünç alınmış kitaplar bölümü	✔
Arama yapılınca filtreleme	✔
Kitap bulunamadı uyarısı	✔
Admin panel (sadece admin görür)	✔
▶️ Çalıştırma Adımları

Terminal:

docker-compose down
docker-compose up --build


Tarayıcı:

Servis	Adres
UI	http://localhost:5001

API	http://localhost:5000/search
👥 Test Kullanıcıları
Kullanıcı	Şifre	Rol
admin	adminpass	Admin
user1	pass123	Kullanıcı
Nisa	nisa94	Kullanıcı

Admin ile giriş → Admin Paneli açılır.

🎨 Ekran Özeti

Modern kart tasarımlı kitap listesi

Her kitapta kapak fotoğrafı, yazar ve durum bilgisi

İşlem butonları (Ödünç al / Sil / İade)

Duruma göre mesajlar Bootstrap alert ile gösterilir

📌 Sonuç

Bu proje aşağıdaki konularda yetkinlik göstermektedir:

✔ Microservice Architecture
✔ RESTful API Geliştirme
✔ JWT Authentication & Authorization
✔ Docker & Docker Compose
✔ UI/UX geliştirme
✔ HTTP Request Management (Token Forwarding)