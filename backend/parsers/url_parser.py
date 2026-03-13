"""URL Parser - web sayfasından temiz metin çıkarır (trafilatura)."""
import trafilatura


def extract_text(url: str) -> dict:
    """
    Verilen URL'den makale/içerik metnini çıkarır.
    Reklam, menü, footer gibi gürültüyü otomatik eler.
    """
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        raise ValueError(f"URL indirilemedi: {url}")

    text = trafilatura.extract(
        downloaded,
        include_comments=False,
        include_tables=True,
        no_fallback=False
    )

    if not text:
        raise ValueError(f"Bu URL'den içerik çıkarılamadı: {url}")

    text = text.strip()
    words = text.split()

    # Başlık almaya çalış
    meta = trafilatura.extract_metadata(downloaded)
    title = meta.title if meta and meta.title else url

    return {
        "text": text,
        "pages": None,
        "word_count": len(words),
        "source": title,
        "url": url
    }
