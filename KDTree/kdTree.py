import heapq  # Import for k-nearest neighbors

class KDTreeNode:
    def __init__(self, point, left=None, right=None):
        self.point = point  # The 2D point (x, y) stored in this node
        self.left = left    # Left subtree
        self.right = right  # Right subtree


class KDTree:
    def __init__(self):
        self.root = None

    def insert(self, point, depth=0):
        def _insert(node, point, depth):
            if node is None:
                return KDTreeNode(point)

            axis = depth % 2
            if point[axis] < node.point[axis]:
                node.left = _insert(node.left, point, depth + 1)
            else:
                node.right = _insert(node.right, point, depth + 1)
            return node

        self.root = _insert(self.root, point, depth)

    def nearest_neighbor(self, target, depth=0, best=None):
        def _nearest(node, target, depth, best):
            if node is None:
                return best

            point = node.point
            dist = (point[0] - target[0]) ** 2 + (point[1] - target[1]) ** 2
            if best is None or dist < best[1]:
                best = (node.point, dist)

            axis = depth % 2
            next_branch = node.left if target[axis] < point[axis] else node.right
            opposite_branch = node.right if target[axis] < point[axis] else node.left

            best = _nearest(next_branch, target, depth + 1, best)

            if (target[axis] - point[axis]) ** 2 < best[1]:
                best = _nearest(opposite_branch, target, depth + 1, best)

            return best

        best = _nearest(self.root, target, depth, best)
        return best[0]

    def k_nearest_neighbors(self, target, k, depth=0):
        heap = []

        def _k_nearest(node, target, depth):
            if node is None:
                return

            point = node.point
            dist = (point[0] - target[0]) ** 2 + (point[1] - target[1]) ** 2

            if len(heap) < k:
                heapq.heappush(heap, (-dist, point))
            else:
                if dist < -heap[0][0]:
                    heapq.heappushpop(heap, (-dist, point))

            axis = depth % 2
            next_branch = node.left if target[axis] < point[axis] else node.right
            opposite_branch = node.right if target[axis] < point[axis] else node.left

            _k_nearest(next_branch, target, depth + 1)

            if (target[axis] - point[axis]) ** 2 < -heap[0][0] or len(heap) < k:
                _k_nearest(opposite_branch, target, depth + 1)

        _k_nearest(self.root, target, depth)
        return [point for _, point in sorted(heap, reverse=True)]