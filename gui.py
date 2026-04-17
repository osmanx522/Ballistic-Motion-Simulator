
from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal

from engine import PhysicsEngine
from graphics import SimulationGraph

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fizik Motoru")
        self.resize(1280, 720)

        #pages
        self.firstpage = FirstPage()
        self.secondpage = SecondPage()

        # MainWindow
        self.central_widget = QWidget()
        self.central_layout = QHBoxLayout()
        self.button_layout = QVBoxLayout()
        self.stacked_widget = QStackedWidget()

        #button
        self.btn_first_page = QPushButton("Simülasyon")
        self.btn_second_page = QPushButton("Grafikler")
        self.button_layout.addWidget(self.btn_first_page)
        self.button_layout.addWidget(self.btn_second_page)
        self.button_layout.addStretch(20)
        self.central_layout.addLayout(self.button_layout)

        self.btn_first_page.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.btn_second_page.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

        #pages
        self.stacked_widget.addWidget(self.firstpage)
        self.stacked_widget.addWidget(self.secondpage)
        self.central_layout.addWidget(self.stacked_widget)

        self.central_widget.setLayout(self.central_layout)
        self.setCentralWidget(self.central_widget)

class FirstPage(QWidget):
    simulation_signal = pyqtSignal(float, float)
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()
        self.first_label = QLabel("Hız Değeri")
        self.second_label = QLabel("Açı Değeri")
        self.first_spinbox = QDoubleSpinBox()
        self.second_spinbox = QDoubleSpinBox()
        self.start_button = QPushButton("Simülasyonu Başlat")
        self.simulation_graph = SimulationGraph()

        self.first_spinbox.setMaximum(1000)
        self.second_spinbox.setMaximum(180)
        #gridlayout
        self.grid_layout.addWidget(self.first_label, 0, 0)
        self.grid_layout.addWidget(self.first_spinbox, 0, 1)
        self.grid_layout.addWidget(self.second_label, 1, 0)
        self.grid_layout.addWidget(self.second_spinbox, 1, 1)
        self.main_layout.addLayout(self.grid_layout)

        #button
        self.main_layout.addWidget(self.start_button)

        #simulationgraph
        self.main_layout.addWidget(self.simulation_graph)

        self.start_button.clicked.connect(self.func_start_button)

        self.engine_thread = None
    def func_start_button(self):
        velocity = self.first_spinbox.value()
        angle = self.second_spinbox.value()

        self.engine_thread = PhysicsEngine(velocity, angle)
        self.engine_thread.update_coordinates.connect(self.simulation_graph.start_animation)
        self.engine_thread.start()
class SecondPage(QWidget):
    def __init__(self):
        super().__init__()
