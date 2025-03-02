from PySide6.QtCore import (
    Qt, 
    QEvent,
)
from PySide6.QtGui import (
    QFontDatabase,
    QFont,
    QPixmap,
    QMovie,
)
    
from PySide6.QtWidgets import (
    QApplication, 
    QSplashScreen,
    QMainWindow, 
    QWidget, 
    QBoxLayout,
    QVBoxLayout, 
    QHBoxLayout,
    QLabel,
    QStatusBar,
    QToolButton, 
)

from . import control, helper, log
from .. import setting, hash_helper, winLT, no_skin, bnk_tool
import requests

qtwidgets = helper.Keeper()

def show():
    build_app()

def before_build():
    setting.init()
    no_skin.init()
    control.qtwidgets = qtwidgets
    set_font()
    init_theme()

def set_font():
    id = QFontDatabase.addApplicationFont('./res/font.ttf')
    family = QFontDatabase.applicationFontFamilies(id)[0] if id > -1 else 'Consolas'
    qtwidgets.app.setFont(QFont(family, weight=14))

def init_theme():
    # theme stuffs
    global theme_paths
    theme_name = setting.get('qtGUI.theme_name', 'raora')
    theme_paths = {
        'splash': f'./res/themes/{theme_name}/splash.png',
        'background': f'./res/themes/{theme_name}/background.gif',
        'titlebaricon': f'./res/themes/{theme_name}/titlebaricon.png',
    }
    # get the background accent color 
    import colorthief
    r, g, b = colorthief.ColorThief(theme_paths['background']).get_color(quality=1)
    f = 255*0.7 / max(r, g, b)
    qtwidgets.accent_color = (int(r*f), int(g*f), int(b*f))
    # stylesheets
    qtwidgets.window_stylesheet = f"""
        QWidget {{
            background-color: rgba(0, 0, 0, 127);        
        }}  
        QLabel {{
            background-color: transparent;
        }}  
        QScrollArea {{
            border: none;
            background-color: transparent;
        }}         
        QToolButton {{
            min-height: 30;
            border-bottom: 2px solid rgb{qtwidgets.accent_color};
        }}
        QToolButton:hover {{ 
            background-color: rgb{qtwidgets.accent_color}; 
        }}
        QToolButton:checked {{ 
            background-color: rgb{qtwidgets.accent_color}; 
        }}
        QCheckBox {{
            min-height: 30;
        }}
        QCheckBox:hover {{
            border-bottom-color: rgb{qtwidgets.accent_color};  
        }} 
        QLineEdit {{
            min-height: 30;
        }}
        QLineEdit:focus, QPlainTextEdit:focus {{
            border-color: rgb{qtwidgets.accent_color};  
        }}
        QComboBox {{
            border-color: rgb{qtwidgets.accent_color};
        }}
        QComboBox QAbstractItemView:item:hover, QComboBox QAbstractItemView:item:selected {{
            background-color: rgb{qtwidgets.accent_color};    
        }}
        QTabWidget:pane {{
            border: none;
        }}   
        QTabWidget:tab-bar {{
            background-color: rgba(0, 0, 0, 127);        
        }}    
        QTabBar:tab {{
            min-height: 30;
            min-width: 120;
            background-color: rgba(0, 0, 0, 127);        
        }}
        QTabBar:tab:selected {{
            color: #ffffff;
            border-bottom-color: rgb{qtwidgets.accent_color};
            background-color: rgb{qtwidgets.accent_color};
        }}
        QTableView {{
            selection-background-color: rgb{qtwidgets.accent_color};
        }}
        QHeaderView:section {{
            background-color: transparent;
        }}
        QTableView QTableCornerButton::section {{
            background-color: rgba(0, 0, 0, 127);  
        }}
        QHeaderView:section:checked {{
            color: #ffffff;
            background-color: rgb{qtwidgets.accent_color};
        }}
        QTreeView:item:selected  {{
            background-color: rgb{qtwidgets.accent_color};
        }}
    """
    qtwidgets.tab_stylesheet = f"""
        QWidget {{
            background-color: transparent;
        }}     
        QToolButton {{
            min-height: 30;
            background-color: rgba(0, 0, 0, 127);
            border-bottom: 2px solid rgb{qtwidgets.accent_color};
        }}
        QLabel {{
            background-color: transparent;
        }}
        QLineEdit {{
            min-height: 30;
            background-color: rgba(0, 0, 0, 127);
        }}
        QPlainTextEdit {{
            background-color: rgba(0, 0, 0, 127);
        }}
        QToolButton:hover {{ 
            background-color: rgb{qtwidgets.accent_color}; 
        }}
        QToolButton:checked {{ 
            background-color: rgb{qtwidgets.accent_color}; 
        }}
        QTabBar::tab {{
            border-bottom: 2px solid rgb{qtwidgets.accent_color};
        }}
    """
    

