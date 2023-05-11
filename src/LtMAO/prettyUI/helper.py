from datetime import datetime
from customtkinter import CTkImage
from PIL import Image, ImageDraw, ImageFont


class Keeper:
    def __init__(self):
        pass

# profile


def db(func):
    from cProfile import Profile
    from pstats import Stats
    pr = Profile()
    pr.enable()

    func()

    pr.disable()
    stats = Stats(pr)
    stats.sort_stats('tottime').print_stats(20)


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
        # add message to Log.messages
        timed_messages = [
            f'[{str(datetime.now()).split(" ")[1][:-3]}] {msg}' for msg in messages]
        Log.messages.extend(timed_messages)
        while len(Log.messages) > Log.limit:
            Log.messages.pop(0)
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
