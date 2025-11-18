Kütüphane Yönetim Sistemi API

Bu proje, bir kütüphane yönetim sistemi için temel RESTful API uç noktalarını Docker üzerinde çalıştırmak üzere yapılandırılmıştır.

🐳 Docker Kullanımı

1. Docker İmajı Oluşturma

İmajı manuel olarak oluşturmak için:

docker build -t flask-library-app .


2. Uygulamayı Başlatma

İmajı oluşturup uygulamayı 5000 portu üzerinden yayınlamak için:

docker-compose up -d


3. API Testi

Uygulama çalıştıktan sonra, API uç noktalarını (Login, Search, Borrow) Postman veya Swagger UI (http://localhost:5000/swagger gibi bir adresten) üzerinden test edebilirsiniz.