def build_app():
    # set app theme
    import qdarktheme
    qdarktheme.enable_hi_dpi()
    qtwidgets.app = app = QApplication([])
    qdarktheme.setup_theme('dark', corner_shape='sharp')

    before_build()

    # build splash and show splash
    qtwidgets.splash = splash = QSplashScreen()
    build_splash_screen(splash)
    splash.show()
    splash.activateWindow()

    # build main_window
    qtwidgets.main_window = window = QMainWindow() 
    build_main_window(window)

    after_build()

    # close splash and show main window
    splash.close()
    window.show()
    window.showMaximized()
    window.activateWindow()
    app.exec()

def build_splash_screen(splash: QSplashScreen):
    splash.setWindowFlags(splash.windowFlags() | Qt.WindowStaysOnTopHint)
    pixmap = QPixmap(theme_paths['splash']).scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
    splash.setPixmap(pixmap)
    layout = QVBoxLayout()
    label = QLabel()
    label.setStyleSheet('background-color: rgba(0, 0, 0, 127); color: rgba(255, 255, 255, 255);')
    layout.addWidget(label, stretch=1, alignment=Qt.AlignmentFlag.AlignBottom)
    splash.setLayout(layout)
    log.link_splash(label)
    print('qtGUI: Finish: Build splash screen.')

def build_main_window(window: QMainWindow):
    window.setGeometry(0, 0, 1280, 720)
    window.setWindowIcon(QPixmap('./res/appicon.ico'))
    window.setWindowFlags(Qt.Window|Qt.FramelessWindowHint|Qt.WindowMinMaxButtonsHint)
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    window.setContentsMargins(0, 0, 0, 0)
    window.setStyleSheet(qtwidgets.window_stylesheet)
    build_grips(window)
    # set background gif
    widget = QLabel()
    qtwidgets.movie = movie = QMovie(theme_paths['background'])
    widget.setMovie(movie)
    widget.setScaledContents(True)
    movie.start()
    # build main layout
    layout = QVBoxLayout()
    build_main_layout(widget, layout)
    widget.setLayout(layout)
    window.setCentralWidget(widget)

    # events
    def changeEvent(event):
        if event.type() == QEvent.Type.WindowStateChange:
            if window.windowState() == Qt.WindowState.WindowNoState and qtwidgets.main_window.remember_maximized_state:
                qtwidgets.main_window.showMaximized()
                qtwidgets.main_window.remember_maximized_state = False
            if window.windowState() == Qt.WindowState.WindowMaximized:
                qtwidgets.nor_button.setVisible(True)
                qtwidgets.max_button.setVisible(False)
            else:
                qtwidgets.nor_button.setVisible(False)
                qtwidgets.max_button.setVisible(True)
        event.accept()
    window.changeEvent = changeEvent
    
    print('qtGUI: Finish: Build main window.')

def build_grips(window: QMainWindow):
    def build_edge_grip(edge):
        edge_grip = QWidget(window)
        edge_grip.setStyleSheet('background-color: transparent')
        if edge == Qt.Edge.RightEdge:
            edge_grip.setCursor(Qt.CursorShape.SizeHorCursor)
        else:
            edge_grip.setCursor(Qt.CursorShape.SizeVerCursor)
        def mousePressEvent(event):
            if event.button() == Qt.MouseButton.LeftButton:
                edge_grip.mousePos = event.pos()
            event.accept()
        def mouseMoveEvent(event):
            if edge_grip.mousePos is not None:
                delta = event.pos() - edge_grip.mousePos
                if edge == Qt.Edge.RightEdge:
                    window = edge_grip.window()
                    width = max(window.minimumWidth(), window.width() + delta.x())
                    window.resize(width, window.height())
                else:
                    window = edge_grip.window()
                    height = max(window.minimumHeight(), window.height() + delta.y())
                    window.resize(window.width(), height)
            event.accept()
        def mouseReleaseEvent(event):
            edge_grip.mousePos = None
            event.accept()
        edge_grip.mousePressEvent = mousePressEvent
        edge_grip.mouseMoveEvent = mouseMoveEvent
        edge_grip.mouseReleaseEvent = mouseReleaseEvent
        return edge_grip

    right_side_grip = build_edge_grip(Qt.Edge.RightEdge)
    bot_side_grip = build_edge_grip(Qt.Edge.BottomEdge)
    grip_size = 6
    def resizeEvent(event):
        out_rect = window.rect()
        in_rect = out_rect.adjusted(grip_size, grip_size,-grip_size, -grip_size)
        right_side_grip.setGeometry(in_rect.left() + in_rect.width(), in_rect.top(), grip_size, in_rect.height())
        bot_side_grip.setGeometry(grip_size, in_rect.top() + in_rect.height(), in_rect.width(), grip_size)
        right_side_grip.raise_()
        bot_side_grip.raise_()
        event.accept()
    window.resizeEvent = resizeEvent

    print('qtGUI: Finish: Build scale grips.')

