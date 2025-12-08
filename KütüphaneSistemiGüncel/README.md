📚 Kütüphane Yönetim Sistemi

(JWT Authentication + Docker Compose Multi-Service Architecture)

🎯 Projenin Amacı

Bu proje; Backend geliştiren öğrencilerin uygulamalarını Docker Compose ile çok servisli mimari şeklinde çalıştırdığı ve
JWT (Bearer Token) ile kimlik doğrulama & yetkilendirme yaptığı örnek bir sistemdir.

✔ Gereksinim Karşılama Tablosu
Gereksinim	Durum
2 ayrı servis (Frontend + Backend)	✔
Servislerin 2 farklı port üzerinden sunulması	✔ (5000 API, 5001 UI)
Dockerfile + Docker Compose ile çalıştırma	✔
JWT Token ile güvenli erişim	✔
Giriş yapmayan kişinin erişemeyeceği endpoint	✔
Admin ve Kullanıcı rol ayrımı	✔
Kitap ödünç alma & iade işlemleri	✔
Admin Panel üzerinden kitap ekleme / silme	✔
Arama, sayfalama, hata durum mesajları	✔
Şık & responsive UI	✔

🔥 Gereksinimlerin üstüne; kapak görselleri, sayfalama, admin paneli ve Bootstrap UI gibi ekstra özellikler eklenmiştir.

🧱 Proje Dizini (Architecture)
project/
│
├─ api/
│  ├─ app.py
│  ├─ requirements.txt
│  └─ Dockerfile
│
├─ client/
│  ├─ client_app.py
│  ├─ client_requirements.txt
│  └─ Dockerfile
│
└─ docker-compose.yml

🔌 Servisler
Servis	Port	Açıklama
api_service	5000	JWT destekli Backend API
client_service	5001	Web UI – Flask Client
🧿 JWT Kimlik Doğrulama Akışı

/login → kullanıcı adı & parola ile JWT token üretir

Token Session’da tutulur ve API isteklerinde
Authorization: Bearer <TOKEN> başlığı ile gönderilir

Yetkisiz erişimde:

401 Unauthorized

Admin olmayan kullanıcı Admin endpointine girerse → 403 Forbidden

🧪 API Endpointleri
Endpoint	Method	Auth	Açıklama
/login	POST	❌	Token üret
/logout	POST	❌	Çıkış yanıtı
/search	GET	❌	Kitap arama
/my_books	GET	✔	Kullanıcının ödünç aldığı kitapları getir
/borrow	POST	✔	Kitap ödünç alma
/return	POST	✔	Kitap iade etme
/admin_info	GET	✔ (Admin)	Yönetim bilgileri
/admin/books	POST	✔ (Admin)	Kitap ekleme
/admin/books/{id}	DELETE	✔ (Admin)	Kitap silme
🎨 Kullanıcı Arayüzü Özellikleri (UI)
Özellik	Durum
Giriş ekranı	✔
Kapak resimli kitap listesi	✔
Arama	✔
Sayfalama (5’erli gösterim)	✔
Kitap bulunamadı mesajı	✔
Ödünç alınan kitaplar bölümü	✔
Admin panel	✔
Bootstrap ile modern UI	✔

📌 Giriş yapmayan hiçbir işlem yapamaz — sistem tamamen korumalıdır.

▶️ Çalıştırma

Sadece bu iki komut yeterlidir:

docker-compose down
docker-compose up --build


Sonra tarayıcıdan:

Servis	Adres
UI	http://localhost:5001

API Örnek	http://localhost:5000/search?keyword=yabancı
👥 Test Kullanıcıları
Kullanıcı	Şifre	Rol
admin	adminpass	Admin
user1	pass123	User
Nisa	nisa94	User

Admin rolü ile giriş yapınca ➝ Admin Panel otomatik görünür.

🎓 Sonuç

Bu proje kapsamında:

✔ JWT Authentication
✔ Rol bazlı yetkilendirme
✔ Docker Compose ile 2 servisli mimari
✔ UI + Backend entegrasyonu
✔ Modern UX
✔ API güvenliği

tam olarak uygulanmıştır.
