
from PySide6.QtWidgets import (
    QWidget, 
    QToolButton,
    QPlainTextEdit,
    QVBoxLayout,
    QHBoxLayout,
)
from .. import setting

qtwidgets = None

class Control: 
    def __init__(self, name, page_id, build_command):
        self.name = name
        self.page_id = page_id
        self.widget: QToolButton = None
        self.content: QWidget = None
        self.build_command = build_command
        self.built = False
        
def on_page_id_changed(event, page_id):
    for c in all:
        if c.page_id == page_id:
            c.content.setVisible(True)
            if c.page_id == 100:
                c.widget.setStyleSheet(f'background-color: rgb{qtwidgets.accent_color}')
            else:
                c.widget.setChecked(True)
        else:
            c.content.setVisible(False)
            if c.page_id == 100:
                c.widget.setStyleSheet(f'background-color: rgba(0, 0, 0, 127); :hover {{ background-color: rgb{qtwidgets.accent_color} }}')
            else:
                c.widget.setChecked(False)

    setting.set('qtGUI.page_id', page_id)
    setting.save()

all = [
    Control('🕹️\ncslmao', 0, lambda widget: build_cslmao(widget)),
    Control('📖\nhash_helper', 1, lambda widget: build_hashmanager(widget)),
    Control('🎬\nmask_viewer', 2, lambda widget: build_mask_viewer(widget)),
    Control('🐱\nhapiBin', 3, lambda widget: build_hapiBin(widget)),
    Control('🚫\nno_skin', 4, lambda widget: build_no_skin(widget)),
    Control('🧱\nuvee', 5, lambda widget: build_uvee(widget)),
    Control('📦\nwad_tool', 6, lambda widget: build_wad_tool(widget)),
    Control('🛠️\nsborf', 7, lambda widget: build_sborf(widget)),
    Control('🍋\nlemon3d', 8, lambda widget: build_lemon3d(widget)),
    Control('🛣️\nddsmart', 9, lambda widget: build_ddsmart(widget)),
    Control('🔊\nbnk_tool', 10, lambda widget: build_bnk_tool(widget)),
]
extras = []

def build_cslmao(widget: QWidget):
    widget.setStyleSheet(f'background-color: rgba(255, 0, 0, 127)')

def build_hashmanager(widget: QWidget):
    widget.setStyleSheet(f'background-color: rgba(255, 255, 0, 127)')

def build_mask_viewer(widget: QWidget):
    widget.setStyleSheet(f'background-color: rgba(255, 255, 255, 127)')

def build_hapiBin(widget: QWidget):
    widget.setStyleSheet(f'background-color: rgba(0, 255, 0, 127)')

def build_no_skin(widget: QWidget):
    widget.setStyleSheet(f'background-color: rgba(0, 255, 255, 127)')

def build_uvee(widget: QWidget):
    widget.setStyleSheet(f'background-color: rgba(255, 0, 255, 127)')

def build_wad_tool(widget: QWidget):
    widget.setStyleSheet(f'background-color: rgba(0, 0, 255, 127)')

def build_sborf(widget: QWidget):
    widget.setStyleSheet(f'background-color: rgba(0, 0, 0, 127)')

def build_lemon3d(widget: QWidget):
    widget.setStyleSheet(f'background-color: rgba(127, 255, 255, 127)')

def build_ddsmart(widget: QWidget):
    widget.setStyleSheet(f'background-color: rgba(255, 255, 127, 127)')

def build_bnk_tool(widget: QWidget):
    widget.setStyleSheet(f'background-color: rgba(255, 127, 255, 127)')

def build_logbox(widget: QWidget):
    layout = QVBoxLayout()
    qtwidgets.logbox = logbox = QPlainTextEdit()
    logbox.setReadOnly(True)
    layout.addWidget(logbox, stretch=1)
    widget.setLayout(layout)

def build_changelog(widget: QWidget):
    layout = QVBoxLayout()
    qtwidgets.changelog = changelog = QPlainTextEdit()
    changelog.setReadOnly(True)
    layout.addWidget(changelog, stretch=1)
    widget.setLayout(layout)

def build_setting(widget: QWidget):
    widget.setStyleSheet(f'background-color: rgba(127, 127, 255, 127)')
