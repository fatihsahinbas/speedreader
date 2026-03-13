"""
SpeedReader API - Ana FastAPI uygulaması
========================================
Tüm endpoint'leri buradan yönetiyoruz.
"""
import os
import tempfile
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Parser'lar
from parsers import pdf_parser, txt_parser, url_parser, epub_parser

# Transformer'lar
from engines import bionic, rsvp

# Storage
from storage import db

# -----------------------------------------------------------------------
app = FastAPI(
    title="SpeedReader API",
    description="Bionic Reading & RSVP hızlı okuma platformu",
    version="1.0.0"
)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

# CORS - frontend aynı makinede farklı port kullanabilir
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB init
db.init_db()

# -----------------------------------------------------------------------
# Pydantic modeller
# -----------------------------------------------------------------------

class URLRequest(BaseModel):
    url: str

class ProgressRequest(BaseModel):
    session_id: int
    mode: str                   # "bionic" | "rsvp"
    word_position: int = 0
    scroll_pct: float = 0.0
    wpm: int = 250

class StatRequest(BaseModel):
    session_id: int
    mode: str
    words_read: int
    duration_sec: int
    completed: bool = False

# -----------------------------------------------------------------------
# Yardımcı: dosyayı geçici konuma kaydet
# -----------------------------------------------------------------------

def _save_upload(file: UploadFile, suffix: str) -> str:
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp.write(file.file.read())
    tmp.close()
    return tmp.name

# -----------------------------------------------------------------------
# PARSE endpoint'leri
# -----------------------------------------------------------------------

@app.post("/api/parse/pdf")
async def parse_pdf(file: UploadFile = File(...)):
    """PDF dosyasından metin çıkar, session oluştur."""
    tmp_path = _save_upload(file, ".pdf")
    try:
        result = pdf_parser.extract_text(tmp_path)
        session_id = db.create_session(result["source"], "pdf", result["word_count"])
        return {**result, "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        os.unlink(tmp_path)


@app.post("/api/parse/txt")
async def parse_txt(file: UploadFile = File(...)):
    """TXT dosyasından metin çıkar."""
    tmp_path = _save_upload(file, ".txt")
    try:
        result = txt_parser.extract_text(tmp_path)
        session_id = db.create_session(result["source"], "txt", result["word_count"])
        return {**result, "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        os.unlink(tmp_path)


@app.post("/api/parse/epub")
async def parse_epub(file: UploadFile = File(...)):
    """EPUB dosyasından metin çıkar."""
    tmp_path = _save_upload(file, ".epub")
    try:
        result = epub_parser.extract_text(tmp_path)
        session_id = db.create_session(result["source"], "epub", result["word_count"])
        return {**result, "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        os.unlink(tmp_path)


@app.post("/api/parse/url")
async def parse_url(req: URLRequest):
    """Web URL'sinden içerik çıkar."""
    try:
        result = url_parser.extract_text(req.url)
        session_id = db.create_session(result["source"], "url", result["word_count"])
        return {**result, "session_id": session_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# -----------------------------------------------------------------------
# TRANSFORM endpoint'leri
# -----------------------------------------------------------------------

class TransformRequest(BaseModel):
    text: str
    session_id: int | None = None


@app.post("/api/transform/bionic")
async def transform_bionic(req: TransformRequest):
    """Metni Bionic Reading HTML formatına çevirir."""
    html = bionic.transform_to_html(req.text)
    return {"html": html, "session_id": req.session_id}


@app.post("/api/transform/rsvp")
async def transform_rsvp(
    req: TransformRequest,
    wpm: int = Query(default=250, ge=50, le=1500),
    chunk_size: int = Query(default=1, ge=1, le=3)
):
    """Metni RSVP kelime listesine böler + süre istatistikleri."""
    words = rsvp.transform(req.text, chunk_size=chunk_size)
    stats = rsvp.get_stats(words, wpm)
    return {
        "words": words,
        "stats": stats,
        "session_id": req.session_id
    }


# -----------------------------------------------------------------------
# PROGRESS endpoint'leri
# -----------------------------------------------------------------------

@app.post("/api/progress/save")
async def save_progress(req: ProgressRequest):
    """Okuma pozisyonunu kaydet."""
    db.save_progress(
        session_id=req.session_id,
        mode=req.mode,
        word_position=req.word_position,
        scroll_pct=req.scroll_pct,
        wpm=req.wpm
    )
    return {"ok": True}


@app.get("/api/progress/{session_id}/{mode}")
async def get_progress(session_id: int, mode: str):
    """Kaydedilmiş okuma pozisyonunu getir."""
    progress = db.get_progress(session_id, mode)
    if not progress:
        return {"found": False}
    return {"found": True, **progress}


# -----------------------------------------------------------------------
# STATS endpoint'leri
# -----------------------------------------------------------------------

@app.post("/api/stats/save")
async def save_stat(req: StatRequest):
    """Okuma istatistiği kaydet."""
    db.save_stat(
        session_id=req.session_id,
        mode=req.mode,
        words_read=req.words_read,
        duration_sec=req.duration_sec,
        completed=req.completed
    )
    return {"ok": True}


@app.get("/api/stats")
async def get_stats():
    """Tüm okuma istatistiklerini getir."""
    return {"stats": db.get_all_stats()}


@app.get("/api/sessions")
async def get_sessions(limit: int = Query(default=10, ge=1, le=50)):
    """Son okunan içerikleri getir."""
    return {"sessions": db.get_recent_sessions(limit)}


@app.get("/api/sessions/{session_id}")
async def get_session(session_id: int):
    """Tek session + ilerleme bilgisi."""
    data = db.get_session_with_progress(session_id)
    if not data:
        raise HTTPException(status_code=404, detail="Session bulunamadı")
    return data


@app.get("/api/stats/dashboard")
async def get_dashboard():
    """Dashboard özet istatistikleri."""
    return db.get_dashboard_summary()


# -----------------------------------------------------------------------
# Sağlık kontrolü
# -----------------------------------------------------------------------

@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}