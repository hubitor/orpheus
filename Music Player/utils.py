import base64
from musicpd import MPDClient
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from pathlib import Path
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

class OrpheusUtils():
    
    def getOpenClient():
        client = MPDClient()
        client.connect('localhost', 6600)
        return client
    
    def getFilename(currentSong):
        songFile = Path.home().joinpath('Music').joinpath(currentSong['file'])
        filename = songFile.stem
        return filename
    
    def getCoverPixmap(currentSong):
        songPath = Path.home().joinpath('Music').joinpath(currentSong['file'])
        coverPixmap = QPixmap()
        artFound = False
                
        if songPath.suffix.lower() == '.flac':
            artMetadata = FLAC(str(songPath)).pictures
            if artMetadata:
                embeddedCover = artMetadata[0].data
                coverPixmap.loadFromData(embeddedCover)
                artFound = True      
        elif songPath.suffix.lower() == '.mp3':
            tagData = MP3(str(songPath)).tags
            if 'APIC:' in tagData:
                embeddedCover = tagData['APIC:'].data
                coverPixmap.loadFromData(embeddedCover)
                artFound = True
        elif songPath.suffix.lower() == '.m4a':
            tagData = MP4(str(songPath)).tags
            if 'covr' in tagData:
                embeddedCover = tagData['covr'][0]
                coverPixmap.loadFromData(embeddedCover)
                artFound = True                    
        elif songPath.suffix.lower() == '.ogg':
            tagData = OggVorbis(str(songPath)).tags
            #if 'METADATA_BLOCK_PICTURE' in tagData:
            #    embeddedCover = base64.b64decode(tagData['METADATA_BLOCK_PICTURE'][0])
            #    print(tagData['METADATA_BLOCK_PICTURE'][0])
            #    coverPixmap.loadFromData(embeddedCover)
            #    artFound = True
        #elif:
        
        if not artFound:     
            albumCoverPath = songPath.parent.joinpath('cover.jpg') 
            if albumCoverPath.exists():
                coverPixmap = QPixmap(str(albumCoverPath))
                artFound = True
                
        if artFound:
            return coverPixmap.scaled(500, 500, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        else:
            return None