def build_main_layout(widget: QWidget, layout: QBoxLayout):
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    widget = QWidget()
    hlayout = QHBoxLayout()
    build_title_bar(widget, hlayout)
    widget.setLayout(hlayout)
    layout.addWidget(widget, stretch=5)
    
    widget = QWidget()
    hlayout = QHBoxLayout()
    build_midcontent(widget, hlayout)
    widget.setLayout(hlayout)
    layout.addWidget(widget, stretch=93)

    widget = QWidget()
    hlayout = QHBoxLayout()
    build_status_bar(widget, hlayout)
    widget.setLayout(hlayout)
    layout.addWidget(widget, stretch=2)

    # build controlcontent after both mid content and status bar
    for c in control.all:
        c.build_command(c.content)
    
    print('qtGUI: Finish: Build main layout.')

def build_title_bar(widget: QWidget, layout: QBoxLayout):
    widget.setFixedHeight(40)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    # icon
    pixmap = QPixmap(theme_paths['titlebaricon']).scaled(120, 40, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
    icon_label = QLabel(pixmap=pixmap)
    layout.addWidget(icon_label, stretch=3)

    # icon
    qtwidgets.title_label = title_label = QLabel('LtMAO-hai')
    title_label.setStyleSheet('background-color: rgba(0, 0, 0, 127)')
    layout.addWidget(title_label, stretch=100)

    # buttons
    min_button = QToolButton()
    min_button.setText('🟢 Minimize')
    min_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    qtwidgets.main_window.remember_maximized_state = False
    def min_button_cmd(event):
        if qtwidgets.main_window.windowState() == Qt.WindowState.WindowMaximized:
            qtwidgets.main_window.showNormal()
            qtwidgets.main_window.remember_maximized_state = True
        qtwidgets.main_window.showMinimized()
    min_button.clicked.connect(min_button_cmd)
    layout.addWidget(min_button, stretch=3)
    
    qtwidgets.nor_button = nor_button = QToolButton()
    nor_button.setText('🟡 Restore')
    nor_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    nor_button.clicked.connect(qtwidgets.main_window.showNormal)
    layout.addWidget(nor_button, stretch=3)

    qtwidgets.max_button = max_button = QToolButton()
    max_button.setText('🔵 Maximize')
    max_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    max_button.setVisible(False)
    max_button.clicked.connect(qtwidgets.main_window.showMaximized)
    layout.addWidget(max_button, stretch=3)
    
    close_button = QToolButton()
    close_button.setText('🔴 Close')
    close_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    close_button.clicked.connect(qtwidgets.main_window.close)
    layout.addWidget(close_button, stretch=3)

    # events
    def mousePressEvent(event):
        if event.button() == Qt.MouseButton.LeftButton:
            widget.initial_pos = event.position().toPoint()
        event.accept()
    widget.mousePressEvent = mousePressEvent
    
    def mouseMoveEvent(event):
        if widget.initial_pos is not None:
            delta = event.position().toPoint() - widget.initial_pos
            widget.window().move(
                widget.window().x() + delta.x(),
                widget.window().y() + delta.y(),
            )
        event.accept()
    widget.mouseMoveEvent = mouseMoveEvent

    def mouseReleaseEvent(event):
        widget.initial_pos = None
        event.accept()
    widget.mouseReleaseEvent = mouseReleaseEvent

    def mouseDoubleClickEvent(event):
        if qtwidgets.main_window.isMaximized():
            qtwidgets.main_window.showNormal()
        else:
            qtwidgets.main_window.showMaximized()
        event.accept()
    widget.mouseDoubleClickEvent = mouseDoubleClickEvent

    print('qtGUI: Finish: Build title bar.')
    
def build_midcontent(widget: QWidget, layout: QBoxLayout):
    qtwidgets.content_layout = layout
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    widget = QWidget()
    control_layout = QVBoxLayout()
    control_layout.setContentsMargins(0, 0, 0, 0)
    control_layout.setSpacing(0)
    widget.setLayout(control_layout)
    layout.addWidget(widget, stretch=1)
    # build controls
    for c in control.all:
        # create control
        control_button = QToolButton()
        control_button.setText(c.name)
        control_button.setMinimumWidth(120)
        control_button.setCheckable(True)
        c.widget = control_button
        control_button.clicked.connect(lambda event, page_id=c.page_id: control.on_page_id_changed(event, page_id))
        control_layout.addWidget(control_button, stretch=1)
        # create content
        content_widget = QWidget()
        content_widget.setVisible(False)
        c.content = content_widget  
        layout.addWidget(content_widget, stretch=99)
    control_layout.addStretch()

    print('qtGUI: Finish: Build mid content.')
    
def build_status_bar(widget: QWidget, layout: QBoxLayout):
    widget.setFixedHeight(40)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    
    qtwidgets.statusbar = statusbar = QStatusBar(sizeGripEnabled=False)
    content_widget = QWidget()
    content_widget.setVisible(False)
    qtwidgets.content_layout.addWidget(content_widget, stretch=99)
    c = control.Control('', 100, lambda widget: control.build_logbox(widget))
    c.widget = statusbar
    c.content = content_widget
    control.all.append(c)
    def mousePressEvent(event):
        if event.button() == Qt.MouseButton.LeftButton:
            control.on_page_id_changed(True, 100)
        event.accept()
    statusbar.mousePressEvent = mousePressEvent
    layout.addWidget(statusbar, stretch=94)

    changelog_button = QToolButton()
    changelog_button.setText('📑 Changelog')
    changelog_button.setCheckable(True)
    content_widget = QWidget()
    content_widget.setVisible(False)
    qtwidgets.content_layout.addWidget(content_widget, stretch=99)
    c = control.Control('', 101, lambda widget: control.build_changelog(widget))
    c.widget = changelog_button
    c.content = content_widget
    control.all.append(c)
    changelog_button.clicked.connect(lambda event, page_id=101: control.on_page_id_changed(event, page_id))
    layout.addWidget(changelog_button, stretch=3)

    setting_button = QToolButton()
    setting_button.setText('⚙️ Setting')
    setting_button.setCheckable(True)
    content_widget = QWidget()
    content_widget.setVisible(False)
    qtwidgets.content_layout.addWidget(content_widget, stretch=99)
    c = control.Control('', 102, lambda widget: control.build_setting(widget))
    c.widget = setting_button
    c.content = content_widget
    control.all.append(c)
    setting_button.clicked.connect(lambda event, page_id=102: control.on_page_id_changed(event, page_id))
    layout.addWidget(setting_button, stretch=3)

    print('qtGUI: Finish: Build status bar.')

def after_build():
    print('qtGUI: Finish: Build main window.')
    log.link_main_window(qtwidgets.logbox, qtwidgets.statusbar)
    helper.SafeThread.start('check_version', lambda: check_version(qtwidgets.title_label))
    helper.SafeThread.start('sync_changelog', lambda: sync_changelog(qtwidgets.changelog))
    control.on_page_id_changed(True, setting.get('qtGUI.page_id', 0))
    hash_helper.init()
    helper.SafeThread.start('sync_ctdb_hashes', hash_helper.CDTBHashes.sync_all)
    winLT.init()
    bnk_tool.init()
    
 
def check_version(label):
    try:
        # read offline
        local_file = './version'
        with open(local_file, 'r') as f:
            VERSION = f.read()
        title = f'LtMAO-hai V{VERSION}'
        label.setText(title)
        # read online
        remote_file = 'https://raw.githubusercontent.com/tarngaina/LtMAO/hai/version'
        get = requests.get(remote_file)
        get.raise_for_status()
        NEW_VERSION = get.text
        if VERSION != NEW_VERSION:
            title += f' - New version found: {NEW_VERSION}, redownload LtMAO to update.'
        label.setText(title)
    except Exception as e:
        print(f'qtGUI: check_version: Error: {str(e)}')
    print('qtGUI: Finish: Check version.')

def sync_changelog(changelog):
    full_changelog_text = ''
    local_file = './pref/changelog.txt'
    try:
        # read online
        url=f'https://api.github.com/repos/tarngaina/ltmao/commits?sha=hai&per_page=100'
        commits=requests.get(url).json()
        for commit in commits:
            commit = commit['commit']
            author = commit['author']['name']
            date = commit['author']['date']
            message = commit['message']
            full_changelog_text += f'[{date}] by {author}:\n{message}\n\n'
        with open(local_file, 'w+', encoding='utf-8') as f:
            f.write(full_changelog_text)

    except Exception as e:
        import os.path
        print(f'get_changelog: Error: {e}, switching to local file if exists.')
        if os.path.exists(local_file):
            # read offline
            with open(local_file, 'r', encoding='utf-8') as f:
                full_changelog_text = f.read()
        else:
            full_changelog_text = 'get_changelog: Error: Download changelog failed, no local changelog to read.'
    changelog.insertPlainText(full_changelog_text)
    print('qtGUI: Finish: Sync changelog.')