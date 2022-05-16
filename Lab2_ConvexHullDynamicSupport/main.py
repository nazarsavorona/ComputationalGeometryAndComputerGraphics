import sys
import matplotlib.pyplot as plt

from enum import Enum

import numpy


class PointClass(Enum):
    CONVEX = 1  # REFLEX
    CONCAVE = 2  # CONCAVE
    SUPPORTING = 3  # SUPPORTING
    ERROR = -1


class Point:
    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_

    def __repr__(self):
        return str(f"({self.x}; {self.y})")

    def __lt__(self, other):
        return self.x < other.x or (self.x == other.x and self.y < other.y)


class NodeData:
    def __init__(self, key=None):
        self.left_most_right: Node = None
        self.left_most_right_point: Point = key
        self.points_array = []
        self.separating_index = 0
        self.convex_hull = []
        self.convex_hull.append(key)

    def __lt__(self, other):
        return self.left_most_right_point < other.left_most_right_point

    def __repr__(self):
        return str(f"{self.left_most_right_point}; {self.points_array}; {self.separating_index}")


class NodeColor(Enum):
    RED = 1
    BLACK = 2


# data structure that represents a node in the tree
class Node:
    i = 0

    def __init__(self, data):
        self.data: NodeData = data  # holds the key
        self.parent: Node = None  # pointer to the parent
        self.left: Node = None  # pointer to left child
        self.right: Node = None  # pointer to right child
        self.color = NodeColor.RED
        self.id = Node.i
        Node.i += 1

    def __lt__(self, other):
        return self.data < other.data

    def __repr__(self):
        return str(f"{self.id}: {self.data}")

    def plot(self, fig, ax, TNULL):
        if self is None or self == TNULL:
            return fig, ax

        if self.left == TNULL:
            _x, _y, = self.data.left_most_right_point.x, self.data.left_most_right_point.y
            ax.scatter([_x], [_y], color="green")
            ax.annotate(f"({_x}; {_y})", (_x, _y), xytext=(_x - 0.025, _y + 0.1))
            return fig, ax

        chain = self.data.convex_hull
        color = numpy.random.rand(3, )

        for i in range(1, len(chain)):
            ax.plot([chain[i - 1].x, chain[i].x], [chain[i - 1].y, chain[i].y], color=color)

        self.left.plot(fig, ax, TNULL)
        return self.right.plot(fig, ax, TNULL)

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

        self.left.graph_viz(TNULL, wrapper)
        self.right.graph_viz(TNULL, wrapper)


