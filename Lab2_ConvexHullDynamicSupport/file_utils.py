from enum import Enum

from Lab2_ConvexHullDynamicSupport.point import Point


class OperationType(Enum):
    INSERT = 1
    DELETE = 2


def points_from_file(path):
    points_queue = []

    with open(path) as file:
        while line := file.readline().strip():
            point_tokens = line.split(sep=" ")
            operation_type = OperationType.DELETE if point_tokens[0] == "d" else OperationType.INSERT

            to_delete = operation_type == OperationType.DELETE
            points_queue.append([operation_type, Point(float(point_tokens[1]), float(point_tokens[2]), to_delete)])

    return points_queue
