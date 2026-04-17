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
        self.setLabel("left", "Yükseklik(Y)")
        self.setLabel("bottom", "Mesafe(X)")
        self.curve = self.plot(self.x_array, self.y_array, pen=pg.mkPen('r', width=3))

        self.current_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.graph_guncelle)

    def graph_guncelle(self, t_array, x_array, y_array):
        self.x_array = x_array
        self.y_array = y_array

        self.current_index= 0
        self.timer.start(30)