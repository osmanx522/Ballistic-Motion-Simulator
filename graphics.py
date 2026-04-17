import pyqtgraph as pg
import numpy as np
from PyQt6.QtCore import QTimer

class SimulationGraph(pg.PlotWidget):
    def __init__(self):
        super().__init__()
        self.x_array = np.array([])
        self.y_array = np.array([])

        self.setBackground("w")
        self.showGrid(x= True, y= True)
        self.setTitle("Canlı Atış Simülasyonu", color ="b", size = "15pt")
        self.setLabel("left", "Yükseklik(Y: 0)")
        self.setLabel("bottom", "Mesafe(X: 0)")
        self.curve = self.plot(self.x_array, self.y_array, pen=pg.mkPen('r', width=3))
        self.projectile = self.plot([], [], pen=None, symbol='o', symbolBrush='r', symbolSize=10)

        self.time_label = pg.TextItem(html='<div style="color: red; font-size: 16pt; font-weight: bold;">Zaman: 0.00 s</div>', anchor=(1, 0))
        self.addItem(self.time_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.kare_guncelle)

    def start_animation(self, t_array, x_array, y_array):
        self.t_array = t_array
        self.x_array =  x_array
        self.y_array = y_array
        self.current_index = 0

        self.time_label.setHtml('<div style="color: red; font-size: 16pt; font-weight: bold;">Zaman: 0.00 s</div>')
        self.timer.start(30)
    
    def kare_guncelle(self):
        if self.current_index <= self.x_array.size:
            x_step = self.x_array[:self.current_index]
            y_step = self.y_array[:self.current_index]
            self.curve.setData(x_step, y_step)
            if x_step.size > 0:
                self.projectile.setData([x_step[-1]], [y_step[-1]])

                current_time = self.t_array[self.current_index - 1]
                self.time_label.setHtml(f'<div style="color: red; font-size: 16pt; font-weight: bold;">Zaman: {current_time:.2f} s</div>')

                max_x = max(self.x_array) if max(self.x_array) > 0 else 1
                max_y = max(self.y_array) if max(self.y_array) > 0 else 1

                self.time_label.setPos(max_x * 0.9, max_y * 0.9)

                self.setLabel("left", f"Yükseklik(Y: {y_step[-1]:.2f})")
                self.setLabel("bottom", f"Mesafe(X: {x_step[-1]:.2f})")
            self.current_index += 1
    
        else:
            self.timer.stop()