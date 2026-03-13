"""TXT Parser - düz metin dosyalarını okur."""
from pathlib import Path


def extract_text(file_path: str) -> dict:
    """
    TXT dosyasından metin çıkarır, encoding otomatik tespit edilir.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Dosya bulunamadı: {file_path}")

    # Türkçe karakterler için encoding sırası dene
    encodings = ["utf-8", "utf-8-sig", "cp1254", "iso-8859-9", "latin-1"]
    text = None

    for enc in encodings:
        try:
            text = path.read_text(encoding=enc)
            break
        except (UnicodeDecodeError, LookupError):
            continue

    if text is None:
        raise ValueError(f"Dosya encoding tespit edilemedi: {file_path}")

    text = text.strip()
    words = text.split()

    return {
        "text": text,
        "pages": None,
        "word_count": len(words),
        "source": path.name
    }
