import csv
import random
import time
from engine import saf_fizik_motoru

random.seed(42)

dosya_adi = "atis_veriseti.csv"
toplam_veri = 100000

print(f"Yapay Zeka veri seti uretimi basliyor... ({toplam_veri} atis)")
baslangic = time.time()

with open(dosya_adi, mode="w", newline="") as dosya:
    yazici = csv.writer(dosya)
    # Excel tablomuzun başlıkları (Sütunlar)
    yazici.writerow(["Hiz_ms", "Aci_derece", "Kutle_kg", "Alan_m2", "Cd", "Ucus_Suresi_s", "Hedef_Mesafe_X"])
    
    for i in range(toplam_veri):
        velocity = random.uniform(50.0, 1000.0)
        angle = random.uniform(5.0, 85.0)
        mass = random.uniform(0.1, 100.0)
        area = random.uniform(0.005, 0.5)
        cd = random.uniform(0.1, 1.0)
        
        # Eğitimde gereksiz detaya girmemek için FPS = 60 gayet yeterlidir, hızı artırır.
        t_array, x_array, y_array = saf_fizik_motoru(velocity, angle, 60, True, mass, area, cd)
        
        # Bize sadece merminin yere çarptığı an (en son veri) gereklidir
        ucus_suresi = t_array[-1]
        bitis_x = x_array[-1]
        
        yazici.writerow([
            round(velocity, 2), 
            round(angle, 2), 
            round(mass, 2), 
            round(area, 4), 
            round(cd, 2), 
            round(ucus_suresi, 3), 
            round(bitis_x, 2)
        ])
        
        # İlerlemeyi görmek için bilgi ver
        if (i+1) % 1000 == 0:
            print(f"{i+1} veri uretildi...")

bitis = time.time()
print(f"\nTamamlandi! Toplam sure: {bitis - baslangic:.2f} saniye")
print(f"Veriler '{dosya_adi}' dosyasina basariyla kaydedildi.")

