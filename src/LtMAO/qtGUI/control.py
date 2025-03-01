from PySide6.QtWidgets import (
    QWidget, 
    QLabel,
    QToolButton,
    QPlainTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QCheckBox,
    QLineEdit,
    QScrollArea,
    QTabWidget,
    QComboBox,
    QGridLayout,
    QTableWidget,
    QTableWidgetItem,
    QItemDelegate,
)
from PySide6.QtCore import Qt

import os, os.path
from PIL import Image

from . import helper
from .. import setting, tools, Ritoddstex, winLT, hash_helper, pyRitoFile, hapiBin, no_skin, sborf, mask_viewer
from ..lemon3d import lemon_fbx, lemon_maya

qtwidgets = None

class Control: 
    def __init__(self, name, page_id, build_command):
        self.name = name
        self.page_id = page_id
        self.widget: QToolButton = None
        self.content: QWidget = None
        self.build_command = build_command
        
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
    Control('📦\nwad_tool', 5, lambda widget: build_wad_tool(widget)),
    Control('🛠️\nsborf', 6, lambda widget: build_sborf(widget)),
    Control('🍋\nlemon3d', 7, lambda widget: build_lemon3d(widget)),
    Control('🛣️\nddsmart', 8, lambda widget: build_ddsmart(widget)),
    Control('🔊\nbnk_tool', 9, lambda widget: build_bnk_tool(widget)),
]
extras = []

def build_cslmao(widget: QWidget):
    widget.setStyleSheet(f'background-color: rgba(255, 0, 0, 127)')

