from PySide6.QtCore import (
    Qt, 
    QEvent,
)
from PySide6.QtGui import (
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
from .. import setting, hash_helper, winLT, tools, Ritoddstex
import requests


def show():
    build_app()

qtwidgets = helper.Keeper()
LOG = log.LOG

def before_build():
    control.qtwidgets = qtwidgets
    log.qtwidgets = qtwidgets

def build_app():
    import qdarktheme
    qdarktheme.enable_hi_dpi()
    app = QApplication([])
    qdarktheme.setup_theme(theme='dark', corner_shape='sharp')
    app.setFont(QFont('Consolas', weight=14))
    # build splash and show splash
    qtwidgets.splash = splash = QSplashScreen()
    build_splash_screen(splash)
    splash.show()
    splash.activateWindow()

    # build main_window
    before_build()
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
    pixmap = QPixmap('./res/splash.png').scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
    splash.setPixmap(pixmap)
    layout = QVBoxLayout()
    message = QLabel()
    message.setStyleSheet('background-color: rgba(0, 0, 0, 127); color: rgba(255, 255, 255, 255);')
    layout.addWidget(message, stretch=1, alignment=Qt.AlignmentFlag.AlignBottom)
    splash.setLayout(layout)
    def update_msg(msg):
        message.setText('🗒️ ' + msg) 
        message.repaint()
    global LOGSPLASH
    LOGSPLASH = lambda msg: update_msg(msg)
    LOGSPLASH('qtGUI: Finish: Build splash screen.')

def build_main_window(window: QMainWindow):
    window.setGeometry(10, 10, 1000, 700)
    window.setWindowIcon(QPixmap('./res/appicon.ico'))
    window.setWindowFlags(Qt.Window|Qt.FramelessWindowHint|Qt.WindowMinMaxButtonsHint)
    window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    window.setContentsMargins(0, 0, 0, 0)
    build_grips(window)
    # set background gif
    widget = QLabel()
    qtwidgets.movie = movie = QMovie('./res/background.gif')
    widget.setMovie(movie)
    widget.setScaledContents(True)
    movie.start()
    # get the background accent color
    import colorthief
    qtwidgets.accent_color = colorthief.ColorThief('./res/background.gif').get_color(quality=1)
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
    
    LOGSPLASH('qtGUI: Finish: Build main window.')

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

    LOGSPLASH('qtGUI: Finish: Build scale grips.')

def build_main_layout(widget: QWidget, layout: QBoxLayout):
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    widget.setStyleSheet(f"""
        QWidget {{
            background-color: rgba(0, 0, 0, 127);        
        }}         
        QToolButton {{
            min-height: 30;
        }}
        QToolButton:hover {{ 
            background-color: rgb{qtwidgets.accent_color}; 
        }}
        QToolButton:checked {{ 
            background-color: rgb{qtwidgets.accent_color}; 
        }}
    """)
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
    
    LOGSPLASH('qtGUI: Finish: Build main layout.')

def build_title_bar(widget: QWidget, layout: QBoxLayout):
    widget.setMinimumHeight(30)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    # icon
    pixmap = QPixmap('./res/titlebaricon.png').scaled(118, 40, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
    icon_label = QLabel(pixmap=pixmap)
    layout.addWidget(icon_label, stretch=4)

    # icon
    qtwidgets.title_label = title_label = QLabel('LtMAO-hai')
    layout.addWidget(title_label, stretch=80)

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
    layout.addWidget(min_button, stretch=4)
    
    qtwidgets.nor_button = nor_button = QToolButton()
    nor_button.setText('🟡 Restore')
    nor_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    nor_button.clicked.connect(qtwidgets.main_window.showNormal)
    layout.addWidget(nor_button, stretch=4)

    qtwidgets.max_button = max_button = QToolButton()
    max_button.setText('🔵 Maximize')
    max_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    max_button.setVisible(False)
    max_button.clicked.connect(qtwidgets.main_window.showMaximized)
    layout.addWidget(max_button, stretch=4)
    
    close_button = QToolButton()
    close_button.setText('🔴 Close')
    close_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
    close_button.clicked.connect(qtwidgets.main_window.close)
    layout.addWidget(close_button, stretch=4)

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

    LOGSPLASH('qtGUI: Finish: Build title bar.')
    
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

    LOGSPLASH('qtGUI: Finish: Build mid content.')
    
def build_status_bar(widget: QWidget, layout: QBoxLayout):
    widget.setMinimumHeight(30)
    widget.setStyleSheet(f'QStatusBar:hover {{ background-color: rgb{qtwidgets.accent_color}; }}')
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)
    
    qtwidgets.statusbar = statusbar = QStatusBar(sizeGripEnabled=False)
    content_widget = QWidget()
    content_widget.setVisible(False)
    qtwidgets.content_layout.addWidget(content_widget, stretch=99)
    c = control.Control('', 100, lambda widget: control.build_logbox(widget))
    c.widget = statusbar
    c.accent_color = qtwidgets.accent_color
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

    LOGSPLASH('qtGUI: Finish: Build status bar.')

def after_build():
    LOG('qtGUI: Finish: Build main window.')
    check_version()
    sync_changelog()
    setting.prepare(LOG)
    control.on_page_id_changed(True, setting.get('qtGUI.page_id', 0))
    hash_helper.prepare(LOG)
    winLT.prepare(LOG)
    tools.prepare(LOG)
    Ritoddstex.prepare(LOG)
    
 
def check_version():
    def check_version_thrd():
        try:
            # read offline
            local_file = './version'
            with open(local_file, 'r') as f:
                global VERSION
                VERSION = f.read()
            title = f'LtMAO-hai V{VERSION}'
            qtwidgets.title_label.setText(title)
            # read online
            remote_file = 'https://raw.githubusercontent.com/tarngaina/LtMAO/hai/version'
            get = requests.get(remote_file)
            get.raise_for_status()
            global NEW_VERSION
            NEW_VERSION = get.text
            if VERSION != NEW_VERSION:
                title += f' - New version found: {NEW_VERSION}, redownload LtMAO to update.'
            qtwidgets.title_label.setText(title)
        except Exception as e:
            LOG(f'qtGUI: check_version: Error: {str(e)}')
    helper.SafeThread.start('check_version', check_version_thrd)
    LOG('qtGUI: Finish: Check version.')

def sync_changelog():
    def sync_changelog_thrd():
        full_changelog_text = ''
        local_file = './pref/changelog.txt'
        try:
            page = 1
            while True:
                url=f'https://api.github.com/repos/tarngaina/ltmao/commits?sha=hai&per_page=100&page={page}'
                commits=requests.get(url).json()
                if len(commits) > 0:
                    for commit in commits:
                        commit = commit['commit']
                        author = commit['author']['name']
                        date = commit['author']['date']
                        message = commit['message']
                        full_changelog_text += f'[{date}] by {author}:\n{message}\n\n'
                else:
                    break
                page+=1
            with open(local_file, 'w+', encoding='utf-8') as f:
                f.write(full_changelog_text)

        except Exception as e:
            import os.path
            LOG(f'get_changelog: Error: {e}, switching to local file if exists.')
            if os.path.exists(local_file):
                with open(local_file, 'r', encoding='utf-8') as f:
                    full_changelog_text = f.read()
            else:
                full_changelog_text = 'Error: Download changelog failed, no local changelog to read.'
        qtwidgets.changelog.insertPlainText(full_changelog_text)
        
        
    helper.SafeThread.start('sync_changelog', sync_changelog_thrd)
    LOG('qtGUI: Finish: Sync changelog.')

   