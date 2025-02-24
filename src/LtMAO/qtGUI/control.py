from PySide6.QtCore import (
    Qt,
)
from PySide6.QtWidgets import (
    QWidget, 
    QLabel,
    QToolButton,
    QPlainTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,

)

import os, posixpath
from PIL import Image

from . import log, helper
from .. import setting, tools, Ritoddstex
LOG = log.LOG

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
    # helper function since dont have a ddsmart.py???
    def make2x4x(src):
        with Image.open(src) as img:
            basename = os.path.basename(src)
            dirname = os.path.dirname(src)
            width_2x = img.width // 2
            height_2x = img.height // 2
            file_2x = os.path.join(dirname, '2x_'+basename).replace('\\', '/')
            width_4x = img.width // 4
            height_4x = img.height // 4
            file_4x = os.path.join(dirname, '4x_'+basename).replace('\\', '/')
        if not os.path.exists(file_2x):
            tools.ImageMagick.resize_dds(
                src=src,
                dst=file_2x, width=width_2x, height=height_2x
            )
        if not os.path.exists(file_4x):
            tools.ImageMagick.resize_dds(
                src=src,
                dst=file_4x, width=width_4x, height=height_4x
            )

    

    def convert_cmd(isfile, title, input_type, func):
        dialog = QFileDialog()
        final_paths = []
        # scan first
        if isfile:
            filepaths = dialog.getOpenFileNames(
                widget, 
                f'Select {input_type}s',
                setting.get('default_folder', None),
                f'{input_type} Files (*.{input_type})'
            )
            if len(filepaths[0]) > 0:
                final_paths += filepaths[0]
        else:
            dirpath = dialog.getExistingDirectory(
                widget,
                f'Select Folder',
                setting.get('default_folder', None),
            )
            if dirpath != '':
                for root, dirs, files in os.walk(dirpath):
                    for file in files:
                        if file.endswith(f'.{input_type.lower()}'):
                            final_paths.append(posixpath.join(root, file).replace('\\','/'))
        final_path_count = len(final_paths)
        if  final_path_count > 0:
            LOG(f'ddsmart: Start: {title}: {final_path_count} items.')
            helper.SafeThread.start('ddsmart', lambda: [func(final_path) for final_path in final_paths])
            LOG(f'ddsmart: Finish: {title}: {final_path_count} items.')
    
    converters = [
        { 
            'title': 'DDS to PNG',
            'input_type': 'DDS',
            'icon': '🏞️',
            'func': lambda src: tools.ImageMagick.to_png(
                src=src,
                png=src.replace('.dds', '.png')
            ),
        },
        { 
            'title': 'PNG to DDS',
            'input_type': 'PNG',
            'icon': '🌇',
            'func': lambda src: tools.ImageMagick.to_dds(
                src=src,
                png=src.replace('.png', '.dds')
            ),
        },
        { 
            'title': 'DDS to TEX',
            'input_type': 'DDS',
            'icon': '🏞️',
            'func': lambda src: Ritoddstex.dds2tex(src)
        },
        { 
            'title': 'TEX to DDS',
            'input_type': 'TEX',
            'icon': '🌌',
            'func': lambda src: Ritoddstex.tex2dds(src)
        },
        { 
            'title': 'Make 2x, 4x DDS',
            'input_type': 'DDS',
            'icon': '🏞️',
            'func': lambda src: make2x4x(src)
        },
    ]

    layout = QVBoxLayout()
    for converter in converters:
        label = QLabel(converter['title'])
        label.setStyleSheet('background-color: transparent')
        layout.addWidget(label)

        layout2 = QHBoxLayout()
        file_button = QToolButton()
        file_button.setText(f'{converter["icon"]} Select {converter['input_type']}')
        file_button.clicked.connect(lambda event, converter=converter: convert_cmd(True, converter['title'], converter['input_type'], converter['func']))
        layout2.addWidget(file_button)
        dir_button = QToolButton()
        dir_button.setText('📁 Select Folder')
        dir_button.clicked.connect(lambda event, converter=converter: convert_cmd(False, converter['title'], converter['input_type'], converter['func']))
        layout2.addWidget(dir_button)
        layout2.addStretch()
        layout.addLayout(layout2)

    layout.addStretch()
    widget.setLayout(layout)


def build_bnk_tool(widget: QWidget):
    widget.setStyleSheet(f'background-color: rgba(255, 127, 255, 127)')

def build_logbox(widget: QWidget):
    layout = QVBoxLayout()
    qtwidgets.logbox = logbox = QPlainTextEdit()
    logbox.setReadOnly(True)
    logbox.setMaximumBlockCount(1000)
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
