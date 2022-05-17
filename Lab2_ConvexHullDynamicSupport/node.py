from enum import Enum

import numpy

from Lab2_ConvexHullDynamicSupport.point import Point


class NodeColor(Enum):
    RED = 1
    BLACK = 2


class NodeSide(Enum):
    LEFT = 1
    RIGHT = 2
    ERROR = 3


class NodeData:
    def __init__(self, key=None):
        self.left_most_right: Node = None
        self.left_most_right_point: Point = key
        self.points_array = []
        self.separating_index = 0
        self.convex_hull = []
        self.graph_hull = []
        self.convex_hull.append(key)

    def __lt__(self, other):
        return self.left_most_right_point < other.left_most_right_point

    def __repr__(self):
        return str(f"{self.left_most_right_point}; {self.points_array}; {self.separating_index}")


class Node:
    i = 0

    def __init__(self, data):
        self.data: NodeData = data
        self.parent: Node = None
        self.left: Node = None
        self.right: Node = None
        self.color = NodeColor.RED
        self.id = Node.i
        Node.i += 1

    def __lt__(self, other):
        return self.data < other.data

    def __repr__(self):
        return str(f"{self.id}: {self.data}")

    def plot(self, fig, ax, TNULL, reverse=False):
        if self is None or self == TNULL:
            return fig, ax

        if self.left == TNULL:
            _x, _y, _id = self.data.left_most_right_point.x, self.data.left_most_right_point.y, \
                          self.data.left_most_right_point.id
            if reverse:
                _y *= -1
            ax.scatter([_x], [_y], color="blue")
            ax.annotate(f"{_id}: ({_x}; {_y})", (_x, _y), xytext=(_x - 0.025, _y + 0.1))
            return fig, ax

        chain = self.data.graph_hull
        if self.parent == TNULL:
            chain = self.data.points_array
        color = numpy.random.rand(3, )

        for i in range(1, len(chain)):
            if reverse:
                ax.plot([chain[i - 1].x, chain[i].x], [-1 * chain[i - 1].y, -1 * chain[i].y], color=color)
            else:
                ax.plot([chain[i - 1].x, chain[i].x], [chain[i - 1].y, chain[i].y], color=color)

        if self.left != TNULL:
            self.left.data.graph_hull = chain[:self.data.separating_index + 1] + self.left.data.points_array

        if self.right != TNULL:
            self.right.data.graph_hull = self.right.data.points_array + chain[self.data.separating_index + 1:]

        self.left.plot(fig, ax, TNULL, reverse)
        return self.right.plot(fig, ax, TNULL, reverse)

    def node_side(self):
        if self.parent.left == self:
            return NodeSide.LEFT
        elif self.parent.right == self:
            return NodeSide.RIGHT
        else:
            return NodeSide.ERROR

    def graph_viz(self, TNULL, wrapper):
        if self is None or self == TNULL:
            return

        wrapper[0] += f"\"{self}\""

        if self.color == NodeColor.RED:
            wrapper[0] += " [color = \"red\"]"
        wrapper[0] += "\n"

        if self.left != TNULL:
            wrapper[0] += f"\"{self}\" -> \"{self.left}\" [label = \"left\"]\n"
        if self.right != TNULL:
            wrapper[0] += f"\"{self}\" -> \"{self.right}\" [label = \"right\"]\n"
        # if self.parent != TNULL:
        #     wrapper[0] += f"\"{self}\" -> \"{self.parent}\" [label = \"parent\"]\n"

        self.left.graph_viz(TNULL, wrapper)
        self.right.graph_viz(TNULL, wrapper)
