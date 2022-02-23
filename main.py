
import tkinter
import json
from MyEntry import MyEntry
from Schedule import Schedule
from params import *
from tools import *


class MenuOption:
    def __init__(self, labeltext, fun):
        new_win = tkinter.Toplevel()
        new_win.geometry('200x100')
        e = MyEntry(new_win, labeltext)

        def fnc():
            text = e.get_entry().get()
            new_win.destroy()
            fun(text)

        tkinter.Button(new_win, text='OK', command=fnc).pack()


class Rec:
    _fnc_position = None
    _rectangles = []

    def __init__(self, cvs, **kwargs):
        self.cvs = cvs
        self.__dict__.update(**{**SIG, **kwargs})
        self._create_widgets()
        # cvs.tag_bind(f'movable-{self.rec}', '<1>', lambda e: self.cvs.focus(self.rec))
        self._set_tags()
        Rec._rectangles.append(self)
        self._adjust_position()

    def _create_widgets(self):
        self.rec = self.cvs.create_rectangle(
            self.x0, self.y0, self.x0 + self.width, self.y0 + self.height, fill=self.color)
        self.cvs.itemconfig(self.rec, tags=(f'movable-{self.rec}'))

        self.text = self.cvs.create_text(
            self.x0 + self.width / 2, self.y0 + ROW_HEIGHT / 2, text=self.content, anchor='c')
        self.cvs.itemconfig(self.text, tags=(f'movable-{self.text}'))

    def _set_tags(self):
        widgets = [
            f'movable-{self.rec}',
            f'movable-{self.text}',
        ]
        events = [
            ['<3>', lambda e: self._menu(e)],
            ['<ButtonRelease>', lambda e: self._adjust_position()],
            ['<Control-Button-1>', lambda e: self._delete()],
            ['<B1-Motion>', lambda e: self._move(e)],
        ]

        for w in widgets:
            for e, f in events:
                self.cvs.tag_bind(w, e, f)

    def _move_center_to(self, x, y):
        self.x0 = x - round(self.width / 2)
        self.y0 = y - round(self.height / 2)
        self.cvs.moveto(self.rec, self.x0, self.y0)
        self.cvs.moveto(self.text, x - self.width / 6, y - self.height / 6)

    def _to_string(self):
        d = self._get_kwargs()
        print('_to_string:', d)
        return json.dumps(d)

    def _adjust_position(self):
        if Rec._fnc_position:
            Rec._fnc_position(self)

    def _move(self, e):
        self._move_center_to(e.x, e.y)
        self.cvs.lift(self.rec)
        self.cvs.lift(self.text)

    def _delete(self):
        # print(Rec._rectangles)
        Rec._rectangles.remove(self)
        self.cvs.after(0, self.cvs.delete, self.rec)
        self.cvs.after(0, self.cvs.delete, self.text)

    def _menu(self, e):
        m = tkinter.Menu(self.cvs, tearoff=0)

        def text_func(a):
            self.cvs.itemconfig(self.text, text=a)
            self.content = a

        def from_func(a):
            x0 = SCHEDULE_START[0] + \
                (string_to_hours(a) - START_TIME) * COL_WIDTH
            delta = x0 - self.x0
            self.move_delta(delta, 0)

        def duration_func(a):
            self.duration = a
            self.cvs.coords(self.rec, self.x0, self.y0,
                            self.x0 + self.width, self.y0 + self.height)

        def color_func(a):
            self.cvs.itemconfig(self.rec, fill=a)
            self.color = a

        m.add_command(label='text',
                      command=lambda: MenuOption('text', text_func))
        m.add_command(label='from',
                      command=lambda: MenuOption('from', from_func))
        m.add_command(label='duration',
                      command=lambda: MenuOption('duration', duration_func))
        m.add_command(label='color',
                      command=lambda: MenuOption('color', color_func))
        m.tk_popup(e.x_root, e.y_root)

    def _get_kwargs(self):
        x = {key: value for key, value in self.__dict__.items() if not key.startswith('__')
             and not callable(key)}
        if 'cvs' in x:
            x.pop('cvs')
        return x

    @ property
    def width(self):
        return int(self.duration) / 60 * COL_WIDTH

    @ property
    def height(self):
        return ROW_HEIGHT

    def coords(self):
        return self.cvs.coords(self.rec)

    def move_delta(self, x, y):
        self.x0 += x
        self.y0 += y
        self.cvs.move(self.rec, x, y)
        self.cvs.move(self.text, x, y)

    @ classmethod
    def set_adjust_position(cls, fnc):
        cls._fnc_position = fnc

    @ classmethod
    def all_to_string(cls):
        # Return string from which the rectangles can be again built from.
        text = ''
        for i in Rec._rectangles:
            text += i._to_string() + ';'
        text = text[:-1]
        return text

    @ classmethod
    def build_from_text(cls, cvs, text):
        s = text.split(';')
        for i in s:
            d = json.loads(i)
            Rec(cvs, **d)


if __name__ == '__main__':
    root = tkinter.Tk()
    root.geometry(f'{CANVAS_WIDTH}x{CANVAS_HEIGHT}')
    root.resizable(False, False)

    Rec.set_adjust_position(adjust_position_horizontally)

    with open(FILE_NAME, 'a', encoding='utf-8') as f:
        pass

    schedule = Schedule(root)

    with open(FILE_NAME, 'r', encoding='utf-8') as f:
        text = f.read()
        if text != '':
            Rec.build_from_text(schedule.cvs, text)

    root.protocol('WM_DELETE_WINDOW', root.destroy)

    schedule.set_orange_rec(lambda e: Rec(schedule.cvs))

    root.mainloop()

    with open(FILE_NAME, 'w+', encoding='utf-8') as f:
        f.write(Rec.all_to_string())
