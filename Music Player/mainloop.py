from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import QApplication

from utils import OrpheusUtils

class OrpheusMainloop(QApplication):

    def __init__(self, argv):
        super().__init__(argv)                
        
    def setWindow(self, window):
        self.window = window

    def exec_(self):                
        client = OrpheusUtils.getOpenClient()
        state = client.status()['state']
        client.disconnect()        
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateTimeDisplays)
        self.timer.start(1000)
        
        self.resetScrollTimer(state)
        
        super().exec_()

    def updateTimeDisplays(self):
        slider = self.window.slider
        value = slider.value() + 1
        if value <= slider.maximum():
            slider.setValue(value)
        else:
            print ('ERROR: Slider went past the end, hombre.')
            
        self.window.elapsedTime = self.window.elapsedTime + 1
        minutes, seconds = divmod(self.window.elapsedTime, 60)
        
        self.window.visibleTimeDisplay.setText("%d:%02d" % (minutes, seconds) + self.window.formattedDurationTime)
            
    @pyqtSlot(str)
    def resetScrollTimer(self, state):
        if state == 'play':
            if not self.timer.isActive():
                self.timer.start(1000)
        else:
            if self.timer.isActive():
                self.timer.stop()                