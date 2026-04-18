# -*- coding: utf-8 -*-
"""
Created on Wed Dec 31 19:57:17 2025

@author: osman

~ Y Ekseni Referans Noktası yer seviyesi seçilmiştir
~ X Ekseni Referans Noktası atışın başlangıç noktası seçilmiştir
"""

import sys
from gui import MainWindow
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    
    # YENİ: Ayrı tuttuğumuz QSS dosyasını okuyup tüm uygulamaya giydiriyoruz
    with open("style.qss", "r") as f:
        app.setStyleSheet(f.read())
        
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()