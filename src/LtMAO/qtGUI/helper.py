class Keeper:
    def __init__(self):
        pass

from threading import Thread

class SafeThread:
    cached = {}
    
    @staticmethod
    def check_safe(thread):
        if thread == None:
            return True
        return False
    
    @staticmethod
    def start(thread_name, target):
        if thread_name not in SafeThread.cached:
            SafeThread.cached[thread_name] = None
        if SafeThread.check_safe(SafeThread.cached[thread_name]):
            def cmd():
                try:
                    target()
                except:
                    import traceback
                    print(traceback.format_exc())
                SafeThread.cached[thread_name] = None
            SafeThread.cached[thread_name] = Thread(target=cmd, daemon=True)
            SafeThread.cached[thread_name].start()
        else:
            print(f'{thread_name}: Error: Thread is already running, wait for it to end.')


def link_dnd_cmd(widget, dnd_cmd):
    def dragEvent(e):
        if e.mimeData().hasUrls:
            e.accept()
        else:
            e.ignore()

    def dropEvent(e):
        if e.mimeData().hasUrls:
            dnd_cmd([url.toLocalFile() for url in e.mimeData().urls()])
            e.accept()
        else:
            e.ignore()

    widget.setAcceptDrops(True)
    widget.dragEnterEvent = dragEvent
    widget.dragMoveEvent = dragEvent
    widget.dropEvent = dropEvent