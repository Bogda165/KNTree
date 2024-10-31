import copy
import heapq

import numpy as np
import matplotlib.pyplot as plt
import random

size = 5000

color_dict = {
    -1: "B",
    0: "R",
    1: "G",
    2: "B",
    3: "P"
}

def calibrate_i(index: int) -> int:
    return index + size

class KDTreeNode:
    def __init__(self, point, left=None, right=None):
        self.point = point  # The 2D point (x, y) stored in this node
        self.left = left    # Left subtree
        self.right = right  # Right subtree


class KDTree:
    def __init__(self):
        self.root = None

    def insert(self, point, depth=0):
        """Insert a new point into the KD-tree."""
        def _insert(node, point, depth):
            if node is None:
                return KDTreeNode(point)

            # Alternate between x and y axis
            axis = depth % 2
            if point[axis] < node.point[axis]:
                node.left = _insert(node.left, point, depth + 1)
            else:
                node.right = _insert(node.right, point, depth + 1)
            return node

        self.root = _insert(self.root, point, depth)

    def nearest_neighbor(self, target, depth=0, best=None):
        """Find the nearest neighbor for a target point."""
        def _nearest(node, target, depth, best):
            if node is None:
                return best

            # Compute squared distance to avoid unnecessary sqrt calls
            point = node.point
            dist = (point[0] - target[0]) ** 2 + (point[1] - target[1]) ** 2
            if best is None or dist < best[1]:
                best = (node.point, dist)

            # Determine which side of the split line to search
            axis = depth % 2
            next_branch = node.left if target[axis] < point[axis] else node.right
            opposite_branch = node.right if target[axis] < point[axis] else node.left

            # Search the nearest branch
            best = _nearest(next_branch, target, depth + 1, best)

            # Check if we need to search the opposite branch
            if (target[axis] - point[axis]) ** 2 < best[1]:
                best = _nearest(opposite_branch, target, depth + 1, best)

            return best

        best = _nearest(self.root, target, depth, best)
        return best[0]  # Return only the point, not the distance

    def k_nearest_neighbors(self, target, k, depth=0):
        """Find the k nearest neighbors for a target point."""
        heap = []  # Max-heap to store the k nearest neighbors

        def _k_nearest(node, target, depth):
            if node is None:
                return

            point = node.point
            dist = (point[0] - target[0]) ** 2 + (point[1] - target[1]) ** 2

            # If the heap is not full, add the current point
            if len(heap) < k:
                heapq.heappush(heap, (-dist, point))
            else:
                # If the heap is full and current point is closer, replace the farthest point
                if dist < -heap[0][0]:
                    heapq.heappushpop(heap, (-dist, point))

            # Determine which side of the split line to search
            axis = depth % 2
            next_branch = node.left if target[axis] < point[axis] else node.right
            opposite_branch = node.right if target[axis] < point[axis] else node.left

            # Search the nearest branch
            _k_nearest(next_branch, target, depth + 1)

            # Check if we need to search the opposite branch
            if (target[axis] - point[axis]) ** 2 < -heap[0][0] or len(heap) < k:
                _k_nearest(opposite_branch, target, depth + 1)

        _k_nearest(self.root, target, depth)
        return [point for _, point in sorted(heap, reverse=True)]


class Point:
    def __init__(self, x=0, y=0, color = -1):
        self.x = x
        self.y = y
        self.color = color

    def __repr__(self):
        return f"Point: {self.x} {self.y} {self.color}"

class Matrix:
    def __init__(self):
        # Store only needed points in a dictionary
        self.point_map = {}

    def add_point(self, x: int, y: int, color = -1):
        # Use calibrated coordinates for dictionary keys
        key = (x, y)
        if key in self.point_map:
            return False
        if key not in self.point_map:
            self.point_map[key] = Point(x, y, color)
        return True

    def add_point_force(self, color = -1):
        while True:
            x = random.randint(0, size * 2 + 1)
            y = random.randint(0, size * 2 + 1)
            if self.add_point(x, y, color):
                break


    def basi_init(self):
        # Initialize points for "R"
            self.add_point(calibrate_i(-4500), calibrate_i(-4400), 0),
            self.add_point(calibrate_i(-4100), calibrate_i(-3000), 0),
            self.add_point(calibrate_i(-1800), calibrate_i(-2400), 0),
            self.add_point(calibrate_i(-2000), calibrate_i(-1400), 0),
            self.add_point(calibrate_i(-2500), calibrate_i(-3400), 0)

        # Initialize points for "G"
            self.add_point(calibrate_i(4500), calibrate_i(-4400), 1),
            self.add_point(calibrate_i(4100), calibrate_i(-3000), 1),
            self.add_point(calibrate_i(1800), calibrate_i(-2400), 1),
            self.add_point(calibrate_i(2500), calibrate_i(-3400), 1),
            self.add_point(calibrate_i(2000), calibrate_i(-1400), 1)

        # Initialize points for "B"
            self.add_point(calibrate_i(-4500), calibrate_i(4400), 2),
            self.add_point(calibrate_i(-4100), calibrate_i(3000), 2),
            self.add_point(calibrate_i(-1800), calibrate_i(2400), 2),
            self.add_point(calibrate_i(-2500), calibrate_i(3400), 2),
            self.add_point(calibrate_i(-2000), calibrate_i(1400), 2)

        # Initialize points for "P"
            self.add_point(calibrate_i(4500), calibrate_i(4400), 3),
            self.add_point(calibrate_i(4100), calibrate_i(3000), 3),
            self.add_point(calibrate_i(1800), calibrate_i(2400), 3),
            self.add_point(calibrate_i(2500), calibrate_i(3400), 3),
            self.add_point(calibrate_i(2000), calibrate_i(1400), 3)



    #Function to draw the matrix with colored points

    def display_field(self):
        """Display the field with colored points."""
        color_map = {
            -1: 'black',
            0: 'red',
            1: 'green',
            2: 'blue',
            3: 'purple'
        }

        x_coords = []
        y_coords = []
        colors = []

        for key in self.point_map:
            point = self.point_map[key]
            x_coords.append(point.x - size)
            y_coords.append(point.y - size)
            colors.append(color_map[point.color])

        plt.figure(figsize=(10, 10))
        plt.scatter(x_coords, y_coords, c=colors, s=10)

        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.title("Field of Points with Colors")
        plt.grid(True)
        plt.show()

def color(matrix, k = 1):
    tree = KDTree()
    for point in matrix.point_map.values():
        if point.color == -1:
            nearest = tree.k_nearest_neighbors((point.x, point.y), k)
            dic = {}
            for neighbor in nearest:
                _point = matrix.point_map[(neighbor[0], neighbor[1])]
                dic[_point.color] = dic.get(_point.color, 0) + 1

            point.color = max(dic, key=dic.get)
            _color = max(dic, key=dic.get)
            point.color = _color
        tree.insert((point.x, point.y))
    matrix.display_field()


# Example usage
matrix = Matrix()
matrix.basi_init()

for i in range(0, 40000):
    matrix.add_point_force(-1)

print("added")
color(copy.deepcopy(matrix), 1)
color(copy.deepcopy(matrix), 3)
color(copy.deepcopy(matrix), 7)
color(copy.deepcopy(matrix), 15)
