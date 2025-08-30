from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap
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
    # create widget
    return QLabel(pixmap=QPixmap(png_path), alignment=Qt.AlignmentFlag.AlignCenter)
