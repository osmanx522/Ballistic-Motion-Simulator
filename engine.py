
import numpy as np
import math
from PyQt6.QtCore import QThread, pyqtSignal

class PhysicsEngine(QThread):
    update_coordinates = pyqtSignal(np.ndarray, np.ndarray, np.ndarray)
    def __init__(self, velocity, angle):
        super().__init__()
        self.velocity = velocity
        self.angle = angle
    
    def run(self):
        gravity = 9.81
        radian = math.radians(self.angle)

        cos_theta = round(math.cos(radian), 5)
        sin_theta = round(math.sin(radian), 5)
        V0x = self.velocity * cos_theta
        V0y = self.velocity * sin_theta
        
        if V0y <= 0:
            t_array = np.array([0])
            x_array = np.array([0])
            y_array = np.array([0])
        else:
            time_flight = (2 * V0y) / gravity

            t_array = np.linspace(0, time_flight, 100)
            x_array = V0x * t_array
            y_array = (V0y * t_array) - ((1/2) * gravity * (t_array**2))

        self.update_coordinates.emit(t_array, x_array, y_array)
