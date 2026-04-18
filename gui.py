
from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal, Qt

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
    def __init__(self):
        super().__init__()

        self.main_layout = QVBoxLayout(self)
        self.grid_layout = QGridLayout()

        self.first_label = QLabel("Hız Değeri (m/s)")
        self.second_label = QLabel("Açı Değeri")

        self.first_spinbox = QDoubleSpinBox()
        self.first_spinbox.setMaximum(1000)
        self.second_spinbox = QDoubleSpinBox()
        self.second_spinbox.setMaximum(180)

        self.start_button = QPushButton("Simülasyonu Başlat")
        self.simulation_graph = SimulationGraph()

        self.fps_label = QLabel("FPS: 60")
        self.fps_slider = QSlider(Qt.Orientation.Horizontal)
        self.fps_slider.setMinimum(30)
        self.fps_slider.setMaximum(240)
        self.fps_slider.setValue(60)
        self.fps_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.fps_slider.setTickInterval(30)
        self.fps_slider.valueChanged.connect(lambda v: self.fps_label.setText(f"FPS: {v}"))
        
        self.friction_label = QLabel("Sürtünme")
        self.mass_label = QLabel("Kütle (kg)")
        self.cross_area_label = QLabel("Kesit Alanı (m²)")
        self.cd_label = QLabel("Aerodinamik Şekil Katsayısı")

        self.friction_box = QCheckBox()
        self.mass_spinbox = QDoubleSpinBox()
        self.cross_area_spinbox = QDoubleSpinBox()
        self.cd_spinbox = QDoubleSpinBox()
        
        self.mass_spinbox.setRange(0.01, 1000)
        self.mass_spinbox.setValue(10.0) 
        self.mass_spinbox.setSingleStep(1.0)
        
        self.cross_area_spinbox.setDecimals(4)
        self.cross_area_spinbox.setRange(0.0001, 10)
        self.cross_area_spinbox.setValue(0.05)
        self.cross_area_spinbox.setSingleStep(0.01)

        self.cd_spinbox.setRange(0.01, 2.5)
        self.cd_spinbox.setValue(0.47)
        self.cd_spinbox.setSingleStep(0.05)

        self.mass_spinbox.setEnabled(False)
        self.cross_area_spinbox.setEnabled(False)
        self.cd_spinbox.setEnabled(False)

        self.friction_box.toggled.connect(self.mass_spinbox.setEnabled)
        self.friction_box.toggled.connect(self.cross_area_spinbox.setEnabled)
        self.friction_box.toggled.connect(self.cd_spinbox.setEnabled)
        self.friction_grid_layout = QGridLayout()

        #gridlayout
        self.grid_layout.addWidget(self.first_label, 0, 0)
        self.grid_layout.addWidget(self.first_spinbox, 0, 1)

        self.grid_layout.addWidget(self.second_label, 1, 0)
        self.grid_layout.addWidget(self.second_spinbox, 1, 1)

        self.grid_layout.addWidget(self.fps_label, 2,0)
        self.grid_layout.addWidget(self.fps_slider, 2,1)

        self.grid_layout.addLayout(self.friction_grid_layout, 3, 0, 1, 2)

        self.friction_grid_layout.addWidget(self.friction_label, 0, 0)
        self.friction_grid_layout.addWidget(self.friction_box, 1, 0)
        self.friction_grid_layout.addWidget(self.mass_label, 0,1)
        self.friction_grid_layout.addWidget(self.mass_spinbox, 1, 1)
        self.friction_grid_layout.addWidget(self.cross_area_label, 0, 2)
        self.friction_grid_layout.addWidget(self.cross_area_spinbox, 1, 2)
        self.friction_grid_layout.addWidget(self.cd_label, 0, 3)
        self.friction_grid_layout.addWidget(self.cd_spinbox, 1, 3)

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
        selection_fps = int(self.fps_slider.value())
        use_friction = self.friction_box.isChecked()
        mass = self.mass_spinbox.value()
        area = self.cross_area_spinbox.value()
        cd = self.cd_spinbox.value()

        self.engine_thread = PhysicsEngine(velocity, angle, selection_fps, use_friction, mass, area, cd)
        self.engine_thread.update_coordinates.connect(self.simulation_graph.start_animation)
        self.engine_thread.start()
class SecondPage(QWidget):
    def __init__(self):
        super().__init__()
