from Lab2_ConvexHullDynamicSupport.node import Node, NodeData, NodeColor, NodeSide
from Lab2_ConvexHullDynamicSupport.point import Point, PointClass, get_intersect_point, define_point_type_left, \
    define_point_type_right, is_left


class RedBlackTree:
    def __init__(self):
        self.TNULL = Node(NodeData())
        self.TNULL.color = NodeColor.BLACK
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    def left_rotate(self, x):
        temp_array = x.data.points_array

        y = x.right
        temp_j = x.data.separating_index + 1

        x.data.points_array = x.right.data.points_array
        x.right.data.points_array = temp_array

        y.data.separating_index += temp_j

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

    def right_rotate(self, x):
        temp_array = x.data.points_array

        y = x.left
        temp_j = y.data.separating_index + 1

        x.data.points_array = x.left.data.points_array
        x.left.data.points_array = temp_array

        x.data.separating_index -= temp_j

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

    def insert(self, key):
        node = Node(NodeData(key))
        node.parent = None
        node.data.left_most_right = node
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = NodeColor.RED

        x = self.root

        if x == self.TNULL:
            self.root = node
            return

        left_neighbour, right_neighbour = self.down(x, key)

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

            neighbour_side = right_neighbour.node_side()
            if neighbour_side == NodeSide.LEFT:
                right_neighbour.parent.left = new_node_parent
            else:
                right_neighbour.parent.right = new_node_parent

            right_neighbour.parent = new_node_parent

        self.up(node)

        if node.parent == self.TNULL:
            node.color = NodeColor.BLACK
            return

        if node.parent.parent == self.TNULL:
            return

    def down(self, current_node: Node, point: Point, left_neighbour: Node = None, right_neighbour: Node = None):
        if current_node.left == self.TNULL:
            if point.x <= current_node.data.left_most_right_point.x:
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

        if point.x <= current_node.data.left_most_right_point.x:
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
        if side == NodeSide.LEFT:
            q_1, q_2, q_3, q_4, j = merge_chains(current_brother.data.convex_hull, current_node.data.convex_hull)
        elif side == NodeSide.RIGHT:
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
            return node.parent.right, NodeSide.RIGHT
        elif node.parent.right == node:
            return node.parent.left, NodeSide.LEFT
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

    def delete(self, data):
        node = Node(NodeData(data))
        node.parent = None
        node.data.left_most_right = node
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = NodeColor.RED  # new node must be red

        x = self.root

        _, to_delete_node = self.down(x, data)

        if to_delete_node is None or \
                (to_delete_node.data.left_most_right_point.x != data.x or
                 to_delete_node.data.left_most_right_point.y != data.y):
            return
        elif to_delete_node == self.get_root():
            self.root = self.TNULL
        elif to_delete_node.parent.parent == self.TNULL:
            brother, _ = self.find_brother(to_delete_node)

            brother.data.points_array = brother.data.convex_hull

            self.root = brother
            brother.parent = self.TNULL
        else:
            node_parent = to_delete_node.parent
            brother, _ = self.find_brother(to_delete_node)

            side = node_parent.node_side()

            if side == NodeSide.LEFT:
                node_parent.parent.left = brother
            elif side == NodeSide.RIGHT:
                node_parent.parent.right = brother

            brother.parent = node_parent.parent
            self.up(brother)

    def plot(self, fig, ax, reverse=False):
        return self.get_root().plot(fig, ax, self.TNULL, reverse=reverse)

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

    # is_extreme_point_left_1 = False
    # is_extreme_point_right_1 = False

    # is_extreme_point_left_2 = False
    # is_extreme_point_right_2 = False

    while True:
        is_extreme_point_left_1 = False
        is_extreme_point_right_1 = False

        is_extreme_point_left_2 = False
        is_extreme_point_right_2 = False

        if index_1 == temp_min_1:
            is_extreme_point_left_1 = True
        if index_1 == temp_max_1:
            is_extreme_point_right_1 = True

        if index_2 == temp_min_2:
            is_extreme_point_left_2 = True
        if index_2 == temp_max_2:
            is_extreme_point_right_2 = True

        # type_1 = PointClass.ERROR
        # type_2 = PointClass.ERROR

        if is_extreme_point_left_1 and is_extreme_point_right_1:
            type_1 = PointClass.SUPPORTING

        elif is_extreme_point_left_1:
            type_1 = define_point_type_left(Point(chain_1[index_1].x, chain_1[index_1].y - 1),
                                            chain_1[index_1],
                                            chain_1[index_1 + 1], chain_2[index_2])
        elif is_extreme_point_right_1:
            type_1 = define_point_type_left(chain_1[index_1 - 1], chain_1[index_1],
                                            Point(chain_1[index_1].x, chain_1[index_1].y - 1),
                                            chain_2[index_2])
        else:
            type_1 = define_point_type_left(chain_1[index_1 - 1], chain_1[index_1], chain_1[index_1 + 1],
                                            chain_2[index_2])

        if is_extreme_point_left_2 and is_extreme_point_right_2:
            type_2 = PointClass.SUPPORTING

        elif is_extreme_point_left_2:
            type_2 = define_point_type_right(Point(chain_2[index_2].x, chain_2[index_2].y - 1),
                                             chain_2[index_2],
                                             chain_2[index_2 + 1], chain_1[index_1])
        elif is_extreme_point_right_2:
            type_2 = define_point_type_right(chain_2[index_2 - 1], chain_2[index_2],
                                             Point(chain_2[index_2].x, chain_2[index_2].y - 1),
                                             chain_1[index_1])
        else:
            type_2 = define_point_type_right(chain_2[index_2 - 1], chain_2[index_2], chain_2[index_2 + 1],
                                             chain_1[index_1])

        if type_1 == PointClass.CONCAVE and type_2 == PointClass.CONCAVE:
            check_result = concave_concave_case(chain_1[index_1], chain_1[index_1 + 1], chain_1[temp_max_1],
                                                chain_2[temp_min_2], chain_2[index_2 - 1], chain_2[index_2])
            if check_result == NodeSide.LEFT:
                temp_min_1 = index_1
                if temp_max_1 - index_1 != 1:
                    index_1 = int((index_1 + temp_max_1) / 2)
                else:
                    index_1 = temp_max_1
            elif check_result == NodeSide.RIGHT:
                temp_max_2 = index_2
                index_2 = int((temp_min_2 + index_2) / 2)
            else:
                temp_min_1 = index_1
                if temp_max_1 - index_1 != 1:
                    index_1 = int((index_1 + temp_max_1) / 2)
                else:
                    index_1 = temp_max_1
                temp_max_2 = index_2
                index_2 = int((temp_min_2 + index_2) / 2)

        elif type_1 == PointClass.CONCAVE and type_2 == PointClass.SUPPORTING:
            temp_min_1 = index_1
            if temp_max_1 - index_1 != 1:
                index_1 = int((index_1 + temp_max_1) / 2)
            else:
                index_1 = temp_max_1

            temp_min_2 = index_2
            # index_2 = int((index_2 + temp_max_2) / 2)

        elif type_1 == PointClass.CONCAVE and type_2 == PointClass.CONVEX:
            temp_min_2 = index_2
            if temp_max_2 - index_2 != 1:
                index_2 = int((index_2 + temp_max_2) / 2)
            else:
                index_2 = temp_max_2

        elif type_1 == PointClass.SUPPORTING and type_2 == PointClass.CONCAVE:
            temp_max_1 = index_1
            # index_1 = int((temp_min_1 + index_1) / 2)

            temp_max_2 = index_2
            index_2 = int((temp_min_2 + index_2) / 2)

        elif type_1 == PointClass.SUPPORTING and type_2 == PointClass.SUPPORTING:
            break

        elif type_1 == PointClass.SUPPORTING and type_2 == PointClass.CONVEX:
            temp_max_1 = index_1
            # index_1 = int((temp_min_1 + index_1) / 2)

            temp_min_2 = index_2
            if temp_max_2 - index_2 != 1:
                index_2 = int((index_2 + temp_max_2) / 2)
            else:
                index_2 = temp_max_2

        elif type_1 == PointClass.CONVEX and type_2 == PointClass.CONCAVE:
            temp_max_1 = index_1
            index_1 = int((temp_min_1 + index_1) / 2)

        elif type_1 == PointClass.CONVEX and type_2 == PointClass.SUPPORTING:
            temp_max_1 = index_1
            index_1 = int((temp_min_1 + index_1) / 2)

            temp_min_2 = index_2
            # index_2 = int((index_2 + temp_max_2) / 2)

        elif type_1 == PointClass.CONVEX and type_2 == PointClass.CONVEX:
            temp_max_1 = index_1
            index_1 = int((temp_min_1 + index_1) / 2)

            temp_min_2 = index_2
            if temp_max_2 - index_2 != 1:
                index_2 = int((index_2 + temp_max_2) / 2)
            else:
                index_2 = temp_max_2

    q_1 = chain_1[:index_1 + 1]
    q_2 = chain_1[index_1 + 1:]
    q_3 = chain_2[:index_2]
    q_4 = chain_2[index_2:]
    j = index_1

    return q_1, q_2, q_3, q_4, j


def concave_concave_case(q1, q1_successor, max_left, min_right, q2_predecessor, q2):
    center_line_x = (max_left.x + min_right.x) / 2
    if get_intersect_point(q1, q1_successor, q2_predecessor, q2).x < center_line_x:
        return NodeSide.LEFT
    elif get_intersect_point(q1, q1_successor, q2_predecessor, q2).x > center_line_x:
        return NodeSide.RIGHT
    else:
        return NodeSide.ERROR
