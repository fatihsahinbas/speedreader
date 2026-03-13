# SpeedReader ⚡

> **Bionic Reading ve RSVP teknikleriyle okuma hızını 2 katına çıkar.**

PDF, TXT, EPUB ve web sayfalarını anında hızlı okuma formatına dönüştüren, Python/FastAPI tabanlı açık kaynak okuma platformu.

---

## ✨ Özellikler

| Özellik | Açıklama |
|---|---|
| 🧠 **Bionic Reading** | Her kelimenin ilk yarısı kalınlaştırılır — beyin boşluğu tamamlar |
| ⚡ **RSVP Flash** | Kelimeler sırayla ekranda belirir, göz hareketi sıfıra iner |
| 📄 **PDF Desteği** | `pdfplumber` ile sayfa sayfa metin çıkarma |
| 📚 **EPUB Desteği** | e-Kitap formatı tam destek |
| 🌐 **URL Desteği** | Herhangi bir web sayfasını otomatik temizleyip okuma moduna al |
| 💾 **İlerleme Kaydetme** | Kaldığın yerden devam et |
| 📊 **İstatistik Dashboard** | Günlük okuma, WPM trendi, geçmiş |
| 🌙 **Koyu/Açık Tema** | Göz yorgunluğunu azalt |
| ⊙ **Odak Modu** | UI tamamen kaybolur, sadece metin kalır |

---

## 🚀 Kurulum

### Gereksinimler
- Python 3.12+
- [uv](https://github.com/astral-sh/uv) (önerilen) veya pip

### 1. Repoyu klonla
```bash
git clone https://github.com/kullaniciadi/speedreader.git
cd speedreader/backend
```

### 2. Sanal ortam oluştur ve bağımlılıkları yükle
```bash
uv venv
.venv\Scripts\activate   # Windows
# veya: source .venv/bin/activate  # Linux/Mac

uv pip install -r requirements.txt
```

### 3. Çalıştır
```bash
uvicorn main:app --reload
```

### 4. Tarayıcıda aç
```
http://127.0.0.1:8000
```

> Swagger API dökümantasyonu: `http://127.0.0.1:8000/docs`

---

## 🗂 Proje Yapısı

```
speedreader/
├── backend/
│   ├── main.py                  # FastAPI uygulaması
│   ├── requirements.txt
│   ├── parsers/
│   │   ├── pdf_parser.py        # PDF → metin (pdfplumber)
│   │   ├── txt_parser.py        # TXT (Türkçe encoding desteği)
│   │   ├── url_parser.py        # Web scraping (trafilatura)
│   │   └── epub_parser.py       # EPUB (ebooklib)
│   ├── engines/
│   │   ├── bionic.py            # Bionic Reading motoru
│   │   └── rsvp.py              # RSVP kelime dizisi
│   ├── storage/
│   │   └── db.py                # SQLite (oturum, ilerleme, istatistik)
│   └── frontend/
│       └── index.html           # Tek sayfa uygulama
```

---

## 🔌 API Endpoint'leri

### Parse
| Method | Endpoint | Açıklama |
|---|---|---|
| POST | `/api/parse/pdf` | PDF yükle |
| POST | `/api/parse/txt` | TXT yükle |
| POST | `/api/parse/epub` | EPUB yükle |
| POST | `/api/parse/url` | URL'den içerik çek |

### Transform
| Method | Endpoint | Açıklama |
|---|---|---|
| POST | `/api/transform/bionic` | Bionic HTML üret |
| POST | `/api/transform/rsvp` | Kelime listesi üret |

### Progress & Stats
| Method | Endpoint | Açıklama |
|---|---|---|
| POST | `/api/progress/save` | İlerleme kaydet |
| GET | `/api/progress/{id}/{mode}` | İlerleme getir |
| POST | `/api/stats/save` | İstatistik kaydet |
| GET | `/api/stats/dashboard` | Dashboard verileri |

---

## 🛠 Teknoloji Stack'i

**Backend**
- [FastAPI](https://fastapi.tiangolo.com/) — modern Python web framework
- [pdfplumber](https://github.com/jsvine/pdfplumber) — PDF text extraction
- [trafilatura](https://github.com/adbar/trafilatura) — web content extraction
- [ebooklib](https://github.com/aerkalov/ebooklib) — EPUB parsing
- SQLite — hafif, dosya tabanlı veritabanı

**Frontend**
- Vanilla JS — sıfır bağımlılık
- Playfair Display + Syne + JetBrains Mono — tipografi
- CSS Custom Properties — tema sistemi

---

## 🗺 Yol Haritası

- [ ] Kullanıcı hesapları ve bulut senkronizasyonu
- [ ] Tarayıcı eklentisi (Chrome/Firefox)
- [ ] Mobil PWA
- [ ] AI özet (okumadan önce içeriği özetle)
- [ ] Kelime vurgulama ve sözlük entegrasyonu
- [ ] Çoklu dil desteği

---

## 🤝 Katkıda Bulunma

Lütfen [CONTRIBUTING.md](CONTRIBUTING.md) dosyasını incele.

---

## 📄 Lisans

MIT — bkz. [LICENSE](LICENSE)

---

<p align="center">
  <strong>Fatih Şahinbaş</strong> tarafından yapıldı · Bursa, Türkiye<br>
  <a href="https://linkedin.com/in/fatihsahinbas">LinkedIn</a>
</p>