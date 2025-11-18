# Temel imaj olarak resmi Python 3.11 Slim imajını kullan
# Slim versiyonu, geliştirme araçları gibi gereksiz dosyaları içermez ve imaj boyutunu küçültür.
FROM python:3.11-slim

# Uygulamanın çalışacağı dizini ayarla
WORKDIR /app

# Gereksinimler dosyasını WORKDIR'a kopyala
COPY requirements.txt .

# Gerekli Python bağımlılıklarını kur
# --no-cache-dir, daha temiz bir imaj için pip önbelleğini devre dışı bırakır
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama kodunu WORKDIR'a (yani /app) kopyala
COPY app.py .

# Flask uygulamasının varsayılan olarak dinleyeceği portu belirt (isteğe bağlı ama iyi bir uygulama)
EXPOSE 5000

# Uygulamayı başlatmak için komut. Gunicorn gibi bir WSGI sunucusu kullanmak daha iyidir
# ancak bu örnekte basitlik için doğrudan Flask'ın dahili sunucusunu kullanıyoruz.
# 0.0.0.0'a bağlanmak, container dışından erişilebilir olmasını sağlar.
CMD ["python", "app.py"]