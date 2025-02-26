from PySide6.QtCore import (
    Signal,
    QObject
)
import sys
from datetime import datetime

class Log(QObject):
    logbox_signal = Signal(str)
    statusbar_signal = Signal(str)

    def __init__(self, logbox, statusbar):
        QObject.__init__(self)
        self.logbox = logbox
        self.statusbar = statusbar
        self.logbox_signal.connect(logbox.appendPlainText)
        self.statusbar_signal.connect(statusbar.showMessage)

    def write_log(self, msg):
        msg = f'[{datetime.now().time()}] {msg}'
        self.show_statusbar('🗒️ ' + msg)
        self.write_logbox(msg)
        scrollbar = self.logbox.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def write_logbox(self, msg):
        self.logbox_signal.emit(msg)

    def show_statusbar(self, msg):
        self.statusbar_signal.emit(msg)

def link_main_window(logbox, statusbar):
    log = Log(logbox, statusbar)
    class Writer():
        def write(self, msg):
            if msg == '' or msg.isspace():
                return
            log.write_log(msg.replace('\\', '/'))
    writer = Writer()
    sys.stdout = writer
    sys.stderr = writer

def link_splash(label):
    class Writer():
        def write(self, msg):
            if msg == '' or msg.isspace():
                return
            label.setText('🗒️ ' + msg) 
            label.repaint()
    writer = Writer() 
    sys.stdout = writer
    sys.stderr = writer