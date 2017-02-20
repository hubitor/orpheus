import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QLabel, QMenu

from utils import OrpheusUtils

class OrpheusCoverLabel(QLabel):

    def __init__(self, window):
        super().__init__()
        self.window = window
        
        #self.palette = QPalette()
        #self.palette.setColor(QPalette.Background, QColor('#383C4A'))        
        #self.palette.setColor(QPalette.WindowText, QColor('#C1C1C1'))        
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.window.onToggle()
        elif event.button() == Qt.RightButton:
            client = OrpheusUtils.getOpenClient()
            status = client.status()
            client.disconnect()

            optionsMenu = QMenu(self)
            #optionsMenu.setPalette(self.palette)
            randomMenu = optionsMenu.addAction('Random')
            randomMenu.setCheckable(True)
            randomMenu.setChecked(int(status['random']))
            randomMenu.triggered.connect(self.window.onRandom)
            repeatMenu = optionsMenu.addAction('Repeat')
            repeatMenu.setCheckable(True)
            repeatMenu.setChecked(int(status['repeat']))
            repeatMenu.triggered.connect(self.window.onRepeat)
            optionsMenu.popup(event.globalPos())

    def wheelEvent(self, event):
        if event.angleDelta().y() < 0:
            os.system('pactl set-sink-volume 0 -7%')
            os.system('pactl set-sink-volume 1 -7%')
            os.system('pactl set-sink-volume 2 -7%')
        else:
            os.system('pactl set-sink-volume 0 +7%')
            os.system('pactl set-sink-volume 1 +7%')
            os.system('pactl set-sink-volume 2 +7%')