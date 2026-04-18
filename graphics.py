import time
import pyqtgraph as pg
import numpy as np
from PyQt6.QtCore import QTimer

class SimulationGraph(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.x_array = np.array([])
        self.y_array = np.array([])

        self.setMouseEnabled(x=False, y=False)
        self.setBackground("#1E1E2E")
        self.showGrid(x=True, y=True, alpha=0.3)
        self.setTitle("Canlı Atış Simülasyonu", color ="#FFFFFF", size = "18pt")
        self.setLabel("left", "Yükseklik(Y: 0.00)", color="#A6ACCD", size="14pt", bold=True)
        self.setLabel("bottom", "Mesafe(X: 0.00)", color="#A6ACCD", size="14pt", bold=True)

        neon_pen = pg.mkPen(color='#F28C28', width=4)
        self.curve = self.plot(self.x_array, self.y_array, pen=neon_pen)

        self.projectile = self.plot([], [], pen=None, symbol='o', symbolBrush='#F28C28', symbolSize=14)

        self.time_label = pg.TextItem(html='<div style="color: #F28C28; font-size: 16pt; font-weight: bold;">Zaman: 0.00 s</div>', anchor=(1, 0))
        self.addItem(self.time_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.kare_guncelle)

    def start_animation(self, t_array, x_array, y_array):
        self.t_array = t_array
        self.x_array =  x_array
        self.y_array = y_array
        self.current_index = 0

        self.time_label.setHtml('<div style="color: red; font-size: 16pt; font-weight: bold;">Zaman: 0.00 s</div>')

        gercek_zaman_farki = (self.t_array[1]-self.t_array[0]) * 1000

        self.baslangic_zamani = time.time()
        self.timer.start(int(gercek_zaman_farki))
    
    def kare_guncelle(self):
        gecen_sure = time.time() - self.baslangic_zamani

        self.current_index = np.searchsorted(self.t_array, gecen_sure, side="right")
        safe_index = min(self.current_index, self.x_array.size)

        if safe_index > 0:
            x_step = self.x_array[:self.current_index]
            y_step = self.y_array[:self.current_index]
            self.curve.setData(x_step, y_step)
            self.projectile.setData([x_step[-1]], [y_step[-1]])

            time_index = max(0, safe_index-1)
            current_time = self.t_array[time_index]

            self.time_label.setHtml(f'<div style="color: red; font-size: 16pt; font-weight: bold;">Zaman: {current_time:.2f} s</div>')
            max_x = max(self.x_array) if max(self.x_array) > 0 else 1
            max_y = max(self.y_array) if max(self.y_array) > 0 else 1

            self.time_label.setPos(max_x * 0.9, max_y * 0.9)

            self.setLabel("left", f"Yükseklik(Y: {y_step[-1]:.2f})")
            self.setLabel("bottom", f"Mesafe(X: {x_step[-1]:.2f})")

        if self.current_index >= self.x_array.size:
            self.timer.stop()