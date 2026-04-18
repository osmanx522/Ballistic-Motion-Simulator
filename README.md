# 🚀 Ballistic Motion Simulator (Gerçek Zamanlı Balistik Simülatörü)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

Bu proje, temel kinematik prensiplerini ve **Akışkanlar Mekaniğine (Fluid Dynamics)** dayalı hava sürtünmesi (Drag) kurallarını kullanarak 2D uzayda eğik atış hareketini simüle eden profesyonel bir Python uçuş simülatörüdür. 

Özellikle Savunma Sanayi ve Oyun Motoru mimarilerine uygun olarak; **Sayısal İntegrasyon (Euler Metodu)**, **QThread ile Multithreading** ve FPS bağımlılığını ortadan kaldıran **Delta-Time Game Loop** prensipleriyle (Sıfırdan) geliştirilmiştir.

Uygulama, hesaplama yükü ile arayüz çizimini birbirinden ayırarak (QThread) donmaların önüne geçen profesyonel bir mimariye (Clean Architecture) sahiptir.

---

## 🛠️ Öne Çıkan Özellikler (V2.0)

* **Aerodinamik Sürtünme ve Akışkanlar Mekaniği (Tam Akademik Model):** Merminin *Kütlesi (kg)*, *Rüzgar Alanı (m²)* ve *Aerodinamik Şekil Katsayısı (Cd)* hesaba katılarak rüzgar direnci hesaplanır. Kapalı matematik formülleri ($x = v \cdot t$) yerine, her mili-saniyede hızın azaldığı **Euler İntegrasyonu (Sayısal Analiz)** döngüsü kullanılarak gerçekçi, asimetrik mermi yörüngeleri elde edilir.
* **Delta-Time Game Loop (Zaman Bağımsız Çizim):** Çizim motoru `QTimer` gecikmelerine (`Thread Sleep` / İşletim Sistemi Sapması) yenik düşmez. `time.time()` ve `numpy.searchsorted` algoritmaları sayesinde ekran FPS'i düşse bile (Frame Skipping) simülasyon tam zamanında ve doğru koordinatta gerçek zamanlı (Real-Time) biter.
* **Seçilebilir FPS (Tick Rate) ve A/B Testi:** Arayüzdeki FPS kaydırıcısı ile donanımsal çizim hızı (30 FPS - 240 FPS) anlık ayarlanabilir. Sürtünmesiz (İdeal Formül) ve Sürtünmeli (Dinamik Motor) algoritmalar arası tek tıkla geçiş (Backward Compatibility) yapılabilir.
* **Modern Karanlık Tema (Dark UI / QSS):** Tüm uygulama, harici bir `style.qss` dosyası üzerinden giydirilmiş Cyberpunk tarzı koyu lacivert/parlak turuncu bir arayüze sahiptir. Kullanılmayan girdi kutuları profesyonel UX prensipleri ile anında kilitlenir (`setEnabled(False)`).
* **Multi-Threading Motor (QThread):** Ağır diferansiyel fizik hesaplamaları `engine.py` içerisinde ayrı bir işlemci parçacığında (Thread) yapılır, arayüz (GUI) pürüzsüz çalışır.

---

## 🧮 Matematiksel Model & Motor

Motorumuz iki farklı modele sahiptir ("Geriye Dönük Uyumluluk"):

### 1. İdeal (Sürtünmesiz) Mod:
Klasik lise/üniversite analitik denklemleri kullanılır ($x = V \cdot \cos(\theta) \cdot t$). Matris çarpımları ile anında hedef bulunur.

### 2. Gelişmiş Balistik (Euler) Modu:
Gerçek uzayda rüzgarın anlık itme kuvveti şu formülle (Kalkülüs) adım adım işlenir:
$$F_{drag} = \frac{1}{2} \cdot \rho \cdot V^2 \cdot C_d \cdot A$$

Motor bu formülü her donanım adımında ($dt$) şu şekilde uygular:
1. $a = \frac{-F_{drag}}{m}$ (İvmenin eksi yönde hızı kesmesi)
2. $V_{new} = V_{current} + a \cdot dt$
3. $Pos_{new} = Pos_{current} + V_{new} \cdot dt$

Bu sayede mermi tepe noktasından sonra sert bir asimetrik düşüş (Paraşüt Etkisi) yaşar.

---

## 📂 Mimari (Dosya Yapısı)

Proje, yazılım mühendisliği standartlarına (Separation of Concerns) uygun olarak bölünmüştür:

```text
ballistic-simulator/
├── main.py          # Uygulama başlatıcısı ve global QSS tema yükleyicisi
├── gui.py           # PyQt6 Arayüz bileşenleri (Butonlar, Sinyaller, Sayfalar)
├── engine.py        # QThread tabanlı Fizik/Matematik motoru
├── graphics.py      # PyQtGraph tabanlı 60 FPS çizim ve animasyon ekranı
├── style.qss        # Arayüzün CSS tarzı karanlık tema (Dark Mode) kodları
├── requirements.txt # Gerekli kütüphaneler listesi
└── README.md        # Proje dokümantasyonu
```

---

## ⚙️ Kurulum ve Kullanım

Sistemin çok yüksek hızda çizim yapabilmesi için gerekli kütüphaneleri kurmanız gerekmektedir:

1.  **Gerekli Kütüphaneleri Yükleyin:**
    Matplotlib kullanımdan kaldırılmış, yerine endüstri standartlarındaki çizim motoru PyQtGraph eklenmiştir.
    ```bash
    pip install numpy pyqt6 pyqtgraph
    ```

2.  **Simülasyonu Başlatın:**
    Özel temaların ve arayüzün doğru birleştirilmesi için uygulamayı `main.py` üzerinden çalıştırın:
    ```bash
    python main.py
    ```

3.  **Kullanım:** 
    Arayüzdeki **Hız (m/s)** ve **Açı (Derece)** kutucuklarına değerleri girip "Simülasyonu Başlat" butonuna tıklayın. Top yuvarlağı yörünge boyunca süreyle uyumlu olarak hedefine uçacaktır.