# class RedBlackTree implements the operations in Red Black Tree
class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(NodeData())
        self.TNULL.color = NodeColor.BLACK
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    def __pre_order_helper(self, node):
        if node != self.TNULL:
            sys.stdout.write(node.data + " ")
            self.__pre_order_helper(node.left)
            self.__pre_order_helper(node.right)

    def __in_order_helper(self, node):
        if node != self.TNULL:
            self.__in_order_helper(node.left)
            sys.stdout.write(node.data + " ")
            self.__in_order_helper(node.right)

    def __post_order_helper(self, node):
        if node != self.TNULL:
            self.__post_order_helper(node.left)
            self.__post_order_helper(node.right)
            sys.stdout.write(node.data + " ")

    def __search_tree_helper(self, node, key):
        if node == self.TNULL or key == node.data:
            return node

        if key < node.data:
            return self.__search_tree_helper(node.left, key)
        return self.__search_tree_helper(node.right, key)

    # fix the rb tree modified by the delete operation
    def __fix_delete(self, x):
        while x != self.root and x.color == NodeColor.BLACK:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == NodeColor.RED:
                    # case 3.1
                    s.color = NodeColor.BLACK
                    x.parent.color = NodeColor.RED
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == NodeColor.BLACK and s.right.color == NodeColor.BLACK:
                    # case 3.2
                    s.color = NodeColor.RED
                    x = x.parent
                else:
                    if s.right.color == NodeColor.BLACK:
                        # case 3.3
                        s.left.color = NodeColor.BLACK
                        s.color = NodeColor.RED
                        self.right_rotate(s)
                        s = x.parent.right

                    # case 3.4
                    s.color = x.parent.color
                    x.parent.color = NodeColor.BLACK
                    s.right.color = NodeColor.BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == NodeColor.RED:
                    # case 3.1
                    s.color = NodeColor.BLACK
                    x.parent.color = NodeColor.RED
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.left.color == NodeColor.BLACK and s.right.color == NodeColor.BLACK:
                    # case 3.2
                    s.color = NodeColor.RED
                    x = x.parent
                else:
                    if s.left.color == NodeColor.BLACK:
                        # case 3.3
                        s.right.color = NodeColor.BLACK
                        s.color = NodeColor.RED
                        self.left_rotate(s)
                        s = x.parent.left

                        # case 3.4
                    s.color = x.parent.color
                    x.parent.color = NodeColor.BLACK
                    s.left.color = NodeColor.BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = NodeColor.BLACK

    def __rb_transplant(self, u, v):
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def __delete_node_helper(self, node, key):
        # find the node containing key
        z = self.TNULL
        while node != self.TNULL:
            if node.data == key:
                z = node

            if node.data <= key:
                node = node.right
            else:
                node = node.left

        if z == self.TNULL:
            print("Couldn't find key in the tree")
            return

        y = z
        y_original_color = y.color
        if z.left == self.TNULL:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif (z.right == self.TNULL):
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == NodeColor.BLACK:
            self.__fix_delete(x)

    # fix the red-black tree
    def __fix_insert(self, k):
        while k.parent.color == NodeColor.RED:
            if k.parent.parent == self.TNULL:
                k.parent.color = NodeColor.BLACK
                k.parent.left.color = NodeColor.RED
                k.parent.right.color = NodeColor.RED
                return
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left  # uncle
                if u.color == NodeColor.RED:
                    # case 3.1
                    u.color = NodeColor.BLACK
                    k.parent.color = NodeColor.BLACK
                    k.parent.parent.color = NodeColor.RED
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        # case 3.2.2
                        k = k.parent
                        self.right_rotate(k)
                    # case 3.2.1
                    k.parent.color = NodeColor.BLACK
                    k.parent.parent.color = NodeColor.RED
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right  # uncle

                if u.color == NodeColor.RED:
                    # mirror case 3.1
                    u.color = NodeColor.BLACK
                    k.parent.color = NodeColor.BLACK
                    k.parent.parent.color = NodeColor.RED
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        # mirror case 3.2.2
                        k = k.parent
                        self.left_rotate(k)
                    # mirror case 3.2.1
                    k.parent.color = NodeColor.BLACK
                    k.parent.parent.color = NodeColor.RED
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = NodeColor.BLACK

    def __print_helper(self, node, indent, last):
        # print the tree structure on the screen
        if node != self.TNULL:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            s_color = "RED" if node.color == NodeColor.RED else "BLACK"
            print(str(node.data) + "(" + s_color + ")")
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)

    # Pre-Order traversal
    # Node.Left Subtree.Right Subtree
    def preorder(self):
        self.__pre_order_helper(self.root)

    # In-Order traversal
    # left Subtree . Node . Right Subtree
    def inorder(self):
        self.__in_order_helper(self.root)

    # Post-Order traversal
    # Left Subtree . Right Subtree . Node
    def postorder(self):
        self.__post_order_helper(self.root)

    # search the tree for the key k
    # and return the corresponding node
    def searchTree(self, k):
        return self.__search_tree_helper(self.root, k)

    # find the node with the minimum key
    def minimum(self, node):
        while node.left != self.TNULL:
            node = node.left
        return node

    # find the node with the maximum key
    def maximum(self, node):
        while node.right != self.TNULL:
            node = node.right
        return node

    # find the successor of a given node
    def successor(self, x):
        # if the right subtree is not None,
        # the successor is the leftmost node in the
        # right subtree
        if x.right != self.TNULL:
            return self.minimum(x.right)

        # else it is the lowest ancestor of x whose
        # left child is also an ancestor of x.
        y = x.parent
        while y != self.TNULL and x == y.right:
            x = y
            y = y.parent
        return y

    # find the predecessor of a given node
    def predecessor(self, x):
        # if the left subtree is not None,
        # the predecessor is the rightmost node in the
        # left subtree
        if (x.left != self.TNULL):
            return self.maximum(x.left)

        y = x.parent
        while y != self.TNULL and x == y.left:
            x = y
            y = y.parent

        return y

    # rotate left at node x
    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left != self.TNULL:
            y.left.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    # rotate right at node x
    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right != self.TNULL:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    # insert the key to the tree in its appropriate position
    # and fix the tree
    def insert(self, key):
        # Ordinary Binary Search Insertion
        node = Node(NodeData(key))
        node.parent = None
        node.data.left_most_right = node
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = NodeColor.RED  # new node must be red

        x = self.root

        if x == self.TNULL:
            self.root = node
            return

        left_neighbour = None
        right_neighbour = None

        left_neighbour, right_neighbour = self.down(x, key, left_neighbour, right_neighbour)

        new_node_parent = Node(NodeData())
        node.parent = new_node_parent

        if left_neighbour is None:
            new_node_parent.left = node
            new_node_parent.right = right_neighbour

            new_node_parent.parent = right_neighbour.parent
            if right_neighbour.parent is None:
                self.root = new_node_parent
                new_node_parent.parent = self.TNULL
            else:
                right_neighbour.parent.left = new_node_parent

            right_neighbour.parent = new_node_parent

        elif right_neighbour is None:
            new_node_parent.right = node
            new_node_parent.left = left_neighbour

            new_node_parent.parent = left_neighbour.parent
            if left_neighbour.parent is None:
                self.root = new_node_parent
                new_node_parent.parent = self.TNULL
            else:
                left_neighbour.parent.right = new_node_parent

            left_neighbour.parent = new_node_parent

        elif self.find_brother(left_neighbour)[0] == right_neighbour:
            new_node_parent.left = left_neighbour
            new_node_parent.right = node

            new_node_parent.parent = left_neighbour.parent
            left_neighbour.parent.left = new_node_parent

            left_neighbour.parent = new_node_parent
        else:
            new_node_parent.left = node
            new_node_parent.right = right_neighbour

            new_node_parent.parent = right_neighbour.parent
            right_neighbour.parent.left = new_node_parent

            right_neighbour.parent = new_node_parent

        self.up(node)

        # while x != self.TNULL:
        #     y = x
        #     if node.data < x.data:
        #         x = x.left
        #     else:
        #         x = x.right
        #
        # # y is parent of x
        # node.parent = y
        # if y is None:
        #     self.root = node
        # elif node.data < y.data:
        #     y.left = node
        # else:
        #     y.right = node
        #

        # if new node is a root node, simply return
        if node.parent == self.TNULL:
            node.color = NodeColor.BLACK
            return

        # if the grandparent is None, simply return
        if node.parent.parent == self.TNULL:
            return

        # Fix the tree
        self.__fix_insert(node)

    def down(self, current_node: Node, point: Point, left_neighbour: Node, right_neighbour: Node):
        if current_node.left == self.TNULL:
            if point.x < current_node.data.left_most_right_point.x:
                right_neighbour = current_node
            else:
                left_neighbour = current_node
            return left_neighbour, right_neighbour

        left_queue = current_node.data.convex_hull[:current_node.data.separating_index + 1]
        right_queue = current_node.data.convex_hull[current_node.data.separating_index + 1:]

        left_son = current_node.left
        right_son = current_node.right

        if left_son.left != self.TNULL:
            left_son.data.convex_hull = left_queue + left_son.data.points_array

        if right_son.left != self.TNULL:
            right_son.data.convex_hull = right_son.data.points_array + right_queue

        if point.x < current_node.data.left_most_right_point.x:
            right_neighbour = current_node
            current_node = current_node.left

        else:
            left_neighbour = current_node.data.left_most_right
            current_node = current_node.right

        return self.down(current_node, point, left_neighbour, right_neighbour)

    def up(self, current_node: Node):
        if current_node == self.get_root():
            current_node.data.points_array = current_node.data.convex_hull
            return

        current_brother, side = self.find_brother(current_node)

        q_1, q_2, q_3, q_4, j = [], [], [], [], 0
        if side == -1:
            q_1, q_2, q_3, q_4, j = merge_chains(current_brother.data.convex_hull, current_node.data.convex_hull)
        elif side == 1:
            q_1, q_2, q_3, q_4, j = merge_chains(current_node.data.convex_hull, current_brother.data.convex_hull)

        current_node.parent.left.data.points_array = q_2
        current_node.parent.right.data.points_array = q_3

        current_node.parent.data.convex_hull = q_1 + q_4
        current_node.parent.data.separating_index = j

        current_node.parent.data.left_most_right = self.find_left_most_right(current_node.parent)
        current_node.parent.data.left_most_right_point = current_node.parent.data.left_most_right.data.left_most_right_point

        self.up(current_node.parent)

    def find_brother(self, node: Node):
        if node.parent.left == node:
            return node.parent.right, 1
        elif node.parent.right == node:
            return node.parent.left, -1
        return self.TNULL

    def find_left_most_right(self, node: Node):
        current_node = node

        if current_node.left != self.TNULL:
            current_node = current_node.left

        while current_node.right != self.TNULL:
            current_node = current_node.right

        return current_node.data.left_most_right

    def get_root(self):
        return self.root

    # delete the node from the tree
    def delete_node(self, data):
        self.__delete_node_helper(self.root, data)

    # print the tree structure on the screen
    def pretty_print(self):
        self.__print_helper(self.root, "", True)

    def plot(self):
        fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))

        return self.get_root().plot(fig, ax, self.TNULL)

    def graph_viz(self):
        string = "digraph g {\n"
        wrapper = [string]

        self.get_root().graph_viz(self.TNULL, wrapper)

        return wrapper[0] + "}\n"


