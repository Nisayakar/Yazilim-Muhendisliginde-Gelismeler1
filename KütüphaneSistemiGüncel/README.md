📌 README — Kütüphane Yönetim Sistemi

(JWT + Docker Compose Multi-Service Architecture)


Türkçe Açıklama — Library Management System
🎯 Proje Amacı

Bu proje; Backend geliştiren öğrencilerin uygulamalarını Docker Compose ile çok servisli mimari şeklinde çalıştırdığını ve JWT (Bearer Token) ile güvenli erişim sağladığını göstermek için geliştirilmiştir.

✔️ Gereksinim Karşılama Tablosu
Özellik / Gereksinim	Durum
Backend + Frontend ayrı servis	✔
Servisler farklı portlarda yayınlanır	✔ (5000 API, 5001 UI)
Dockerfile + Docker Compose ile çalışır	✔
JWT ile korunan endpoint	✔
Admin & User rol yönetimi	✔
Ödünç alma / iade	✔
Admin kitap ekle / sil	✔
Arama, sayfalama, sonuç bulunamadı UI	✔
Bootstrap modern UI	✔

🧱 Mimari — Project Architecture
project/
│
├─ api/ (Backend — Flask API)
│   ├─ app.py
│   ├─ requirements.txt
│   └─ Dockerfile
│
├─ client/ (Frontend — Flask Client UI)
│   ├─ client_app.py
│   ├─ client_requirements.txt
│   └─ Dockerfile
│
└─ docker-compose.yml

🔌 Servis Portları
Servis	Görev	Port
api_service	JWT destekli Backend API	5000
client_service	Web UI — Flask Client UI	5001

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

