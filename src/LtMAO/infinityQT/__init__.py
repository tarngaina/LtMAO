import os.path, shutil
from PySide6.QtWidgets import (
    QApplication, 
    QMainWindow, 
)
from PySide6.QtGui import QPixmap

from . import skn, tex, wem, bin

infinityQT_dir = './pref/infinityQT'

def delete_cache():
    shutil.rmtree(infinityQT_dir, ignore_errors=True)

def build_tabs(paths):
    tabs = []
    for path in paths:
        title = os.path.basename(path)
        if path.endswith('.skn'):
            tabs.append((title, skn.create_widget(path)))
        elif path.endswith('.tex'):
            tabs.append((title, tex.create_widget(path)))
        elif path.endswith('.wem'):
            tabs.append((title, wem.create_widget(path)))
        elif path.endswith('.bin'):
            tabs.append((title, bin.create_widget(path)))
        else:
            tabs.append((title, None))

    return tabs

class PreviewGUI():
    def __init__(self):
        self.app = app = QApplication([])
        self.window = window = QMainWindow() 
        screen_size = app.primaryScreen().size()
        window.setGeometry((screen_size.width() - 1280) // 2, (screen_size.height() - 720) // 2, 1280, 720)
        # set icon
        from .. import setting
        setting.init()
        theme_name = setting.get('qtGUI.theme_name', 'raora')
        appicon = f'./res/themes/{theme_name}/appicon.ico'
        window.setWindowIcon(QPixmap(appicon))
    
    def set_central_widget(self, window_title, central_widget):
        self.window.setWindowTitle(window_title)
        self.window.setCentralWidget(central_widget)

    def show(self):
        self.window.show()
        self.app.exec()


def init():
    delete_cache()
    os.makedirs(infinityQT_dir, exist_ok=True)