def build_hash_helper(widget: QWidget):
    layout = QVBoxLayout()

    # path hash + reset button
    def get_hash_size(hash_id):
        if hash_id == 0:
            return hash_helper.CDTBHashes.calculate_size()
        elif hash_id == 1:
            return hash_helper.ExtractedHashes.calculate_size()
        else:
            return hash_helper.CustomHashes.calculate_size()

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
                    raise Exception(f'hash_helper: Error: Set hash path: {abspath} is already selected as another hash path. All hash paths must be different.')
                hash_helper.CDTBHashes.local_dir = abspath
                setting.set('CDTBHashes.local_dir', abspath)
            elif hash_id == 1:
                if abspath in (abspath_cdtb, abspath_custom):
                    raise Exception(f'hash_helper: Error: Set hash path: {abspath} is already selected as another hash path. All hash paths must be different.')
                hash_helper.ExtractedHashes.local_dir = abspath
                setting.set('ExtractedHashes.local_dir', abspath)
            else:
                if abspath in (abspath_cdtb, abspath_extracted):
                    raise Exception(f'hash_helper: Error: Set hash path: {abspath} is already selected as another hash path. All hash paths must be different.')
                hash_helper.CustomHashes.local_dir = abspath
                setting.set('CustomHashes.local_dir', abspath)
            setting.save()
            label.setText(f'📖 {hash_name}: {get_hash_size(hash_id)}] {get_hash_path(hash_id)}')

    def open_hash_path(hash_id):
        if hash_id == 0:
            os.startfile(os.path.abspath(hash_helper.CDTBHashes.local_dir))
        elif hash_id == 1:
            os.startfile(os.path.abspath(hash_helper.ExtractedHashes.local_dir))
        else:
            os.startfile(os.path.abspath(hash_helper.CustomHashes.local_dir))
    
    for hash_id, hash_name in enumerate(['CDTB', 'Extracted', 'Custom']):
        layout2 = QHBoxLayout()
        label = QLabel(f'📖 {hash_name}: [{get_hash_size(hash_id)}] {get_hash_path(hash_id)}')
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

    layout2 = QHBoxLayout()
    button = QToolButton()
    button.setText('❌ Reset Custom hash to CDTB hash')
    button.clicked.connect(lambda event: hash_helper.reset_custom_hashes(*hash_helper.ALL_HASHES))
    layout2.addWidget(button)
    button = QToolButton()
    button.setText('❌ Clear Extract hash')
    button.clicked.connect(lambda event: hash_helper.clear_extract_hashes(*hash_helper.ALL_HASHES))
    layout2.addWidget(button)
    layout2.addStretch()
    layout.addLayout(layout2)

    # extract hash
    def extract_hash(isfile):
        dialog = QFileDialog()
        final_paths = []
        if isfile:
            filepaths = dialog.getOpenFileNames(
                widget, 
                f'Select WADs',
                setting.get('qtGUI.default_folder', None),
                f'WAD Files (*.wad.client)'
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
                        final_paths.append(os.path.join(root, file).replace('\\', '/'))
        final_path_count = len(final_paths)
        if  final_path_count > 0:
            def extract_thrd():
                print(f'hash_helper: Start: Extract hashes with {final_path_count} items.')
                hash_helper.ExtractedHashes.extract(*final_paths)
                print('hash_helper: Finish: Extract hashes.')
            helper.SafeThread.start('hash_helper', extract_thrd)

    layout2 = QHBoxLayout()
    button = QToolButton()
    button.setText('📦 Extract from WADs')
    button.clicked.connect(lambda event: extract_hash(True))
    layout2.addWidget(button)
    button = QToolButton()
    button.setText('📁 Extract from Folder')
    button.clicked.connect(lambda event: extract_hash(False))
    layout2.addWidget(button)
    layout2.addStretch()
    layout.addLayout(layout2)

    # generate bin hash
    layout2 = QHBoxLayout()
    layout3 = QVBoxLayout()
    label = QLabel('🤖 Generate BIN hash:')
    label.setMinimumHeight(40)
    layout3.addWidget(label, stretch=1)
    textedit = QPlainTextEdit()
    layout3.addWidget(textedit, stretch=99) 
    layout2.addLayout(layout3, stretch=1)
    layout3 = QVBoxLayout()
    layout4 = QHBoxLayout()
    def add_bin_hash(binhash_name):
        raws = [text for text in textedit.toPlainText().split('\n') if text != '']
        hashes =  [text for text in textedit2.toPlainText().split('\n') if text != '']
        raw_count = len(raws)
        if raw_count > 0:
            filename = f'hashes.bin{binhash_name.lower()}.txt'
            hash_helper.CustomHashes.read_hashes(filename)
            for i in range(len(raws)):
                hash_helper.HASHTABLES[filename][hashes[i]] = raws[i]
            hash_helper.CustomHashes.write_hashes(filename)
            hash_helper.CustomHashes.free_hashes(filename)
            print(f'hash_helper: Finish: Add {raw_count} hashes to {filename} of custom hash.')
    for binhash_name in ['Entries', 'Fields', 'Types', 'Hashes']:
        button = QToolButton()
        button.setText('✍️ '+binhash_name)
        button.clicked.connect(lambda event, binhash_name=binhash_name: add_bin_hash(binhash_name))
        layout4.addWidget(button)
    layout4.addStretch()
    layout3.addLayout(layout4, stretch=1)
    textedit2 = QPlainTextEdit()
    textedit2.setReadOnly(True)
    layout3.addWidget(textedit2, stretch=99) 
    layout2.addLayout(layout3, stretch=1)
    layout.addLayout(layout2)
    def input_text():
        textedit2.clear()
        textedit2.setPlainText('\n'.join([pyRitoFile.bin_hash(text) if text != '' else '' for text in textedit.toPlainText().split('\n')]))
    textedit.textChanged.connect(input_text)
    
    # generate wad hash
    layout2 = QHBoxLayout()
    layout3 = QVBoxLayout()
    label = QLabel('🤖 Generate WAD hash:')
    label.setMinimumHeight(40)
    layout3.addWidget(label, stretch=1)
    textedit3 = QPlainTextEdit()
    layout3.addWidget(textedit3, stretch=99) 
    layout2.addLayout(layout3, stretch=1)
    layout3 = QVBoxLayout()
    layout4 = QHBoxLayout()
    def add_wad_hash(wadhash_name):
        raws = [text for text in textedit3.toPlainText().split('\n') if text != '']
        hashes =  [text for text in textedit4.toPlainText().split('\n') if text != '']
        raw_count = len(raws)
        if raw_count > 0:
            filename = f'hashes.{wadhash_name.lower()}.txt'
            hash_helper.CustomHashes.read_hashes(filename)
            for i in range(len(raws)):
                hash_helper.HASHTABLES[filename][hashes[i]] = raws[i]
            hash_helper.CustomHashes.write_hashes(filename)
            hash_helper.CustomHashes.free_hashes(filename)
            print(f'hash_helper: Finish: Add {raw_count} hashes to {filename} of custom hash.')
    for wadhash_name in ['Game', 'Lcu']:
        button = QToolButton()
        button.setText('✍️ '+wadhash_name)
        button.clicked.connect(lambda event, wadhash_name=wadhash_name: add_wad_hash(wadhash_name))
        layout4.addWidget(button)
    layout4.addStretch()
    layout3.addLayout(layout4, stretch=1)
    textedit4 = QPlainTextEdit()
    textedit4.setReadOnly(True)
    layout3.addWidget(textedit4, stretch=99) 
    layout2.addLayout(layout3, stretch=1)
    layout.addLayout(layout2)
    def input_text():
        textedit4.clear()
        textedit4.setPlainText('\n'.join([pyRitoFile.wad_hash(text) if text != '' else '' for text in textedit3.toPlainText().split('\n')]))
    textedit3.textChanged.connect(input_text)


    layout.addStretch()
    widget.setLayout(layout)

def build_mask_viewer(widget: QWidget):
    layout = QVBoxLayout()
    
    # browse layout
    layout2 = QGridLayout()
    def browse(line, title, file_type):
        dialog = QFileDialog()
        filepath = dialog.getOpenFileName(
            widget, 
            title,
            setting.get('qtGUI.default_folder', None),
            f'{file_type} Files (*.{file_type.lower()})'
        )
        if len(filepath[0]) > 0:
            final_path = filepath[0]
            line.setText(final_path)
    # skl
    skl_line = QLineEdit()
    layout2.addWidget(skl_line, 0, 0)
    button = QToolButton()
    button.setText('🦴 Browse SKL')    
    button.setMinimumWidth(260)
    button.clicked.connect(lambda event, line=skl_line: browse(line, 'Select SKL', 'SKL'))
    layout2.addWidget(button, 0, 1)
    # bin
    anm_bin_line = QLineEdit()
    layout2.addWidget(anm_bin_line, 1, 0)
    button = QToolButton()
    button.setText('📝 Browse Animation BIN')    
    button.setMinimumWidth(260)
    button.clicked.connect(lambda event, line=anm_bin_line: browse(line, 'Select Animation BIN', 'BIN'))
    layout2.addWidget(button, 1, 1)
    layout.addLayout(layout2)

    # table init 
    table = QTableWidget()
    class WeightValidate(QItemDelegate):
        def createEditor(self, parent, option, index):
            w = QLineEdit(parent)
            w.setInputMask('0.000')
            return w
    weight_validate = WeightValidate()
    table.setItemDelegate(weight_validate)
    qtwidgets.mask_viewer_bin_file = None

    # action button
    layout2 = QHBoxLayout()
    button = QToolButton()
    button.setText('🗿 Load')
    button.clicked.connect(lambda event: load_table(skl_line, anm_bin_line, table))
    layout2.addWidget(button)

    button = QToolButton()
    button.setText('💾 Save as')
    button.clicked.connect(lambda event: save_table(table))
    layout2.addWidget(button)
    
    button = QToolButton()
    button.setText('❌ Clear')
    button.clicked.connect(lambda event: clear_table(table))
    layout2.addWidget(button)

    layout2.addWidget(QLabel('💡 Correct weight value range: [0.000-1.000]'))
    layout2.addStretch()
    layout.addLayout(layout2)

    layout.addWidget(table, stretch=1)

    # action cmds
    def load_table(skl_line, anm_bin_line, table: QTableWidget):
        hash_helper.read_bin_hashes()
        skl_file = pyRitoFile.read_skl(skl_line.text())
        joint_names = [joint.name for joint in skl_file.joints]
        hash_helper.free_bin_hashes()
        qtwidgets.mask_viewer_bin_file = bin_file = pyRitoFile.read_bin(anm_bin_line.text())
        mask_data = mask_viewer.get_weights(bin_file)
        mask_names, weights = list(mask_data.keys()), list(mask_data.values())
        if len(joint_names) > len(weights):
            weights += [0.0] * (len(joint_names) - len(weights))
        table.setRowCount(len(joint_names))
        table.setColumnCount(len(mask_names))
        table.setHorizontalHeaderLabels(mask_names)
        table.setVerticalHeaderLabels(joint_names)
        for j in range(table.columnCount()):
            for i in range(table.rowCount()):
                table.setItem(i, j, QTableWidgetItem(str(weights[j][i])))
        print(f'mask_viewer: Finish: Load table: {anm_bin_line.text()}')

    def save_table(table: QTableWidget):
        dialog = QFileDialog()
        filepath = dialog.getSaveFileName(
            widget, 
            'Save Animation BIN as',
            setting.get('qtGUI.default_folder', None),
            f'BIN Files (*.bin)'
        )
        if len(filepath[0]) > 0:
            final_path = filepath[0]
            mask_data = {}
            for j in range(table.columnCount()):
                mask_data[table.horizontalHeaderItem(j).text()] = [float(table.itemAt(i, j).text()) for i in range(table.rowCount())]
            mask_viewer.set_weights(qtwidgets.mask_viewer_bin_file, mask_data)
            pyRitoFile.write_bin(final_path, qtwidgets.mask_viewer_bin_file)
            print(f'mask_viewer: Finish: Save table: {final_path}')

    def clear_table(table: QTableWidget):
        qtwidgets.mask_viewer_bin_file = None
        table.clear()
        table.setRowCount(0)
        table.setColumnCount(0)
        print(f'mask_viewer: Finish: Clear table.')

    layout.addStretch()
    widget.setLayout(layout)

def build_hapiBin(widget: QWidget):
    layout = QVBoxLayout()
    # tutorial label + backup
    layout2 = QHBoxLayout()
    label = QLabel("""
Target type (if needed) must match source type.
    📝 BIN: run functions directly on selected bin.
    📦 WAD/📁 Folder/🗃️ Fantome: run functions on all bins inside selected WAD/Folder/Fantome.
    """)
    layout2.addWidget(label, stretch=99)
    checkbox = QCheckBox()
    checkbox.setChecked(setting.get('hapiBin.backup', True))
    checkbox.setText('💿 Backup file')
    def backup_cmd():
        setting.set('hapiBin.backup', checkbox.isChecked())
        setting.save()
    checkbox.clicked.connect(backup_cmd)
    layout2.addWidget(checkbox, stretch=1)
    layout.addLayout(layout2)

    # browse stuffs
    def browse_cmd(line, browse_type):
        dialog = QFileDialog()
        final_path = ''
        if browse_type == 'BIN':
            filepaths = dialog.getOpenFileName(
                widget, 
                f'Select BINs',
                setting.get('qtGUI.default_folder', None),
                f'BIN Files (*.bin)'
            )
            if len(filepaths[0]) > 0:
                final_path = filepaths[0]
        elif browse_type == 'WAD':
            filepaths = dialog.getOpenFileName(
                widget, 
                f'Select WADs',
                setting.get('qtGUI.default_folder', None),
                f'WAD Files (*.wad.client)'
            )
            if len(filepaths[0]) > 0:
                final_path = filepaths[0]
        else:
            dirpath = dialog.getExistingDirectory(
                widget,
                f'Select Folder',
                setting.get('qtGUI.default_folder', None),
            )
            if dirpath != '':
                final_path = dirpath
        if final_path != '':
            line.setText(final_path)
    # source 
    src_line = QLineEdit()
    layout.addWidget(src_line)
    layout2 = QHBoxLayout()
    layout2.addStretch()
    for browse_type in ['BIN', 'WAD', 'Folder']:
        button = QToolButton()
        button.setText(f'🏹 Browse Source {browse_type}')
        button.clicked.connect(lambda event, line=src_line, browse_type=browse_type: browse_cmd(line, browse_type))
        layout2.addWidget(button)
    layout.addLayout(layout2)
    # target 
    dst_line = QLineEdit()
    layout.addWidget(dst_line)
    layout2 = QHBoxLayout()
    layout2.addStretch()
    for browse_type in ['BIN', 'WAD', 'Folder']:
        button = QToolButton()
        button.setText(f'🎯 Browse Target {browse_type}')
        button.clicked.connect(lambda event, line=dst_line, browse_type=browse_type: browse_cmd(line, browse_type))
        layout2.addWidget(button)
    layout.addLayout(layout2)

    # funcs
    def run_hp_command(src_line, dst_line, hp_command, require_dst):
        def run_hp_thrd():
            hapiBin.Helper.run_command(
                src=src_line.text(), 
                dst=dst_line.text(),
                hp_command=hp_command, 
                require_dst=require_dst, 
                backup=setting.get('hapiBin.backup', 1)
            )
        
        helper.SafeThread.start('hapiBin', run_hp_thrd)
    scrollarea = QScrollArea()
    layout2 = QVBoxLayout()
    for name, description, hp_command, require_dst in hapiBin.Helper.qt_datas: 
        button = QToolButton()
        button.setText(name)
        button.clicked.connect(lambda event, src_line=src_line, dst_line=dst_line, hp_command=hp_command, require_dst=require_dst: run_hp_command(src_line, dst_line, hp_command, require_dst))
        layout2.addWidget(button)
        label = QLabel(description)
        layout2.addWidget(label)
    scrollarea.setLayout(layout2)
    layout.addWidget(scrollarea, stretch=999)

    widget.setLayout(layout)

def build_no_skin(widget: QWidget):
    layout = QHBoxLayout()
    tab_widget = QTabWidget()
    tab_widget.setStyleSheet(qtwidgets.tab_stylesheet)
    
    # no skin full
    tab1 = QWidget()
    layout2 = QVBoxLayout()

    layout3 = QHBoxLayout()
    line = QLineEdit()
    layout3.addWidget(line, stretch=1)
    game_folder = setting.get('game_folder', '')
    if game_folder != '':
        line.setText(game_folder)
    button = QToolButton()
    button.setText('📁 Select Champions folder')
    def select_champions_folder(line):
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget,
            f'Select Champions Folder',
            setting.get('qtGUI.default_folder', None),
        )
        if dirpath != '':
            final_path = dirpath
            line.setText(final_path)
    button.clicked.connect(lambda event: select_champions_folder(line))
    layout3.addWidget(button)
    layout2.addLayout(layout3)
    
    layout3 = QHBoxLayout()
    button = QToolButton()
    button.setText('💾 Save SKIPS.json')
    layout3.addWidget(button)
    layout3.addStretch()
    button = QToolButton()
    button.setText('🐧 Make NO SKIN.fantome')
    def no_skin_full(line):
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget,
            f'Select Output Fantome Folder',
            setting.get('qtGUI.default_folder', None),
        )
        if dirpath != '':
            def no_skin_thrd():
                final_path = dirpath
                no_skin.parse(line.text(), final_path)
    
            helper.SafeThread.start('no_skin', no_skin_thrd)
    button.clicked.connect(lambda event: no_skin_full(line))
    layout3.addWidget(button)
    layout2.addLayout(layout3)

    # skips
    text = QPlainTextEdit()
    text.setPlainText(no_skin.get_skips())
    layout2.addWidget(text, stretch=1)
    def save_skips(text):
        no_skin.set_skips(text.toPlainText())
        no_skin.save_skips()
    button.clicked.connect(lambda event: save_skips(text))

    tab1.setLayout(layout2)
    tab_widget.addTab(tab1, '🔴 Full')
    # no skin lite
    tab2 = QWidget()
    layout2 = QVBoxLayout()

    layout3 = QHBoxLayout()
    label = QLabel()
    layout3.addWidget(label,stretch=99)
    button = QToolButton()
    button.setMinimumWidth(220)
    button.setText('📝 Select Skin0 BIN')
    def select_skin0(label):
        dialog = QFileDialog()
        filepaths = dialog.getOpenFileName(
            widget, 
            f'Select Skin0 BIN',
            setting.get('qtGUI.default_folder', None),
            f'BIN Files (*.bin)'
        )
        if len(filepaths[0]) > 0:
            final_path = filepaths[0]
            label.setText(final_path)
    button.clicked.connect(lambda event: select_skin0(label)) 
    layout3.addWidget(button)
    layout2.addLayout(layout3)

    layout3 = QHBoxLayout()
    text = QPlainTextEdit()
    text.setReadOnly(True)
    layout3.addWidget(text, stretch=99)
    button = QToolButton()
    button.setMinimumWidth(220)
    button.setText('📝 Select SkinX BINs')
    def select_skinx(text):
        dialog = QFileDialog()
        filepaths = dialog.getOpenFileNames(
            widget, 
            f'Select SkinX BINs',
            setting.get('qtGUI.default_folder', None),
            f'BIN Files (*.bin)'
        )
        if len(filepaths[0]) > 0:
            final_paths = filepaths[0]
        text.setPlainText('\n'.join(final_paths))
    button.clicked.connect(lambda event: select_skinx(text))
    layout3.addWidget(button, alignment=Qt.AlignmentFlag.AlignTop)
    layout2.addLayout(layout3, stretch=999)

    button = QToolButton()
    button.setText('🦭 Make all Skinx BIN same as Skin0 BIN')
    def no_skin_lite(label, text):
        def no_skin_thrd():
            no_skin.mini_no_skin(
                skin0_file=label.text(), 
                otherskins_files=text.toPlainText().split('\n')
            )
        
        helper.SafeThread.start('no_skin', no_skin_thrd)
    button.clicked.connect(lambda event: no_skin_lite(label, text))
    layout2.addWidget(button)
    
    #layout2.addStretch()
    tab2.setLayout(layout2)
    tab_widget.addTab(tab2, '⭕ Lite')

    
    layout.addWidget(tab_widget, stretch=1)
    widget.setLayout(layout)

