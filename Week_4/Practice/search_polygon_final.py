from collections import defaultdict
from queue import Queue, PriorityQueue
import math
from matplotlib import pyplot as plt


class Point(object):
    def __init__(self, x, y, polygon_id=-1):
        self.x = x
        self.y = y
        self.polygon_id = polygon_id
        self.g = 0
        self.pre = None

    def rel(self, other, line):
        return line.d(self) * line.d(other) >= 0

    # giữ lại phiên bản cũ cho đủ định nghĩa, nhưng Graph.can_see mới sẽ được dùng
    def can_see(self, other, line):
        l1 = self.line_to(line.p1)
        l2 = self.line_to(line.p2)
        d3 = line.d(self) * line.d(other) < 0
        d1 = other.rel(line.p2, l1)
        d2 = other.rel(line.p1, l2)
        return not (d1 and d2 and d3)

    def line_to(self, other):
        return Edge(self, other)

    def heuristic(self, other):
        return euclid_distance(self, other)

    def __eq__(self, point):
        return point and self.x == point.x and self.y == point.y

    def __ne__(self, point):
        return not self.__eq__(point)

    def __lt__(self, point):
        return hash(self) < hash(point)

    def __str__(self):
        return "(%d, %d)" % (self.x, self.y)

    def __hash__(self):
        return self.x.__hash__() ^ self.y.__hash__()

    def __repr__(self):
        return "(%d, %d)" % (self.x, self.y)


class Edge(object):
    def __init__(self, point1, point2):
        self.p1 = point1
        self.p2 = point2

    def get_adjacent(self, point):
        if point == self.p1:
            return self.p2
        if point == self.p2:
            return self.p1

    def d(self, point):
        vect_a = Point(self.p2.x - self.p1.x, self.p2.y - self.p1.y)
        vect_n = Point(-vect_a.y, vect_a.x)
        return vect_n.x * (point.x - self.p1.x) + vect_n.y * (point.y - self.p1.y)

    def __str__(self):
        return "({}, {})".format(self.p1, self.p2)

    def __contains__(self, point):
        return self.p1 == point or self.p2 == point

    def __hash__(self):
        return self.p1.__hash__() ^ self.p2.__hash__()

    def __repr__(self):
        return "Edge({!r}, {!r})".format(self.p1, self.p2)


class Graph:
    def __init__(self, polygons):
        self.graph = defaultdict(set)
        self.edges = set()
        self.polygons = defaultdict(set)
        pid = 0
        for polygon in polygons:
            if len(polygon) == 2:
                polygon.pop()
            if polygon[0] == polygon[-1]:
                self.add_point(polygon[0])
            else:
                for i, point in enumerate(polygon):
                    neighbor_point = polygon[(i + 1) % len(polygon)]
                    edge = Edge(point, neighbor_point)
                    if len(polygon) > 2:
                        point.polygon_id = pid
                        neighbor_point.polygon_id = pid
                        self.polygons[pid].add(edge)
                    self.add_edge(edge)
                if len(polygon) > 2:
                    pid += 1

    def get_adjacent_points(self, point):
        # khử trùng ngay tại nguồn
        return list({
            adj for adj in (edge.get_adjacent(point) for edge in self.edges)
            if adj is not None
        })

    # Visibility: kiểm tra cắt đoạn với tất cả cạnh đa giác
    def can_see(self, start):
        visible = []
        for target in self.get_points():
            if target == start:
                continue
            segment = Edge(start, target)
            blocked = False
            for edges in self.polygons.values():
                for edge in edges:
                    # bỏ qua nếu trùng cạnh
                    if start in edge or target in edge:
                        continue
                    if self._intersect(segment, edge):
                        blocked = True
                        break
                if blocked:
                    break
            if not blocked:
                visible.append(target)
        return visible

    def _intersect(self, e1, e2):
        def ccw(A, B, C):
            return (C.y - A.y) * (B.x - A.x) > (B.y - A.y) * (C.x - A.x)
        A, B = e1.p1, e1.p2
        C, D = e2.p1, e2.p2
        return (ccw(A, C, D) != ccw(B, C, D)) and (ccw(A, B, C) != ccw(A, B, D))

    def get_polygon_points(self, index):
        point_set = set()
        for edge in self.polygons[index]:
            point_set.add(edge.p1)
            point_set.add(edge.p2)
        return point_set

    def get_points(self):
        return list(self.graph)

    def get_edges(self):
        return self.edges

    def add_point(self, point):
        self.graph[point].add(point)

    def add_edge(self, edge):
        self.graph[edge.p1].add(edge)
        self.graph[edge.p2].add(edge)
        self.edges.add(edge)

    def __contains__(self, item):
        if isinstance(item, Point):
            return item in self.graph
        if isinstance(item, Edge):
            return item in self.edges
        return False

    def __getitem__(self, point):
        if point in self.graph:
            return self.graph[point]
        return set()

    def __str__(self):
        res = ""
        for point in self.graph:
            res += "\n" + str(point) + ": "
            for edge in self.graph[point]:
                res += str(edge)
        return res

    def __repr__(self):
        return self.__str__()

    def h(self, point):
        heuristic = getattr(self, 'heuristic', None)
        if heuristic:
            return heuristic[point]
        else:
            return -1


def euclid_distance(point1, point2):
    return round(float(math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)), 3)

def neighbors_sorted(graph, node):
    # để kết quả ổn định giữa các lần chạy
    return sorted(graph.can_see(node), key=lambda p: (p.x, p.y))

