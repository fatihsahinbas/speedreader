# ── Build stage ──────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

# uv ile hızlı kurulum
COPY requirements.txt .
RUN pip install --no-cache-dir uv && \
    uv pip install --system --no-cache -r requirements.txt

# ── Runtime stage ─────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# Sistem bağımlılıkları (pdfplumber için)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpoppler-cpp-dev \
    && rm -rf /var/lib/apt/lists/*

# Kurulu paketleri builder'dan kopyala
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Uygulama dosyalarını kopyala
COPY . .

# Veri klasörü (SQLite DB burada tutulacak)
RUN mkdir -p /app/data

# Port
EXPOSE 8000

# Çalıştır
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
