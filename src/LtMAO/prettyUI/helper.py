from datetime import datetime


def now():
    return datetime.now().strftime('%H:%M:%S.%f')[:-3]


class Keeper:
    def __init__(self):
        pass


class Log:
    limit = 1000
    cooldown = 1000
    messages = []
    tk_minilog = None
    tk_log = None

    @staticmethod
    def add(text):
        if isinstance(text, list):
            text = ''.join(text)
        messages = text.split('\n')
        while '' in messages:
            messages.remove('')
        if len(messages) > 0:
            for msg in messages:
                # delete first line if reach limit
                if len(Log.messages) > Log.limit:
                    Log.messages.pop(0)
                    if Log.tk_log != None:
                        Log.tk_log.configure(state='normal')
                        Log.tk_log.delete('1.0', '2.0')
                        Log.tk_log.configure(state='disabled')

                # add messages to log
                timed_msg = f'[{now()}] {msg}'
                Log.messages.append(timed_msg)

                # update UI log
                if Log.tk_log != None:
                    Log.tk_log.configure(state='normal')
                    Log.tk_log.insert('end', timed_msg+'\n')
                    Log.tk_log.configure(state='disabled')
                    Log.tk_log.see('end')

                # update UI minilog
                if Log.tk_minilog != None:
                    Log.tk_minilog.configure(text=Log.messages[-1])
