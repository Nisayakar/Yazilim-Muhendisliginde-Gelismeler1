📘 Kütüphane Yönetim Sistemi

(Flask + Docker + Çoklu Servis Mimari Uygulaması)

Bu proje, kullanıcıların kitap arayabildiği, ödünç alıp iade edebildiği basit bir RESTful API + Client UI sistemidir.
Backend ve Client, Docker Compose ile birlikte yönetilmektedir.

🧩 Servis Mimarisi
Servis	Görev	Port
API (Backend)	Login, Search, Borrow, Admin işlemleri	5000
Client (Frontend)	Kullanıcı arayüzü ile kitap işlemleri	5001
🐳 Docker Kullanımı
1️⃣ Tüm Servisleri Çalıştır
docker-compose up --build


Çalıştırdıktan sonra:

Link	Açıklama
http://localhost:5001
	Kullanıcı Arayüzü
http://localhost:5000
	API Servisi
2️⃣ Servisleri Durdur
docker-compose down

🔑 Örnek Giriş Bilgileri
Kullanıcı	Şifre	Rol
admin	admin	Admin

Admin, yönetici paneli butonunu görür.

🔍 API Testi

Swagger veya Postman üzerinden test edebilirsiniz:

Uç Nokta	Amaç
/login	Kullanıcı giriş
/search	Kitap arama
/borrow	Kitap ödünç alma
/return	İade işlemleri
/admin_info	Yönetici bilgisi (sadece admin)

🆕 3 Aralık Docker & GitHub Ödevi Kapsamındaki Güncellemeler

Yapılan İşlem	Durum
Client uygulamasına footer eklendi ve tarih dinamikleştirildi	
UI düzenlemeleri yapıldı	
Docker bağımlılıkları düzeltildi	
Docker Compose ile iki servis birlikte çalıştığı test edildi	
Commit + Push işlemi yapıldı	

Commit Mesajı:

3 Aralık Ödevi: Yeni footer + Docker fix + UI iyileştirme

📦 Kullanılan Teknolojiler

Python 3.11

Flask & Flask-CORS

Docker & Docker Compose

Requests

Gunicorn

HTML/CSS
