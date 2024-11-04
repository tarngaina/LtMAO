import sys

from PySide6 import QtCore, QtWidgets, QtGui

class RoundPixmapStyle(QtWidgets.QProxyStyle):
    def __init__(self, radius=10, *args, **kwargs):
        super(RoundPixmapStyle, self).__init__(*args, **kwargs)
        self._radius = radius

    def drawItemPixmap(self, painter, rectangle, alignment, pixmap):
        painter.save()
        pix = QtGui.QPixmap(pixmap.size())
        pix.fill(QtCore.Qt.transparent)
        p = QtGui.QPainter(pix)
        p.setBrush(QtGui.QBrush(pixmap))
        p.setPen(QtCore.Qt.NoPen)
        p.drawRoundedRect(pixmap.rect(), self._radius, self._radius)
        p.end()
        super(RoundPixmapStyle, self).drawItemPixmap(painter, rectangle, alignment, pix)
        painter.restore()


def create_qt_ui():
    app = QtWidgets.QApplication(sys.argv)
    app.setWindowIcon(QtGui.QIcon('./resources/qtGUI/app.ico'))
    # main window
    main_window = QtWidgets.QMainWindow()
    main_window.setGeometry(35, 35, 1080, 660)
    main_window.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    main_window.setAttribute(QtCore.Qt.WA_TranslucentBackground)
    from BlurWindow.blurWindow import blur
    blur(main_window.winId())   
    
    # central widget
    central_widget = QtWidgets.QWidget()
    central_layout = QtWidgets.QVBoxLayout()
    central_layout.setContentsMargins(0, 0, 0, 0)
    central_layout.setSpacing(0)

    # top widget
    top_widget = QtWidgets.QLabel()
    top_widget.setStyleSheet('background-color: palette(base); border-radius: 5px;')
    top_widget.setMaximumHeight(40)
    top_widget.setScaledContents(True)
    top_layout = QtWidgets.QHBoxLayout()
    top_layout.setContentsMargins(0, 0, 0, 0)
    top_widget.setLayout(top_layout)
    
    proxy_style = RoundPixmapStyle(10, top_widget.style())
    top_widget.setStyle(proxy_style)
    movie = QtGui.QMovie('./resources/qtGUI/title_bar.gif')
    top_widget.setMovie(movie)
    movie.start()
    central_layout.addWidget(top_widget, stretch=0)# alignment=QtCore.Qt.AlignmentFlag.AlignTop)
    # title label
    title_label = QtWidgets.QLabel(text='LtMAO')
    top_layout.addWidget(title_label, stretch=1, alignment=QtCore.Qt.AlignmentFlag.AlignCenter)
    # minimize button
    minimize_button = QtWidgets.QPushButton(text='➖')
    minimize_button.setToolTip('Minimize LtMAO gui.')
    minimize_button.setMaximumSize(40, 40)
    minimize_button.setStyleSheet('background-color: transparent;')
    minimize_button.setFlat(True)
    minimize_button.clicked.connect(lambda: main_window.showMinimized())
    top_layout.addWidget(minimize_button, stretch=0, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
    # close button
    close_button = QtWidgets.QPushButton(text='❌')
    close_button.setToolTip('Close LtMAO gui.')
    close_button.setMaximumSize(40, 40)
    close_button.setStyleSheet('background-color: transparent;')
    close_button.setFlat(True)
    top_layout.addWidget(close_button, stretch=0, alignment=QtCore.Qt.AlignmentFlag.AlignRight)
    close_button.clicked.connect(lambda: main_window.close())

    # mid widget
    mid_widget = QtWidgets.QWidget()
    mid_widget.setStyleSheet('background-color: palette(base); border-image: url(./resources/qtGUI/main.jpg) 0 0 0 0 stretch stretch;')
    opacity_effect = QtWidgets.QGraphicsOpacityEffect()
    opacity_effect.opacity = 0.66
    mid_widget.setGraphicsEffect(opacity_effect)
    #mid_widget.setStyleSheet('background-color: transparent')
    mid_layout = QtWidgets.QGridLayout()
    mid_widget.setLayout(mid_layout)
    central_layout.addWidget(mid_widget, stretch=1)
    # test test
    test = QtWidgets.QLabel('Mid content')
    mid_layout.addWidget(test, 0, 0, 1, 1)
    
    # bot widget
    bot_widget = QtWidgets.QWidget()
    bot_widget.setStyleSheet('background-color: palette(base);')
    bot_layout = QtWidgets.QGridLayout()
    bot_layout.setContentsMargins(0, 0, 0, 0)
    bot_widget.setLayout(bot_layout)
    central_layout.addWidget(bot_widget, stretch=0, alignment=QtCore.Qt.AlignmentFlag.AlignBottom )
    # log
    log_label = QtWidgets.QLabel('This is a log message')
    bot_layout.addWidget(log_label, 0, 0, 1, 1)
    # run app
    central_widget.setLayout(central_layout)
    main_window.setCentralWidget(central_widget)
    main_window.show()
    app.exec()


def show():
    create_qt_ui()
    