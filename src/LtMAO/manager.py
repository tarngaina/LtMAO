class Keeper:
    def __init__(self):
        pass


class Log:
    messages = []
    single_label = None

    @staticmethod
    def add(message):
        Log.messages.append(message)
        if Log.single_label != None:
            Log.single_label.configure(text=message)
            Log.single_label.update_idletasks()
