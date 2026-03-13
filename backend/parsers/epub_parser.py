"""EPUB Parser - ebooklib + html temizleme ile metin çıkarır."""
import ebooklib
from ebooklib import epub
from html.parser import HTMLParser
from pathlib import Path


class _HTMLStripper(HTMLParser):
    """Basit HTML tag temizleyici."""
    def __init__(self):
        super().__init__()
        self._lines = []

    def handle_data(self, data):
        stripped = data.strip()
        if stripped:
            self._lines.append(stripped)

    def get_text(self) -> str:
        return " ".join(self._lines)


def _strip_html(html_content: str) -> str:
    stripper = _HTMLStripper()
    stripper.feed(html_content)
    return stripper.get_text()


def extract_text(file_path: str) -> dict:
    """
    EPUB dosyasından tüm bölümleri okuyup birleştirir.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"EPUB bulunamadı: {file_path}")

    book = epub.read_epub(file_path)

    # Kitap başlığı
    title = book.get_metadata("DC", "title")
    book_title = title[0][0] if title else path.stem

    chapters = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        content = item.get_content().decode("utf-8", errors="ignore")
        text = _strip_html(content).strip()
        if len(text) > 100:  # Çok kısa (nav, toc) bölümleri atla
            chapters.append(text)

    full_text = "\n\n".join(chapters)
    words = full_text.split()

    return {
        "text": full_text,
        "pages": len(chapters),   # EPUB'da "bölüm" sayısı
        "word_count": len(words),
        "source": book_title
    }
