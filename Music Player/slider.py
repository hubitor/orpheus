from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider

from utils import OrpheusUtils

class OrpheusSlider(QSlider):
    
    def __init__(self):
        super().__init__()    
        self.setOrientation(Qt.Horizontal)
        self.setTracking(False)
        self.setFocusPolicy(Qt.NoFocus)
  
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            e.accept()
            
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            value = self.maximum() * e.x() / self.width()
            self.setValue(value)
            
            client = OrpheusUtils.getOpenClient()
            client.seekcur(value)
            client.disconnect()            
        
            e.accept()            