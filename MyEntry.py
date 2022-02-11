import tkinter


class MyEntry:
    def __init__(self, parent, label_text, entry_text='', label_width=8):
        self.frame = tkinter.Frame(parent)
        self.label = tkinter.Label(
            self.frame, text=label_text, width=label_width)
        self.label.pack(side=tkinter.LEFT)
        self.entry = tkinter.Entry(self.frame)
        self.entry.insert(0, entry_text)
        self.entry.pack(side=tkinter.LEFT)
        self.frame.pack(side=tkinter.TOP)

    def get_entry(self):
        return self.entry
