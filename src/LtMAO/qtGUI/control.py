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
    QSlider, 
    QTreeWidget,
    QTreeWidgetItem,
    QMessageBox,
)
from PySide6.QtGui import QColor, QStandardItem, QStandardItemModel, QPixmap, QMovie, QShortcut, QKeySequence
from PySide6.QtCore import Qt, QObject, Signal


import os, os.path, time
from threading import Thread

from . import helper
from .. import (
    setting, 
    winLT, 
    hash_helper, 
    pyRitoFile, 
    hapiBin, 
    no_skin, 
    sborf, 
    mask_viewer, 
    wad_tool,
    bnk_tool,
    cslmao,
    texsmart,
    wiwawe,
    lepath,
    bumpath,
    infinityQT
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
                c.widget.setStyleSheet(f'background-color: {qtwidgets.accent_color};')
            else:
                c.widget.setChecked(True)
        else:
            c.content.setVisible(False)
            if c.page_id == 100:
                c.widget.setStyleSheet(f'QStatusBar {{ background-color: rgba(0, 0, 0, 127) }} QStatusBar:hover {{ background-color: {qtwidgets.accent_color}; }}')
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
    Control('🍑\nbumpath', 5, lambda widget: build_bumpath(widget)),
    Control('📦\nwad_tool', 6, lambda widget: build_wad_tool(widget)),
    Control('🛠️\nsborf', 7, lambda widget: build_sborf(widget)),
    Control('🍋\nlemon3d', 8, lambda widget: build_lemon3d(widget)),
    Control('🛣️\ntexsmart', 9, lambda widget: build_texsmart(widget)),
    Control('🔊\nbnk_tool', 10, lambda widget: build_bnk_tool(widget)),
    Control('📼\nwiwawe', 11, lambda widget: build_wiwawe(widget)),
    Control('♾️\ninfinityQT', 12, lambda widget: build_infinityQT(widget)),
    Control('🪟\nwinLT', 13, lambda widget: build_winLT(widget)),
]

