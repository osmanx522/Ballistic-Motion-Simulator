# 🚀 Ballistic Motion Simulator (Gerçek Zamanlı Balistik Simülatörü)

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/Numpy-777BB4?style=for-the-badge&logo=numpy&logoColor=white)
![PyQt6](https://img.shields.io/badge/PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white)

Bu proje, temel kinematik prensiplerini kullanarak 2D uzayda eğik atış (projectile motion) hareketini simüle eden, modern arayüzlü ve gerçek zamanlı bir Python uygulamasıdır. **PyQt6** ile geliştirilmiş kontrol paneli ve **PyQtGraph** motoru kullanılarak, mühimmatın uçuşu 60 FPS akıcılığında canlandırılır (animate edilir). 

Uygulama, hesaplama yükü ile arayüz çizimini birbirinden ayırarak (QThread) donmaların önüne geçen profesyonel bir mimariye (Clean Architecture) sahiptir.

---

## 🛠️ Öne Çıkan Özellikler (V2.0)

* **Gerçek Zamanlı Simülasyon (Real-Time 60 FPS):** Atışın fizikteki havada kalma süresi ile ekrandaki uçuş süresi saniyesi saniyesine eşlenmiştir. Uzun uçuşlar `np.arange` ile 60 FPS'e uygun zaman adımlarına (dt=1/60) bölünür.
* **Modern Karanlık Tema (Dark UI / QSS):** Tüm uygulama, harici bir `style.qss` dosyası üzerinden giydirilmiş Cyberpunk tarzı koyu lacivert/parlak turuncu bir arayüze sahiptir.
* **Multi-Threading Motor (QThread):** Ağır vektörel fizik hesaplamaları `engine.py` içerisinde ayrı bir işlemci parçacığında (Thread) yapılır, arayüz (GUI) asla kasmaz.
* **Dinamik Radar Başlıkları:** Mermi havada süzülürken anlık *Zaman (s)*, *Yükseklik (m)* ve *Uzaklık (x)* değerleri grafiğin köşesine ve eksenlerine anlık olarak basılır.
* **Akıllı Ölçekleme & Yuvarlama:** 90 derece (Tam dikey) ve 180 derece (Yatay ters) atışlarda oluşabilecek "Precision Error" (Kayan Nokta Sapması) hataları matematiksel olarak bloke edilmiştir.

---

## 🧮 Matematiksel Model & Motor

Motorumuz ideal ortam analizi yapar. Hareket denklemleri modüler olarak `engine.py` içinde hesaplanır:

**Yatay Konum ($x$):**
$$x(t) = v_0 \cdot \cos(\theta) \cdot t$$

**Dikey Konum ($y$):**
$$y(t) = v_0 \cdot \sin(\theta) \cdot t - \frac{1}{2} g t^2$$

*(Not: Merminin Y eksenindeki ilk hız bileşeni ($V_{0y}$) sıfır veya negatif olursa sistem otomatik olarak atışı iptal eder.)*

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
