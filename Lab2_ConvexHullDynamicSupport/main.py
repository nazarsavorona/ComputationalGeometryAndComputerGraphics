import sys
import matplotlib.pyplot as plt

from Lab2_ConvexHullDynamicSupport.convex_hull import ConvexHull
from Lab2_ConvexHullDynamicSupport.file_utils import OperationType, points_from_file

if __name__ == "__main__":
    points = points_from_file(sys.argv[1])

    convex_hull = ConvexHull()

    for operation, point in points:
        if operation == OperationType.INSERT:
            convex_hull.insert(point)
        if operation == OperationType.DELETE:
            convex_hull.delete(point)

    plt.style.use('ggplot')
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    convex_hull.upper_hull.plot(fig, ax)
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    convex_hull.lower_hull.plot(fig, ax)
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    convex_hull.plot(fig, ax)
    plt.show()
