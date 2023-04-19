from datetime import datetime


def now():
    return datetime.now().strftime('%H:%M:%S.%f')[:-3]


class Keeper:
    def __init__(self):
        pass


class Log:
    messages = []
    minilog_label = None
    log_textbox = None

    @staticmethod
    def add(text):

        if isinstance(text, list):
            text = ''.join(text)
        messages = text.split('\n')
        while '' in messages:
            messages.remove('')
        if len(messages) > 0:
            for msg in messages:
                # delete limit log
                if len(Log.messages) > 1000:
                    Log.messages = []
                    Log.log_textbox.configure(state='normal')
                    Log.log_textbox.delete('0.0', 'end')
                    Log.log_textbox.configure(state='disabled')

                timed_msg = f'[{now()}] {msg}'

                # add messages to log
                Log.messages.append(timed_msg)

                # update UI log
                if Log.log_textbox != None:
                    Log.log_textbox.configure(state='normal')
                    Log.log_textbox.insert('end', timed_msg+'\n')
                    Log.log_textbox.configure(state='disabled')
                    Log.log_textbox.see('end')

                # update UI minilog
                if Log.minilog_label != None:
                    Log.minilog_label.configure(text=Log.messages[-1])
                    Log.minilog_label.update_idletasks()
