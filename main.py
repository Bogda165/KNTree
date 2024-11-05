import copy
from collections import defaultdict

import numpy as np
from KDTree.kdTree import KDTree
from Matrix.matrix import Matrix

size = 4000

def basi_init(matrix):
    # Initialize points for "R"
    matrix.add_point(calibrate_i(-4500), calibrate_i(-4400), 0),
    matrix.add_point(calibrate_i(-4100), calibrate_i(-3000), 0),
    matrix.add_point(calibrate_i(-1800), calibrate_i(-2400), 0),
    matrix.add_point(calibrate_i(-2000), calibrate_i(-1400), 0),
    matrix.add_point(calibrate_i(-2500), calibrate_i(-3400), 0),
    matrix.add_point(calibrate_i(-4501), calibrate_i(-4401), 0),
    matrix.add_point(calibrate_i(-4101), calibrate_i(-3001), 0),
    matrix.add_point(calibrate_i(-1801), calibrate_i(-2401), 0),
    matrix.add_point(calibrate_i(-2001), calibrate_i(-1401), 0),
    matrix.add_point(calibrate_i(-2501), calibrate_i(-3401), 0)

    # Initialize points for "G"
    matrix.add_point(calibrate_i(4500), calibrate_i(-4400), 1),
    matrix.add_point(calibrate_i(4100), calibrate_i(-3000), 1),
    matrix.add_point(calibrate_i(1800), calibrate_i(-2400), 1),
    matrix.add_point(calibrate_i(2500), calibrate_i(-3400), 1),
    matrix.add_point(calibrate_i(2000), calibrate_i(-1400), 1),

    matrix.add_point(calibrate_i(4501), calibrate_i(-4401), 1),
    matrix.add_point(calibrate_i(4101), calibrate_i(-3001), 1),
    matrix.add_point(calibrate_i(1801), calibrate_i(-2401), 1),
    matrix.add_point(calibrate_i(2501), calibrate_i(-3401), 1),
    matrix.add_point(calibrate_i(2001), calibrate_i(-1401), 1)

    # Initialize points for "B"
    matrix.add_point(calibrate_i(-4500), calibrate_i(4400), 2),
    matrix.add_point(calibrate_i(-4100), calibrate_i(3000), 2),
    matrix.add_point(calibrate_i(-1800), calibrate_i(2400), 2),
    matrix.add_point(calibrate_i(-2500), calibrate_i(3400), 2),
    matrix.add_point(calibrate_i(-2000), calibrate_i(1400), 2),

    matrix.add_point(calibrate_i(-4501), calibrate_i(4401), 2),
    matrix.add_point(calibrate_i(-4101), calibrate_i(3001), 2),
    matrix.add_point(calibrate_i(-1801), calibrate_i(2401), 2),
    matrix.add_point(calibrate_i(-2501), calibrate_i(3401), 2),
    matrix.add_point(calibrate_i(-2001), calibrate_i(1401), 2)

    # Initialize points for "P"
    matrix.add_point(calibrate_i(4500), calibrate_i(4400), 3),
    matrix.add_point(calibrate_i(4100), calibrate_i(3000), 3),
    matrix.add_point(calibrate_i(1800), calibrate_i(2400), 3),
    matrix.add_point(calibrate_i(2500), calibrate_i(3400), 3),
    matrix.add_point(calibrate_i(2000), calibrate_i(1400), 3),

    matrix.add_point(calibrate_i(4501), calibrate_i(4401), 3),
    matrix.add_point(calibrate_i(4101), calibrate_i(3001), 3),
    matrix.add_point(calibrate_i(1801), calibrate_i(2401), 3),
    matrix.add_point(calibrate_i(2501), calibrate_i(3401), 3),
    matrix.add_point(calibrate_i(2001), calibrate_i(1401), 3)

def calibrate_i(index: int) -> int:
    return index + size

def decalibrate_i(index: int) -> int:
    return index - size


def calculate_accuracy(matrix):
    dic = {
        1: [0, 0],
        2: [0, 0],
        3: [0, 0],
        4: [0, 0]
    }

    for point in matrix.point_map.values():
        if point.color == 0:
            #red
            if point.x < calibrate_i(500) and point.y < calibrate_i(500):
                dic[1][1] += 1
            dic[1][0] += 1
        elif point.color == 1:
            #green
            if point.x > calibrate_i(-500) and point.y < calibrate_i(500):
                dic[2][1] += 1
            dic[2][0] += 1
        elif point.color == 2:
            if point.x < calibrate_i(500) and point.y > calibrate_i(-500):
                dic[3][1] += 1
            dic[3][0] += 1
        elif point.color == 3:
            if point.x > calibrate_i(-500) and point.y > calibrate_i(-500):
                dic[4][1] += 1
            dic[4][0] += 1
        else:
            print("Error")

    return dic

def print_statistics(dic):
    _return = []
    for key in dic:
        total = dic[key][0]
        count = dic[key][1]
        percentage = (count / total) * 100 if total > 0 else 0
        _return += f"Color {key}: {count}/{total} ({percentage:.2f}%)" + "\n"
    return _return

def color(matrix, k):
    tree = KDTree()
    for point in matrix.point_map.values():
        if point.color == -1:
            nearest = tree.k_nearest_neighbors((point.x, point.y), k)
            _dic = defaultdict(float)
            #print(point, "-> ")
            for neighbor in nearest:
                _point = matrix.point_map[(neighbor[0], neighbor[1])]
                #print(_point)
                distance = np.sqrt((point.x - _point.x) ** 2 + (point.y - _point.y) ** 2)
                weight = 1 / (distance + 1e-5)
                _dic[_point.color] += weight

            point.color = max(_dic, key=_dic.get)
        tree.insert((point.x, point.y))
    return matrix

def _color(matrix, k):
    tree = KDTree()
    for point in matrix.point_map.values():
        if point.color == -1:
            nearest = tree.k_nearest_neighbors((point.x, point.y), k)
            _dic = defaultdict(float)
            #print(point, "-> ")
            for neighbor in nearest:
                _point = matrix.point_map[(neighbor[0], neighbor[1])]
                #print(_point)
                distance = np.sqrt((point.x - _point.x) ** 2 + (point.y - _point.y) ** 2)
                weight = 1 / (distance + 1e-5)  # Add a small value to avoid division by zero
                _dic[_point.color] += weight

            point.color = max(_dic, key=_dic.get)
        tree.insert((point.x, point.y))
    return matrix


def main() :
    # Example usage
    matrix = Matrix(size)
    basi_init(matrix)

    dic = {
        0: [-size, size / 10, -size, size / 10],
        1: [-size / 10, size, -size , size / 10],
        2: [-size, size / 10, -size / 10, size],
        3: [-size / 10, size, -size / 10, size]
    }

    for i in range(0, 40000):
        matrix.add_point_force(calibrate_i(dic[i % 4][0]), calibrate_i(dic[i % 4][1]), calibrate_i(dic[i % 4][2]), calibrate_i(dic[i % 4][3]), -1)

    ks = [1, 3, 7, 15, 30]

    for i in ks:
        print(f"K = {i}")
        k = color(copy.deepcopy(matrix), i)
        k.display_field()
        print("".join(print_statistics(calculate_accuracy(k))))


if __name__ == "__main__":
    main()
