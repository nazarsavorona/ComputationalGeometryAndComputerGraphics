from enum import Enum


class PointClass(Enum):
    CONVEX = 1  # REFLEX
    CONCAVE = 2  # CONCAVE
    SUPPORTING = 3  # SUPPORTING
    ERROR = -1


class Point:
    i = 1

    def __init__(self, x_, y_, to_delete=False):
        self.x = x_
        self.y = y_

        if not to_delete:
            self.id = Point.i
            Point.i += 1

    def __repr__(self):
        return str(f"({self.x}; {self.y})")

    def __lt__(self, other):
        return self.x < other.x or (self.x == other.x and self.y < other.y)


def get_intersect_point(a, b, c, d):
    return Point(((a.x * b.y - a.y * b.x) * (c.x - d.x) - (a.x - b.x) * (c.x * d.y - c.y * d.x))
                 / ((a.x - b.x) * (c.y - d.y) - (a.y - b.y) * (c.x - d.x)),
                 ((a.x * b.y - a.y * b.x) * (c.y - d.y) - (a.y - b.y) * (c.x * d.y - c.y * d.x))
                 / ((a.x - b.x) * (c.y - d.y) - (a.y - b.y) * (c.x - d.x)))


def define_point_type_left(q1_pred: Point, q1: Point, q1_suc: Point, q2: Point):
    if is_left(q2, q1, q1_pred) and is_left(q2, q1, q1_suc):
        return PointClass.SUPPORTING
    if is_left(q2, q1, q1_pred) and not is_left(q2, q1, q1_suc):
        return PointClass.CONCAVE
    else:
        return PointClass.CONVEX


def define_point_type_right(q2_pred: Point, q2: Point, q2_suc: Point, q1: Point):
    if not is_left(q1, q2, q2_pred) and not is_left(q1, q2, q2_suc):
        return PointClass.SUPPORTING
    if is_left(q1, q2, q2_pred) and not is_left(q1, q2, q2_suc):
        return PointClass.CONCAVE
    else:
        return PointClass.CONVEX


def is_left(chain_point_1, chain_point_2, point):
    return ((chain_point_2.x - chain_point_1.x) * (point.y - chain_point_1.y) - (chain_point_2.y - chain_point_1.y) * (
            point.x - chain_point_1.x)) >= 0
