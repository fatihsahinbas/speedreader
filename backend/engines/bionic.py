"""
Bionic Reading Transformer
--------------------------
Her kelimenin ilk yarısını <b> tag'i ile kalın yapar.
Beyin ilk yarıyı görünce kelimeyi tamamlar — okuma hızlanır.

Analoji: Trafik levhalarına bakarken tüm metni okumadan anlarsın.
Bionic reading aynı ilkeyi kullanır: beyin eksik bilgiyi tamamlar.
"""
import re


def _bionic_word(word: str) -> str:
    """
    Tek kelimeyi bionic formata çevirir.
    
    Örnekler:
        "merhaba"  → "<b>mer</b>haba"
        "kitap"    → "<b>ki</b>tap"
        "a"        → "<b>a</b>"
        "Python"   → "<b>Py</b>thon"
    """
    # Başındaki/sonundaki noktalama işaretlerini koru
    prefix_match = re.match(r'^([^a-zA-ZğüşıöçĞÜŞİÖÇ]*)', word)
    suffix_match = re.search(r'([^a-zA-ZğüşıöçĞÜŞİÖÇ]*)$', word)

    prefix = prefix_match.group(1) if prefix_match else ""
    suffix = suffix_match.group(1) if suffix_match else ""
    core = word[len(prefix):len(word) - len(suffix)] if suffix else word[len(prefix):]

    if not core:
        return word

    # Kalın yapılacak harf sayısı: en az 1, maksimum ceil(len/2)
    bold_len = max(1, -(-len(core) // 2))  # ceiling division
    bold_part = core[:bold_len]
    rest_part = core[bold_len:]

    return f"{prefix}<b>{bold_part}</b>{rest_part}{suffix}"


def transform(text: str) -> str:
    """
    Tüm metni Bionic Reading formatına çevirir.
    Paragraf yapısını (boş satırlar) korur.
    
    Returns:
        HTML string — <b> tagları içeren metin
    """
    paragraphs = text.split("\n")
    result_paragraphs = []

    for paragraph in paragraphs:
        if not paragraph.strip():
            result_paragraphs.append("")
            continue

        words = paragraph.split(" ")
        bionic_words = [_bionic_word(w) for w in words]
        result_paragraphs.append(" ".join(bionic_words))

    return "\n".join(result_paragraphs)


def transform_to_html(text: str) -> str:
    """
    Paragrafları <p> taglarına sarar — direkt HTML render için.
    """
    bionic_text = transform(text)
    paragraphs = bionic_text.split("\n")
    html_parts = []

    for p in paragraphs:
        if p.strip():
            html_parts.append(f"<p>{p}</p>")

    return "\n".join(html_parts)
