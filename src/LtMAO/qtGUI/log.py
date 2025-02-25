
from PySide6.QtWidgets import (
    QStatusBar,
    QPlainTextEdit
)
from datetime import datetime

# start of all
LOG = lambda msg: log_cmd(msg)
qtwidgets = None

def log_cmd(msg):
    if msg == '' or msg.isspace():
        return
    msg = msg.rstrip('\n')
    msg = f'[{datetime.now().time()}] {msg}'
    statusbar: QStatusBar = qtwidgets.statusbar
    statusbar.showMessage('🗒️ ' + msg)
    logbox: QPlainTextEdit = qtwidgets.logbox
    logbox.appendPlainText(msg)
    scrollbar = logbox.verticalScrollBar()
    scrollbar.setValue(scrollbar.maximum())

# redirect stderr 
class Writer():
    def write(self, msg):
        log_cmd(msg)
writer = Writer()
import sys 
sys.stdout = writer
sys.stderr = writer
