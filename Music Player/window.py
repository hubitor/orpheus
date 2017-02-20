from musicpd import MPDClient
from PyQt5.QtCore import pyqtSlot, QSize, Qt
from PyQt5.QtGui import QColor, QFont, QIcon, QPalette, QPixmap
from PyQt5.QtWidgets import (QDesktopWidget, QHBoxLayout, QLabel, QLayout,
                             QPushButton, QStatusBar, QVBoxLayout, QWidget)

from coverlabel import OrpheusCoverLabel
from slider import OrpheusSlider
from utils import OrpheusUtils

class OrpheusWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        
        QIcon.setThemeName('papirus-arc-dark')
        
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor('#3F5068'))        
        palette.setColor(QPalette.WindowText, QColor('#FFFFFF'))        
        self.setPalette(palette)

        self.font = 'Bebas Neue'
        #self.font = 'Segoe UI'
        self.defaultTitleSize = 32
        #self.defaultTitleSize = 24
        titleFont = QFont(self.font, self.defaultTitleSize)
        albumArtistFont = QFont(self.font, 18)                
        albumArtistMiscFont = QFont(self.font, 12)
        #albumArtistFont = QFont(self.font, 12)                
        #albumArtistMiscFont = QFont(self.font, 10)
        
        #self.font = 'Arial'        
        #self.defaultTitleSize = 30
        #titleFont = QFont(self.font, self.defaultTitleSize)
        #titleFont.setCapitalization(QFont.AllUppercase)
        #albumArtistFont = QFont(self.font, 14)                
        #albumArtistMiscFont = QFont(self.font, 10)

        #titleFont = QFont('Arial', 20)
        #albumArtistFont = QFont('Arial', 12)                
        #albumArtistMiscFont = QFont('Arial', 10)
        
        #titleFont = QFont('Corbel', 24)        
        #titleFont = QFont('Calibri', 24)
        #albumArtistFont = QFont('Calibri', 14)                
        #albumArtistMiscFont = QFont('Calibri', 10)
        
        vbox = QVBoxLayout()                
        vbox.setSizeConstraint(QLayout.SetFixedSize)
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 7)
        
        self.coverLabel = OrpheusCoverLabel(self)
        vbox.addWidget(self.coverLabel)        
        
        self.titleLabel = QLabel()
        self.albumLabel = QLabel()
        self.artistLabel = QLabel()
        self.lastArtistLabel = QLabel()
        
        self.titleLabel.setFont(titleFont)
        self.titleLabel.setMaximumSize(100000, 40)        
        self.titleLabel.setAlignment(Qt.AlignBottom)
        self.albumLabel.setFont(albumArtistFont)        
        self.albumLabel.setMaximumSize(100000, 20)        
        self.albumLabel.setAlignment(Qt.AlignBottom)        
        self.artistLabel.setFont(albumArtistFont)                
        self.artistLabel.setMaximumSize(100000, 25)        
        self.artistLabel.setAlignment(Qt.AlignBottom)                
        self.lastArtistLabel.setFont(albumArtistFont)
        self.lastArtistLabel.setMaximumSize(100000, 25)        
        self.lastArtistLabel.setAlignment(Qt.AlignBottom)                

        self.albumFromLabel = QLabel('from')
        self.albumFromLabel.setFont(albumArtistMiscFont)        
        
        self.artistFromLabel = QLabel('by')
        self.artistFromLabel.setFont(albumArtistMiscFont)                
        
        self.artistAndLabel = QLabel('and')
        self.artistAndLabel.setFont(albumArtistMiscFont)                        

        self.titleTimeDisplay = QLabel()
        self.titleTimeDisplay.setFont(albumArtistMiscFont)
        self.albumTimeDisplay = QLabel()
        self.albumTimeDisplay.setFont(albumArtistMiscFont)
        self.artistTimeDisplay = QLabel()
        self.artistTimeDisplay.setFont(albumArtistMiscFont)

        titleBox = QHBoxLayout()
        titleBox.addWidget(self.titleLabel)
        titleBox.addStretch(1)
        titleBox.addWidget(self.titleTimeDisplay)

        albumBox = QHBoxLayout()
        albumBox.setContentsMargins(2, 0, 0, 0)                
        albumBox.setSpacing(10)                           
        albumBox.addWidget(self.albumFromLabel)                
        albumBox.addWidget(self.albumLabel)
        albumBox.addStretch(1)        
        albumBox.addWidget(self.albumTimeDisplay)        

        subArtistBox = QHBoxLayout()
        subArtistBox.setSpacing(7)
        subArtistBox.addWidget(self.artistLabel)
        subArtistBox.addWidget(self.artistAndLabel)
        subArtistBox.addWidget(self.lastArtistLabel)        

        artistBox = QHBoxLayout()
        artistBox.setContentsMargins(2, 0, 0, 0)                
        artistBox.setSpacing(20)
        #artistBox.setSpacing(21)                   
        artistBox.addWidget(self.artistFromLabel)
        artistBox.addLayout(subArtistBox)
        artistBox.addStretch(1)
        artistBox.addWidget(self.artistTimeDisplay)
        
        songInfoBox = QVBoxLayout()
        songInfoBox.setContentsMargins(0, 3, 0, 0)        
        songInfoBox.setSpacing(4)        
        songInfoBox.addStretch(1)        
        songInfoBox.addLayout(albumBox)                
        songInfoBox.addLayout(artistBox)                
        
        displayBox = QVBoxLayout()
        displayBox.setContentsMargins(7, 9, 7, 3)
        #displayBox.setContentsMargins(7, 0, 7, 3)        
        displayBox.addLayout(titleBox)
        displayBox.addLayout(songInfoBox)        
        
        vbox.addLayout(displayBox)
            
        self.slider = OrpheusSlider()            
        sliderBox = QHBoxLayout()
        sliderBox.setContentsMargins(4, 0, 4, 0)
        sliderBox.addWidget(self.slider)
        vbox.addLayout(sliderBox)
        
        self.prevBtn = QPushButton()
        self.prevBtn.setFlat(True)
        self.prevBtn.setFixedSize(125, 40)        
        self.prevBtn.setFocusPolicy(Qt.NoFocus)      
        self.prevBtn.clicked.connect(self.onPrevious)
        toggleBtn = QPushButton()
        toggleBtn.setFlat(True)
        toggleBtn.setIcon(QIcon.fromTheme('media-playback-start'))
        toggleBtn.setIconSize(QSize(48, 48))
        toggleBtn.setFixedSize(125, 40)
        toggleBtn.setFocusPolicy(Qt.NoFocus)                
        toggleBtn.clicked.connect(self.onToggle)
        stopBtn = QPushButton()
        stopBtn.setFlat(True)
        stopBtn.setIcon(QIcon.fromTheme('media-playback-stop'))
        stopBtn.setIconSize(QSize(48, 48))  
        stopBtn.setFixedSize(125, 40)        
        stopBtn.setFocusPolicy(Qt.NoFocus)                
        stopBtn.clicked.connect(self.onStop)
        self.nextBtn = QPushButton()
        self.nextBtn.setFlat(True)
        self.nextBtn.setFixedSize(125, 40)        
        self.nextBtn.setFocusPolicy(Qt.NoFocus)                
        self.nextBtn.clicked.connect(self.onNext)
        
        buttonbox = QHBoxLayout()
        buttonbox.addWidget(self.prevBtn)
        buttonbox.addWidget(toggleBtn)
        buttonbox.addWidget(stopBtn)
        buttonbox.addWidget(self.nextBtn)
        vbox.addLayout(buttonbox)
        
        self.setLayout(vbox)
        
        client = OrpheusUtils.getOpenClient()
        currentSong = client.currentsong()
        status = client.status()        
        self.refresh(currentSong, status)
        client.disconnect()        

    @pyqtSlot(dict, dict)        
    def refresh(self, currentSong, status):
        
        self.autoSetWindowTitle(currentSong, status)
        self.updateMusicLabels(currentSong)
        self.renderArt(currentSong)
        self.configureTimeDisplays(currentSong, status)
        self.enableProperButtons(status)
        
    def autoSetWindowTitle(self, currentSong, status):
        if 'title' in currentSong:
            windowTitle = currentSong['title']
        else:
            windowTitle = OrpheusUtils.getFilename(currentSong)
        self.setWindowTitle(windowTitle)
        
        if status['state'] == 'play':
            icon = QIcon.fromTheme('media-playback-start')
        elif status['state'] == 'pause':
            icon = QIcon.fromTheme('media-playback-pause')
        else:
            icon = QIcon.fromTheme('media-playback-stop')
        self.setWindowIcon(icon)
        
    def updateMusicLabels(self, currentSong):        
        if 'title' in currentSong:
            self.titleLabel.setText(currentSong['title'])
        else:
            self.titleLabel.setText(OrpheusUtils.getFilename(currentSong))

        album = ''
        if 'album' in currentSong:
            album = currentSong['album']
            self.albumLabel.setVisible(True)            
            self.albumFromLabel.setVisible(True)
            self.albumLabel.setText(album)
        else:
            self.albumLabel.setVisible(False)
            self.albumFromLabel.setVisible(False)            
            
        if 'artist' in currentSong:
            artist = currentSong['artist']
            artistList = artist.split(' & ')
            formattedArtist = artistList[0]        
            artistCount = len(artistList)
            if artistCount == 1:
                self.artistAndLabel.setVisible(False)                    
                self.lastArtistLabel.setVisible(False)                
            else:
                for i in range(1, len(artistList) - 1):
                    formattedArtist = formattedArtist + ', ' + artistList[i]
                self.artistAndLabel.setVisible(True)                    
                self.lastArtistLabel.setText(artistList[artistCount - 1])
                self.lastArtistLabel.setVisible(True)
            
            self.artistLabel.setText(formattedArtist)
            
            self.artistLabel.setVisible(True)
            self.artistFromLabel.setVisible(True)
        else:
            self.artistLabel.setVisible(False)            
            self.artistFromLabel.setVisible(False)            
            self.artistAndLabel.setVisible(False)                    
            self.lastArtistLabel.setVisible(False)             
            
    def renderArt(self, currentSong):
        coverPixmap = OrpheusUtils.getCoverPixmap(currentSong)        
        if not coverPixmap:
            self.coverLabel.setVisible(False)            
        else:
            self.coverLabel.setPixmap(coverPixmap)
            self.coverLabel.setVisible(True)            
            
    def configureTimeDisplays(self, currentSong, status):       
        self.slider.setMaximum(int(currentSong['time']))        
    
        stopped = status['state'] == 'stop'
        if stopped:
            self.slider.setValue(0)
            self.elapsedTime = 0
        elif 'elapsed' in status:
            self.slider.setValue(float(status['elapsed']))
            self.elapsedTime = round(float((status['elapsed'])))
            
        durationTime = round(float((currentSong['time'])))
        minutes, seconds = divmod(durationTime, 60)
        self.formattedDurationTime = " / %d:%02d" % (minutes, seconds)
        
        minutes, seconds = divmod(self.elapsedTime, 60)
        
        if 'artist' in currentSong:        
            self.titleTimeDisplay.setVisible(False)                        
            self.albumTimeDisplay.setVisible(False)            
            self.artistTimeDisplay.setVisible(True)          
            self.visibleTimeDisplay = self.artistTimeDisplay
        elif 'album' in currentSong:
            self.titleTimeDisplay.setVisible(False)            
            self.albumTimeDisplay.setVisible(True)            
            self.artistTimeDisplay.setVisible(False)                      
            self.visibleTimeDisplay = self.albumTimeDisplay            
        else:
            self.titleTimeDisplay.setVisible(True)
            self.albumTimeDisplay.setVisible(False)            
            self.artistTimeDisplay.setVisible(False)                      
            self.visibleTimeDisplay = self.titleTimeDisplay            
            
        self.visibleTimeDisplay.setText("%d:%02d" % (minutes, seconds) + self.formattedDurationTime)                        

    def enableProperButtons(self, status):
        notStopped = not status['state'] == 'stop'
        self.prevBtn.setEnabled(notStopped)
        self.nextBtn.setEnabled(notStopped)                    
        if notStopped:
            self.prevBtn.setIcon(QIcon.fromTheme('media-skip-backward'))
            self.nextBtn.setIcon(QIcon.fromTheme('media-skip-forward'))            
        else:
            self.prevBtn.setIcon(QIcon())
            self.nextBtn.setIcon(QIcon())            
            
    def resizeMetadataLabels(self):
        titleFont = QFont(self.font, self.defaultTitleSize)        
        self.titleLabel.setFont(titleFont)        
        pointSize = self.defaultTitleSize
        while self.titleLabel.sizeHint().width() >  486:
            pointSize = pointSize - 2
            titleFont = QFont(self.font, pointSize)
            self.titleLabel.setFont(titleFont)
        
    def center(self):
        width = self.frameGeometry().width()
        height = self.frameGeometry().height()

        desktopInfo = QDesktopWidget()

        screenWidth = desktopInfo.screen().width()
        screenHeight = desktopInfo.screen().height()

        self.setGeometry((screenWidth / 2) - (width / 2), 
                           (screenHeight / 2) - (height / 2), 
                           width, height)
        
    def onPrevious(self):
        client = OrpheusUtils.getOpenClient()
        client.previous()
        client.disconnect()
    
    def onToggle(self):
        client = OrpheusUtils.getOpenClient()
        state = client.status()['state']                
        if state == 'play':
            client.send_pause(1)
        else:
            client.send_play()
        client.disconnect()
        
    def onStop(self):
        client = OrpheusUtils.getOpenClient()      
        client.stop()
        client.disconnect()        
        self.slider.setValue(0)
    
    def onNext(self):
        client = OrpheusUtils.getOpenClient()
        client.next()
        client.disconnect()
        
    def onRandom(self, toggled):
        client = OrpheusUtils.getOpenClient()
        client.random(int(toggled))
        client.disconnect()
        
    def onRepeat(self, toggled):
        client = OrpheusUtils.getOpenClient()
        client.repeat(int(toggled))
        client.single(int(toggled))
        client.disconnect()        

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Space or e.key() == Qt.Key_Return or e.key() == Qt.Key_Enter:
            self.onToggle()
        elif e.key() == Qt.Key_Left:
            self.onPrevious()
        elif e.key() == Qt.Key_Right:
            self.onNext()
        elif e.key() == Qt.Key_Escape:
            self.close() 