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
    QTextEdit,
    QTreeView,
)
from PySide6.QtGui import QBrush, QColor, QStandardItem, QStandardItemModel, QPixmap
from PySide6.QtCore import Qt, QObject, Signal


import os, os.path
from PIL import Image
from threading import Thread

from . import helper
from .. import (
    setting, 
    tools, 
    Ritoddstex,
    winLT, 
    hash_helper, 
    pyRitoFile, 
    hapiBin, 
    no_skin, 
    sborf, 
    mask_viewer, 
    wad_tool,
    bnk_tool,
    cslmao
)
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

def build_cslmao(widget: QWidget):
    layout = QVBoxLayout()
    # setting bar
    layout2 = QHBoxLayout()
    button = QToolButton()
    button.setText('🎮 Select Game Folder')
    layout2.addWidget(button)
    label = QLabel()
    label.setText(setting.get('game_folder', 'Please select League of Legends/Game folder.'))
    layout2.addWidget(label, stretch=1)
    def select_game_folder(label):
        if is_overlay_running():
            return
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget,
            'Select League of Legends/Game folder',
            setting.get('qtGUI.default_folder', None)
        )
        if dirpath != '':
            final_path = dirpath.replace('\\', '/')
            if not os.path.exists(os.path.join(final_path, 'League of Legends.exe')):
                raise Exception(f'cslmao: Error:  Select game folder: No "League of Legends.exe" found in {final_path}')
            setting.set('game_folder', final_path)
            setting.save()
            label.setText(final_path)
    button.clicked.connect(lambda event: select_game_folder(label))

    checkbox = QCheckBox()
    checkbox.setText('🕹️ TFT and other modes')
    checkbox.setChecked(setting.get('cslmao.tft', False))
    def tft_cmd():
        setting.set('cslmao.tft', checkbox.isChecked())
        setting.save()
    checkbox.clicked.connect(tft_cmd)
    layout2.addWidget(checkbox)
    button = QToolButton()
    button.setText('🩺 Diagnose') 
    button.clicked.connect(cslmao.diagnose)
    layout2.addWidget(button)
    layout.addLayout(layout2)
    # action bar
    layout2 = QHBoxLayout()
    run_button = QToolButton()
    run_button.setText('🚀 Run')
    run_button.setMinimumWidth(130)
    layout2.addWidget(run_button)
    import_button = QToolButton()
    import_button.setText('📥 Import')
    import_button.setMinimumWidth(130)
    layout2.addWidget(import_button)
    new_button = QToolButton()
    new_button.setText('💥 New')
    new_button.setMinimumWidth(130)
    layout2.addWidget(new_button)
    layout2.addStretch()
    layout2.addWidget(QLabel('📚 Profile: '))
    box = QComboBox()
    box.setMinimumWidth(200)
    box.addItems(['all', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    box.setCurrentText(setting.get('cslmao.profile', 'all'))
    def change_profile():
        profile = box.currentText()
        refresh_profile(profile)
        setting.set('cslmao.profile', profile)
        setting.save()
    box.currentTextChanged.connect(change_profile)
    layout2.addWidget(box)
    layout.addLayout(layout2)
    # view layout
    scrollarea = QScrollArea()
    scrollarea.setWidgetResizable(True)
    view_widget = QWidget()
    view_layout = QVBoxLayout(scrollarea)
    view_layout.setContentsMargins(0, 0, 0, 0)
    view_layout.addStretch()
    view_widget.setLayout(view_layout)
    scrollarea.setWidget(view_widget)
    layout.addWidget(scrollarea, stretch=1)
    layout.addStretch()
    widget.setLayout(layout)

    # simple empty pixmap
    display_image_empty = QPixmap(192, 108)
    display_image_empty.fill(QColor(33, 33, 33))

    edit_image_empty = QPixmap(256, 144)
    edit_image_empty.fill(QColor(33, 33, 33))

    # main build function
    view_layout.mod_widgets = {}
    def build_mod_widget(mod):
        mod_widget = QWidget()
        info, image = cslmao.get_info(mod)

        # edit
        edit_layout = QHBoxLayout()
        edit_layout.setContentsMargins(0, 0, 0, 0)
        layout = QVBoxLayout()
        name_line = QLineEdit()
        layout.addWidget(name_line)
        author_line = QLineEdit()
        layout.addWidget(author_line)
        version_line = QLineEdit()
        layout.addWidget(version_line)
        desc_line = QLineEdit()
        layout.addWidget(desc_line)
        edit_layout.addLayout(layout)

        layout = QVBoxLayout()
        profile_box = QComboBox()
        profile_box.addItems(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        layout.addWidget(profile_box)
        edit_image = QLabel()
        def edit_image_cmd(event):
            dialog = QFileDialog()
            filepath = dialog.getOpenFileName(
                widget, 
                'Select PNG',
                setting.get('qtGUI.default_folder', None),
                f'PNG Files (*.png)'
            )
            if len(filepath[0]) > 0:
                final_path = filepath[0]
                mod_widget.edit_image_path = final_path
                edit_image.setPixmap(QPixmap(final_path).scaled(256, 144, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
            else:
                mod_widget.edit_image_path = None
                edit_image.setPixmap(edit_image_empty)

        edit_image.mousePressEvent = edit_image_cmd
        layout.addWidget(edit_image)
        edit_layout.addLayout(layout)

        layout = QVBoxLayout()
        button = QToolButton()
        button.setMinimumWidth(130)
        button.setText('❌ Back')
        def cancel_cmd():
            display_widget.setVisible(True)
            edit_widget.setVisible(False)
        button.clicked.connect(cancel_cmd)
        layout.addWidget(button)
        button = QToolButton()
        button.setMinimumWidth(130)
        button.setText('✔️ Confirm')
        def save_cmd():
            info = {
                'Name': name_line.text(),
                'Author': author_line.text(),
                'Version': version_line.text(),
                'Description': desc_line.text()
            }
            # very complex behaviour here
            image = None
            if hasattr(mod_widget, 'edit_image_path'): # mean that user at least click the image one
                image = mod_widget.edit_image_path  
                if image == None: # user click and remove image
                    cslmao.delete_info_image(mod)
            cslmao.set_info(mod, info, image)
            display_image.setPixmap(
                QPixmap(image).scaled(192, 108, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                if image != None else display_image_empty
            )
            mod.profile = profile_box.currentText()
            cslmao.save_mods()
            display_label.setText(f'📚 {mod.profile}\n🆔 {info["Name"]}\n👤 {info["Author"]}\n🏷️ {info["Version"]}\n📃 {info["Description"]}')
            refresh_profile(setting.get('cslmao.profile', 'all'))
            display_widget.setVisible(True)
            edit_widget.setVisible(False)
        button.clicked.connect(save_cmd)
        layout.addWidget(button)
        edit_layout.addLayout(layout)

        # display
        display_layout = QHBoxLayout()
        display_layout.setContentsMargins(0, 0, 0, 0)
        checkbox = QCheckBox()
        checkbox.setStyleSheet(':indicator { width: 30; height: 30; }')
        checkbox.setChecked(mod.enable)
        def enable_mod():
            if is_overlay_running():
                # reverse it bacc, big brain
                checkbox.setChecked(not checkbox.isChecked())
                return
            mod.enable = checkbox.isChecked()
            cslmao.save_mods()
        checkbox.clicked.connect(enable_mod)
        display_layout.addWidget(checkbox)
        
        display_image = QLabel()
        display_image.setPixmap(
            QPixmap(image).scaled(192, 108, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
            if image != None else display_image_empty
        )
        display_layout.addWidget(display_image)

        display_label = QLabel()
        display_label.setText(f'📚 {mod.profile}\n🆔 {info["Name"]}\n👤 {info["Author"]}\n🏷️ {info["Version"]}\n📃 {info["Description"]}')
        display_layout.addWidget(display_label, stretch=1)
        
        layout = QGridLayout()
        button = QToolButton()
        button.setMinimumWidth(130)
        button.setText('📂 Locate')
        def locate_cmd():
            os.startfile(os.path.join(cslmao.raw_dir, mod.get_path()))
        button.clicked.connect(locate_cmd)
        layout.addWidget(button, 0, 0)
        button = QToolButton()
        button.setMinimumWidth(130)
        button.setText('✏️ Edit')
        def edit_cmd():
            if is_overlay_running():
                return
            info, image = cslmao.get_info(mod)
            name_line.setText(info['Name'])
            author_line.setText(info['Author'])
            version_line.setText(info['Version'])
            desc_line.setText(info['Description'])
            profile_box.setCurrentText(mod.profile)
            edit_image.setPixmap(
                QPixmap(image).scaled(256, 144, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
                if image != None else edit_image_empty
            )
            display_widget.setVisible(False)
            edit_widget.setVisible(True)
        button.clicked.connect(edit_cmd)
        layout.addWidget(button, 1, 0)
        button = QToolButton()
        button.setMinimumWidth(130)
        button.setText('📤 Export')
        def export_cmd():
            if is_overlay_running():
                return
            dialog = QFileDialog()
            info, image = cslmao.get_info(mod)
            default_filename = f'{info["Name"]} V{info["Version"]} by {info["Author"]}.fantome'
            filepath = dialog.getSaveFileName(
                widget, 
                'Export FANTOME',
                os.path.join(setting.get('qtGUI.default_folder', ''), default_filename),
                f'FANTOME File (*.fantome)'
            )
            if len(filepath[0]) > 0:
                final_path = filepath[0]
                def export_thrd():
                    p = cslmao.export_fantome(
                        mod_path=os.path.join(
                            cslmao.raw_dir,
                            mod.get_path()
                        ),
                        fantome_path=final_path
                    )
                    if p.returncode == 0:
                        print(f'cslmao: Exported: {final_path}')
                helper.SafeThread.start('cslmao', export_thrd)

        button.clicked.connect(export_cmd)
        layout.addWidget(button, 0, 1)
        button = QToolButton()
        button.setMinimumWidth(130)
        button.setText('❌ Remove')
        def remove_cmd():
            if is_overlay_running():
                return
            mod_widget.setParent(None)
            view_layout.mod_widgets.pop(mod)
            cslmao.delete_mod(mod)
            cslmao.save_mods()
        button.clicked.connect(remove_cmd)
        layout.addWidget(button, 1, 1)
        display_layout.addLayout(layout)

        mod_layout = QVBoxLayout()
        mod_layout.setContentsMargins(0, 0, 0, 0)
        edit_widget = QWidget()
        edit_widget.setLayout(edit_layout)
        edit_widget.setVisible(False)
        mod_layout.addWidget(edit_widget)
        display_widget = QWidget()
        display_widget.setLayout(display_layout)
        mod_layout.addWidget(display_widget)
        mod_widget.setLayout(mod_layout)

        view_layout.insertWidget(view_layout.count()-1, mod_widget)
        # save the value for profiles - cant do much
        view_layout.mod_widgets[mod] = mod_widget

    # for thread safe
    class ViewLayoutSmart(QObject):
        signal = Signal(object)

        def __init__(self, view_layout):
            QObject.__init__(self)
            self.signal.connect(build_mod_widget)
        
        def build_mod_widget(self, mod):
            self.signal.emit(mod)
    qtwidgets.view_layout_smart = view_layout_smart = ViewLayoutSmart(view_layout)
    class RunButtonSmart(QObject):
        signal = Signal(str)

        def __init__(self, run_button):
            QObject.__init__(self)
            self.signal.connect(run_button.setText)
        
        def setText(self, text):
            self.signal.emit(text)
    qtwidgets.RunButtonSmart = run_button_smart = RunButtonSmart(run_button)

    qtwidgets.make_overlay = None
    qtwidgets.run_overlay = None
    def run_mods():
        if qtwidgets.is_loading_cslmao:
            print('cslmao: Error: Loading mods, can not run yet.')
            return
        if qtwidgets.make_overlay == None and qtwidgets.run_overlay == None:
            def run_thrd():
                profile = setting.get('Cslmao.profile', 'all')
                qtwidgets.make_overlay = p = cslmao.make_overlay(
                    profile)
                cslmao.block_and_stream_process_output(
                    p, 'CSLMAO: ')
                if p.returncode == 0:
                    qtwidgets.make_overlay = None
                    qtwidgets.run_overlay = p2 = cslmao.run_overlay(
                        profile)
                    cslmao.block_and_stream_process_output(
                        p2, 'CSLMAO: ')
                    if p2.returncode not in (None, 0, 1):
                        run_button_smart.setText('🚀 Run')
                        print('cslmao: Error: Run overlay failed.')
                        qtwidgets.run_overlay = None
                else:
                    run_button_smart.setText('🚀 Run')
                    print('cslmao: Error: Make overlay failed.')
                    qtwidgets.make_overlay = None
            run_button_smart.setText('🚧 Stop')
            Thread(target=run_thrd, daemon=True).start()
        else:
            if qtwidgets.make_overlay != None:
                qtwidgets.make_overlay.kill()
            if qtwidgets.run_overlay != None:
                qtwidgets.run_overlay.kill()
            run_button_smart.setText('🚀 Run')
            print('cslmao: Status: Stopped running overlay, idling.')
            qtwidgets.make_overlay = None
            qtwidgets.run_overlay = None

    run_button.clicked.connect(run_mods)
    # new mod
    def new_mod():
        if is_overlay_running():
            return
        mod_path = 'New Mod'
        mod_info = {
            'Name': 'New Mod',
            'Author': 'Author',
            'Version': '1.0',
            'Description': ''
        }
        mod_profile = setting.get('cslmao.profile', 'all')
        if mod_profile == 'all':
            mod_profile = '0'
        mod = cslmao.create_mod(path=mod_path, enable=False, profile=mod_profile)
        cslmao.create_mod_folder(mod)
        cslmao.set_info(
            mod,
            info=mod_info,
            image_path=None
        )
        cslmao.save_mods()
        view_layout_smart.build_mod_widget(mod)
    new_button.clicked.connect(new_mod)

    # import mod
    def import_mod():
        if is_overlay_running():
            return
        dialog = QFileDialog()
        filepaths = dialog.getOpenFileNames(
            widget, 
            f'Select MOD',
            setting.get('qtGUI.default_folder', None),
            f'MOD Files (*.fantome *.zip)'
        )
        if len(filepaths[0]) > 0:
            def import_thrd():
                final_paths = filepaths[0]
                for final_path in final_paths:
                    mod_path = '.'.join(os.path.basename(final_path).split('.')[:-1])
                    mod_profile = setting.get('cslmao.profile', 'all')
                    if mod_profile == 'all':
                        mod_profile = '0'
                    mod = cslmao.create_mod(
                        path=mod_path, enable=False, profile=mod_profile)
                    p = cslmao.import_fantome(final_path, mod.get_path())
                    if p.returncode == 0:
                        print(f'cslmao: Imported: {final_path}')
                        info, image = cslmao.get_info(mod)
                        view_layout_smart.build_mod_widget(mod)
                    else:
                        cslmao.delete_mod(mod)
                cslmao.save_mods()

            helper.SafeThread.start('cslmao', import_thrd)
    import_button.clicked.connect(import_mod)

    # refresh profile
    def refresh_profile(profile):
        if profile == 'all':
            for mod, mod_widget in view_layout.mod_widgets.items():
                mod_widget.setVisible(True)
        else:
            for mod, mod_widget in view_layout.mod_widgets.items():
                if mod.profile == profile:
                    mod_widget.setVisible(True)
                else:
                    mod_widget.setVisible(False)

    # check overlay running
    def is_overlay_running():
        if qtwidgets.make_overlay != None or qtwidgets.run_overlay != None:
            return True
        return False
    
    # after finish build, load all mods
    def load_after_build():
        qtwidgets.is_loading_cslmao = True
        print(f'cslmao: Status: Loading mods.')
        for mod in cslmao.MOD.mods:
            try:
                info, image = cslmao.get_info(mod)
                view_layout_smart.build_mod_widget(mod)
            except Exception as e:
                cslmao.MOD.mods.remove(mod)
                print(f'cslmao: Error: Load {mod.get_path()}: {e}')
                import traceback
                print(traceback.format_exc())
        refresh_profile(setting.get('cslmao.profile', 'all'))
        print(f'cslmao: Status: Finished loading mods.')
        qtwidgets.is_loading_cslmao = False
    helper.SafeThread.start('cslmao', load_after_build)

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
        joint_names = [f'[{joint_id}] {joint.name}' for joint_id, joint in enumerate(skl_file.joints)]
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
💡 Target type (if needed) must match source type.
    📝 BIN: run functions directly on selected bin.
    📁 Folder: run functions on all bins inside Wads or Subfolders of selected Folder.
Hover mouse on button to see functions description.
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
    for browse_type in ['BIN', 'Folder']:
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
    for browse_type in ['BIN', 'Folder']:
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
    layout2 = QGridLayout()
    row_index = 0
    col_index = 0
    for name, description, hp_command, require_dst in hapiBin.Helper.qt_datas: 
        button = QToolButton()
        button.setText(name)
        button.clicked.connect(lambda event, src_line=src_line, dst_line=dst_line, hp_command=hp_command, require_dst=require_dst: run_hp_command(src_line, dst_line, hp_command, require_dst))
        button.setToolTip(description)
        layout2.addWidget(button, row_index, col_index)
        col_index += 1
        if col_index > 1:
            col_index = 0
            row_index += 1
    layout2.setRowStretch(layout2.rowCount(), 1)
    layout2.setColumnStretch(layout2.columnCount(), 1)
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
    champs_line = QLineEdit()
    layout3.addWidget(champs_line, stretch=1)
    game_folder = setting.get('game_folder', '')
    if game_folder != '':
        champs_line.setText(game_folder+'/DATA/FINAL/Champions')
    browse_button = QToolButton()
    browse_button.setText('📁 Select Champions folder')
    def select_champions_folder():
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget,
            f'Select Champions Folder',
            setting.get('qtGUI.default_folder', None),
        )
        if dirpath != '':
            final_path = dirpath
            champs_line.setText(final_path)
    browse_button.clicked.connect(select_champions_folder)
    layout3.addWidget(browse_button)
    layout2.addLayout(layout3)
    
    layout3 = QHBoxLayout()
    save_button = QToolButton()
    save_button.setText('💾 Save SKIPS.json')
    layout3.addWidget(save_button)

    label = QLabel('🦺 Thread: ')
    layout3.addWidget(label)
    thread_box = QComboBox()
    thread_box.setMinimumWidth(50)
    thread_box.addItems(['1', '2', '4', '6', '8', '16'])
    thread_box.setCurrentText(setting.get('no_skin.pool_size', '4'))
    def change_thread_num():
        setting.set('no_skin.pool_size', thread_box.currentText())
        setting.save()
    thread_box.currentTextChanged.connect(change_thread_num)
    layout3.addWidget(thread_box)

    layout3.addStretch()
    full_button = QToolButton()
    full_button.setText('🐧 Make NO SKIN.fantome')
    def no_skin_full():
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget,
            f'Select Output Fantome Folder',
            setting.get('qtGUI.default_folder', None),
        )
        if dirpath != '':
            def no_skin_thrd():
                final_path = dirpath
                no_skin.parse(champs_line.text(), final_path, pool_size=int(setting.get('no_skin.pool_size', '4')))
    
            helper.SafeThread.start('no_skin', no_skin_thrd)
    full_button.clicked.connect(no_skin_full)
    layout3.addWidget(full_button)
    layout2.addLayout(layout3)

    # skips
    skips_text = QPlainTextEdit()
    skips_text.setPlainText(no_skin.get_skips())
    layout2.addWidget(skips_text, stretch=1)
    def save_skips():
        no_skin.set_skips(skips_text.toPlainText())
        no_skin.save_skips()
    save_button.clicked.connect(save_skips)


    tab1.setLayout(layout2)
    tab_widget.addTab(tab1, '🔴 Full')
    # no skin lite
    tab2 = QWidget()
    layout2 = QVBoxLayout()

    layout3 = QHBoxLayout()
    skin0_line = QLineEdit()
    skin0_line.setReadOnly(True)
    layout3.addWidget(skin0_line, stretch=99)
    skin0_button = QToolButton()
    skin0_button.setMinimumWidth(220)
    skin0_button.setText('📝 Select Skin0 BIN')
    def select_skin0():
        dialog = QFileDialog()
        filepaths = dialog.getOpenFileName(
            widget, 
            f'Select Skin0 BIN',
            setting.get('qtGUI.default_folder', None),
            f'BIN Files (*.bin)'
        )
        if len(filepaths[0]) > 0:
            final_path = filepaths[0]
            skin0_line.setText(final_path)
    skin0_button.clicked.connect(select_skin0)
    layout3.addWidget(skin0_button)
    layout2.addLayout(layout3)

    layout3 = QHBoxLayout()
    skinx_text = QPlainTextEdit()
    skinx_text.setReadOnly(True)
    layout3.addWidget(skinx_text, stretch=99)
    skinx_button = QToolButton()
    skinx_button.setMinimumWidth(220)
    skinx_button.setText('📝 Select SkinX BINs')
    def select_skinx():
        dialog = QFileDialog()
        filepaths = dialog.getOpenFileNames(
            widget, 
            f'Select SkinX BINs',
            setting.get('qtGUI.default_folder', None),
            f'BIN Files (*.bin)'
        )
        if len(filepaths[0]) > 0:
            final_paths = filepaths[0]
        skinx_text.setPlainText('\n'.join(final_paths))
    skinx_button.clicked.connect(select_skinx)
    layout3.addWidget(skinx_button, alignment=Qt.AlignmentFlag.AlignTop)
    layout2.addLayout(layout3, stretch=999)

    mini_button = QToolButton()
    mini_button.setText('🦭 Make all Skinx BIN same as Skin0 BIN')
    def no_skin_lite(label, text):
        def no_skin_thrd():
            no_skin.mini_no_skin(
                skin0_file=skin0_line.text(), 
                otherskins_files=skinx_text.toPlainText().split('\n')
            )
        
        helper.SafeThread.start('no_skin', no_skin_thrd)
    mini_button.clicked.connect(lambda event: no_skin_lite(skin0_line, skinx_text))
    layout2.addWidget(mini_button)
    
    #layout2.addStretch()
    tab2.setLayout(layout2)
    tab_widget.addTab(tab2, '⭕ Lite')

    
    layout.addWidget(tab_widget, stretch=1)
    widget.setLayout(layout)

def build_wad_tool(widget: QWidget):
    layout = QVBoxLayout()

    qtwidgets.text_wad_paths = []
    qtwidgets.text_chunk_hashes = []
    # pack, unpack wad
    layout2 = QHBoxLayout()
    button = QToolButton()
    button.setText('📦 WAD to Folder')
    def wad_to_dir():
        dialog = QFileDialog()
        filepath = dialog.getOpenFileName(
            widget, 
            'Select WAD',
            setting.get('qtGUI.default_folder', None),
            f'WAD Files (*.wad.client)'
        )
        if len(filepath[0]) > 0:
            def wad_thrd(): 
                hash_helper.read_wad_hashes()
                src = filepath[0]
                dst = src.replace('.wad.client', '.wad')
                wad_tool.unpack(src, dst, hash_helper.HASHTABLES)
                print(f'wad_tool: Finish: Unpack {src}')
                hash_helper.free_wad_hashes()
            helper.SafeThread.start('wad_tool', wad_thrd)
    button.clicked.connect(wad_to_dir)
    layout2.addWidget(button)
    button = QToolButton()
    button.setText('📁 Folder to WAD')
    def dir_to_wad():
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget, 
            'Select Folder',
            setting.get('qtGUI.default_folder', None)
        )
        if dirpath != '':
            def wad_thrd(): 
                src = dirpath
                dst = src
                if dst.endswith('.wad'):
                    dst += '.client'
                else:
                    if not dst.endswith('.wad.client'):
                        dst += '.wad.client'
                wad_tool.pack(src, dst)
                print(f'wad_tool: Finish: Pack {src}')
            helper.SafeThread.start('wad_tool', wad_thrd)
    button.clicked.connect(dir_to_wad)
    layout2.addWidget(button)
    layout2.addStretch()
    layout.addLayout(layout2)

    # bulk unpack
    layout.addSpacing(30)
    layout2 = QHBoxLayout()
    add_button = QToolButton()
    add_button.setText('💰 Add WADs')
    layout2.addWidget(add_button)
    scan_button = QToolButton()
    scan_button.setText('🔎 Scan WADs in Folder')
    layout2.addWidget(scan_button)
    clear_button = QToolButton()
    clear_button.setText('❌ Clear')
    layout2.addWidget(clear_button)
    filter_line = QLineEdit()
    filter_line.setPlaceholderText('Include keywords, press Enter to filter')
    layout2.addWidget(filter_line, stretch=1)
    layout.addLayout(layout2)
    # text view
    layout2 = QHBoxLayout()
    wad_text = QPlainTextEdit()
    wad_text.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
    wad_text.setReadOnly(True)
    layout2.addWidget(wad_text, stretch=3)
    chunk_text = QPlainTextEdit()
    chunk_text.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
    chunk_text.setReadOnly(True)
    layout2.addWidget(chunk_text, stretch=7)
    layout.addLayout(layout2, stretch=1)

    unpack_button = QToolButton()
    unpack_button.setText('🔪 Bulk Unpack')
    unpack_button.setMinimumWidth(300)
    layout.addWidget(unpack_button, alignment=Qt.AlignmentFlag.AlignHCenter)

    class WadChunkText(QObject):
        wad_text_singal = Signal(str)
        chunk_text_signal = Signal(str)

        def __init__(self, wad_text, chunk_text):
            QObject.__init__(self)
            self.wad_text_singal.connect(wad_text.setPlainText)
            self.chunk_text_signal.connect(chunk_text.setPlainText)
        
        def setPlainText(self, wad_text_content, chunk_text_content):
            if wad_text_content != None:
                self.wad_text_singal.emit(wad_text_content)
            if chunk_text_content != None:
                self.chunk_text_signal.emit(chunk_text_content)
    
    wadchunk_text = WadChunkText(wad_text, chunk_text)
    # add wads
    def add_wads(isfile):
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
                        if file.endswith('.wad.client'):
                            final_paths.append(os.path.join(root, file).replace('\\', '/'))
        if len(final_paths) > 0:
            def wad_thrd():
                hash_helper.read_wad_hashes()
                for wad_path in final_paths:
                    try:
                        if wad_path not in qtwidgets.text_wad_paths:
                            wad = pyRitoFile.read_wad(wad_path)
                            wad.un_hash(hash_helper.HASHTABLES)
                            qtwidgets.text_wad_paths.append(wad_path)
                            qtwidgets.text_chunk_hashes.extend(chunk.hash for chunk in wad.chunks)
                    except:
                        pass
                hash_helper.free_wad_hashes()
                
                print('wad_tool: Finish: Load WADs.')
                wadchunk_text.setPlainText('\n'.join(qtwidgets.text_wad_paths), '\n'.join(qtwidgets.text_chunk_hashes))

            helper.SafeThread.start('wad_tool', wad_thrd)
    add_button.clicked.connect(lambda event: add_wads(True))
    scan_button.clicked.connect(lambda event: add_wads(False))
    # clear wads
    def clear_wads():
        qtwidgets.text_wad_paths = []
        qtwidgets.text_chunk_hashes = []
        wad_text.clear()
        chunk_text.clear()
        print('wad_tool: Finish: Clear WADs.')
    clear_button.clicked.connect(clear_wads)
    # filter    
    def filter_chunk(keywords):
        new_text_chunk_hashesh = []
        keywords = keywords.split(' ')
        for chunk_hash in qtwidgets.text_chunk_hashes:
            for word in keywords:
                if word in chunk_hash:
                    new_text_chunk_hashesh.append(chunk_hash)
                    break
        chunk_text.setPlainText('\n'.join(new_text_chunk_hashesh))
        chunk_doc = chunk_text.document()
        brush = QBrush(QColor(*qtwidgets.accent_color))
        ess = []        
        for word in keywords:
            text_cursor = chunk_doc.find(word, 0)
            if text_cursor.isNull():
                continue
            
            es = QTextEdit.ExtraSelection()
            es.cursor = text_cursor
            es.format.setForeground(brush)
            ess.append(es)
            while not text_cursor.isNull():
                text_cursor = chunk_doc.find(word, text_cursor.selectionEnd())
                es = QTextEdit.ExtraSelection()
                es.cursor = text_cursor
                es.format.setForeground(brush)
                ess.append(es)
        chunk_text.setExtraSelections(ess)
    filter_line.returnPressed.connect(lambda: filter_chunk(filter_line.text()))
    # bulk unpack
    def bulk_unpack():
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget,
            f'Select Output Folder',
            setting.get('qtGUI.default_folder', None),
        )
        if dirpath != '':
            wad_paths = wad_text.toPlainText().split('\n')
            chunk_hashes = chunk_text.toPlainText().split('\n')
            if len(chunk_hashes) == 0:
                chunk_hashes = None
            if len(wad_paths) > 0:
                def bulk_unpack_thrd():
                    hash_helper.read_wad_hashes()
                    for wad_path in wad_paths:
                        wad_tool.unpack(wad_path, dirpath, hash_helper.HASHTABLES, filter=chunk_hashes)
                    hash_helper.free_wad_hashes()
                    print(f'wad_tool: Finish: Unpack to {dirpath}')
                helper.SafeThread.start('wad_tool', bulk_unpack_thrd)
    unpack_button.clicked.connect(bulk_unpack)

    widget.setLayout(layout)

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

    def browse_dir(line, title):
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget, 
            title,
            setting.get('qtGUI.default_folder', None)
        )
        if dirpath != '':
            final_path = dirpath
            line.setText(final_path)
    # browse skin to fbx
    layout2.addWidget(QLabel('👽 SKIN to FBX'))
    layout3 = QGridLayout()
    skn_line = QLineEdit()
    layout3.addWidget(skn_line, 0, 0)
    button = QToolButton()
    button.setText('🧊 Select SKN')    
    button.setMinimumWidth(260)
    button.clicked.connect(lambda event, line=skn_line: browse(line, 'Select SKN', 'SKN'))
    layout3.addWidget(button, 0, 1)
    skl_line = QLineEdit()
    layout3.addWidget(skl_line, 1, 0)
    button = QToolButton()
    button.setText('🦴 Select SKL')    
    button.setMinimumWidth(260)
    button.clicked.connect(lambda event, line=skl_line: browse(line, 'Select SKL', 'SKL'))
    layout3.addWidget(button, 1, 1)
    anm_line = QLineEdit()
    layout3.addWidget(anm_line, 2, 0)
    button = QToolButton()
    button.setText('🦴 Select ANMs Folder')    
    button.setMinimumWidth(260)
    button.clicked.connect(lambda event, line=anm_line: browse_dir(line, 'Select ANMs Folder'))
    layout3.addWidget(button, 2, 1)
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
    def to_fbx():
        def lemon_thrd():
            lemon_fbx.skin_to_fbx(
                skl_line.text(), 
                skn_line.text(), 
                anm_line.text(),
                output_fbx.text()
            )
        helper.SafeThread.start('lemon_fbx', lemon_thrd)
    button.clicked.connect(to_fbx)

    layout2.addSpacing(30)

    # browse fbx to skin
    layout2.addWidget(QLabel('👻 FBX to SKIN'))
    layout3 = QGridLayout()
    fbx_line = QLineEdit()
    layout3.addWidget(fbx_line, 0, 0)
    button = QToolButton()
    button.setText('🌄 Select FBX')    
    button.setMinimumWidth(260)
    button.clicked.connect(lambda event, line=fbx_line: browse(line, 'Select FBX', 'FBX'))
    layout3.addWidget(button, 0, 1)
    layout2.addLayout(layout3)
    # to skin
    layout3 = QHBoxLayout()
    button = QToolButton()
    button.setText('🚗 To SKN + SKL + ANMs')
    layout3.addWidget(button)
    output_skn = QLabel()
    fbx_line.textChanged.connect(lambda event: output_skn.setText(event.replace('.fbx', '.skn')))
    layout3.addWidget(output_skn)
    layout2.addLayout(layout3)
    def to_skin():
        def lemon_thrd():
            lemon_fbx.fbx_to_skin(
                fbx_line.text(), 
                output_skn.text().replace('.skn', '.skl'), 
                output_skn.text(),
                os.path.join(os.path.dirname(output_skn.text()), 'animations')
            )
        helper.SafeThread.start('lemon_fbx', lemon_thrd)
    button.clicked.connect(to_skin)

    layout2.addStretch()
    tab1.setLayout(layout2)
    tab_widget.addTab(tab1, '💦 fbx')


    # maya
    tab2 = QWidget()
    layout2 = QVBoxLayout()
    layout2.addWidget(QLabel("""
Maya recommend version: 2022+. 
Steps to install lemon3d maya:
    1. Please close maya before installing lemon3d.
    2. Click Install button below, select Documents/maya/<version> folder to install lemon3d.
    3. Open maya, on toolbar select Windows -> Settings/Preferences -> Plug-in Manager. 
    4. Tick Loaded/Auto Load on lemon3d.py inside Plug-in Manager panel.
Note: lemon3d is part of LtMAO so do not delete/move LtMAO, 
      otherwise lemon3d need to reinstalled through below button again.                
"""))
    button = QToolButton()
    button.setText('🔌Install lemon3d for maya')
    def install_lemon3d_maya():
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget,
            f'Select Documents/maya/<version> Folder',
            setting.get('qtGUI.default_folder', None),
        )
        if dirpath != '':
            lemon_maya.install_plugin(dirpath.replace('\\', '/'))
    button.clicked.connect(install_lemon3d_maya)
    layout2.addWidget(button)
    layout2.addStretch()
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
    layout = QVBoxLayout()

    # browse layout
    layout2 = QGridLayout()
    # audio
    audio_line = QLineEdit()
    audio_line.setPlaceholderText('Require')
    layout2.addWidget(audio_line, 0, 0)
    button = QToolButton()
    button.setText('🔈 Select Audio BNK/WPK')    
    button.setMinimumWidth(260)
    def browse_audio(line):
        dialog = QFileDialog()
        filepath = dialog.getOpenFileName(
            widget, 
            'Select Audio BNK/WPK',
            setting.get('qtGUI.default_folder', None),
            f'BNK/WPK Files (*.bnk *.wpk)'
        )
        if len(filepath[0]) > 0:
            final_path = filepath[0]
            line.setText(final_path)
    button.clicked.connect(lambda event, line=audio_line: browse_audio(line))
    layout2.addWidget(button, 0, 1)
    # event
    event_line = QLineEdit()
    event_line.setPlaceholderText('Require')
    layout2.addWidget(event_line, 1, 0)
    button = QToolButton()
    button.setText('📋 Select Event BNK')    
    button.setMinimumWidth(260)
    def browse_event(line):
        dialog = QFileDialog()
        filepath = dialog.getOpenFileName(
            widget, 
            'Select Event BNK',
            setting.get('qtGUI.default_folder', None),
            f'BNK Files (*.bnk)'
        )
        if len(filepath[0]) > 0:
            final_path = filepath[0]
            line.setText(final_path)
    button.clicked.connect(lambda event, line=event_line: browse_event(line))
    layout2.addWidget(button, 1, 1)
    # bin
    bin_line = QLineEdit()
    layout2.addWidget(bin_line, 2, 0)
    button = QToolButton()
    button.setText('📝 Select BIN')    
    button.setMinimumWidth(260)
    def browse_bin(line):
        dialog = QFileDialog()
        filepath = dialog.getOpenFileName(
            widget, 
            'Select BIN',
            setting.get('qtGUI.default_folder', None),
            f'BIN Files (*.bin)'
        )
        if len(filepath[0]) > 0:
            final_path = filepath[0]
            line.setText(final_path)
    button.clicked.connect(lambda event, line=bin_line: browse_bin(line))
    layout2.addWidget(button, 2, 1)
    layout.addLayout(layout2)
    
    layout2 = QHBoxLayout()
    # treeview
    qtwidgets.inspector = None
    treeview = QTreeView()
    treeview.setHeaderHidden(True)
    model = QStandardItemModel()
    treeview.setModel(model)
    treeview.setSelectionMode(treeview.SelectionMode.ExtendedSelection)
    layout2.addWidget(treeview, stretch=1)
    # actions
    layout3 = QVBoxLayout()
    
    button = QToolButton()
    button.setText('📻 Load')
    button.setMinimumWidth(230)
    def load_bnk():
        # clear cache
        model.clear()
        bnk_tool.Inspector.reset_cache()
        # inspect
        qtwidgets.inspector = inspector = bnk_tool.Inspector(
            audio_path=audio_line.text(),
            events_path=event_line.text(),
            bin_path=bin_line.text()
        )
        inspector.unpack(inspector.get_cache_dir())
        
        # set root and expand
        root_item = QStandardItem('🔈 ' + audio_line.text())
        root_item.setEditable(False)
        model.appendRow(root_item)
        treeview.setExpanded(model.indexFromItem(root_item), True)

        # build treeview with audio_tree
        for event_id in inspector.audio_tree:
            event_item = QStandardItem('📢 ' + str(event_id))
            event_item.setEditable(False)
            root_item.appendRow(event_item)
            for container_id in inspector.audio_tree[event_id]:
                container_item = QStandardItem('📣 ' + str(container_id))
                container_item.setEditable(False)
                event_item.appendRow(container_item)
                for audio_id in inspector.audio_tree[event_id][container_id]:
                    audio_item = QStandardItem('🎵 ' + str(audio_id))
                    audio_item.setEditable(False)
                    container_item.appendRow(audio_item)
    button.clicked.connect(load_bnk)
    layout3.addWidget(button)

    button = QToolButton()
    button.setText('💾 Save as')
    button.setMinimumWidth(230)
    def save_as():
        if qtwidgets.inspector == None:
            return
        dialog = QFileDialog()
        final_path = ''
        if qtwidgets.inspector.is_bnk:
            filepath = dialog.getSaveFileName(
                widget, 
                'Save Audio BNK as',
                setting.get('qtGUI.default_folder', None),
                f'BNK (*.bnk)'
            )
            if len(filepath[0]) > 0:
                final_path = filepath[0]
        else:
            filepath = dialog.getSaveFileName(
                widget, 
                'Save Audio WPK as',
                setting.get('qtGUI.default_folder', None),
                f'WPK (*.wpk)'
            )
            if len(filepath[0]) > 0:
                final_path = filepath[0]
        if final_path != '':
            def save_thrd():
                qtwidgets.inspector.pack(final_path)
                print(f'bnk_tool: Finish: Save Audio: {final_path}')

            helper.SafeThread.start('bnk_tool', save_thrd)
    button.clicked.connect(save_as)
    layout3.addWidget(button)

    button = QToolButton()
    button.setText('❌ Clear')
    button.setMinimumWidth(230)
    def clear_bnk():
        model.clear()
        bnk_tool.Inspector.reset_cache()
        qtwidgets.inspector = None
    button.clicked.connect(clear_bnk)
    layout3.addWidget(button)

    button = QToolButton()
    button.setText('📤 Extract all sound')
    button.setMinimumWidth(230)
    def extract_bnk():
        if qtwidgets.inspector == None:
            return
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget,
            f'Select Output Fantome Folder',
            setting.get('qtGUI.default_folder', None),
        )
        if dirpath != '':
            def extract_thrd():
                qtwidgets.inspector.extract(dirpath)
                print(f'bnk_tool: Finish: Extract all sounds: {dirpath}')
            
            helper.SafeThread.start('bnk_tool', extract_thrd)
    button.clicked.connect(extract_bnk)
    layout3.addWidget(button)

    button = QToolButton()
    button.setText('🎶 Replace sound')
    button.setMinimumWidth(230)
    def replace_sound():
        if qtwidgets.inspector == None:
            return
        unique_select_wem_ids = []
        select_model = treeview.selectionModel()
        if select_model != None:
            select_index = select_model.selectedIndexes()
            if len(select_index) > 0:
                for index in select_index:
                    text = index.data()
                    if text.startswith('🎵'):
                        wem_id = text[2:]
                        if wem_id not in unique_select_wem_ids:
                            unique_select_wem_ids.append(wem_id)
        if len(unique_select_wem_ids) > 0:
            dialog = QFileDialog()
            final_paths = []
            filepath = dialog.getOpenFileNames(
                widget, 
                'Select BIN',
                setting.get('qtGUI.default_folder', None),
                f'BIN Files (*.bin)'
            )
            if len(filepath[0]) > 0:
                final_paths = filepath[0]
                def replace_thrd():
                    wem_path_id = 0
                    wem_path_count = len(final_paths)
                    for wem_id in unique_select_wem_ids:
                        wem_id = int(wem_id)
                        qtwidgets.inspector.replace_wem(wem_id, final_paths[wem_path_id])
                        wem_path_id += 1
                        if wem_path_id == wem_path_count:
                            wem_path_id = 0
                    print(f'Done: bnk_tool: Replace wems: Successfully replace {len(unique_select_wem_ids)} selected wems with {wem_path_count} WEM files.')
                helper.SafeThread.start('bnk_tool', replace_thrd)
    button.clicked.connect(replace_sound)
    layout3.addWidget(button)

    button = QToolButton()
    button.setText('▶️ Play selected')
    button.setMinimumWidth(230)
    def play_selected():
        if qtwidgets.inspector == None:
            return
        select_model = treeview.selectionModel()
        if select_model != None:
            select_index = select_model.selectedIndexes()
            if len(select_index) > 0:
                text = select_index[-1].data()
                if text.startswith('🎵'):
                    wem_id = text[2:]
                    qtwidgets.inspector.play(wem_id)
        treeview.selectionModel().selectedIndexes()[-1].data
    button.clicked.connect(play_selected)
    layout3.addWidget(button)

    button = QToolButton()
    button.setText('⏹️ Stop playing')
    button.setMinimumWidth(230)
    def stop_playing():
        if qtwidgets.inspector == None:
            return
        qtwidgets.inspector.stop()
    button.clicked.connect(stop_playing)
    layout3.addWidget(button)

    checkbox = QCheckBox()
    checkbox.setChecked(setting.get('bnk_tool.auto_play', True))
    checkbox.setText('🔁 Auto play')
    checkbox.setMinimumWidth(230)
    def autoplay_checkbox():
        setting.set('bnk_tool.auto_play', checkbox.isChecked())
        setting.save()
    checkbox.clicked.connect(autoplay_checkbox)
    layout3.addWidget(checkbox)
    def autoplay_cmd(selected, deselected):
        if qtwidgets.inspector == None:
            return
        if selected != None and setting.get('bnk_tool.auto_play', True) :
            select_range = selected.data()
            if select_range != None:
                select_index = select_range.indexes()
                if len(select_index) > 0:
                    text = select_index[-1].data()
                    if text.startswith('🎵'): 
                        wem_id = text[2:]
                        qtwidgets.inspector.play(wem_id)
    treeview.selectionModel().selectionChanged.connect(autoplay_cmd)
    
    layout3.addStretch()
    layout2.addLayout(layout3)
    
    layout.addLayout(layout2, stretch=1)
    widget.setLayout(layout)

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
    box.addItems([f.name for f in os.scandir('./res/themes') if f.is_dir()])
    box.setCurrentText(setting.get('qtGUI.theme_name', 'raora'))
    def change_theme(box):
        setting.set('qtGUI.theme_name', box.currentText())
        setting.save()
        print('setting: Restart is require for theme changes to take effect.')
    box.currentTextChanged.connect(lambda event: change_theme(box))
    layout2.addWidget(box)

    checkbox = QCheckBox()
    checkbox.setText('🎞️ Animated background')
    checkbox.setChecked(setting.get('qtGUI.animated_background', True))
    def animated_background_cmd():
        setting.set('qtGUI.animated_background', checkbox.isChecked())
        setting.save()
        print('setting: Restart is require for theme changes to take effect.')
    checkbox.clicked.connect(animated_background_cmd)
    layout2.addWidget(checkbox)

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
        print(f'Running: Restart LtMAO')
        os.system(os.path.join(os.path.abspath(os.path.curdir),'start.bat'))
        qtwidgets.app.quit()
        
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