def build_wad_tool(widget: QWidget):
    widget.setStyleSheet(f'background-color: rgba(0, 0, 255, 127)')

def build_sborf(widget: QWidget):
    layout = QVBoxLayout()
    # backup
    checkbox = QCheckBox()
    checkbox.setChecked(setting.get('sborf.backup', True))
    checkbox.setText('💿 Backup file')
    def backup_cmd():
        setting.set('sborf.backup', checkbox.isChecked())
        setting.save()
    checkbox.clicked.connect(backup_cmd)
    layout.addWidget(checkbox, alignment=Qt.AlignmentFlag.AlignLeft)
    # browse layout
    layout2 = QGridLayout()
    
    # your skin
    layout2.addWidget(QLabel('🐢 Your skin'), 0, 0)
    layout2.addWidget(QLabel('🐇 Rito skin'), 0, 2)

    def browse(line, title, file_type):
        dialog = QFileDialog()
        filepath = dialog.getOpenFileName(
            widget, 
            title,
            setting.get('qtGUI.default_folder', None),
            f'{file_type} Files (*.{file_type.lower()})'
        )
        if len(filepath[0]) > 0:
            final_path = filepath[0]
            line.setText(final_path)

    # skl
    skl_line = QLineEdit()
    skl_line.setPlaceholderText('Require')
    layout2.addWidget(skl_line, 1, 0)
    button = QToolButton()
    button.setText('🦴 Browse SKL')    
    button.setMinimumWidth(260)
    button.clicked.connect(lambda event, line=skl_line: browse(line, 'Select SKL', 'SKL'))
    layout2.addWidget(button, 1, 1)
    riot_skl_line = QLineEdit()
    riot_skl_line.setPlaceholderText('Require')
    layout2.addWidget(riot_skl_line, 1, 2)
    button = QToolButton()
    button.setText('🦴 Browse Riot SKL')    
    button.setMinimumWidth(260)
    button.clicked.connect(lambda event, line=riot_skl_line: browse(line, 'Select Riot SKL', 'SKL'))
    layout2.addWidget(button, 1, 3)

    # skn
    skn_line = QLineEdit()
    skn_line.setPlaceholderText('Require if fix your skin')
    layout2.addWidget(skn_line, 2, 0)
    button = QToolButton()
    button.setText('🧊 Browse SKN')    
    button.setMinimumWidth(260)
    button.clicked.connect(lambda event, line=skn_line: browse(line, 'Select SKN', 'SKN'))
    layout2.addWidget(button, 2, 1)
    riot_skn_line = QLineEdit()
    riot_skn_line.setPlaceholderText('Leave empty if dont need')
    layout2.addWidget(riot_skn_line, 2, 2)
    button = QToolButton()
    button.setText('🧊 Browse Riot SKN') 
    button.setMinimumWidth(260)   
    button.clicked.connect(lambda event, line=riot_skn_line: browse(line, 'Select Riot SKN', 'SKN'))
    layout2.addWidget(button, 2, 3)

    # anm bin
    anm_bin_line = QLineEdit()
    anm_bin_line.setPlaceholderText('Require if adapt MaskData')
    layout2.addWidget(anm_bin_line, 3, 0)
    button = QToolButton()
    button.setText('📝 Browse Animation BIN')    
    button.setMinimumWidth(260)
    button.clicked.connect(lambda event, line=anm_bin_line: browse(line, 'Select Animation BIN', 'BIN'))
    layout2.addWidget(button, 3, 1)
    riot_anm_bin_line = QLineEdit()
    riot_anm_bin_line.setPlaceholderText('Require if adapt MaskData')
    layout2.addWidget(riot_anm_bin_line, 3, 2)
    button = QToolButton()
    button.setText('📝 Browse Riot Animation BIN')    
    button.setMinimumWidth(260)
    button.clicked.connect(lambda event, line=riot_anm_bin_line: browse(line, 'Select Riot Animation BIN', 'BIN'))
    layout2.addWidget(button, 3, 3)
    
    layout.addLayout(layout2)

    # funcs
    button = QToolButton()
    button.setText('🐊 Fix your skin')
    layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignLeft)
    layout.addWidget(QLabel("""
Sort your SKL joints base on riot SKL, fill removed riot joints back and move new custom joints to the end of list.
Sort SKN vertex influences base on the new order.
If selected riot SKN, sort SKN materials base on riot SKN.
Throw exception if total joints = your SKL joints + removed joints > 256.',
    """), alignment=Qt.AlignmentFlag.AlignLeft) 
    button.clicked.connect(
        lambda event: sborf.skin_fix(
            skl_line.text(),
            skn_line.text(),
            riot_skl_line.text(),
            riot_skn_line.text(),
            setting.get('sborf.backup', True),
            False
        )
    )

    button = QToolButton()
    button.setText('🐸 Fix your skin but do not add removed riot joint back')
    layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignLeft)
    layout.addWidget(QLabel("""
Sort your custom SKL joints order similar to riot SKL and your new joints also moved to the end of list.
You may need to use custom animation BIN MaskData tho.
    """), alignment=Qt.AlignmentFlag.AlignLeft) 
    button.clicked.connect(
        lambda event: sborf.skin_fix(
            skl_line.text(),
            skn_line.text(),
            riot_skl_line.text(),
            riot_skn_line.text(),
            setting.get('sborf.backup', True),
            True
        )
    )

    button = QToolButton()
    button.setText('🦀 Adapt animation BIN MaskData')
    layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignLeft)
    layout.addWidget(QLabel("""
Copy MaskData weight values from riot animation BIN to your custom animation BIN base on your SKL+riot SKL.
New custom joints will have weight set to 0.0.
    """), alignment=Qt.AlignmentFlag.AlignLeft) 
    button.clicked.connect(
        lambda event: sborf.skin_fix(
            skl_line.text(),
            anm_bin_line.text(),
            riot_skl_line.text(),
            riot_anm_bin_line.text(),
            setting.get('sborf.backup', True),
        )
    )
    layout.addStretch()
    widget.setLayout(layout)

