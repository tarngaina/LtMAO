from PySide6.QtWidgets import QWidget, QVBoxLayout, QSlider, QGraphicsScene, QGraphicsItemGroup, QGraphicsPixmapItem, QGraphicsView
from PySide6.QtGui import QPixmap, QTransform
from PySide6.QtCore import Qt

import os.path
from .. import lepath, Ritoddstex, tools

infinityQT_dir = './pref/infinityQT'

def create_widget(tex_path):
    # convert tex to dds to png
    dds_path = lepath.join(infinityQT_dir, lepath.ext(os.path.basename(tex_path), '.tex', '.dds'))
    Ritoddstex.tex2dds(tex_path, dds_path)
    png_path = lepath.ext(dds_path, '.dds', '.png')
    tools.ImageMagick.to_png(dds_path, png_path)
    # create pixmap + graphic view
    pixmap = QPixmap(png_path)
    graphic_scene = QGraphicsScene()
    graphic_pixmap = QGraphicsPixmapItem(pixmap)
    graphic_pixmap.setTransform(QTransform().translate(-0.5 * pixmap.width(), -0.5 * pixmap.height()))
    graphic_group = QGraphicsItemGroup()
    graphic_group.addToGroup(graphic_pixmap)
    graphic_scene.addItem(graphic_group)
    graphic_view = QGraphicsView()
    graphic_view.setScene(graphic_scene)
    # create widget
    widget = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(graphic_view, stretch=1)
    slider = QSlider()
    slider.setOrientation(Qt.Orientation.Horizontal)
    layout.addWidget(slider)
    # to scale img
    def scale_img(value):
        exp = value * 0.01
        scale = pow(10.0, exp)
        graphic_group.setTransform(QTransform().scale(scale, scale))
    slider.valueChanged.connect(scale_img)
    widget.setLayout(layout)
    return widget