def merge_chains(chain_1: [], chain_2: []):
    if len(chain_2) == 1:
        if len(chain_1) == 1:
            return chain_1, [], [], chain_2, 0

        if len(chain_1) == 2:
            if is_left(chain_1[0], chain_1[1], chain_2[0]):
                return chain_1[:1], chain_1[1:], [], chain_2, 0
            else:
                return chain_1, [], [], chain_2, 1

    if len(chain_1) == 1:
        if is_left(chain_2[0], chain_2[1], chain_1[0]):
            return chain_1, [], chain_2[:1], chain_2[1:], 0
        else:
            return chain_1, [], [], chain_2, 0

    index_1 = int((len(chain_1) - 1) / 2)

    index_2 = int((len(chain_2) - 1) / 2)

    temp_min_1 = 0
    temp_max_1 = len(chain_1) - 1

    temp_min_2 = 0
    temp_max_2 = len(chain_2) - 1

    is_extreme_point_left_1 = False
    is_extreme_point_right_1 = False

    is_extreme_point_left_2 = False
    is_extreme_point_right_2 = False

    # if len(chain_1) == 2:
    #     if len(chain_2) == 2:
    #         types_array = []
    #
    #         types_array.append(define_point_type(Point(chain_1[0].x, chain_1[0].y - 1),
    #                                              chain_1[0],
    #                                              chain_1[1], chain_2[0]))
    #         types_array.append(define_point_type(Point(chain_1[0].x, chain_1[0].y - 1),
    #                                              chain_1[0],
    #                                              chain_1[1], chain_2[1]))
    #         types_array.append(define_point_type(chain_1[0],
    #                                              chain_1[1],
    #                                              Point(chain_1[1].x, chain_1[1].y - 1), chain_2[0]))
    #         types_array.append(define_point_type(chain_1[0],
    #                                              chain_1[1],
    #                                              Point(chain_1[1].x, chain_1[1].y - 1), chain_2[1]))
    #         types_array.append(define_point_type(Point(chain_2[0].x, chain_2[0].y - 1),
    #                                              chain_1[0],
    #                                              chain_2[1], chain_2[0]))
    #         types_array.append(define_point_type(chain_2[0],
    #                                              chain_1[0],
    #                                              Point(chain_2[1].x, chain_2[1].y - 1), chain_2[1]))
    #         types_array.append(define_point_type(Point(chain_2[0].x, chain_2[0].y - 1),
    #                                              chain_1[1],
    #                                              chain_2[1], chain_2[0]))
    #         types_array.append(define_point_type(chain_2[0],
    #                                              chain_1[1],
    #                                              Point(chain_2[1].x, chain_2[1].y - 1), chain_2[1]))
    #
    #         correct_type_index_1 = -1
    #         correct_type_index_2 = -1
    #         for i in range(4):
    #             if types_array[i] == PointClass.SUPPORTING and types_array[i + 4] == PointClass.SUPPORTING:
    #                 correct_type_index_1 = i
    #                 correct_type_index_2 = i + 4
    #                 break
    #
    #         q_1 = chain_1[:correct_type_index_1 + 1]
    #         q_2 = chain_1[correct_type_index_1 + 1:]
    #         q_3 = chain_2[:correct_type_index_2]
    #         q_4 = chain_2[correct_type_index_2:]
    #         j = correct_type_index_1
    #
    #         return q_1, q_2, q_3, q_4, j

    while True:
        is_extreme_point_left_1 = False
        is_extreme_point_right_1 = False

        is_extreme_point_left_2 = False
        is_extreme_point_right_2 = False

        if index_1 == temp_min_1:
            is_extreme_point_left_1 = True
        elif index_1 == temp_max_1:
            is_extreme_point_right_1 = True

        if index_2 == temp_min_2:
            is_extreme_point_left_2 = True
        elif index_2 == temp_max_2:
            is_extreme_point_right_2 = True

        type_1 = PointClass.ERROR
        type_2 = PointClass.ERROR

        if is_extreme_point_left_1:
            type_1 = define_point_type(Point(chain_1[index_1].x, chain_1[index_1].y - 1),
                                       chain_1[index_1],
                                       chain_1[index_1 + 1], chain_2[index_2])
        elif is_extreme_point_right_1:
            type_1 = define_point_type(chain_1[index_1 - 1], chain_1[index_1],
                                       Point(chain_1[index_1].x, chain_1[index_1].y - 1),
                                       chain_2[index_2])
        else:
            type_1 = define_point_type(chain_1[index_1 - 1], chain_1[index_1], chain_1[index_1 + 1],
                                       chain_2[index_2])

        if is_extreme_point_left_2:
            type_2 = define_point_type(Point(chain_2[index_2].x, chain_2[index_2].y - 1),
                                       chain_1[index_1],
                                       chain_2[index_2 + 1], chain_2[index_2])
        elif is_extreme_point_right_2:
            type_2 = define_point_type(chain_2[index_2 - 1], chain_1[index_1],
                                       Point(chain_2[index_2].x, chain_2[index_2].y - 1),
                                       chain_2[index_2])
        else:
            type_2 = define_point_type(chain_2[index_2 - 1], chain_1[index_1], chain_2[index_2 + 1],
                                       chain_2[index_2])

        if type_1 == PointClass.CONCAVE:
            if type_2 == PointClass.CONCAVE:
                check_result = concave_concave(chain_1[index_1], chain_1[index_1 + 1], chain_1[temp_max_1 - 1],
                                               chain_2[temp_min_2], chain_2[index_2 - 1], chain_2[index_2])
                if check_result == -1:
                    temp_min_1 = index_1
                    index_1 = int((index_1 + temp_max_1) / 2)
                elif check_result == 1:
                    temp_max_2 = index_2
                    index_2 = int((temp_min_2 + index_2) / 2)
                else:
                    temp_min_1 = index_1
                    index_1 = int((index_1 + temp_max_1) / 2)
                    temp_max_2 = index_2
                    index_2 = int((temp_min_2 + index_2) / 2)

            else:
                if type_2 == PointClass.SUPPORTING:
                    temp_min_1 = index_1
                    index_1 = int((index_1 + temp_max_1) / 2)

                temp_min_2 = index_2
                index_2 = int((index_2 + temp_max_2) / 2)

            if index_1 + temp_max_1 == 1:
                index_1 = 1

        elif type_1 == PointClass.SUPPORTING:
            if type_2 == PointClass.SUPPORTING:
                break

            else:
                temp_max_1 = index_1
                index_1 = int((temp_min_1 + index_1) / 2)

                if type_2 == PointClass.CONCAVE:
                    temp_max_2 = index_2
                    index_2 = int((temp_min_2 + index_2) / 2)
                else:
                    temp_min_2 = index_2
                    if index_2 + temp_max_2 == 1:
                        index_2 = 1
                    else:
                        index_2 = int((index_2 + temp_max_2) / 2)

        else:
            temp_max_1 = index_1
            index_1 = int((temp_min_1 + index_1) / 2)

            if type_2 == PointClass.SUPPORTING:
                temp_min_2 = index_2
                index_2 = int((index_2 + temp_max_2) / 2)
            elif type_2 == PointClass.CONVEX:
                temp_min_2 = index_2
                if index_2 + temp_max_2 == 1:
                    index_2 = 1
                else:
                    index_2 = int((index_2 + temp_max_2) / 2)

    q_1 = chain_1[:index_1 + 1]
    q_2 = chain_1[index_1 + 1:]
    q_3 = chain_2[:index_2]
    q_4 = chain_2[index_2:]
    j = index_1

    return q_1, q_2, q_3, q_4, j


