from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtCore import Qt

import f3d
import os.path
from .. import lepath
from ..lemon3d import lemon_fbx

infinityQT_dir = './pref/infinityQT'

def create_widget(skn_path):
    # convert skn to fbx
    fbx_path = lepath.join(infinityQT_dir, lepath.ext(os.path.basename(skn_path), '.skn', '.fbx'))
    lemon_fbx.skin_to_fbx(None, skn_path, None, fbx_path)

    # create glwidget embed f3d inside
    gl_widget = QOpenGLWidget()
    gl_widget.initializeGL()
    engine = engine = f3d.Engine.create_external_wgl()
    engine.window.width = 300
    engine.window.height = 300
    engine.scene.add(fbx_path)
    gl_widget.paintGL = engine.window.render
  
    # resize
    def resizeEvent(event):
        size = event.size()
        engine.window.width, engine.window.height = size.width(), size.height()
    gl_widget.resizeEvent = resizeEvent
    
    # mouse interact - pan rotate zoom camera
    gl_widget.is_pan = False
    gl_widget.is_rotate = False
    gl_widget.is_zoom = False
    gl_widget.pan_speed = 5.0
    gl_widget.rotate_speed = 1.5
    gl_widget.zoom_speed = 0.025
    def mousePressEvent(event):
        if event.button() == Qt.MouseButton.MiddleButton:
            gl_widget.last_pos = event.position()
            gl_widget.is_pan = True
        if event.button() == Qt.MouseButton.LeftButton:
            gl_widget.last_pos = event.position()
            gl_widget.is_rotate = True
        if event.button() == Qt.MouseButton.RightButton:
            gl_widget.last_pos = event.position()
            gl_widget.is_zoom = True
    gl_widget.mousePressEvent = mousePressEvent
    def mouseReleaseEvent(event):
        if event.button() == Qt.MouseButton.MiddleButton:
            gl_widget.is_pan = False
        if event.button() == Qt.MouseButton.LeftButton:
            gl_widget.is_rotate = False
        if event.button() == Qt.MouseButton.RightButton:
            gl_widget.is_zoom = False
    gl_widget.mouseReleaseEvent = mouseReleaseEvent
    def mouseMoveEvent(event):
        if gl_widget.is_pan or gl_widget.is_rotate or gl_widget.is_zoom:
            cur_pos = event.position()
            if cur_pos != gl_widget.last_pos:
                # calculate distance
                x_offset = cur_pos.x() - gl_widget.last_pos.x()
                y_offset = cur_pos.y() - gl_widget.last_pos.y()
                x_distance = x_offset * x_offset
                y_distance = y_offset * y_offset
                sum_distance = x_distance + y_distance
                # calculate normalized x, y 
                x_normalized = x_distance / sum_distance
                y_normalized = y_distance / sum_distance
                # get original x, y direction
                x_direction = -1 if x_offset < 0 else 1
                y_direction = -1 if y_offset < 0 else 1
                # pan
                if gl_widget.is_pan:
                    engine.window.camera.pan(
                        x_normalized * -x_direction * gl_widget.pan_speed,
                        y_normalized * y_direction * gl_widget.pan_speed
                    )
                    gl_widget.update()
                if gl_widget.is_rotate:
                    engine.window.camera.azimuth(
                        x_normalized * -x_direction * gl_widget.rotate_speed,
                    )
                    engine.window.camera.elevation(
                        y_normalized * y_direction * gl_widget.rotate_speed
                    )
                    gl_widget.update()
                if gl_widget.is_zoom:
                    engine.window.camera.dolly(1.0 + y_normalized * y_direction * gl_widget.zoom_speed)
                    gl_widget.update()
                gl_widget.last_pos = cur_pos
    gl_widget.mouseMoveEvent = mouseMoveEvent

    return gl_widget