def build_lemon3d(widget: QWidget):
    layout = QHBoxLayout()
    tab_widget = QTabWidget()
    tab_widget.setStyleSheet(qtwidgets.tab_stylesheet)
    # fbx
    
    tab1 = QWidget()
    layout2 = QVBoxLayout()
    
    def browse(line, title, file_type):
        dialog = QFileDialog()
        filepath = dialog.getOpenFileName(
            widget, 
            title,
            setting.get('qtGUI.default_folder', None),
            f'{file_type} Files (*.{file_type.lower()})'
        )
        if len(filepath[0]) > 0:
            final_path = filepath[0]
            line.setText(final_path)

    # browse skin to fbx
    layout2.addWidget(QLabel('👽 SKIN to FBX'))
    layout3 = QGridLayout()
    skn_line = QLineEdit()
    layout3.addWidget(skn_line, 0, 0)
    button = QToolButton()
    button.setText('🧊 Browse SKN')    
    button.setMinimumWidth(260)
    button.clicked.connect(lambda event, line=skn_line: browse(line, 'Select SKN', 'SKN'))
    layout3.addWidget(button, 0, 1)
    skl_line = QLineEdit()
    layout3.addWidget(skl_line, 1, 0)
    button = QToolButton()
    button.setText('🦴 Browse SKL')    
    button.setMinimumWidth(260)
    button.clicked.connect(lambda event, line=skl_line: browse(line, 'Select SKL', 'SKL'))
    layout3.addWidget(button, 1, 1)
    layout2.addLayout(layout3)
    # to fbx
    layout3 = QHBoxLayout()
    button = QToolButton()
    button.setText('🚙 To FBX')
    layout3.addWidget(button)
    output_fbx = QLabel()
    skn_line.textChanged.connect(lambda event: output_fbx.setText(event.replace('.skn', '.fbx')))
    layout3.addWidget(output_fbx)
    layout2.addLayout(layout3)
    button.clicked.connect(lambda event: lemon_fbx.skin_to_fbx(skl_line.text(), skn_line.text(), output_fbx.text()))

    layout2.addSpacing(30)

    # browse fbx to skin
    layout2.addWidget(QLabel('👻 FBX to SKIN'))
    layout3 = QGridLayout()
    fbx_line = QLineEdit()
    layout3.addWidget(fbx_line, 0, 0)
    button = QToolButton()
    button.setText('🌄 Browse FBX')    
    button.setMinimumWidth(260)
    button.clicked.connect(lambda event, line=fbx_line: browse(line, 'Select FBX', 'FBX'))
    layout3.addWidget(button, 0, 1)
    layout2.addLayout(layout3)
    # to skin
    layout3 = QHBoxLayout()
    button = QToolButton()
    button.setText('🚗 To SKN + SKL')
    layout3.addWidget(button)
    output_skn = QLabel()
    fbx_line.textChanged.connect(lambda event: output_skn.setText(event.replace('.fbx', '.skn')))
    layout3.addWidget(output_skn)
    layout2.addLayout(layout3)
    button.clicked.connect(lambda event: lemon_fbx.fbx_to_skin(fbx_line.text(), output_skn.text().replace('.skn', '.skl'), output_skn.text()))

    layout2.addStretch()
    tab1.setLayout(layout2)
    tab_widget.addTab(tab1, '💦 fbx')


    # maya
    tab2 = QWidget()
    layout2 = QVBoxLayout()
    
    tab2.setLayout(layout2)
    tab_widget.addTab(tab2, '🔥 maya')
    layout.addWidget(tab_widget, stretch=1)
    widget.setLayout(layout)

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
 
    def convert(isfile, title, input_type, func):
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
        file_button.clicked.connect(lambda event, converter=converter: convert(True, converter['title'], converter['input_type'], converter['func']))
        layout2.addWidget(file_button)
        dir_button = QToolButton()
        dir_button.setText('📁 Select Folder')
        dir_button.clicked.connect(lambda event, converter=converter: convert(False, converter['title'], converter['input_type'], converter['func']))
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

    # theme
    layout2 = QHBoxLayout()
    layout2.addWidget(QLabel('☀️ Theme: '))
    box = QComboBox()
    box.setMinimumWidth(200)
    box.addItems(['raora', 'nahida', 'arona'])
    box.setCurrentText(setting.get('qtGUI.theme_name', 'raora'))
    def change_theme(box):
        setting.set('qtGUI.theme_name', box.currentText())
        setting.save()
        print('setting: Restart is require for theme changes to take effect.')
    
    box.currentTextChanged.connect(lambda event: change_theme(box))
    layout2.addWidget(box)
    layout2.addStretch()
    layout.addLayout(layout2)
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


