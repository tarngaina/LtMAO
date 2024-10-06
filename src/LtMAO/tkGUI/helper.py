from datetime import datetime
from customtkinter import CTkImage
from PIL import Image, ImageDraw, ImageFont, ImageTk
from traceback import format_exc
from threading import Thread

class Keeper:
    def __init__(self):
        pass


class SmartThread:
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
        if thread_name not in SmartThread.cached:
            SmartThread.cached[thread_name] = None
        if SmartThread.check_safe(SmartThread.cached[thread_name]):
            def cmd():
                try:
                    target()
                except:
                    SmartThread.log(format_exc())
            SmartThread.cached[thread_name] = Thread(target=cmd, daemon=True)
            SmartThread.cached[thread_name].start()
        else:
            SmartThread.log(
                f'{thread_name}: Failed: A thread is already running, wait for it to finished.')

class EmojiImage:
    font_file = './resources/emojifont.ttf'
    cache = {}

    @staticmethod
    def create(emoji, size=24, weird=False, return_ctk=True):
        if emoji in EmojiImage.cache:
            if return_ctk:
                return EmojiImage.cache[emoji]
            else:
                return ImageTk.PhotoImage(EmojiImage.cache[emoji].cget('light_image'))
        # convert emoji to CTkImage
        font = ImageFont.truetype(EmojiImage.font_file, size=int(size/1.5))
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # fix weird coordinate problem
        draw.text((size if weird else size/2, size/2), emoji,
                  embedded_color=True, font=font, anchor='mm', align='center')
        img = CTkImage(img, size=(size, size))
        EmojiImage.cache[emoji] = img
        if return_ctk:
            return img
        else:
            return ImageTk.PhotoImage(EmojiImage.cache[emoji].cget('light_image'))

class Log:
    limit = 1000
    messages = []
    tk_minilog = None
    tk_log = None

    tk_lines = 0
    tk_cooldown = 0
    tk_enable = True
    cd_messages = []

    @staticmethod
    def block_tk():
        Log.tk_enable = False

    @staticmethod
    def free_tk():
        Log.tk_enable = True

    @staticmethod
    def add(text):
        if Log.tk_minilog == None or Log.tk_log == None:
            print(text)
            return
        # parsing text
        if isinstance(text, list):
            text = ''.join(text)
        messages = text.split('\n')
        if len(messages) == 0:
            return
        if messages[-1] == '':
            messages = messages[:-1]
        # add message to Log.messages
        timed_messages = [
            f'[{datetime.now().time()}] {msg}' for msg in messages]
        Log.messages.extend(timed_messages)
        over_limit = len(Log.messages) - Log.limit
        if over_limit > 0:
            Log.messages = Log.messages[over_limit:]
        # handle tkinter relate stuff
        if Log.tk_cooldown == 0:
            # realtime mode -> drag perfomance down
            Log.tk_log.configure(state='normal')
            # update left over messages from delay modes
            if len(Log.cd_messages) > 0:
                Log.tk_log.insert('end', '\n'.join(Log.cd_messages)+'\n')
                Log.tk_lines += len(Log.cd_messages)
                Log.cd_messages.clear()
            Log.tk_log.insert('end', '\n'.join(timed_messages)+'\n')
            Log.tk_lines += len(timed_messages)
            over_limit = Log.tk_lines - Log.limit
            if over_limit > 0:
                Log.tk_log.delete('1.0', f'{over_limit}.0')
                Log.tk_lines -= over_limit
            Log.tk_log.configure(state='disabled')
            Log.tk_log.see('end')
            Log.tk_minilog.configure(text=Log.messages[-1])
        else:
            # delay mode -> drag perfomance down but not much
            # delay mode doesnt update all delay messages
            # -> so it need realtime mode to update the left over
            Log.cd_messages.extend(timed_messages)
            if Log.tk_enable:
                Log.block_tk()
                Log.tk_log.configure(state='normal')
                Log.tk_log.insert('end', '\n'.join(Log.cd_messages)+'\n')
                Log.tk_lines += len(Log.cd_messages)
                over_limit = Log.tk_lines - Log.limit
                if over_limit > 0:
                    Log.tk_log.delete('1.0', f'{over_limit}.0')
                    Log.tk_lines -= over_limit
                Log.tk_log.configure(state='disabled')
                Log.tk_log.see('end')
                Log.tk_minilog.configure(text=Log.cd_messages[-1])
                Log.cd_messages.clear()
                Log.tk_minilog.after(Log.tk_cooldown, Log.free_tk)
