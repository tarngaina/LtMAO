from datetime import datetime
from customtkinter import CTkImage
from PIL import Image, ImageDraw, ImageFont


def now():
    return datetime.now().strftime('%H:%M:%S.%f')[:-3]


class Keeper:
    def __init__(self):
        pass


class Log:
    limit = 1000
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


class EmojiImage:
    font_file = './resources/emojifont.ttf'
    cache = {}

    @staticmethod
    def create(emoji, size=24, weird=False):
        if emoji in EmojiImage.cache:
            return EmojiImage.cache[emoji]
        # convert emoji to CTkImage
        font = ImageFont.truetype(EmojiImage.font_file, size=int(size/1.5))
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        # fix weird coordinate problem
        draw.text((size if weird else size/2, size/2), emoji,
                  embedded_color=True, font=font, anchor='mm', align='center')
        img = CTkImage(img, size=(size, size))
        EmojiImage.cache[emoji] = img
        return img
