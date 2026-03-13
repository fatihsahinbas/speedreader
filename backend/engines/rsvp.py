"""
RSVP (Rapid Serial Visual Presentation) Transformer
----------------------------------------------------
Metni kelime listesine böler. Frontend bu listeyi alır,
WPM ayarına göre timer ile ekranda kelime kelime gösterir.

Analoji: Sinema filmi aslında saatte 24 kare — gözün
birleştirip hareket olarak algılaması gibi, RSVP da
kelimeleri art arda gösterip okuma hissini yaratır.
"""
import re


def transform(text: str, chunk_size: int = 1) -> list[str]:
    """
    Metni kelime (veya kelime grubu) listesine böler.
    
    Args:
        text: Ham metin
        chunk_size: Kaç kelime bir arada gösterilsin (varsayılan: 1)
    
    Returns:
        ["Merhaba", "dünya", "bu", "bir", "test", ...]
    """
    # Çoklu boşluk ve satır sonlarını temizle
    clean = re.sub(r'\s+', ' ', text).strip()
    words = clean.split(' ')
    words = [w for w in words if w]  # boş string'leri at

    if chunk_size <= 1:
        return words

    # Chunk gruplama: ["hızlı okuma", "tekniği ile", ...]
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)

    return chunks


def get_stats(words: list[str], wpm: int) -> dict:
    """
    RSVP oturumu için süre istatistikleri hesaplar.
    
    Args:
        words: Kelime listesi
        wpm: Dakikadaki kelime sayısı
    
    Returns:
        {
            "total_words": 1500,
            "estimated_minutes": 5.0,
            "estimated_seconds": 300,
            "interval_ms": 200   # Her kelime arası bekleme
        }
    """
    total = len(words)
    interval_ms = int(60_000 / wpm)
    total_seconds = int((total / wpm) * 60)

    return {
        "total_words": total,
        "estimated_minutes": round(total / wpm, 1),
        "estimated_seconds": total_seconds,
        "interval_ms": interval_ms
    }
