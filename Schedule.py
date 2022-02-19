import tkinter
from params import *


class Schedule:
    def __init__(self, parent):
        self.parent = parent
        self.cvs = tkinter.Canvas(
            parent, width=CANVAS_WIDTH, height=400, bg='gray')
        self.cvs.pack()
        self.draw_schedule()
        self.cvs.create_rectangle(
            10, 360, 70, 330, fill='orange', tags=('new'))

    def draw_schedule(self):
        for i in range(ROWS + 1):
            # Horizontal lines
            self.cvs.create_line(SCHEDULE_START[0],
                                 SCHEDULE_START[1] + i * ROW_HEIGHT,
                                 SCHEDULE_END[0],
                                 SCHEDULE_START[1] + i * ROW_HEIGHT)

        for i in range(COLS + 1):
            # Vertical lines
            self.cvs.create_line(SCHEDULE_START[0] + i * COL_WIDTH,
                                 SCHEDULE_START[1],
                                 SCHEDULE_START[0] + i * COL_WIDTH,
                                 SCHEDULE_END[1])
        for i in range(COLS + 1):
            # Time labels
            l = tkinter.Label(
                self.parent, text=f'{i + START_TIME}:00', bg='gray')
            self.cvs.create_window(
                SCHEDULE_START[0] + i * COL_WIDTH, SCHEDULE_START[1] - 20, window=l)

    def set_orange_rec(self, fnc):
        self.cvs.tag_bind('new', '<1>', fnc)
