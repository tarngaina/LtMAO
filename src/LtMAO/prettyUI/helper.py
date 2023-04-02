from threading import Thread
from time import sleep
from datetime import datetime


def now():
    return datetime.now().strftime('%H:%M:%S.%f')[:-3]


class Keeper:
    def __init__(self):
        pass


class Log:
    messages = []
    minilog_label = None

    @staticmethod
    def add(text):
        messages = text.split('\n')
        if len(messages) > 0:
            Log.messages.extend(f'[{now()}] {msg}' for msg in messages)
            if Log.minilog_label != None:
                Log.minilog_label.configure(text=Log.messages[-1])
                Log.minilog_label.update_idletasks()
            if len(Log.messages) > 1000:
                Log.messages = Log.messages[-1000:]
