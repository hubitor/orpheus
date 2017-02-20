#!/usr/bin/python3

import sys
from networkthread import OrpheusNetworkThread
from mainloop import OrpheusMainloop
from window import OrpheusWindow

if __name__ == '__main__':
    mainloop = OrpheusMainloop(sys.argv)
    
    window = OrpheusWindow()            
    window.show()    
    #window.resizeMetadataLabels()
    #window.center()

    mainloop.setWindow(window)

    thread = OrpheusNetworkThread(window)
    thread.refreshWindow.connect(window.refresh)
    thread.updateTimer.connect(mainloop.resetScrollTimer)
    thread.start()
    
    mainloop.exec_()

    thread.disconnect()
    
    sys.exit()