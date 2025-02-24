from PySide6.QtWidgets import (
    QStatusBar,
    QPlainTextEdit
)
from datetime import datetime

# start of all
LOG = lambda msg: log_cmd(msg)
qtwidgets = None

def log_cmd(msg):
    msg = f'[{datetime.now().time()}] {msg}'
    statusbar: QStatusBar = qtwidgets.statusbar
    statusbar.showMessage('🗒️ ' + msg)
    
    logbox: QPlainTextEdit = qtwidgets.logbox
    logbox.appendPlainText(msg)
    scrollbar = logbox.verticalScrollBar()
    scrollbar.setValue(scrollbar.maximum())
    
    