def build_cslmao(widget: QWidget):
    layout = QVBoxLayout()
    # setting bar
    setting_layout = QVBoxLayout()
    setting_layout.setContentsMargins(0, 0, 0, 0)

    hide_layout = QHBoxLayout()
    hide_layout.setContentsMargins(0, 0, 0, 0)
    hide_layout.addStretch()
    show_setting_button = QToolButton()
    show_setting_button.setText('⚙️ Show settings')
    hide_layout.addWidget(show_setting_button)


    show_layout = QVBoxLayout()
    show_layout.setContentsMargins(0, 0, 0, 0)
    layout2 = QHBoxLayout()
    layout2.addStretch()
    hide_setting_button = QToolButton()
    hide_setting_button.setText('❌ Hide settings')
    layout2.addWidget(hide_setting_button)
    show_layout.addLayout(layout2)
    # game folder and diagnose
    layout2 = QHBoxLayout()
    button = QToolButton()
    button.setText('🎮 Select Game Folder')
    layout2.addWidget(button)
    label = QLabel()
    label.setText(setting.get('game_folder', 'Please select League of Legends/Game folder.'))
    layout2.addWidget(label, stretch=1)
    def select_game_folder(label):
        if is_overlay_running():
            print('clsmao: Stop running mods to proceed.')
            return
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget,
            'Select League of Legends/Game folder',
            setting.get('qtGUI.default_folder', '')
        )
        if dirpath != '':
            final_path = dirpath.replace('\\', '/')
            if not os.path.exists(lepath.join(final_path, 'League of Legends.exe')):
                raise Exception(f'cslmao: Error:  Select game folder: No "League of Legends.exe" found in {final_path}')
            setting.set('game_folder', final_path)
            setting.save()
            label.setText(final_path)
    button.clicked.connect(lambda event: select_game_folder(label))
    button = QToolButton()
    button.setText('🩺 Diagnose problem') 
    button.clicked.connect(cslmao.diagnose)
    layout2.addWidget(button)
    show_layout.addLayout(layout2)
    # tft
    layout2 = QHBoxLayout()
    tft_checkbox = QCheckBox()
    tft_checkbox.setText('🕹️ Enable TFT and other modes')
    tft_checkbox.setChecked(setting.get('cslmao.tft', False))
    def tft_cmd():
        setting.set('cslmao.tft', tft_checkbox.isChecked())
        setting.save()
    tft_checkbox.clicked.connect(tft_cmd)
    layout2.addWidget(tft_checkbox)
    layout2.addStretch()
    show_layout.addLayout(layout2)
    # auto py to bin
    layout2 = QHBoxLayout()
    py2bin_checkbox = QCheckBox()
    py2bin_checkbox.setText('📝 Auto convert all PY to BIN before run')
    py2bin_checkbox.setChecked(setting.get('cslmao.auto_py2bin', False))
    def py2bin_cmd():
        setting.set('cslmao.auto_py2bin', py2bin_checkbox.isChecked())
        setting.save()
    py2bin_checkbox.clicked.connect(py2bin_cmd)
    layout2.addWidget(py2bin_checkbox)
    layout2.addStretch()
    show_layout.addLayout(layout2)
    # auto dds to tex
    layout2 = QHBoxLayout()
    dds2tex_checkbox = QCheckBox()
    dds2tex_checkbox.setText('🌌 Auto convert all DDS to TEX before run')
    dds2tex_checkbox.setChecked(setting.get('cslmao.auto_dds2tex', False))
    def dds2tex_cmd():
        setting.set('cslmao.auto_dds2tex', dds2tex_checkbox.isChecked())
        setting.save()
    dds2tex_checkbox.clicked.connect(dds2tex_cmd)
    layout2.addWidget(dds2tex_checkbox)
    layout2.addStretch()
    show_layout.addLayout(layout2)

    hide_widget = QWidget()
    hide_widget.setStyleSheet(qtwidgets.tab_stylesheet)
    qtwidgets.tab_widgets.append(hide_widget)
    hide_widget.setLayout(hide_layout)
    setting_layout.addWidget(hide_widget)
    def show_setting_cmd():
        hide_widget.setVisible(False)
        show_widget.setVisible(True)
    show_setting_button.clicked.connect(show_setting_cmd)

    show_widget = QWidget()
    show_widget.setStyleSheet(qtwidgets.tab_stylesheet)
    qtwidgets.tab_widgets.append(show_widget)
    show_widget.setLayout(show_layout)
    show_widget.setVisible(False)
    setting_layout.addWidget(show_widget)
    def hide_setting_cmd():
        hide_widget.setVisible(True)
        show_widget.setVisible(False)
    hide_setting_button.clicked.connect(hide_setting_cmd)

    layout.addLayout(setting_layout)
    
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
    all_button = QToolButton()
    qtwidgets.all_mod_enable = True
    all_button.setText('🖲️ On/Off All')
    all_button.setMinimumWidth(130)
    layout2.addWidget(all_button)
    search_line = QLineEdit()
    search_line.setPlaceholderText('🔎 Filter')
    # rebuild layout if search changed
    def search_text():
        view_layout_smart.build_view_layout()
    search_line.textChanged.connect(search_text)
    layout2.addWidget(search_line, stretch=1)
    layout2.addWidget(QLabel('📚 Profile: '))
    box = QComboBox()
    box.setMinimumWidth(100)
    box.addItems(['all', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    box.setCurrentText(setting.get('cslmao.profile', 'all'))
    # rebuild layout if profile changed
    def change_profile():
        profile = box.currentText()
        setting.set('cslmao.profile', profile)
        setting.save()
        view_layout_smart.build_view_layout()
    box.currentTextChanged.connect(change_profile)
    layout2.addWidget(box)
    layout.addLayout(layout2)
    # empty image
    image_empty = QPixmap(256, 144)
    image_empty.fill(QColor(33, 33, 33))
    # view layout
    scrollarea = QScrollArea()
    scrollarea.setWidgetResizable(True)
    view_widget = QWidget()
    view_layout = QGridLayout(scrollarea)
    view_layout.setContentsMargins(0, 0, 0, 0)
    view_widget.setLayout(view_layout)
    scrollarea.setWidget(view_widget)
    layout.addWidget(scrollarea, stretch=1)
    layout.addStretch()
    widget.setLayout(layout)
    # build view layout func
    view_layout.mod_widgets = {}
    def build_view_layout():
        mods = cslmao.MOD.mods
        max_column = qtwidgets.max_column
        search = search_line.text().lower()
        profile = setting.get('cslmao.profile', 'all')
        qtwidgets.view_mods = view_mods = [False] * len(mods)
        # get view mods with search and profile
        for mod_index, mod in enumerate(mods):
            cslmao.get_info(mod)
            mod_text = f'{mod.info["Name"]} {mod.info["Version"]} {mod.info["Author"]} {mod.info["Description"]}'.lower()
            if search in mod_text and (mod.profile == profile or profile == 'all'):
                view_mods[mod_index] = True   
        view_index =   0
        for mod_index in range(len(mods)):
            mod = mods[mod_index]
            if not view_mods[mod_index]:
                if mod in view_layout.mod_widgets:
                    mod_widget = view_layout.mod_widgets[mod]
                    mod_widget.setParent(None)
                continue
            # build new mod_widget or get from cache
            if mod not in view_layout.mod_widgets:
                cslmao.get_info(mod)
                # mod widget + layout
                mod_widget = QWidget()
                mod_layout = QHBoxLayout()
                mod_layout.setContentsMargins(3, 3, 3, 3)
                # display
                display_layout = QVBoxLayout()
                display_layout.setContentsMargins(0, 0, 0, 0)
                display_layout.setSpacing(0)
                mod_layout.addLayout(display_layout)
                # mod image
                mod_widget.mod_image = mod_image = QLabel()
                mod_image.setPixmap(
                    QPixmap(mod.image).scaled(256, 144, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    if mod.image != None else image_empty
                )
                display_layout.addWidget(mod_image, alignment=Qt.AlignmentFlag.AlignCenter, stretch=1)
                # mod info
                mod_widget.mod_info = mod_info = QLabel()
                #mod_info.setText(f'📚{mod.profile} 🆔{mod.info["Name"]}\n🏷️{mod.info["Version"]} 👤{mod.info["Author"]}\n{mod.info["Description"]}')
                mod_info.setText(mod.info['Name'])
                mod_info.setFixedWidth(256)
                display_layout.addWidget(mod_info, alignment=Qt.AlignmentFlag.AlignHCenter, stretch=0) 
                # display enable state + mouse press event
                def update_enable_state(mod_widget, enable):
                    if enable:
                        mod_widget.setObjectName('CslmaoModWidgetEnable')
                        mod_widget.setStyleSheet(qtwidgets.mod_enable_stylesheet)
                        mod_widget.mod_info.setObjectName('CslmaoModWidgetEnable')
                        mod_widget.mod_info.setStyleSheet(qtwidgets.mod_enable_stylesheet)
                    else:
                        mod_widget.setObjectName('CslmaoModWidgetDisable')
                        mod_widget.setStyleSheet(qtwidgets.mod_disable_stylesheet)
                        mod_widget.mod_info.setObjectName('CslmaoModWidgetDisable')
                        mod_widget.mod_info.setStyleSheet(qtwidgets.mod_disable_stylesheet)
                update_enable_state(mod_widget, mod.enable)
                def enable_cmd(mod, mod_widget):
                    if is_overlay_running():
                        print('clsmao: Stop running mods to proceed.')
                        return
                    mod.enable = not mod.enable
                    cslmao.save_mods()
                    update_enable_state(mod_widget, mod.enable)
                mod_widget.mousePressEvent = lambda event, mod=mod, mod_widget=mod_widget: enable_cmd(mod, mod_widget)
                # action left right layout
                action_layout = QHBoxLayout()
                action_layout.setContentsMargins(5, 5, 5, 5)
                mod_image.setLayout(action_layout)
                left_action_layout = QVBoxLayout()
                right_action_layout = QVBoxLayout()
                action_layout.addLayout(left_action_layout)
                action_layout.addLayout(right_action_layout)
                # locate
                mod_widget.locate_button = locate_button = QToolButton()
                locate_button.setText('📂')
                def locate_cmd(mod):
                    os.startfile(lepath.abs(lepath.join(cslmao.raw_dir, mod.get_path())))
                locate_button.clicked.connect(lambda event, mod=mod: locate_cmd(mod))
                locate_button.setVisible(False)
                left_action_layout.addWidget(locate_button, alignment=Qt.AlignmentFlag.AlignLeft)
                # edit
                mod_widget.edit_button = edit_button = QToolButton()
                edit_button.setText('✏️')
                def edit_cmd(mod):
                    if is_overlay_running():
                        print('clsmao: Stop running mods to proceed.')
                        return
                    set_edit(mod)
                    edit_widget.setVisible(True)
                edit_button.clicked.connect(lambda event, mod=mod: edit_cmd(mod))
                edit_button.setVisible(False)
                left_action_layout.addWidget(edit_button, alignment=Qt.AlignmentFlag.AlignLeft)
                # export
                mod_widget.export_button = export_button =QToolButton()
                export_button.setText('📤')
                def export_cmd(mod):
                    if is_overlay_running():
                        print('clsmao: Stop running mods to proceed.')
                        return
                    dialog = QFileDialog()
                    cslmao.get_info(mod)
                    default_filename = f'{mod.info["Name"]} V{mod.info["Version"]} by {mod.info["Author"]}.fantome'
                    filepath = dialog.getSaveFileName(
                        widget, 
                        'Export FANTOME',
                        lepath.join(setting.get('qtGUI.default_folder', ''), default_filename),
                        f'FANTOME File (*.fantome)'
                    )
                    if len(filepath[0]) > 0:
                        final_path = filepath[0]
                        def export_thrd():
                            p = cslmao.export_fantome(
                                mod_path=lepath.join(
                                    cslmao.raw_dir,
                                    mod.get_path()
                                ),
                                fantome_path=final_path
                            )
                            if p.returncode == 0:
                                print(f'cslmao: Exported: {final_path}')
                        helper.SafeThread.start('cslmao', export_thrd)
                export_button.clicked.connect(lambda event, mod=mod: export_cmd(mod))
                export_button.setVisible(False)
                right_action_layout.addWidget(export_button, alignment=Qt.AlignmentFlag.AlignRight)
                # remove
                mod_widget.remove_button = remove_button = QToolButton()
                remove_button.setText('❌')
                def remove_cmd(mod):
                    if is_overlay_running():
                        print('clsmao: Stop running mods to proceed.')
                        return
                    mod_widget = view_layout.mod_widgets.pop(mod)
                    mod_widget.setParent(None)
                    cslmao.delete_mod(mod)
                    view_layout_smart.build_view_layout()
                    cslmao.save_mods()
                remove_button.clicked.connect(lambda event, mod=mod: remove_cmd(mod))
                remove_button.setVisible(False)
                right_action_layout.addWidget(remove_button, alignment=Qt.AlignmentFlag.AlignRight)
                # left
                mod_widget.left_button = left_button = QToolButton()
                left_button.setText('◀️')
                def left_cmd(mod):
                    if is_overlay_running():
                        print('clsmao: Stop running mods to proceed.')
                        return
                    cslmao.move_left(mod)
                    view_layout_smart.build_view_layout()
                    cslmao.save_mods()
                left_button.clicked.connect(lambda event, mod=mod: left_cmd(mod))
                left_button.setVisible(False)
                left_action_layout.addWidget(left_button, alignment=Qt.AlignmentFlag.AlignLeft)
                # right
                mod_widget.right_button = right_button = QToolButton()
                right_button.setText('▶️')
                def right_cmd(mod):
                    if is_overlay_running():
                        print('clsmao: Stop running mods to proceed.')
                        return
                    cslmao.move_right(mod)
                    view_layout_smart.build_view_layout()
                    cslmao.save_mods()
                right_button.clicked.connect(lambda event, mod=mod: right_cmd(mod))
                right_button.setVisible(False)
                right_action_layout.addWidget(right_button, alignment=Qt.AlignmentFlag.AlignRight)
                # mouse enter + leave event
                def enter_cmd(mod):
                    if mod in view_layout.mod_widgets:
                        mod_widget = view_layout.mod_widgets[mod]
                        mod_widget.locate_button.setVisible(True)
                        mod_widget.edit_button.setVisible(True)
                        mod_widget.export_button.setVisible(True)
                        mod_widget.remove_button.setVisible(True)
                        mod_widget.left_button.setVisible(True)
                        mod_widget.right_button.setVisible(True)
                mod_widget.enterEvent = lambda event, mod=mod: enter_cmd(mod)
                def leave_cmd(mod):
                    if mod in view_layout.mod_widgets:
                        mod_widget = view_layout.mod_widgets[mod]
                        mod_widget.locate_button.setVisible(False)
                        mod_widget.edit_button.setVisible(False)
                        mod_widget.export_button.setVisible(False)
                        mod_widget.remove_button.setVisible(False)
                        mod_widget.left_button.setVisible(False)
                        mod_widget.right_button.setVisible(False)
                mod_widget.leaveEvent = lambda event, mod=mod: leave_cmd(mod)
                # store mod widget
                mod_widget.setLayout(mod_layout)
                view_layout.mod_widgets[mod] = mod_widget
            else:
                mod_widget = view_layout.mod_widgets[mod]
            row_index = view_index // max_column
            col_index = view_index % max_column
            view_index += 1
            view_layout.addWidget(mod_widget, row_index, col_index)
            view_layout.setColumnStretch(col_index, 0)
        view_layout.setRowStretch(view_layout.rowCount(), 1)
        view_layout.setColumnStretch(view_layout.columnCount(), 1)
    # for thread safe
    class ViewLayoutSmart(QObject):
        signal = Signal()

        def __init__(self, view_layout):
            QObject.__init__(self)
            self.signal.connect(build_view_layout)
        
        def build_view_layout(self):
            self.signal.emit()
    qtwidgets.view_layout_smart = view_layout_smart = ViewLayoutSmart(view_layout)
    class RunButtonSmart(QObject):
        signal = Signal(str)

        def __init__(self, run_button):
            QObject.__init__(self)
            self.signal.connect(run_button.setText)
        
        def setText(self, text):
            self.signal.emit(text)
    qtwidgets.RunButtonSmart = run_button_smart = RunButtonSmart(run_button)
    # rebuild layout if size changed
    qtwidgets.max_column = None
    def rebuild_layout_resize():
        max_column = view_widget.width() // 270
        max_column = 1 if max_column < 1 else max_column
        if max_column != qtwidgets.max_column:
            qtwidgets.max_column = max_column
            view_layout_smart.build_view_layout()
    view_widget.resizeEvent = lambda event: rebuild_layout_resize()

    # edit layout
    edit_layout = QHBoxLayout()
    edit_widget = QWidget()
    edit_widget.setLayout(edit_layout)
    edit_widget.setVisible(False)
    layout.addWidget(edit_widget)
    # info
    label_layout = QVBoxLayout()
    label_layout.addWidget(QLabel('🆔 Name:'))
    label_layout.addWidget(QLabel('👤 Author:'))
    label_layout.addWidget(QLabel('🏷️ Version:'))
    label_layout.addWidget(QLabel('📃 Description:'))
    edit_layout.addLayout(label_layout)
    line_layout = QVBoxLayout()
    edit_layout.name_line = name_line = QLineEdit()
    edit_layout.author_line = author_line = QLineEdit()
    edit_layout.version_line = version_line = QLineEdit()
    edit_layout.desc_line = desc_line = QLineEdit()
    line_layout.addWidget(name_line)
    line_layout.addWidget(author_line)
    line_layout.addWidget(version_line)
    line_layout.addWidget(desc_line)
    edit_layout.addLayout(line_layout)
    # profile 
    image_layout = QVBoxLayout()
    profile_layout = QHBoxLayout()
    profile_layout.addWidget(QLabel('📚 Profile:'))
    edit_layout.profile_box = profile_box = QComboBox()
    profile_box.addItems(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
    profile_layout.addWidget(profile_box)
    image_layout.addLayout(profile_layout)
    # image
    image_layout.addWidget(QLabel('🌇 Image:'))
    edit_layout.edit_image = edit_image = QLabel()
    edit_image.setPixmap(image_empty)
    edit_image.final_path = None
    def edit_image_cmd():
        dialog = QFileDialog()
        filepath = dialog.getOpenFileName(
            widget, 
            'Select PNG',
            setting.get('qtGUI.default_folder', ''),
            f'PNG Files (*.png)'
        )
        if len(filepath[0]) > 0:
            final_path = filepath[0]
            edit_image.final_path = final_path
            edit_image.setPixmap(QPixmap(final_path).scaled(256, 144, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            edit_image.final_path = None
            edit_image.setPixmap(image_empty)
    edit_image.mousePressEvent = lambda event: edit_image_cmd()
    image_layout.addWidget(edit_image)
    edit_layout.addLayout(image_layout)
    # confirm
    confirm_layout = QVBoxLayout()
    # close
    close_button = QToolButton()
    close_button.setMinimumWidth(130)
    close_button.setText('❌ Close')
    def close_cmd():
        edit_widget.setVisible(False)
    close_button.clicked.connect(close_cmd)
    confirm_layout.addWidget(close_button)
    # save
    save_button = QToolButton()
    save_button.setMinimumWidth(130)
    save_button.setText('💾 Save')
    def save_cmd():
        mod = edit_layout.mod
        info = {
            'Name': edit_layout.name_line.text(),
            'Author': edit_layout.author_line.text(),
            'Version': edit_layout.version_line.text(),
            'Description': edit_layout.desc_line.text()
        }
        mod.info = info
        mod.image = edit_layout.edit_image.final_path
        if mod.image == None: 
            cslmao.delete_info_image(mod)
        cslmao.set_info(mod)
        mod.profile = edit_layout.profile_box.currentText()
        # update mod widget
        mod_widget = view_layout.mod_widgets[mod]
        mod_widget.mod_image.setPixmap(
            QPixmap(mod.image).scaled(256, 144, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            if mod.image != None else image_empty
        )
        #mod_widget.mod_info.setText(f'📚{mod.profile} 🆔{mod.info["Name"]}\n🏷️{mod.info["Version"]} 👤{mod.info["Author"]}\n{mod.info["Description"]}')
        mod_widget.mod_info.setText(mod.info['Name'])
        edit_widget.setVisible(False)
        cslmao.save_mods()
        
    save_button.clicked.connect(save_cmd)
    confirm_layout.addWidget(save_button)
    edit_layout.addLayout(confirm_layout)

    # set edit
    def set_edit(mod):
        cslmao.get_info(mod)
        edit_layout.name_line.setText(mod.info['Name'])
        edit_layout.author_line.setText(mod.info['Author'])
        edit_layout.version_line.setText(mod.info['Version'])
        edit_layout.desc_line.setText(mod.info['Description'])
        edit_layout.profile_box.setCurrentText(mod.profile)
        edit_layout.edit_image.setPixmap(
            QPixmap(mod.image).scaled(256, 144, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation)
            if mod.image != None else image_empty
        )
        edit_layout.edit_image.final_path = mod.image
        edit_layout.mod = mod


    # run mods
    qtwidgets.make_overlay = None
    qtwidgets.run_overlay = None
    def run_mods():
        if qtwidgets.make_overlay == None and qtwidgets.run_overlay == None:
            def run_thrd():
                # convert files before we run
                cslmao.convert_raw_files_before_run()
                # run
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
            print('clsmao: Stop running mods to proceed.')
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
        mod.info = mod_info
        cslmao.set_info(mod)
        cslmao.add_mod(mod)
        view_layout_smart.build_view_layout()
        cslmao.save_mods()
    new_button.clicked.connect(new_mod)

    # import mod
    def import_mod():
        if is_overlay_running():
            print('clsmao: Stop running mods to proceed.')
            return
        dialog = QFileDialog()
        filepaths = dialog.getOpenFileNames(
            widget, 
            f'Select MOD',
            setting.get('qtGUI.default_folder', ''),
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
                        cslmao.add_mod(mod)
                    else:
                        cslmao.delete_mod(mod)
                view_layout_smart.build_view_layout()
                cslmao.save_mods()

            helper.SafeThread.start('cslmao', import_thrd)
    import_button.clicked.connect(import_mod)

    # enable/disable all
    def all_mods():
        if is_overlay_running():
            print('clsmao: Stop running mods to proceed.')
            return
        # get view mods with search and profile
        for mod_index in range(len(qtwidgets.view_mods)):
            mod = cslmao.MOD.mods[mod_index]
            mod_widget = view_layout.mod_widgets[mod]
            if qtwidgets.view_mods[mod_index]:
                if qtwidgets.all_mod_enable:
                    mod_widget.setObjectName('CslmaoModWidgetEnable')
                    mod_widget.setStyleSheet(qtwidgets.mod_enable_stylesheet)
                    mod_widget.mod_info.setObjectName('CslmaoModWidgetEnable')
                    mod_widget.mod_info.setStyleSheet(qtwidgets.mod_enable_stylesheet)
                else:
                    mod_widget.setObjectName('CslmaoModWidgetDisable')
                    mod_widget.setStyleSheet(qtwidgets.mod_disable_stylesheet)
                    mod_widget.mod_info.setObjectName('CslmaoModWidgetDisable')
                    mod_widget.mod_info.setStyleSheet(qtwidgets.mod_disable_stylesheet)
                mod.enable = qtwidgets.all_mod_enable
        cslmao.save_mods()
        qtwidgets.all_mod_enable = not qtwidgets.all_mod_enable
    all_button.clicked.connect(all_mods)

    # check overlay running
    def is_overlay_running():
        if qtwidgets.make_overlay != None or qtwidgets.run_overlay != None:
            return True
        return False
    
    # drag and drop 
    def dnd_cmd(paths):
        if is_overlay_running():
            print('clsmao: Stop running mods to proceed.')
            return
        fantome_files = []
        for path in paths:
            if os.path.isdir(path):
                fantome_files += lepath.walk(path, lambda f: f.endswith('.fantome') or f.endswith('.zip'))
            else:
                if path.endswith('.fantome') or path.endswith('.zip'):
                    fantome_files.append(path)  
        def import_thrd():
            for fantome_file in fantome_files:
                mod_path = '.'.join(os.path.basename(fantome_file).split('.')[:-1])
                mod_profile = setting.get('cslmao.profile', 'all')
                if mod_profile == 'all':
                    mod_profile = '0'
                mod = cslmao.create_mod(
                    path=mod_path, enable=False, profile=mod_profile)
                p = cslmao.import_fantome(fantome_file, mod.get_path())
                if p.returncode == 0:
                    print(f'cslmao: Imported: {fantome_file}')
                    cslmao.add_mod(mod)
                else:
                    cslmao.delete_mod(mod)
            view_layout_smart.build_view_layout()
            cslmao.save_mods()
        helper.SafeThread.start('cslmao', import_thrd)
    helper.link_dnd_cmd(widget, dnd_cmd)

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
        dirpath = dialog.getExistingDirectory(widget, 'Select hash folder', setting.get('qtGUI.default_folder', ''))
        if dirpath != '':
            abspath = lepath.abs(dirpath)
            abspath_cdtb = lepath.abs(hash_helper.CDTBHashes.local_dir)
            abspath_extracted = lepath.abs(hash_helper.ExtractedHashes.local_dir)
            abspath_custom = lepath.abs(hash_helper.CustomHashes.local_dir)
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
            os.startfile(lepath.abs(hash_helper.CDTBHashes.local_dir))
        elif hash_id == 1:
            os.startfile(lepath.abs(hash_helper.ExtractedHashes.local_dir))
        else:
            os.startfile(lepath.abs(hash_helper.CustomHashes.local_dir))
    
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
    button.clicked.connect(lambda event: hash_helper.CustomHashes.reset_custom_hashes(*hash_helper.ALL_HASHES))
    layout2.addWidget(button)
    button = QToolButton()
    button.setText('❌ Clear Extract hash')
    button.clicked.connect(lambda event: hash_helper.ExtractedHashes.clear_extract_hashes(*hash_helper.ALL_HASHES))
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
                setting.get('qtGUI.default_folder', ''),
                f'WAD Files (*.wad.client)'
            )
            if len(filepaths[0]) > 0:
                final_paths += filepaths[0]
        else:
            dirpath = dialog.getExistingDirectory(
                widget,
                f'Select Folder',
                setting.get('qtGUI.default_folder', ''),
            )
            if dirpath != '':
                for root, dirs, files in os.walk(dirpath):
                    for file in files:
                        final_paths.append(lepath.join(root, file))
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
                hash_helper.Storage.hashtables[filename][hashes[i]] = raws[i]
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
        textedit2.setPlainText('\n'.join([pyRitoFile.bin.BINHasher.raw_to_hex(text) if text != '' else '' for text in textedit.toPlainText().split('\n')]))
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
                hash_helper.Storage.hashtables[filename][hashes[i]] = raws[i]
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
        textedit4.setPlainText('\n'.join([pyRitoFile.wad.WADHasher.raw_to_hex(text) if text != '' else '' for text in textedit3.toPlainText().split('\n')]))
    textedit3.textChanged.connect(input_text)


    layout.addStretch()
    widget.setLayout(layout)

    # drag and drop 
    def dnd_cmd(paths):
        files = [] 
        for path in paths:
            if os.path.isdir(path):
                files += lepath.walk(path, lambda f: True)
            else:
                files.append(path)
        def extract_thrd():
            print(f'hash_helper: Start: Extract hashes with {len(files)} items.')
            hash_helper.ExtractedHashes.extract(*files)
            print('hash_helper: Finish: Extract hashes.')
        helper.SafeThread.start('hash_helper', extract_thrd) 
    helper.link_dnd_cmd(widget, dnd_cmd)

def build_mask_viewer(widget: QWidget):
    layout = QVBoxLayout()
    
    # browse layout
    layout2 = QGridLayout()
    def browse(line, title, file_type):
        dialog = QFileDialog()
        filepath = dialog.getOpenFileName(
            widget, 
            title,
            setting.get('qtGUI.default_folder', ''),
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
    button.setText('❌ Clear')
    button.clicked.connect(lambda event: clear_table(table))
    layout2.addWidget(button)

    button = QToolButton()
    button.setText('💾 Save as')
    button.clicked.connect(lambda event: save_table(table))
    layout2.addWidget(button)

    layout2.addWidget(QLabel('💡 Correct weight value range: [0.000-1.000]'))
    layout2.addStretch()
    layout.addLayout(layout2)

    layout.addWidget(table, stretch=1)

    # action cmds
    def load_table(skl_line, anm_bin_line, table: QTableWidget):
        hash_helper.Storage.read_bin_hashes()
        skl_file = pyRitoFile.skl.SKL().read(skl_line.text())
        joint_names = [f'[{joint_id}] {joint.name}' for joint_id, joint in enumerate(skl_file.joints)]
        hash_helper.Storage.free_bin_hashes()
        qtwidgets.mask_viewer_bin_file = bin_file = pyRitoFile.bin.BIN().read(anm_bin_line.text())
        mask_data = mask_viewer.get_weights(bin_file)
        mask_names, weights = list(mask_data.keys()), list(mask_data.values())
        table.setRowCount(len(joint_names))
        table.setColumnCount(len(mask_names))
        table.setHorizontalHeaderLabels(mask_names)
        table.setVerticalHeaderLabels(joint_names)
        for j in range(table.columnCount()):
            for i in range(table.rowCount()):
                try:
                    weight = str(weights[j][i])
                except:
                    weight = '0.0'
                table.setItem(i, j, QTableWidgetItem(weight))
        print(f'mask_viewer: Finish: Load table: {anm_bin_line.text()}')

    def save_table(table: QTableWidget):
        dialog = QFileDialog()
        filepath = dialog.getSaveFileName(
            widget, 
            'Save Animation BIN as',
            setting.get('qtGUI.default_folder', ''),
            f'BIN Files (*.bin)'
        )
        if len(filepath[0]) > 0:
            final_path = filepath[0]
            mask_data = {}
            for j in range(table.columnCount()):
                mask_name = table.horizontalHeaderItem(j).text()
                weights = [float(table.item(i, j).text()) for i in range(table.rowCount())]
                mask_data[mask_name] = weights
            mask_viewer.set_weights(qtwidgets.mask_viewer_bin_file, mask_data)
            qtwidgets.mask_viewer_bin_file.write(final_path)
            print(f'mask_viewer: Finish: Save table: {final_path}')

    def clear_table(table: QTableWidget):
        qtwidgets.mask_viewer_bin_file = None
        table.clear()
        table.setRowCount(0)
        table.setColumnCount(0)
        print(f'mask_viewer: Finish: Clear table.')

    layout.addStretch()
    widget.setLayout(layout)

    # drag and drop 
    def dnd_cmd(paths):
        for path in paths:
            if path.endswith('.skl'):
                skl_line.setText(path)
            elif path.endswith('.bin'):
                anm_bin_line.setText(path)
    helper.link_dnd_cmd(widget, dnd_cmd)


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
                setting.get('qtGUI.default_folder', ''),
                f'BIN Files (*.bin)'
            )
            if len(filepaths[0]) > 0:
                final_path = filepaths[0]
        else:
            dirpath = dialog.getExistingDirectory(
                widget,
                f'Select Folder',
                setting.get('qtGUI.default_folder', ''),
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
    qtwidgets.tab_widgets.append(tab_widget)
    
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
            setting.get('qtGUI.default_folder', ''),
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

    layout3.addStretch()
    full_button = QToolButton()
    full_button.setText('🐧 Make NO SKIN.fantome')
    def no_skin_full():
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget,
            f'Select Output Fantome Folder',
            setting.get('qtGUI.default_folder', ''),
        )
        if dirpath != '':
            def no_skin_thrd():
                final_path = dirpath
                no_skin.full_no_skin(champs_line.text(), final_path)
    
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
            setting.get('qtGUI.default_folder', ''),
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
            setting.get('qtGUI.default_folder', ''),
            f'BIN Files (*.bin)'
        )
        if len(filepaths[0]) > 0:
            final_paths = filepaths[0]
        skinx_text.setPlainText('\n'.join(final_paths))
    skinx_button.clicked.connect(select_skinx)
    layout3.addWidget(skinx_button, alignment=Qt.AlignmentFlag.AlignTop)
    layout2.addLayout(layout3, stretch=999)

    mini_button = QToolButton()
    mini_button.setText('🦭 Swap all SkinX to Skin0')
    def no_skin_lite(label, text):
        def no_skin_thrd():
            no_skin.mini_no_skin(
                skin0_file=skin0_line.text(), 
                otherskins_files=skinx_text.toPlainText().split('\n')
            )
        
        helper.SafeThread.start('no_skin', no_skin_thrd)
    mini_button.clicked.connect(lambda event: no_skin_lite(skin0_line, skinx_text))
    layout2.addWidget(mini_button)
    
    tab2.setLayout(layout2)
    tab_widget.addTab(tab2, '⭕ Lite')

    # save load tab_index
    tab_widget.setCurrentIndex(setting.get('qtGUI.no_skin.tab_index', 0))
    def currentChanged(tab_index):
        setting.set('qtGUI.no_skin.tab_index', tab_index)
        setting.save()
    tab_widget.currentChanged.connect(currentChanged)

    layout.addWidget(tab_widget, stretch=1)
    widget.setLayout(layout)

    # drag and drop 
    def dnd_tab1_cmd(paths):
        for path in paths:
            if os.path.isdir(path):
                champs_line.setText(path)
                break
    helper.link_dnd_cmd(tab1, dnd_tab1_cmd)

    def dnd_tab2_cmd(paths):
        bin_files = []
        for path in paths:
            if os.path.isdir(path):
                bin_files = lepath.walk(path, lambda f: f.endswith('.bin'))
            else:
                if path.endswith('.bin'):
                    bin_files.append(path)
        skinx_files = []
        for bin_file in bin_files:
            if bin_file.endswith('skin0.bin'):
                skin0_line.setText(bin_file)
            else:
                if os.path.basename(bin_file).replace('skin', '').replace('.bin', '').isnumeric():
                    skinx_files.append(bin_file)
        if len(skinx_files) > 0:
            skinx_text.setPlainText('\n'.join(skinx_files))
    helper.link_dnd_cmd(tab2, dnd_tab2_cmd)


def build_bumpath(widget: QWidget):
    layout = QVBoxLayout()
    
    # main layout
    layout2 = QHBoxLayout()
    layout.addLayout(layout2, stretch=99)

    # left layout
    layout3 = QVBoxLayout()
    layout2.addLayout(layout3, stretch=3)

    # top left layout
    layout4 = QVBoxLayout()
    layout3.addLayout(layout4, stretch=5)
    # source dirs
    dir_button = QToolButton()
    dir_button.setText('📁 Add Source Folders')
    layout4.addWidget(dir_button)
    # dir layout
    dir_widget = QWidget()
    dir_scrollarea = QScrollArea()
    dir_scrollarea.setWidget(dir_widget)
    dir_scrollarea.setWidgetResizable(True)
    dir_layout = QVBoxLayout()
    dir_layout.widgets = []
    dir_layout.addStretch()
    dir_widget.setLayout(dir_layout)
    layout4.addWidget(dir_scrollarea, stretch=1)

    # bot left layout
    layout5 = QVBoxLayout()
    layout3.addLayout(layout5, stretch=5)
    # source bins
    layout8 = QHBoxLayout()
    layout8.addWidget(QLabel('📝 Source BINs: '))
    search_line = QLineEdit()
    search_line.setPlaceholderText('🔎 Filter')
    def filter_cmd(text):
        for bin_widget in bin_layout.widgets:
            if text in bin_widget.text():
                bin_widget.setVisible(True)
            else:
                bin_widget.setVisible(False)
    search_line.textChanged.connect(filter_cmd)
    layout8.addWidget(search_line)
    layout5.addLayout(layout8)
    # bin layout
    bin_widget = QWidget()
    bin_scrollarea = QScrollArea()
    bin_scrollarea.setWidget(bin_widget)
    bin_scrollarea.setWidgetResizable(True)
    bin_layout = QVBoxLayout()
    bin_layout.widgets = []
    bin_layout.addStretch()
    bin_widget.setLayout(bin_layout)
    layout5.addWidget(bin_scrollarea, stretch=1)
    # right layout
    layout6 = QVBoxLayout()
    layout2.addLayout(layout6, stretch=7)
    # toggle
    layout9 = QHBoxLayout()
    layout9.addWidget(QLabel('🌳 Scanned Tree:'))
    layout9.addStretch()
    missing_checkbox = QCheckBox()
    missing_checkbox.setText('🔴 Show Missing Files Only')
    layout9.addWidget(missing_checkbox)
    layout6.addLayout(layout9)
    # scan tree
    treeview = QTreeView()
    treeview.setHeaderHidden(True)
    treeview.setSelectionMode(treeview.SelectionMode.ExtendedSelection)
    model = QStandardItemModel()
    treeview.setModel(model)
    layout6.addWidget(treeview, stretch=1)
    # bind expand all, collapse all
    shortcut = QShortcut(QKeySequence('/'), treeview)
    shortcut.activated.connect(treeview.collapseAll)
    shortcut2 = QShortcut(QKeySequence('*'), treeview)
    shortcut2.activated.connect(treeview.expandAll)

    # action layout
    layout7 = QHBoxLayout()
    reset_button = QToolButton()
    reset_button.setText('❌ Reset')
    reset_button.setMinimumWidth(130)
    layout7.addWidget(reset_button)
    ignore_checkbox = QCheckBox()
    ignore_checkbox.setText('🚫 Ignore Missing Files')
    ignore_checkbox.setChecked(setting.get('bumpath.ignore_missing', False))
    def ignore_cmd():
        setting.set('bumpath.ignore_missing', ignore_checkbox.isChecked())
        setting.save()
    ignore_checkbox.clicked.connect(ignore_cmd)
    layout7.addWidget(ignore_checkbox)
    combine_checkbox = QCheckBox()
    combine_checkbox.setText('🧬 Combine Linked BINs to Source BINs')
    combine_checkbox.setChecked(setting.get('bumpath.combine_linked', False))
    def combine_cmd():
        setting.set('bumpath.combine_linked', combine_checkbox.isChecked())
        setting.save()
    combine_checkbox.clicked.connect(combine_cmd)
    layout7.addWidget(combine_checkbox)
    layout7.addStretch()
    edit_line = QLineEdit()
    edit_line.setText('bum')
    layout7.addWidget(edit_line)
    edit_button = QToolButton()
    edit_button.setText('🔗 Apply Prefix')
    edit_button.setMinimumWidth(130)
    layout7.addWidget(edit_button)
    bum_button = QToolButton()
    bum_button.setText('🍑 Bum')
    bum_button.setMinimumWidth(130)
    layout7.addWidget(bum_button)
    layout.addLayout(layout7, stretch=1)

    # init
    qtwidgets.bum = bum = bumpath.Bum()

    # add source dir
    def select_source_dir():
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget, 
            'Select Source Folder',
            setting.get('qtGUI.default_folder', '')
        )
        if dirpath != '':
            bum.add_source_dirs([dirpath])
            update_dir_layout()
            update_bin_layout()   
            update_scan_layout()
    dir_button.clicked.connect(lambda event: select_source_dir())

    def build_source_dir_widget(source_dir):
        source_dir_widget = QWidget()
        source_dir_layout = QHBoxLayout()
        up_button = QToolButton()
        up_button.setText('🔼')
        def up_cmd():
            cloned_source_dirs = list(bum.source_dirs)
            source_dir_id = cloned_source_dirs.index(source_dir)
            if source_dir_id > 0:
                cloned_source_dirs[source_dir_id], cloned_source_dirs[source_dir_id-1] = cloned_source_dirs[source_dir_id-1], cloned_source_dirs[source_dir_id] 
            reset_cmd()
            bum.add_source_dirs(cloned_source_dirs)
            update_dir_layout()
            update_bin_layout()   
            update_scan_layout()
        up_button.clicked.connect(up_cmd)
        source_dir_layout.addWidget(up_button)
        down_button = QToolButton()
        down_button.setText('🔽')
        def down_cmd():
            cloned_source_dirs = list(bum.source_dirs)
            source_dir_id = cloned_source_dirs.index(source_dir)
            if source_dir_id < len(cloned_source_dirs)-1:
                cloned_source_dirs[source_dir_id], cloned_source_dirs[source_dir_id+1] = cloned_source_dirs[source_dir_id+1], cloned_source_dirs[source_dir_id] 
            reset_cmd()
            bum.add_source_dirs(cloned_source_dirs)
            update_dir_layout()
            update_bin_layout()   
            update_scan_layout()
        down_button.clicked.connect(down_cmd)
        source_dir_layout.addWidget(down_button)
        source_dir_layout.addWidget(QLabel(source_dir))
        source_dir_widget.setLayout(source_dir_layout)
        dir_layout.insertWidget(dir_layout.count()-1, source_dir_widget)
        dir_layout.widgets.append(source_dir_widget)

    # update dir layout
    def update_dir_layout():
        for dir_layout_widget in dir_layout.widgets:
            dir_layout_widget.setParent(None)
        dir_layout.widgets = []
        for source_dir in bum.source_dirs:
            build_source_dir_widget(source_dir)

    def build_source_bin_widget(unify_path):
        def checkbox_cmd(unify_path, source_bin_widget):
            bum.source_bins[unify_path] = source_bin_widget.isChecked()
            update_scan_layout()
        source_bin_widget = QCheckBox()
        source_bin_widget.setText(bum.source_files[unify_path][1])
        source_bin_widget.setChecked(bum.source_bins[unify_path])
        source_bin_widget.clicked.connect(lambda event: checkbox_cmd(unify_path, source_bin_widget))
        bin_layout.insertWidget(bin_layout.count()-1, source_bin_widget)
        bin_layout.widgets.append(source_bin_widget)

    # update bin layout
    def update_bin_layout():
        for bin_layout_widget in bin_layout.widgets:
            bin_layout_widget.setParent(None)
        bin_layout.widgets = []
        for unify_path in bum.source_bins:
            build_source_bin_widget(unify_path)

        # apply filter
        filter_cmd(search_line.text())

    # update scan layout
    def update_scan_layout():
        model.clear()
        if any(bum.source_bins.values()):
            bum.scan()
            for entry_hash in bum.scanned_tree:
                if len(bum.scanned_tree[entry_hash]) > 0:
                    entry_name = bum.entry_name[entry_hash]
                    entry_item = QStandardItem(f'🎟️ {entry_hash} 🎫 {entry_name}: 🔗 {bum.entry_prefix[entry_hash]}')
                    entry_item.setEditable(False)
                    for unify_file in bum.scanned_tree[entry_hash]:
                        existed, path = bum.scanned_tree[entry_hash][unify_file]
                        path_item = QStandardItem(f'{"🟢" if existed else "🔴"} {path}')
                        path_item.setEditable(False)
                        entry_item.appendRow(path_item)
                    model.appendRow(entry_item)
                    treeview.setExpanded(model.indexFromItem(entry_item), True)
    
    # missing checkbox
    def missing_checkbox_cmd():
        if missing_checkbox.isChecked():
            for i in range(model.rowCount()):
                entry = model.item(i)
                for j in range(entry.rowCount()):
                    path = entry.child(j)
                    if '🔴' not in path.text():
                        treeview.setRowHidden(j, model.indexFromItem(entry), True)
        else:
            for i in range(model.rowCount()):
                entry = model.item(i)
                for j in range(entry.rowCount()):
                    treeview.setRowHidden(j, model.indexFromItem(entry), False)
    missing_checkbox.clicked.connect(missing_checkbox_cmd)

    # reset
    def reset_cmd():
        qtwidgets.bum.reset()
        for dir_layout_widget in dir_layout.widgets:
            dir_layout_widget.setParent(None)
        dir_layout.widgets = []
        for bin_layout_widget in bin_layout.widgets:
            bin_layout_widget.setParent(None)
        bin_layout.widgets = []
        model.clear()
    reset_button.clicked.connect(reset_cmd)

    # edit
    def edit_cmd():
        prefix = edit_line.text()
        if prefix == '':
            raise Exception(f'bumpath: Error: Set prefix: Prefix can not be empty.')
        select_model = treeview.selectionModel()
        if select_model != None:
            select_index = select_model.selectedIndexes()
            if len(select_index) > 0:
                for index in select_index:
                    text = index.data()
                    if text.startswith('🎟️'):
                        entry_hash = text.split(' 🎫 ')[0].replace('🎟️ ', '')
                        if bum.entry_prefix[entry_hash] == 'Uneditable':
                            continue
                        entry_name = bum.entry_name[entry_hash]
                        bum.entry_prefix[entry_hash] = prefix
                        entry_item = model.itemFromIndex(index)
                        entry_item.setText(f'🎟️ {entry_hash} 🎫 {entry_name}: 🔗 {bum.entry_prefix[entry_hash]}')
    edit_button.clicked.connect(edit_cmd)

    # bum
    def bum_cmd():
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget, 
            'Select Output Folder',
            setting.get('qtGUI.default_folder', '')
        )
        if dirpath != '':
            def bum_thrd(): 
                bum.bum(dirpath, setting.get('bumpath.ignore_missing', False), setting.get('bumpath.combine_linked', False))
            helper.SafeThread.start('bumpath', bum_thrd)
            
    bum_button.clicked.connect(bum_cmd)

    widget.setLayout(layout)

    # drag and drop 
    def dnd_cmd(paths):
        dir_paths = [path for path in paths if os.path.isdir(path)]
        bum.add_source_dirs(dir_paths)
        update_dir_layout()
        update_bin_layout()   
        update_scan_layout()
    helper.link_dnd_cmd(widget, dnd_cmd)
    
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
            setting.get('qtGUI.default_folder', ''),
            f'WAD Files (*.wad.client)'
        )
        if len(filepath[0]) > 0:
            def wad_thrd(): 
                hash_helper.Storage.read_wad_hashes()
                src = filepath[0]
                dst = lepath.ext(src, '.wad.client', '.wad')
                wad_tool.unpack(src, dst, hash_helper.Storage.hashtables)
                print(f'wad_tool: Finish: Unpack {src}')
                hash_helper.Storage.free_wad_hashes()
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
            setting.get('qtGUI.default_folder', '')
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
    add_button.setText('📦 Add WADs')
    layout2.addWidget(add_button)
    scan_button = QToolButton()
    scan_button.setText('📁 Add WADs in Folder')
    layout2.addWidget(scan_button)
    clear_button = QToolButton()
    clear_button.setText('❌ Clear')
    layout2.addWidget(clear_button)
    filter_line = QLineEdit()
    filter_line.setPlaceholderText('🔎 Include keywords, press Enter to filter')
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
                setting.get('qtGUI.default_folder', ''),
                f'WAD Files (*.wad.client)'
            )
            if len(filepaths[0]) > 0:
                final_paths += filepaths[0]
        else:
            dirpath = dialog.getExistingDirectory(
                widget,
                f'Select Folder',
                setting.get('qtGUI.default_folder', ''),
            )
            if dirpath != '':
                for root, dirs, files in os.walk(dirpath):
                    for file in files:
                        if file.endswith('.wad.client'):
                            final_paths.append(lepath.join(root, file))
        if len(final_paths) > 0:
            def wad_thrd():
                print('wad_tool: Start: Load WADs.')
                hash_helper.Storage.read_wad_hashes()
                for wad_path in final_paths:
                    try:
                        if wad_path not in qtwidgets.text_wad_paths:
                            wad = pyRitoFile.wad.WAD().read(wad_path)
                            wad.un_hash(hash_helper.Storage.hashtables)
                            qtwidgets.text_wad_paths.append(wad_path)
                            qtwidgets.text_chunk_hashes.extend(chunk.hash for chunk in wad.chunks)
                    except:
                        pass
                hash_helper.Storage.free_wad_hashes()
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
        ess = []        
        for word in keywords:
            text_cursor = chunk_doc.find(word, 0)
            if text_cursor.isNull():
                continue
            
            es = QTextEdit.ExtraSelection()
            es.cursor = text_cursor
            es.format.setForeground(qtwidgets.accent_brush)
            ess.append(es)
            while not text_cursor.isNull():
                text_cursor = chunk_doc.find(word, text_cursor.selectionEnd())
                es = QTextEdit.ExtraSelection()
                es.cursor = text_cursor
                es.format.setForeground(qtwidgets.accent_brush)
                ess.append(es)
        chunk_text.setExtraSelections(ess)
    filter_line.returnPressed.connect(lambda: filter_chunk(filter_line.text()))
    # bulk unpack
    def bulk_unpack():
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget,
            f'Select Output Folder',
            setting.get('qtGUI.default_folder', ''),
        )
        if dirpath != '':
            wad_paths = wad_text.toPlainText().split('\n')
            chunk_hashes = chunk_text.toPlainText().split('\n')
            if len(chunk_hashes) == 0:
                chunk_hashes = None
            if len(wad_paths) > 0:
                def bulk_unpack_thrd():
                    hash_helper.Storage.read_wad_hashes()
                    for wad_path in wad_paths:
                        wad_tool.unpack(wad_path, dirpath, hash_helper.Storage.hashtables, filter=chunk_hashes)
                    hash_helper.Storage.free_wad_hashes()
                    print(f'wad_tool: Finish: Unpack to {dirpath}')
                helper.SafeThread.start('wad_tool', bulk_unpack_thrd)
    unpack_button.clicked.connect(bulk_unpack)

    widget.setLayout(layout)

    # drag and drop
    def dnd_cmd(paths):
        wad_files = []
        wad_dirs = []
        for path in paths:
            if os.path.isdir(path):
                wad_dirs.append(path)
            else:
                if path.endswith('.wad.client'):
                    wad_files.append(path)
        
        def wad_thrd(): 
            # wad to dir
            if len(wad_files) > 0:
                hash_helper.Storage.read_wad_hashes()
                for wad_file in wad_files:
                    src = wad_file
                    dst = lepath.ext(src, '.wad.client', '.wad')
                    wad_tool.unpack(src, dst, hash_helper.Storage.hashtables)
                    print(f'wad_tool: Finish: Unpack {src}')
                hash_helper.Storage.free_wad_hashes()
            # dir to wad
            if len(wad_dirs) > 0:
                for wad_dir in wad_dirs:
                    src = wad_dir
                    dst = src
                    if dst.endswith('.wad'):
                        dst += '.client'
                    else:
                        if not dst.endswith('.wad.client'):
                            dst += '.wad.client'
                    wad_tool.pack(src, dst)
                    print(f'wad_tool: Finish: Pack {src}')
        helper.SafeThread.start('wad_tool', wad_thrd)
    helper.link_dnd_cmd(widget, dnd_cmd)

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
            setting.get('qtGUI.default_folder', ''),
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
    button.setMinimumWidth(300)
    button.clicked.connect(lambda event, line=skl_line: browse(line, 'Select SKL', 'SKL'))
    layout2.addWidget(button, 1, 1)
    riot_skl_line = QLineEdit()
    riot_skl_line.setPlaceholderText('Require')
    layout2.addWidget(riot_skl_line, 1, 2)
    button = QToolButton()
    button.setText('🦴 Browse Riot SKL')    
    button.setMinimumWidth(300)
    button.clicked.connect(lambda event, line=riot_skl_line: browse(line, 'Select Riot SKL', 'SKL'))
    layout2.addWidget(button, 1, 3)

    # skn
    skn_line = QLineEdit()
    skn_line.setPlaceholderText('Require if fix your skin')
    layout2.addWidget(skn_line, 2, 0)
    button = QToolButton()
    button.setText('🧊 Browse SKN')    
    button.setMinimumWidth(300)
    button.clicked.connect(lambda event, line=skn_line: browse(line, 'Select SKN', 'SKN'))
    layout2.addWidget(button, 2, 1)
    riot_skn_line = QLineEdit()
    riot_skn_line.setPlaceholderText('Leave empty if dont need')
    layout2.addWidget(riot_skn_line, 2, 2)
    button = QToolButton()
    button.setText('🧊 Browse Riot SKN') 
    button.setMinimumWidth(300)   
    button.clicked.connect(lambda event, line=riot_skn_line: browse(line, 'Select Riot SKN', 'SKN'))
    layout2.addWidget(button, 2, 3)

    # anm bin
    anm_bin_line = QLineEdit()
    anm_bin_line.setPlaceholderText('Require if adapt MaskData')
    layout2.addWidget(anm_bin_line, 3, 0)
    button = QToolButton()
    button.setText('📝 Browse Animation BIN')    
    button.setMinimumWidth(300)
    button.clicked.connect(lambda event, line=anm_bin_line: browse(line, 'Select Animation BIN', 'BIN'))
    layout2.addWidget(button, 3, 1)
    riot_anm_bin_line = QLineEdit()
    riot_anm_bin_line.setPlaceholderText('Require if adapt MaskData')
    layout2.addWidget(riot_anm_bin_line, 3, 2)
    button = QToolButton()
    button.setText('📝 Browse Riot Animation BIN')    
    button.setMinimumWidth(300)
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
        lambda event: sborf.maskdata_adapt(
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
    qtwidgets.tab_widgets.append(tab_widget)

    # fbx
    tab1 = QWidget()
    layout2 = QVBoxLayout()
    
    def browse(line, title, file_type):
        dialog = QFileDialog()
        filepath = dialog.getOpenFileName(
            widget, 
            title,
            setting.get('qtGUI.default_folder', ''),
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
            setting.get('qtGUI.default_folder', '')
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
    button.setText('🎬 Select ANMs Folder')    
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
    skn_line.textChanged.connect(lambda event: output_fbx.setText(lepath.ext(event, '.skn', '.fbx')))
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
    fbx_line.textChanged.connect(lambda event: output_skn.setText(lepath.ext(event, '.fbx', '.skn')))
    layout3.addWidget(output_skn)
    layout2.addLayout(layout3)
    def to_skin():
        def lemon_thrd():
            lemon_fbx.fbx_to_skin(
                fbx_line.text(), 
                lepath.ext(output_skn.text(), '.skn', '.skl'), 
                output_skn.text(),
                lepath.join(os.path.dirname(output_skn.text()), 'animations')
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
Maya recommend version: 2023+. 
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
            setting.get('qtGUI.default_folder', ''),
        )
        if dirpath != '':
            lemon_maya.install_plugin(dirpath.replace('\\', '/'))
    button.clicked.connect(install_lemon3d_maya)
    layout2.addWidget(button)
    layout2.addStretch()
    tab2.setLayout(layout2)
    tab_widget.addTab(tab2, '🔥 maya')

    # save load tab_index
    tab_widget.setCurrentIndex(setting.get('qtGUI.lemon3d.tab_index', 0))
    def currentChanged(tab_index):
        setting.set('qtGUI.lemon3d.tab_index', tab_index)
        setting.save()
    tab_widget.currentChanged.connect(currentChanged)

    layout.addWidget(tab_widget, stretch=1)
    widget.setLayout(layout)

    # drag and drop 
    def dnd_tab1_cmd(paths):
        for path in paths:
            if path.endswith('.fbx'):
                fbx_line.setText(path)
            elif path.endswith('.skl'):
                skl_line.setText(path)
            elif path.endswith('.skn'):
                skn_line.setText(path)
            elif os.path.isdir(path):
                anm_line.setText(path)
    helper.link_dnd_cmd(tab1, dnd_tab1_cmd)

def build_texsmart(widget: QWidget): 
    def convert(isfile, title, input_type, func):
        dialog = QFileDialog()
        final_paths = []
        if isfile:
            filepaths = dialog.getOpenFileNames(
                widget, 
                f'Select {input_type}s',
                setting.get('qtGUI.default_folder', ''),
                f'{input_type} Files (*.{input_type})'
            )
            if len(filepaths[0]) > 0:
                final_paths += filepaths[0]
        else:
            dirpath = dialog.getExistingDirectory(
                widget,
                f'Select Folder',
                setting.get('qtGUI.default_folder', ''),
            )
            if dirpath != '':
                for root, dirs, files in os.walk(dirpath):
                    for file in files:
                        if file.endswith(f'.{input_type.lower()}'):
                            final_paths.append(lepath.join(root, file))
        final_path_count = len(final_paths)
        if  final_path_count > 0:
            def convert_thrd():
                print(f'texsmart: Start: {title}: {final_path_count} items.')
                for final_path in final_paths:
                    func(final_path)
                print(f'texsmart: Finish: {title}: {final_path_count} items.')
            helper.SafeThread.start('texsmart', convert_thrd)
        
    converters = [
        { 
            'title': 'DDS to PNG',
            'input_type': 'DDS',
            'icon': '🏞️',
            'func': lambda src: texsmart.dds2png(src)
        },
        { 
            'title': 'PNG to DDS',
            'input_type': 'PNG',
            'icon': '🌇',
            'func': lambda src: texsmart.png2dds(src)
        },
        { 
            'title': 'DDS to TEX',
            'input_type': 'DDS',
            'icon': '🏞️',
            'func': lambda src: texsmart.dds2tex(src)
        },
        { 
            'title': 'TEX to DDS',
            'input_type': 'TEX',
            'icon': '🌌',
            'func': lambda src: texsmart.tex2dds(src)
        },
        { 
            'title': 'Make 2x, 4x DDS',
            'input_type': 'DDS',
            'icon': '🏞️',
            'func': lambda src: texsmart.make2x4x(src)
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

    # drag and drop
    def dnd_cmd(paths):
        dds_files = []
        tex_files = []
        for path in paths:
            if os.path.isdir(path):
                dds_files += lepath.walk(path, lambda f: f.endswith('.dds'))
                tex_files += lepath.walk(path, lambda f: f.endswith('.tex'))
            else:
                if path.endswith('.dds'):
                    dds_files.append(path)
                elif path.endswith('.tex'):
                    tex_files.append(path)
        def convert_thrd():
            # dds to tex
            dds_count = len(dds_files)
            if dds_count > 0:
                title, func = converters[2]['title'], converters[2]['func']
                print(f'texsmart: Start: {title}: {dds_count} items.')
                for dds_file in dds_files:
                    func(dds_file)
                print(f'texsmart: Finish: {title}: {dds_count} items.')
            # tex to dds
            tex_count = len(tex_files)
            if tex_count > 0:
                title, func = converters[3]['title'], converters[3]['func']
                print(f'texsmart: Start: {title}: {tex_count} items.')
                for tex_file in tex_files:
                    func(tex_file)
                print(f'texsmart: Finish: {title}: {tex_count} items.')
        helper.SafeThread.start('texsmart', convert_thrd)
    helper.link_dnd_cmd(widget, dnd_cmd)


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
            setting.get('qtGUI.default_folder', ''),
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
    button.setText('📋 Select Events BNK')    
    button.setMinimumWidth(260)
    def browse_event(line):
        dialog = QFileDialog()
        filepath = dialog.getOpenFileName(
            widget, 
            'Select Event BNK',
            setting.get('qtGUI.default_folder', ''),
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
            setting.get('qtGUI.default_folder', ''),
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
    # bind expand all, collapse all
    shortcut = QShortcut(QKeySequence('/'), treeview)
    shortcut.activated.connect(treeview.collapseAll)
    shortcut2 = QShortcut(QKeySequence('*'), treeview)
    shortcut2.activated.connect(treeview.expandAll)
    # actions
    layout3 = QVBoxLayout()
    
    button = QToolButton()
    button.setText('📻 Load')
    button.setMinimumWidth(230)
    def load_bnk():
        reply = QMessageBox.question(widget, 'U serious uwu?',
            "Loading new BNK will clear the loaded wem files.", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply != QMessageBox.Yes:
            return
            
        # clear cache
        model.clear()
        if qtwidgets.inspector != None:
            qtwidgets.inspector.stop()
            qtwidgets.inspector.port.terminate()
        bnk_tool.Inspector.reset_cache()
        reset_autoplay_values()
        # inspect
        qtwidgets.inspector = inspector = bnk_tool.Inspector(
            audio_path=audio_line.text(),
            events_path=event_line.text(),
            bin_path=bin_line.text(),
            volume=setting.get('bnk_tool.volume', 0.5)
        )
        inspector.unpack(inspector.get_cache_dir())
        
        # set root and expand
        root_item = QStandardItem('🔈 ' + audio_line.text())
        root_item.setEditable(False)
        model.appendRow(root_item)
        treeview.setExpanded(model.indexFromItem(root_item), True)

        # build treeview with audio_tree
        for event_id in inspector.bank_tree.events:
            bank_event = inspector.bank_tree.events[event_id]
            event_item = QStandardItem('📢 ' + str(event_id))
            event_item.setEditable(False)
            root_item.appendRow(event_item)
            for container_id in bank_event.containers:
                container = bank_event.containers[container_id]
                container_item = QStandardItem('📣 ' + str(container_id))
                container_item.setEditable(False)
                event_item.appendRow(container_item)
                for wem_id in container.wems:
                    wem_item = QStandardItem('🎵 ' + str(wem_id))
                    wem_item.setEditable(False)
                    container_item.appendRow(wem_item)
            
            for wem_id in bank_event.wems:
                wem_item = QStandardItem('🎵 ' + str(wem_id))
                wem_item.setEditable(False)
                event_item.appendRow(wem_item)
        for wem_id in inspector.bank_tree.wems:
            wem_item = QStandardItem('🎵 ' + str(wem_id))
            wem_item.setEditable(False)
            root_item.appendRow(wem_item)
    
    
    button.clicked.connect(load_bnk)
    layout3.addWidget(button)
    
    button = QToolButton()
    button.setText('❌ Clear')
    button.setMinimumWidth(230)
    def clear_bnk():
        reply = QMessageBox.question(widget, 'U serious uwu?',
            "U REALLY want to CLEAR the WEMS?!!!", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply != QMessageBox.Yes:
            return
    
        model.clear()
        if qtwidgets.inspector != None:
            qtwidgets.inspector.stop()
            qtwidgets.inspector.port.terminate()
        bnk_tool.Inspector.reset_cache()
        qtwidgets.inspector = None
        reset_autoplay_values()
    button.clicked.connect(clear_bnk)
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
                setting.get('qtGUI.default_folder', ''),
                f'BNK (*.bnk)'
            )
            if len(filepath[0]) > 0:
                final_path = filepath[0]
        else:
            filepath = dialog.getSaveFileName(
                widget, 
                'Save Audio WPK as',
                setting.get('qtGUI.default_folder', ''),
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
    button.setText('📤 Extract all sound')
    button.setMinimumWidth(230)
    def extract_bnk():
        if qtwidgets.inspector == None:
            return
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget,
            f'Select Output Fantome Folder',
            setting.get('qtGUI.default_folder', ''),
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
                'Select WEM',
                setting.get('qtGUI.default_folder', ''),
                f'WEM Files (*.wem)'
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
                    play_thrd = lambda: qtwidgets.inspector.play(wem_id, setting.get('bnk_tool.stop_previous', True))
                    helper.SafeThread.start(f'bnk_tool.play_{wem_id}_{time.time()}', play_thrd)
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

    # explain:
    # when we select wem, dont play sound
    # enter selecting state with 1 sec delay, refresh 1 sec every new select
    # if after 1 sec delay of selecting, nothing new selected, play the sound
    # this is very complicated so we need a whole background thread for autoplay
    def reset_autoplay_values():
        qtwidgets.selected_wem_id = None
        qtwidgets.is_selecting = False
        qtwidgets.select_cd = 0.0
    # autoplay thread  
    def autoplay_thread():
        fixed_delta_time = 0.0166
        while setting.get('bnk_tool.auto_play', True):
            if qtwidgets.inspector != None:
                if qtwidgets.is_selecting:
                    if qtwidgets.select_cd >= 0.0:
                        qtwidgets.select_cd -= fixed_delta_time
                    if qtwidgets.select_cd < 0.0:
                        if qtwidgets.selected_wem_id != None:
                            helper.SafeThread.start(
                                f'{qtwidgets.selected_wem_id}{qtwidgets.select_cd}{time.time}',
                                lambda: qtwidgets.inspector.play(qtwidgets.selected_wem_id, setting.get('bnk_tool.stop_previous', True))
                            )
                        qtwidgets.select_cd = 0.0
                        qtwidgets.is_selecting = False
            time.sleep(fixed_delta_time)
    # autoplay checkbox
    auto_playcheckbox = QCheckBox()
    auto_playcheckbox.setChecked(setting.get('bnk_tool.auto_play', True))
    auto_playcheckbox.setText('🔁 Auto play')
    auto_playcheckbox.setMinimumWidth(230)
    def autoplay_checkbox_cmd():
        setting.set('bnk_tool.auto_play', auto_playcheckbox.isChecked())
        setting.save()
        if setting.get('bnk_tool.auto_play', True):
            helper.SafeThread.start('bnk_tool.auto_play', autoplay_thread)
    auto_playcheckbox.clicked.connect(autoplay_checkbox_cmd)
    layout3.addWidget(auto_playcheckbox)
    # autoplay select cmd
    def autoplay_select_cmd(current, previous):
        if qtwidgets.inspector == None:
            return
        if setting.get('bnk_tool.auto_play', True) :
            text = current.data()
            if text != None and text.startswith('🎵'): 
                wem_id = text[2:]
                qtwidgets.is_selecting = True
                qtwidgets.select_cd = 0.25
                qtwidgets.selected_wem_id = wem_id
    treeview.selectionModel().currentChanged.connect(autoplay_select_cmd)
    # start the autoplay event
    reset_autoplay_values()
    if setting.get('bnk_tool.auto_play', True):
        helper.SafeThread.start('bnk_tool.auto_play', autoplay_thread)

    # play one by one
    stopprev_checkbox = QCheckBox()
    stopprev_checkbox.setChecked(setting.get('bnk_tool.stop_previous', True))
    stopprev_checkbox.setText('⏭️ Stop previous sound')
    stopprev_checkbox.setMinimumWidth(230)
    def stopprev_checkbox_cmd():
        setting.set('bnk_tool.stop_previous', stopprev_checkbox.isChecked())
        setting.save()
    stopprev_checkbox.clicked.connect(stopprev_checkbox_cmd)
    layout3.addWidget(stopprev_checkbox)

    # volume
    volume_slider = QSlider()
    volume_slider.setOrientation(Qt.Orientation.Horizontal)
    volume_slider.setRange(0, 100)
    volume_slider.setValue(int(setting.get('bnk_tool.volume', 0.5)*100))
    def volume_changed(value):
        volume_factor = float(value / 100)
        if qtwidgets.inspector != None:
            qtwidgets.inspector.volume = volume_factor
        setting.set('bnk_tool.volume', volume_factor)
        setting.save()
    volume_slider.valueChanged.connect(volume_changed)
    layout3.addWidget(volume_slider)
    
    layout3.addStretch()
    layout2.addLayout(layout3)
    
    layout.addLayout(layout2, stretch=1)
    widget.setLayout(layout)

    # drag and drop 
    def dnd_cmd(paths):
        for path in paths:
            if path.endswith('.bin'):
                bin_line.setText(path)
            elif path.endswith('_events.bnk'):
                event_line.setText(path)
            elif path.endswith('_audio.bnk'):
                audio_line.setText(path)
        # force wpk on audio even if there is already audio bnk
        for path in paths:
            if path.endswith('.wpk'):
                audio_line.setText(path)
    helper.link_dnd_cmd(widget, dnd_cmd)

def build_wiwawe(widget: QWidget):
    layout = QVBoxLayout()
    # convert 
    def convert(isfile, title, input_type, func):
        dialog = QFileDialog()
        final_paths = []
        if isfile:
            filepaths = dialog.getOpenFileNames(
                widget, 
                f'Select {input_type}s',
                setting.get('qtGUI.default_folder', ''),
                f'{input_type} Files (*.{input_type})'
            )
            if len(filepaths[0]) > 0:
                final_paths += filepaths[0]
        else:
            dirpath = dialog.getExistingDirectory(
                widget,
                f'Select Folder',
                setting.get('qtGUI.default_folder', ''),
            )
            if dirpath != '':
                for root, dirs, files in os.walk(dirpath):
                    for file in files:
                        if file.endswith(f'.{input_type.lower()}'):
                            final_paths.append(lepath.join(root, file))
        final_path_count = len(final_paths)
        if  final_path_count > 0:
            def convert_thrd():
                print(f'wiwawe: Start: {title}: {final_path_count} items.')
                func(final_paths)
                print(f'wiwawe: Finish: {title}: {final_path_count} items.')
            helper.SafeThread.start('wiwawe', convert_thrd)
    converters = [
        { 
            'title': 'WAV to WEM',
            'input_type': 'WAV',
            'icon': '🎶',
            'func': lambda src: wiwawe.wav2wem(src)
        },
        { 
            'title': 'WEM to WAV',
            'input_type': 'WEM',
            'icon': '🎵',
            'func': lambda src: wiwawe.wem2wav(src)
        },
        { 
            'title': 'OGG to WEM',
            'input_type': 'OGG',
            'icon': '📀',
            'func': lambda src: wiwawe.ogg2wem(src)
        }
    ]
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

    # drag and drop
    def dnd_cmd(paths):
        wav_files = []
        wem_files = []
        for path in paths:
            if os.path.isdir(path):
                wav_files += lepath.walk(path, lambda f: f.endswith('.wav'))
                wem_files += lepath.walk(path, lambda f: f.endswith('.wem'))
            else:
                if path.endswith('.wav'):
                    wav_files.append(path)
                elif path.endswith('.wem'):
                    wem_files.append(path)
        def convert_thrd():
            # wav to wem
            wav_count = len(wav_files)
            if wav_count > 0:
                title, func = converters[0]['title'], converters[0]['func']
                print(f'wiwawe: Start: {title}: {wav_count} items.')
                func(wav_files)
                print(f'wiwawe: Finish: {title}: {wav_count} items.')
            # wem to wav
            wem_count = len(wem_files)
            if wem_count > 0:
                title, func = converters[1]['title'], converters[1]['func']
                print(f'wiwawe: Start: {title}: {wem_count} items.')
                func(wem_files)
                print(f'wiwawe: Finish: {title}: {wem_count} items.')
        helper.SafeThread.start('wiwawe', convert_thrd)
    helper.link_dnd_cmd(widget, dnd_cmd)

def build_winLT(widget: QWidget):
    layout = QVBoxLayout()

    # shortcuts
    layout2 = QHBoxLayout()
    desktop_button = QToolButton()
    desktop_button.setText('🖥️ Create desktop shortcut')
    desktop_button.clicked.connect(lambda: winLT.Shortcut.create_desktop(qtwidgets.theme_paths['appicon']))
    layout2.addWidget(desktop_button)
    launch_button = QToolButton()
    launch_button.setText('🚀 Create launch shortcut')
    launch_button.clicked.connect(lambda: winLT.Shortcut.create_launch(qtwidgets.theme_paths['appicon']))
    layout2.addWidget(launch_button)
    layout2.addStretch()
    layout.addLayout(layout2)

    layout.addSpacing(30)
    
    # contexts
    # treewidget
    def set_context_data(shell_id, command_id, value):
        winLT.Context.submenus[shell_id][command_id] = value
        setting.set(f'winLT.{shell_id}.{command_id}', value)
        setting.save()
    layout2 = QHBoxLayout()
    treewidget = QTreeWidget()
    treewidget.setHeaderHidden(True)
    treewidget.setSelectionMode(treewidget.SelectionMode.SingleSelection)
    for shell_id in winLT.Context.submenus:
        shell_item = QTreeWidgetItem(treewidget)
        shell_item.setText(0, f'💬 {shell_id}')
        for command_id in winLT.Context.submenus[shell_id]:
            command_item = QTreeWidgetItem(shell_item)
            command_item.setText(0, '')
            checkbox = QCheckBox(f'🔧 {winLT.Context.commands[command_id]["desc"]}')
            checkbox_value = setting.get(f'winLT.{shell_id}.{command_id}', True)
            checkbox.setChecked(checkbox_value)
            winLT.Context.submenus[shell_id][command_id] = checkbox_value
            checkbox.clicked.connect(lambda value, shell_id=shell_id, command_id=command_id: set_context_data(shell_id, command_id, value))
            treewidget.setItemWidget(command_item, 0, checkbox)
    treewidget.expandAll()

    layout2.addWidget(treewidget)
    layout.addLayout(layout2, stretch=1)
    # buttons
    layout2 = QHBoxLayout()
    set_button = QToolButton()
    set_button.setText('💬 Set explorer context')
    set_button.clicked.connect(lambda: winLT.Context.create_contexts(qtwidgets.theme_paths['appicon']))
    layout2.addWidget(set_button)
    remove_button = QToolButton()
    remove_button.setText('❌ Remove explorer context')
    remove_button.clicked.connect(winLT.Context.remove_contexts)
    layout2.addWidget(remove_button)
    layout2.addStretch()
    layout.addLayout(layout2)

    layout.addStretch()
    widget.setLayout(layout)
    
def build_infinityQT(widget: QWidget):
    layout = QVBoxLayout()

    # main tab widget
    tab_widget = QTabWidget()
    tab_widget.setStyleSheet(qtwidgets.tab_stylesheet)
    qtwidgets.tab_widgets.append(tab_widget)
    tab_widget.setTabsClosable(True)
    layout.addWidget(tab_widget)
    
    # first tab, cant be closed
    tab_widget.addTab(QLabel('Drag and drop files in here.\n(you can not close this page).', alignment=Qt.AlignmentFlag.AlignLeading), 'Main')
    def remove_cmd(index):
        if index != 0:
            tab_widget.removeTab(index)
    tab_widget.tabCloseRequested.connect(remove_cmd)
    # drag and drop 
    def dnd_cmd(paths):
        tabs = infinityQT.build_tabs(paths)
        for title, twidget in tabs:
            if twidget != None:
                tab_widget.addTab(twidget, title)    
                tab_widget.setCurrentWidget(twidget)
    helper.link_dnd_cmd(widget, dnd_cmd)
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
    theme_box = QComboBox()
    theme_box.setMinimumWidth(200)
    theme_box.addItems([f.name for f in os.scandir('./res/themes') if f.is_dir()])
    theme_box.setCurrentText(setting.get('qtGUI.theme_name', 'raora'))
    def change_theme():
        # init theme
        theme_name = theme_box.currentText()
        qtwidgets.theme_paths = qtwidgets.init_theme(theme_name)
        # apply theme
        qtwidgets.main_window.setStyleSheet(qtwidgets.window_stylesheet)
        for tab_widget in qtwidgets.tab_widgets:
            tab_widget.setStyleSheet(qtwidgets.tab_stylesheet)
        qtwidgets.icon_label.setPixmap(QPixmap(qtwidgets.theme_paths['titlebaricon']).scaled(118, 40, Qt.AspectRatioMode.IgnoreAspectRatio, Qt.TransformationMode.SmoothTransformation))
        # set background gif
        if setting.get('qtGUI.animated_background', True):
            qtwidgets.background_widget.setMovie(QMovie(qtwidgets.theme_paths['background']))
            qtwidgets.background_widget.setScaledContents(True)
            qtwidgets.background_widget.movie().start()
        else:
            qtwidgets.background_widget.setPixmap(QPixmap(qtwidgets.theme_paths['background']))
            qtwidgets.background_widget.setScaledContents(True)
        # update icon
        qtwidgets.main_window.setWindowIcon(QPixmap(qtwidgets.theme_paths['appicon']))
        qtwidgets.tray_icon.setIcon(QPixmap(qtwidgets.theme_paths['appicon']))
        # update shortcut
        winLT.Shortcut.update_shortcuts(qtwidgets.theme_paths['appicon'])
        # save theme
        setting.set('qtGUI.theme_name', theme_name)
        setting.save()
    theme_box.currentTextChanged.connect(change_theme)
    layout2.addWidget(theme_box)

    checkbox = QCheckBox()
    checkbox.setText('🎞️ Animated background')
    checkbox.setChecked(setting.get('qtGUI.animated_background', True))
    def animated_background_cmd():
        setting.set('qtGUI.animated_background', checkbox.isChecked())
        setting.save()
        if setting.get('qtGUI.animated_background', True):
            qtwidgets.background_widget.setMovie(QMovie(qtwidgets.theme_paths['background']))
            qtwidgets.background_widget.setScaledContents(True)
            qtwidgets.background_widget.movie().start()
        else:
            qtwidgets.background_widget.setPixmap(QPixmap(qtwidgets.theme_paths['background']))
            qtwidgets.background_widget.setScaledContents(True)
    checkbox.clicked.connect(animated_background_cmd)
    layout2.addWidget(checkbox)

    layout2.addStretch()
    layout.addLayout(layout2)
    # default folder
    layout2 = QHBoxLayout()
    button = QToolButton()
    button.setText('🌳 Default folder ')
    def default_dir_cmd():
        dialog = QFileDialog()
        dirpath = dialog.getExistingDirectory(
            widget,
            f'Select Folder',
            setting.get('qtGUI.default_folder', ''),
        )
        if dirpath == '':
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
    # restart + update + support
    layout2 = QHBoxLayout()
    button = QToolButton()
    button.setText('♻️ Restart LtMAO')
    def restart_cmd():
        print(f'Start: Restart LtMAO')
        os.system(lepath.join(lepath.abs(os.path.curdir),'start.bat'))
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
            chunk_size = 1024**2
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
            import zipfile
            with zipfile.ZipFile(local_file, 'r') as zip:
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
            print(f'update_ltmao: Restart is require for updates to take effect.')

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


