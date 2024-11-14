import random

from matplotlib import pyplot as plt


class Point:
    def __init__(self, x=0, y=0, color = -1):
        self.x = x
        self.y = y
        self.color = color

    def __repr__(self):
        return f"Point: {self.x} {self.y} {self.color}"

class Matrix:
    def __init__(self, size):
        # Store only needed points in a dictionary
        self.size = size
        self.point_map = {}

    def add_point(self, x: int, y: int, color = -1):
        # Use calibrated coordinates for dictionary keys
        key = (x, y)
        if key in self.point_map:
            return False
        if key not in self.point_map:
            self.point_map[key] = Point(x, y, color)
        return True


    def add_point_force(self, x1, x2, y1, y2, color = -1,):
        while True:
            x = random.randint(x1, x2)
            y = random.randint(y1, y2)
            if self.add_point(x, y, color):
                break


    def display_field(self):
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
            x_coords.append(point.x - self.size)
            y_coords.append(point.y - self.size)
            colors.append(color_map[point.color])

        plt.figure(figsize=(10, 10))
        plt.scatter(x_coords, y_coords, c=colors, s=10)

        plt.xlabel("X Coordinate")
        plt.ylabel("Y Coordinate")
        plt.title("Field of Points with Colors")
        plt.grid(True)
        plt.show()