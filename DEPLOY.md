# Docker & Render Deploy Rehberi

## Dosya Yerleşimi

```
SpeedReader/
├── backend/
│   ├── Dockerfile          ← buraya koy
│   ├── .dockerignore       ← buraya koy
│   ├── storage/
│   │   └── db.py           ← güncelle (env var desteği)
│   ├── main.py
│   └── requirements.txt
├── docker-compose.yml      ← kök klasöre koy
├── render.yaml             ← kök klasöre koy
├── README.md
└── ...
```

---

## Yerel Docker ile Çalıştırma

### Gereksinim
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) kurulu olmalı

### Komutlar

```powershell
# SpeedReader kök klasöründeyken:

# 1. Build et ve başlat
docker-compose up --build

# 2. Arka planda çalıştır
docker-compose up -d --build

# 3. Durdur
docker-compose down

# 4. Logları izle
docker-compose logs -f
```

Uygulama: http://localhost:8000

---

## Render.com Deploy (Ücretsiz)

### 1. Render hesabı aç
https://render.com → GitHub ile giriş yap

### 2. Yeni servis oluştur
- "New +" → "Web Service"
- GitHub repo'nu bağla: `fatihsahinbas/speedreader`
- **Runtime:** Docker
- **Dockerfile Path:** `./backend/Dockerfile`
- **Docker Context:** `./backend`

### 3. Environment Variables
```
DB_PATH = /app/data/speedreader.db
```

### 4. Disk ekle (opsiyonel, ücretsiz planda yok)
- Name: `speedreader-data`
- Mount Path: `/app/data`
- Size: 1 GB

### 5. Deploy et
"Create Web Service" → Render otomatik build edip yayınlar.

### 6. URL'yi frontend'e ekle
`index.html` içindeki API adresini güncelle:
```javascript
// ESKİ:
const API = 'http://127.0.0.1:8000';

// YENİ (Render URL'in):
const API = 'https://speedreader.onrender.com';
```

---

## Notlar

- Render ücretsiz plan 15 dakika işlem olmazsa **uyku moduna** girer
- İlk istek ~30 saniye bekleyebilir (cold start)
- Ücretsiz planda disk yok → DB her deploy'da sıfırlanır
- Kalıcı veri için Render'ın ücretli planı veya harici DB (PlanetScale, Supabase) gerekir
