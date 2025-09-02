from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QToolButton, QSlider
from PySide6.QtCore import Qt

import os.path, wave, pyaudio, threading
from .. import lepath, tools

infinityQT_dir = './pref/infinityQT'

port = None

def init():
    global port
    if port == None:
        port = pyaudio.PyAudio()

def play_audio(wav_data, sampwidth, nchannels, framerate, nframes, label, slider):
    def play_thrd():
        if port == None:
            return
        stream = port.open(
            format=port.get_format_from_width(sampwidth),
            channels=nchannels,
            rate=framerate,
            output=True
        )
        frame_current = 0
        label.setText(f'{frame_current/framerate:02.2f}/{nframes/framerate:02.2f}')
        slider.setValue(0)
        while frame_current < nframes:
            frame_next = frame_current + 1024
            if frame_next > nframes:
                frame_next = nframes
            stream.write(wav_data[frame_current:frame_next])
            frame_current = frame_next
            label.setText(f'{frame_current/framerate:02.2f}/{nframes/framerate:02.2f}')
            slider.setValue(frame_current)
        stream.close()
    threading.Thread(target=play_thrd, daemon=True).start()

def create_widget(wem_path):
    # convert wem to wav
    wav_path = lepath.join(infinityQT_dir, lepath.ext(os.path.basename(wem_path), '.wem', '.wav'))
    tools.VGMStream.to_wav(wem_path, wav_path)
    # get info & data
    with wave.open(wav_path, 'rb') as wav:
        param = wav.getparams()
        data = wav.readframes(param.nframes)
    # create widget and layout
    widget = QWidget()
    layout = QVBoxLayout()
    widget.setLayout(layout)
    layout2 = QHBoxLayout()
    layout.addLayout(layout2)
    layout.addStretch()
    # play
    play_button = QToolButton()
    play_button.setText('▶️')
    layout2.addWidget(play_button)
    # duration
    label = QLabel()
    label.setText(f'{0}/{param.nframes/param.framerate:02.2f}') 
    layout2.addWidget(label)
    # slider
    slider = QSlider()
    slider.setOrientation(Qt.Orientation.Horizontal)
    slider.setRange(0, param.nframes)
    slider.setValue(0)
    layout2.addWidget(slider)
    # bind command
    def play_cmd():
        init()
        play_audio(data, param.sampwidth, param.nchannels, param.framerate, param.nframes, label, slider)
    play_button.clicked.connect(play_cmd)
    return widget
