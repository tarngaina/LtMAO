from threading import Thread
from time import sleep


class Keeper:
    def __init__(self):
        pass


class Log:
    messages = []
    minilog_label = None

    @staticmethod
    def add(text):
        messages = text.split('\n')
        Log.messages.extend(msg for msg in text)
        if Log.minilog_label != None:
            Log.minilog_label.configure(text=Log.messages[-1])


class ProgressBar:
    progress_bar = None
    show_cmd = None
    hide_cmd = None

    @staticmethod
    def show():
        if ProgressBar.progress_bar != None:
            ProgressBar.show_cmd()

    @staticmethod
    def hide():
        if ProgressBar.progress_bar != None:
            ProgressBar.hide_cmd()

    @staticmethod
    def set(value):
        if ProgressBar.progress_bar != None:
            ProgressBar.progress_bar.set(value)
