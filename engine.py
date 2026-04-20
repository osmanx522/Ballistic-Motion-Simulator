
import numpy as np
import math
from PyQt6.QtCore import QThread, pyqtSignal

def saf_fizik_motoru(velocity, angle, fps, use_friction, mass, area, cd):
    gravity = 9.81
    radian = math.radians(angle)
    cos_theta = round(math.cos(radian), 5)
    sin_theta = round(math.sin(radian), 5)
    V0x = velocity * cos_theta
    V0y = velocity * sin_theta
    if V0y <= 0:
        t_array = np.array([0])
        x_array = np.array([0])
        y_array = np.array([0])
    else:
        if use_friction:
            # BEYİN 1: AKADEMİK SÜRTÜNME MOTORU (EULER METODU)
            rho = 1.225 # Hava Yoğunluğu (Dünya sabiti)
            dt = 1.0 / fps # Zaman adımı
                
            # Başlangıç değerleri
            x, y, t = 0.0, 0.0, 0.0
            v_x, v_y = V0x, V0y
                
            # Listeler olarak biriktireceğiz (Çünkü sınırını baştan bilemeyiz)
            t_list, x_list, y_list = [0.0], [0.0], [0.0]
                
            while y >= 0:
                # 1. Eylemsizlik Hızı (Hipotenüs)
                v_total = math.sqrt(v_x**2 + v_y**2)
                    
                if v_total > 0:
                    # 2. Akışkanlar Mekaniği Sürtünme Kuvveti (F = 0.5 * p * V^2 * Cd * A)
                    f_drag = 0.5 * rho * (v_total**2) * cd * area
                        
                    # 3. İvme (a = F / m)
                    a_drag = f_drag / mass
                        
                    # 4. İvmeyi X ve Y Rüzgarı Olarak Bileşenlerine Ayır (Harekete ZIT Yönde)
                    a_drag_x = -a_drag * (v_x / v_total)
                    a_drag_y = -a_drag * (v_y / v_total)
                else:
                    a_drag_x, a_drag_y = 0.0, 0.0
                        
                # 5. Yeni Hızları Hesapla (Kuvvetler + Yerçekimi)
                v_x_new = v_x + (a_drag_x) * dt
                v_y_new = v_y + (-gravity + a_drag_y) * dt
                    
                # 6. Yeni Konumları Hesapla
                x_new = x + v_x_new * dt
                y_new = y + v_y_new * dt
                t_new = t + dt    
                    
                # 7. Tam yere çarpma (Zeminin Altına Girme) Hassasiyeti (Precision) 
                if y_new < 0:
                    dt_fraction = -y / v_y_new if v_y_new != 0 else 0
                    x_new = x + v_x_new * dt_fraction
                    y_new = 0.0
                    t_new = t + dt_fraction
                    t_list.append(t_new)
                    x_list.append(x_new)
                    y_list.append(y_new)
                    break

                # 8. Değerleri bir sonraki adım için güncelle ve dizilere ekle
                x, y, t = x_new, y_new, t_new
                v_x, v_y = v_x_new, v_y_new
                    
                t_list.append(t)
                x_list.append(x)
                y_list.append(y)
                
            # Listeleri Numpy Array'e çevir
            t_array = np.array(t_list)
            x_array = np.array(x_list)
            y_array = np.array(y_list)    
        else:
            time_flight = (2 * V0y) / gravity
                
            fps_step = 1.0 / fps # saniye başına düşen kare hızı
            t_array = np.arange(0, time_flight, fps_step)
            t_array = np.append(t_array, time_flight)

            x_array = V0x * t_array
            y_array = (V0y * t_array) - ((1/2) * gravity * (t_array**2))
        return t_array, x_array, y_array
class PhysicsEngine(QThread):
    update_coordinates = pyqtSignal(np.ndarray, np.ndarray, np.ndarray)
    def __init__(self, velocity, angle, fps, use_friciton, mass, area, cd):
        super().__init__()
        self.velocity = velocity
        self.angle = angle
        self.fps = fps
        self.use_friction = use_friciton
        self.mass = mass if mass > 0 else 0.01
        self.area = area
        self.cd = cd

    def run(self):
        t_array, x_array, y_array = saf_fizik_motoru(
            self.velocity, self.angle, self.fps, self.use_friction, 
            self.mass, self.area, self.cd
        )
        self.update_coordinates.emit(t_array, x_array, y_array)
