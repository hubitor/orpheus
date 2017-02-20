from musicpd import MPDClient
import select
from PyQt5.QtCore import pyqtSignal, QThread

from utils import OrpheusUtils

class OrpheusNetworkThread(QThread):

    refreshWindow = pyqtSignal(dict, dict)
    updateTimer = pyqtSignal(str)
    
    def __init__(self, window):
        super().__init__()
                
        self.window = window        
    
    def run(self):
        self.client = OrpheusUtils.getOpenClient()
        while True:
            self.client.send_idle()
            select.select([self.client], [], [])
            event = self.client.fetch_idle()
            if event[0] == 'player':
                status = self.client.status()
                currentSong = self.client.currentsong()
                self.refreshWindow.emit(currentSong, status)
                #self.window.resizeMetadataLabels()
                self.updateTimer.emit(self.client.status()['state'])
    
    def disconnect(self):
        self.client.noidle()
        self.client.disconnect()