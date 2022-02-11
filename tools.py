from params import *


def get_middle_point(rec):
    x = (rec[0] + rec[2]) / 2
    y = (rec[1] + rec[3]) / 2
    return (x, y)


def point_in_rec(p, rec):
    if p[0] > rec[0] and p[0] < rec[2] and p[1] > rec[1] and p[1] < rec[3]:
        return True
    return False


def adjust_position(obj):
    coords = obj.coords()
    middle_point = get_middle_point(coords)
    if not point_in_rec(middle_point, SCHEDULE):
        return
    col = (middle_point[0] - SCHEDULE_START[0]) % COL_WIDTH
    row = (middle_point[1] - SCHEDULE_START[1]) % ROW_HEIGHT
    obj.move_delta(-col + COL_WIDTH / 2, -row + ROW_HEIGHT / 2)


def adjust_position_horizontally(obj):
    coords = obj.coords()
    middle_point = get_middle_point(coords)
    if not point_in_rec(middle_point, SCHEDULE):
        return
    # col = (middle_point[0] - SCHEDULE_START[0]) % COL_WIDTH
    row = (middle_point[1] - SCHEDULE_START[1]) % ROW_HEIGHT
    obj.move_delta(0, -row + ROW_HEIGHT / 2)
