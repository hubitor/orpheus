#!/usr/bin/python3

import re
import sys
from musicpd import MPDClient
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLayout, QLineEdit, QListWidget, QListWidgetItem, QScrollBar, QVBoxLayout, QWidget
from PyQt5.QtGui import QColor, QIcon, QPalette

class OrpheusLibrarySearch(QWidget):
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.populateList()
        
    def initUI(self):
        #palette = QPalette()
        #palette.setColor(QPalette.Background, QColor('#383C4A'))        
        #palette.setColor(QPalette.WindowText, QColor('#C1C1C1'))        
        #self.setPalette(palette)
        
        self.setMaximumSize(492, 653)
        self.setMinimumSize(492, 653)
        
        le = QLineEdit(self)
        le.textChanged[str].connect(self.onChanged)
        le.returnPressed.connect(self.onActivation)
        le.setClearButtonEnabled(True)
        le.setPlaceholderText('Start typing to search...')
        self.lw = QListWidget()
        self.visibleLw = QListWidget()
        #palette.setColor(QPalette.Base, QColor('#383C4A'))                        
        #self.visibleLw.setPalette(palette)        
        self.visibleLw.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.visibleLw.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)        
        self.visibleLw.itemActivated.connect(self.onActivation)
        self.scrollBar = QScrollBar()
        self.visibleLw.verticalScrollBar().valueChanged.connect(self.scrollBar.setValue)
        self.scrollBar.valueChanged.connect(self.visibleLw.verticalScrollBar().setValue)
        vbox = QVBoxLayout()
        vbox.setSpacing(3)
        #vbox.setContentsMargins(3, 3, 3, 3)
        vbox.setContentsMargins(0, 4, 0, 0)        
        vbox.addWidget(le)       
        hbox = QHBoxLayout()
        hbox.setSpacing(0)
        #hbox.setContentsMargins(0, 0, 0, 0)                
        hbox.addWidget(self.visibleLw)
        hbox.addWidget(self.scrollBar)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        
        self.setWindowTitle('Music Library')
        
        icon = QIcon.fromTheme('musique')
        self.setWindowIcon(icon)
        
    def populateList(self):
        self.client = MPDClient()
        self.client.connect('localhost', 6600)        
        self.playlistinfo = self.client.playlistinfo()
        self.client.disconnect()
                
        self.playlist = []
        
        #backgroundColor = QColor('#383C4A')
        #foregroundColor = QColor('#C1C1C1')
        
        for i in self.playlistinfo:
            row = ''
            if 'album' in i:
                row = row + i['album'] + ' - '
            if 'title' in i:
                if isinstance(i['title'], str):
                    row = row + i['title']
                else:
                    row = row + i['title'][0]
            if 'artist' in i:
                row = row + ' - ' + i['artist']
            self.playlist.append(row)
            #newRow = QListWidgetItem(row)
            #newRow.setBackground(backgroundColor)
            #newRow.setForeground(foregroundColor)
            #self.lw.addItem(newRow)
        self.visibleLw.addItems(self.playlist)
        self.visibleLw.setCurrentRow(0)
        
    def get_matches(self, pattern):
        self.visibleLw.clear()
        pattern = '.*' + pattern.replace(' ', '.*').lower()
        regexp = re.compile(pattern)
        for i in self.playlist:
            if regexp.match(i.lower()):
                self.visibleLw.addItem(i)                
                
    def formatScrollBar(self):            
        self.scrollBar.setMaximum(self.visibleLw.verticalScrollBar().maximum())                    
        self.scrollBar.setPageStep(self.visibleLw.verticalScrollBar().pageStep())
        
    def onChanged(self, text):
        self.get_matches(text)
        self.visibleLw.setCurrentRow(0)
        self.scrollBar.setMaximum(self.visibleLw.verticalScrollBar().maximum())        
        if self.visibleLw.verticalScrollBar().maximum() == 0:
            self.scrollBar.setVisible(False)
        else:
            self.scrollBar.setVisible(True)

    def onActivation(self):
        selected_song = self.visibleLw.currentItem().text()
        for i in range(0, len(self.playlist)):
            if selected_song == self.playlist[i]:
                self.client.connect('localhost', 6600)
                self.client.play(i)
                self.client.disconnect()       
        
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Down:
            self.visibleLw.setFocus()
        elif e.key() == Qt.Key_Escape:
            self.close()
            
if __name__ == '__main__':
    orpheusls = QApplication(sys.argv)
    
    window = OrpheusLibrarySearch()
    window.show()
    window.formatScrollBar()
    
    sys.exit(orpheusls.exec_())            