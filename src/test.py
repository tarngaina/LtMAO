from PySide6.QtWidgets import QApplication
from PySide6.QtOpenGL import QOpenGLWindow

import f3d

app = QApplication()
window = QOpenGLWindow()
#window.setTitle('hello')
window.setGeometry(0, 0, 800, 600)

window.initializeGL()
engine = f3d.Engine.create_external_wgl()
engine.window.width = 800
engine.window.height = 600
engine.scene.add('D:/test/akali.fbx')
engine.window.camera.pitch(10)
window.paintGL = engine.window.render

window.show()
app.exec()