def concave_concave(q1, q1_suc, max_left, min_right, q2_pred, q2):
    center_line_x = (max_left.x + min_right.x) / 2
    if get_intersect_point(q1, q1_suc, q2_pred, q2).x < center_line_x:
        return -1
    elif get_intersect_point(q1, q1_suc, q2_pred, q2).x > center_line_x:
        return 1
    else:
        return 0


def get_intersect_point(a, b, c, d):
    return Point(((a.x * b.y - a.y * b.x) * (c.x - d.x) - (a.x - b.x) * (c.x * d.y - c.y * d.x))
                 / ((a.x - b.x) * (c.y - d.y) - (a.y - b.y) * (c.x - d.x)),
                 ((a.x * b.y - a.y * b.x) * (c.y - d.y) - (a.y - b.y) * (c.x * d.y - c.y * d.x))
                 / ((a.x - b.x) * (c.y - d.y) - (a.y - b.y) * (c.x - d.x)))


def define_point_type(q1_pred: Point, q1: Point, q1_suc: Point, q2: Point):
    if is_left(q2, q1, q1_pred) and is_left(q2, q1, q1_suc):
        return PointClass.SUPPORTING
    if is_left(q2, q1, q1_pred) and not is_left(q2, q1, q1_suc):
        return PointClass.CONCAVE
    else:
        return PointClass.CONVEX


def is_left(chain_point_1, chain_point_2, point):
    return ((chain_point_2.x - chain_point_1.x) * (point.y - chain_point_1.y) - (chain_point_2.y - chain_point_1.y) * (
            point.x - chain_point_1.x)) >= 0


if __name__ == "__main__":
    bst = RedBlackTree()
    bst.insert(Point(-1, -1))
    print(bst.graph_viz())
    # bst.plot()
    # plt.show()
    bst.insert(Point(0, 0))
    print(bst.graph_viz())
    bst.insert(Point(6, 10))
    print(bst.graph_viz())
    bst.insert(Point(3, 8))
    print(bst.graph_viz())
    bst.insert(Point(-5, -3))
    # bst.plot()
    bst.insert(Point(7, 7))
    bst.plot()
    plt.show()
    bst.insert(Point(100, 8))
    print(bst.graph_viz())
