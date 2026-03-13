Katkıda Bulunma Rehberi

SpeedReader'a katkıda bulunmak istediğin için teşekkürler! 🎉

Nasıl Başlarım?

1. **Fork** — Repoyu fork'la
2. **Clone** — Kendi fork'unu klonla
   ```bash
   git clone https://github.com/SENIN_KULLANICIN/speedreader.git
   ```
3. **Branch** — Yeni bir dal oluştur
   ```bash
   git checkout -b feature/yeni-ozellik
   ```
4. **Geliştir** — Değişikliklerini yap
5. **Test** — Çalıştığından emin ol
6. **Commit** — Anlamlı commit mesajı yaz
   ```bash
   git commit -m "feat: EPUB progress tracking eklendi"
   ```
7. **Push & PR** — Pull Request aç

---

Commit Mesaj Formatı

```
feat: yeni özellik
fix: hata düzeltmesi
docs: dokümantasyon
style: kod stili (işlevsel değişiklik yok)
refactor: yeniden yapılandırma
perf: performans iyileştirmesi
test: test ekleme
```

---

Bug Bildirme

GitHub Issues üzerinden bildir. Lütfen şunları ekle:
- Hata mesajı (varsa)
- İşletim sistemi ve Python sürümü
- Yeniden üretme adımları

---

Özellik Önerisi

Issues açarken `[FEATURE]` etiketiyle başla ve şunları açıkla:
- Ne yapmasını istiyorsun?
- Neden gerekli?
- Nasıl çalışmalı?

---

Test

```bash
cd backend
python -m pytest tests/  # (yakında)
```

---

Kod Stili

- Python: PEP8, type hint'ler tercih edilir
- Türkçe yorum satırları kabul edilir
- Fonksiyonlar için docstring yaz

---

Sorularını Issues üzerinden veya LinkedIn'den iletebilirsin.
