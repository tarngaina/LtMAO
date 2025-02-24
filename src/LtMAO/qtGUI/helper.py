from threading import Thread

class Keeper:
    def __init__(self):
        pass

class SafeThread:
    cached = {}
    log = print

    @staticmethod
    def check_safe(thread):
        if thread == None:
            return True
        else:
            if not thread.is_alive():
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
                    SafeThread.log(traceback.format_exc())
            SafeThread.cached[thread_name] = Thread(target=cmd, daemon=True)
            SafeThread.cached[thread_name].start()
        else:
            SafeThread.log(
                f'{thread_name}: Error: Thread is already running, wait for it to end.')
