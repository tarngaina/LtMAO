from PySide6.QtWidgets import (
    QStatusBar,
    QPlainTextEdit
)
from datetime import datetime
from threading import Thread
from time import sleep

# start of all
LOG = lambda msg: log_cmd(msg)
qtwidgets = None
logbox_cd = False
logbox_queued_msgs = []

def logbox_cooldown():
    sleep(0.1666)
    global logbox_cd, logbox_queued_msgs
    if len(logbox_queued_msgs) > 0:
        msg = '\n'.join(logbox_queued_msgs)
        logbox_queued_msgs = []
        qtwidgets.logbox.appendPlainText(msg)
        scrollbar = qtwidgets.logbox.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    logbox_cd = False

def log_cmd(msg):
    if msg == '':
        return
    msg = msg.rstrip('\n')
    msg = f'[{datetime.now().time()}] {msg}'
    statusbar: QStatusBar = qtwidgets.statusbar
    statusbar.showMessage('🗒️ ' + msg)
    logbox: QPlainTextEdit = qtwidgets.logbox
    global logbox_cd, logbox_queued_msgs
    if not logbox_cd:
        logbox_cd = True
        if len(logbox_queued_msgs) > 0:
            msg = '\n'.join(logbox_queued_msgs) + '\n' + msg
            logbox_queued_msgs = []
        logbox.appendPlainText(msg)
        Thread(target=logbox_cooldown, daemon=True).start()
    else:
        logbox_queued_msgs.append(msg)
    scrollbar = logbox.verticalScrollBar()
    scrollbar.setValue(scrollbar.maximum())

import sys
sys.stderr.write = log_cmd
