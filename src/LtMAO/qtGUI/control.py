from PySide6.QtWidgets import (
    QWidget, 
    QLabel,
    QToolButton,
    QPlainTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
)

import os, os.path
from PIL import Image

from . import helper
from .. import setting, tools, Ritoddstex, winLT, hash_helper

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
                c.widget.setStyleSheet(f'background-color: rgb{qtwidgets.accent_color};')
            else:
                c.widget.setChecked(True)
        else:
            c.content.setVisible(False)
            if c.page_id == 100:
                c.widget.setStyleSheet(f'QStatusBar {{ background-color: rgba(0, 0, 0, 127) }} QStatusBar::hover {{ background-color: rgb{qtwidgets.accent_color}; }}')
            else:
                c.widget.setChecked(False)

    setting.set('qtGUI.page_id', page_id)
    setting.save()

all = [
    Control('🕹️\ncslmao', 0, lambda widget: build_cslmao(widget)),
    Control('📖\nhash_helper', 1, lambda widget: build_hash_helper(widget)),
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

def build_hash_helper(widget: QWidget):
    layout = QVBoxLayout()

    def get_hash_path(hash_id):
        if hash_id == 0:
            return setting.get('CDTBHashes.local_dir', hash_helper.CDTBHashes.local_dir)
        elif hash_id == 1:
            return setting.get('ExtractedHashes.local_dir', hash_helper.ExtractedHashes.local_dir)
        else:
            return setting.get('CustomHashes.local_dir', hash_helper.CustomHashes.local_dir)

    def set_hash_path(hash_id, label):
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(widget, 'Select hash folder', setting.get('qtGUI.default_folder', None))
        if dirpath != '':
            abspath = os.path.abspath(dirpath).replace('\\', '/')
            abspath_cdtb = os.path.abspath(hash_helper.CDTBHashes.local_dir).replace('\\', '/')
            abspath_extracted = os.path.abspath(hash_helper.ExtractedHashes.local_dir).replace('\\', '/')
            abspath_custom = os.path.abspath(hash_helper.CustomHashes.local_dir).replace('\\', '/')
            if hash_id == 0:
                if abspath in (abspath_extracted, abspath_custom):
                    raise Exception(f'hash_manager: Error: Set hash path: {abspath} is already selected as another hash path. All hash paths must be different.')
                hash_helper.CDTBHashes.local_dir = abspath
                setting.set('CDTBHashes.local_dir', abspath)
            elif hash_id == 1:
                if abspath in (abspath_cdtb, abspath_custom):
                    raise Exception(f'hash_manager: Error: Set hash path: {abspath} is already selected as another hash path. All hash paths must be different.')
                hash_helper.ExtractedHashes.local_dir = abspath
                setting.set('ExtractedHashes.local_dir', abspath)
            else:
                if abspath in (abspath_cdtb, abspath_extracted):
                    raise Exception(f'hash_manager: Error: Set hash path: {abspath} is already selected as another hash path. All hash paths must be different.')
                hash_helper.CustomHashes.local_dir = abspath
                setting.set('CustomHashes.local_dir', abspath)
            setting.save()
            label.setText(f'📖 {hash_name}: {get_hash_path(hash_id)}')

    def open_hash_path(hash_id):
        if hash_id == 0:
            os.startfile(os.path.abspath(hash_helper.CDTBHashes.local_dir))
        elif hash_id == 1:
            os.startfile(os.path.abspath(hash_helper.ExtractedHashes.local_dir))
        else:
            os.startfile(os.path.abspath(hash_helper.CustomHashes.local_dir))
    
    for hash_id, hash_name in enumerate(['CDTB', 'Extracted', 'Custom']):
        layout2 = QHBoxLayout()
        label = QLabel(f'📖 {hash_name}: {get_hash_path(hash_id)}')
        layout2.addWidget(label, stretch=8)
        button = QToolButton()
        button.setText('🛠️ Change')
        button.clicked.connect(lambda event, id=hash_id: set_hash_path(id, label))
        layout2.addWidget(button, stretch=1)
        button = QToolButton()
        button.setText('📂 Open')
        button.clicked.connect(lambda event, id=hash_id: open_hash_path(id))
        layout2.addWidget(button, stretch=1)
        layout.addLayout(layout2)

    button = QToolButton()
    button.setText('❌ Reset Custom hash to CDTB hash')
    button.clicked.connect(lambda event: hash_helper.reset_custom_hashes(*hash_helper.ALL_HASHES))
    layout.addWidget(button)
    layout.addStretch()
    widget.setLayout(layout)

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
            file_2x = os.path.join(dirname, '2x_'+basename)
            width_4x = img.width // 4
            height_4x = img.height // 4
            file_4x = os.path.join(dirname, '4x_'+basename)
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
        if isfile:
            filepaths = dialog.getOpenFileNames(
                widget, 
                f'Select {input_type}s',
                setting.get('qtGUI.default_folder', None),
                f'{input_type} Files (*.{input_type})'
            )
            if len(filepaths[0]) > 0:
                final_paths += filepaths[0]
        else:
            dirpath = dialog.getExistingDirectory(
                widget,
                f'Select Folder',
                setting.get('qtGUI.default_folder', None),
            )
            if dirpath != '':
                for root, dirs, files in os.walk(dirpath):
                    for file in files:
                        if file.endswith(f'.{input_type.lower()}'):
                            final_paths.append(os.path.join(root, file).replace('\\', '/'))
        final_path_count = len(final_paths)
        if  final_path_count > 0:
            def convert_thrd():
                print(f'ddsmart: Start: {title}: {final_path_count} items.')
                for final_path in final_paths:
                    func(final_path)
                print(f'ddsmart: Finish: {title}: {final_path_count} items.')
            helper.SafeThread.start('ddsmart', convert_thrd)
        
            
    
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
    layout = QVBoxLayout()
    
    # default folder
    layout2 = QHBoxLayout()
    button = QToolButton()
    button.setText('🌳 Default folder: ')
    def default_dir_cmd():
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget,
            f'Select Folder',
            setting.get('qtGUI.default_folder', None),
        )
        if dirpath == '':
            dirpath = None
            qtwidgets.default_dir_label.setText('Default path for all file/dir dialog.')
        else:
            qtwidgets.default_dir_label.setText(dirpath)
        setting.set('qtGUI.default_folder', dirpath)
        setting.save()
    button.clicked.connect(default_dir_cmd)
    layout2.addWidget(button)
    qtwidgets.default_dir_label = label = QLabel(setting.get('qtGUI.default_folder', 'Default path for all file/dir dialog.'))
    label.setStyleSheet('background-color: transparent')
    layout2.addWidget(label)
    layout2.addStretch()
    layout.addLayout(layout2)
    # winlt stuffs
    layout2 = QHBoxLayout()
    button = QToolButton()
    button.setText('💬 Create explorer context')
    button.clicked.connect(winLT.Context.create_contexts)
    layout2.addWidget(button)
    button = QToolButton()
    button.setText('❌ Remove explorer context')
    button.clicked.connect(winLT.Context.remove_contexts)
    layout2.addWidget(button)
    button = QToolButton()
    button.setText('🖥️ Create desktop shortcut')
    button.clicked.connect(winLT.Shortcut.create_desktop)
    layout2.addWidget(button)
    layout2.addStretch()
    layout.addLayout(layout2)
    # restart + update + support
    layout2 = QHBoxLayout()
    button = QToolButton()
    button.setText('🚀 Restart LtMAO')
    def restart_cmd():
        import sys
        print(f'Running: Restart LtMAO')
        os.system(os.path.join(os.path.abspath(os.path.curdir),'start.bat'))
        qtwidgets.main_window.close()
        sys.exit(0)
        
    button.clicked.connect(restart_cmd)
    layout2.addWidget(button)
    button = QToolButton()
    button.setText('🛠️ Redownload LtMAO')
    def redownload_ltmao():
        def redownload_thrd():
            def to_human(size): 
                return str(size >> ((max(size.bit_length()-1, 0)//10)*10)) + ["", " KB", " MB", " GB", " TB", " PB", " EB"][max(size.bit_length()-1, 0)//10]
            
            import requests
            local_file = './LtMAO-hai.zip'
            remote_file = 'https://codeload.github.com/tarngaina/LtMAO/zip/refs/heads/hai'
            # GET request
            get = requests.get(remote_file, stream=True)
            get.raise_for_status()
            # download update
            bytes_downloaded = 0
            chunk_size = 1024**2*5
            bytes_downloaded_log = 0
            bytes_downloaded_log_limit = 1024**2
            with open(local_file, 'wb') as f:
                for chunk in get.iter_content(chunk_size):
                    chunk_length = len(chunk)
                    bytes_downloaded += chunk_length
                    f.write(chunk)
                    bytes_downloaded_log += chunk_length
                    if bytes_downloaded_log > bytes_downloaded_log_limit:
                        print(
                            f'update_ltmao: Downloading: {remote_file}: {to_human(bytes_downloaded)}')
                        bytes_downloaded_log = 0
            print(f'update_ltmao: Finish: Download: {local_file}')
            # extract update
            from zipfile import ZipFile
            with ZipFile(local_file) as zip:
                for zipinfo in zip.infolist():
                    zipinfo.filename = zipinfo.filename.replace('LtMAO-hai/', '')
                    try:
                        zip.extract(zipinfo, '.')
                    except Exception as e:
                        filename = zipinfo.filename
                        print(f'update_ltmao: Error but ignored: Extract: {filename}: {e}')
            # remove update file
            os.remove(local_file)
            # restat ltmao
            restart_cmd()

        helper.SafeThread.start('update_ltmao', redownload_thrd)
    button.clicked.connect(redownload_ltmao)
    layout2.addWidget(button)
    button = QToolButton()
    button.setText('🤝 Support me')
    def support_cmd():
        import webbrowser
        webbrowser.open('https://paypal.me/tarngaina')
    button.clicked.connect(support_cmd)
    layout2.addWidget(button)
    layout2.addStretch()
    layout.addLayout(layout2)
    
    layout.addStretch()
    widget.setLayout(layout)

