#  ZenMonitor-CLI

**ZenMonitor-CLI**, Windows sistemlerde CPU, RAM, Disk kullanımını ve diski/ağı en çok yoran (I/O) süreçleri anlık olarak takip etmenizi sağlayan, hafif (lightweight) ve özelleştirilebilir bir terminal tabanlı sistem izleme aracıdır.

---

## 🌟 Öne Çıkan Özellikler

*  **Dual Mode (Çift Ekran Modu):** Tam ekran detaylı dashboard ile sağ alt köşeye sabitlenen minimalist **Mini HUD** modu arasında tek tuşla geçiş.
*  **Always-on-Top Mini HUD (F8):** `F8` tuşuna basarak terminali ekranın sağ alt köşesine küçültebilir ve diğer pencerelerin üzerinde sabit (`Always on Top`) kalmasını sağlayabilirsiniz.
*  **I/O & Süreç Takibi:** Sistem kaynağını (Disk/Ağ) en çok tüketen top 2 süreci anlık olarak tespit eder ve listeler.
*  **Masaüstü Bildirimleri:** RAM (%85+) veya Disk (%90+) kritik seviyelere ulaştığında `plyer` entegrasyonu ile Windows masaüstü bildirimi gönderir.

---

## 📸 Ekran Görüntüsü

> *Geliştirici Notu: Buraya projenin Mini HUD ve Tam Ekran modundaki ekran görüntülerini ekleyebilirsiniz.*

---

## 🚀 Kurulum

1. Depoyu klonlayın veya indirin:
   ```bash
   git clone [https://github.com/TheGkyTkn/ZenMonitor-CLI.git](https://github.com/TheGkyTkn/ZenMonitor-CLI.git)
   cd ZenMonitor-CLI
2. Gerekli bağımlılıkları yükleyin:
   pip install psutil plyer

## Kullanım
Uygulamayı başlatmak için terminalde şu komutu çalıştırın:
  python main.py

## Kısayollar & Kontroller
F8 : Tam Ekran Dashboard ile Sağ Alt Mini HUD modu arasında geçiş yapar.
CTRL + C : Uygulamadan güvenli bir şekilde çıkar ve terminal penceresini varsayılan boyutuna getirir.

## Lisans
Bu proje açık kaynaklıdır ve eğitim/geliştirme amaçlı paylaşılmıştır.
