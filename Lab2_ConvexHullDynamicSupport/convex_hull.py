import copy

from Lab2_ConvexHullDynamicSupport.rb_tree import RedBlackTree


class ConvexHull:
    def __init__(self):
        self.upper_hull = UpperHull()
        self.lower_hull = LowerHull()

    def insert(self, insert_point):
        self.upper_hull.insert(insert_point)
        self.lower_hull.insert(insert_point)

    def delete(self, delete_point):
        self.upper_hull.delete(delete_point)
        self.lower_hull.delete(delete_point)

    def plot(self, fig, ax):
        self.upper_hull.plot(fig, ax)
        return self.lower_hull.plot(fig, ax)


class UpperHull:
    def __init__(self):
        self.bst = RedBlackTree()

    def insert(self, insert_point):
        self.bst.insert(insert_point)

    def delete(self, delete_point):
        self.bst.delete(delete_point)

    def plot(self, fig, ax):
        return self.bst.plot(fig, ax)


class LowerHull:
    def __init__(self):
        self.bst = RedBlackTree()

    def insert(self, insert_point):
        to_insert = copy.deepcopy(insert_point)
        to_insert.y *= -1

        self.bst.insert(to_insert)

    def delete(self, delete_point):
        to_delete = copy.deepcopy(delete_point)
        to_delete.y *= -1

        self.bst.delete(to_delete)

    def plot(self, fig, ax):
        return self.bst.plot(fig, ax, reverse=True)
