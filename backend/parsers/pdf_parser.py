"""PDF Parser - pdfplumber kullanarak metin çıkarır."""
import pdfplumber
from pathlib import Path


def extract_text(file_path: str) -> dict:
    """
    PDF dosyasından metin çıkarır.
    
    Returns:
        {
            "text": str,          # Ham metin
            "pages": int,         # Sayfa sayısı
            "word_count": int,    # Kelime sayısı
            "source": str         # Kaynak dosya adı
        }
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF bulunamadı: {file_path}")

    pages_text = []
    
    with pdfplumber.open(file_path) as pdf:
        page_count = len(pdf.pages)
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                pages_text.append(text.strip())

    full_text = "\n\n".join(pages_text)
    words = full_text.split()

    return {
        "text": full_text,
        "pages": page_count,
        "word_count": len(words),
        "source": path.name
    }