def reset_points(graph):
    for p in graph.get_points():
        p.g = 0
        p.pre = None


def search(graph, start, goal, func):
    closed = set()
    queue = PriorityQueue()
    queue.put((0 + func(graph, start), start))
    if start not in closed:
        closed.add(start)
    while not queue.empty():
        cost, node = queue.get()
        if node == goal:
            return node
        for i in graph.can_see(node):
            new_cost = node.g + euclid_distance(node, i)
            if i not in closed or new_cost < i.g:
                closed.add(i)
                i.g = new_cost
                i.pre = node
                queue.put((func(graph, i), i))
    return None


a_star = lambda graph, i: i.g + graph.h(i)
greedy = lambda graph, i: graph.h(i)

#     BFS, DFS, UCS

def bfs_path(graph, start, goal):
    visited = set()
    frontier = Queue()
    parent = {start: None}
    frontier.put(start)
    visited.add(start)

    while not frontier.empty():
        current = frontier.get()
        if current == goal:
            break
        for neighbor in neighbors_sorted(graph, current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                frontier.put(neighbor)

    path = []
    if goal in parent:
        node = goal
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
    return path


def dfs_path(graph, start, goal):
    stack = [start]
    visited = {start}
    parent = {start: None}

    while stack:
        current = stack.pop()
        if current == goal:
            break
        for neighbor in reversed(neighbors_sorted(graph, current)):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)

    path = []
    if goal in parent:
        node = goal
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
    return path


def ucs_path(graph, start, goal):
    frontier = PriorityQueue()
    frontier.put((0, start))
    parent = {start: None}
    cost = {start: 0}

    while not frontier.empty():
        current_cost, current = frontier.get()
        if current == goal:
            break
        for neighbor in neighbors_sorted(graph, current):
            new_cost = current_cost + euclid_distance(current, neighbor)
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                parent[neighbor] = current
                frontier.put((new_cost, neighbor))

    path = []
    if goal in parent:
        node = goal
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
    return path


def main():
    n_polygon = 0
    poly_list = []
    x, y = [], []

    with open('Input.txt', 'r') as f:
        line = f.readline().strip().split()
        line = list(map(int, line))
        n_polygon = line[0]
        start = Point(line[1], line[2])
        goal = Point(line[3], line[4])
        poly_list.append([start])
        for line in f:
            point_list = []
            line = line.split()
            n_vertex = int(line[0])
            for j in range(0, 2 * n_vertex, 2):
                point_list.append(Point(int(line[j + 1]), int(line[j + 2])))
            poly_list.append(point_list[:])
    poly_list.append([goal])

    graph = Graph(poly_list)
    graph.heuristic = {point: point.heuristic(goal) for point in graph.get_points()}

    # A* 
    reset_points(graph)
    a = search(graph, start, goal, a_star)
    result = []
    node = a
    while node is not None:
        result.append(node)
        node = node.pre
    result.reverse()
    print_res = [(p, p.polygon_id) for p in result]
    print(*print_res, sep=' -> ')

    # BFS 
    reset_points(graph)
    bfs_result = bfs_path(graph, start, goal)

    # DFS 
    reset_points(graph)
    dfs_result = dfs_path(graph, start, goal)

    # UCS 
    reset_points(graph)
    ucs_result = ucs_path(graph, start, goal)

    print("\n[BFS PATH]:", [(p.x, p.y, p.polygon_id) for p in bfs_result])
    print("[DFS PATH]:", [(p.x, p.y, p.polygon_id) for p in dfs_result])
    print("[UCS PATH]:", [(p.x, p.y, p.polygon_id) for p in ucs_result])

    # Visualization (so sánh) 
    plt.figure(figsize=(8, 5))
    colors = {"BFS": "green", "DFS": "orange", "UCS": "purple", "A*": "blue"}
    algos = {"BFS": bfs_result, "DFS": dfs_result, "UCS": ucs_result, "A*": result}

    for name, path in algos.items():
        if len(path) > 1:
            xs = [p.x for p in path]
            ys = [p.y for p in path]
            plt.plot(xs, ys, label=name, linewidth=2.0, color=colors[name])

    for i in range(1, len(poly_list) - 1):
        coord = [(p.x, p.y) for p in poly_list[i]]
        coord.append(coord[0])
        xs, ys = zip(*coord)
        plt.plot(xs, ys, 'k', linewidth=1.0)

    plt.scatter(start.x, start.y, c='red', marker='o')
    plt.scatter(goal.x, goal.y, c='red', marker='o')
    plt.legend()
    plt.title("So sánh đường đi giữa BFS - DFS - UCS - A*")
    plt.show()

    # Visualization (A* riêng) 
    plt.figure()
    plt.plot([start.x], [start.y], 'ro')
    plt.plot([goal.x], [goal.y], 'ro')

    for point in graph.get_points():
        x.append(point.x)
        y.append(point.y)
    plt.plot(x, y, 'ro')

    for i in range(1, len(poly_list) - 1):
        coord = []
        for p in poly_list[i]:
            coord.append([p.x, p.y])
        coord.append(coord[0])
        xs, ys = zip(*coord)
        plt.plot(xs, ys)

    xs = [p.x for p in result]
    ys = [p.y for p in result]
    plt.plot(xs, ys, 'b', linewidth=2.0)
    plt.show()


if __name__ == "__main__":
    main()
