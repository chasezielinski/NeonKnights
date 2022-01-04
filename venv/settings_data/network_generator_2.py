import math
import random
from itertools import product, permutations, combinations
from dataclasses import dataclass
import networkx as nx
import settings
from shapely.geometry import Point, MultiPolygon, Polygon


@dataclass(eq=True, frozen=True)
class Node:
    x: int
    y: int
    index: int

    def get_distance(self, x, y) -> float:
        return (self.x - x) ** 2 + (self.y - y) ** 2


@dataclass(eq=True, frozen=True)
class Edge:
    node_1: Node
    node_2: Node

    def neighbor(self, node):
        if self.node_1 == node:
            return self.node_2
        elif self.node_2 == node:
            return self.node_1

    def get_length(self) -> float:
        return (self.node_1.x - self.node_2.x)**2 + (self.node_1.y - self.node_2.y)**2

    # def get_angle(self) -> float:
    #     return theta_calc((0, 0, 1, 0), (self.node_1.x, self.node_1.y, self.node_2.x, self.node_2.y))

    def has_node(self, node):
        return node == self.node_1 or node == self.node_2

    def __lt__(self, other):
        return self.get_length() < other.get_length()

    def cross(self, other):
        return self.cross_check_2((self.node_1.x, self.node_1.y), (self.node_2.x, self.node_2.y),
                             (other.node_1.x, other.node_1.y), (other.node_2.x, other.node_2.y))

    def share_node(self, other):
        return self.node_1 == other.node_1 or self.node_1 == other.node_2 \
               or self.node_2 == other.node_1 or self.node_2 == other.node_2

    def on_segment(self, p, q, r, ignore_endpoints=False):
        if ((q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
                (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
            return True
        return False

    def orientation(self, p, q, r):
        val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
        if (val > 0):
            return 1
        elif (val < 0):
            return 2
        else:
            return 0

    def do_intersect(self, p1, q1, p2, q2, ignore_endpoints=False):
        o1 = self.orientation(p1, q1, p2)
        o2 = self.orientation(p1, q1, q2)
        o3 = self.orientation(p2, q2, p1)
        o4 = self.orientation(p2, q2, q1)

        if (o1 != o2) and (o3 != o4):
            return True

        if not ignore_endpoints:
            if (o1 == 0) and self.on_segment(p1, p2, q1):
                return True
            if (o2 == 0) and self.on_segment(p1, q2, q1):
                return True
            if (o3 == 0) and self.on_segment(p2, p1, q2):
                return True
            if (o4 == 0) and self.on_segment(p2, q1, q2):
                return True
        return False

    def cross_check_2(self, a, b, c, d, ignore_endpoints=False):
        p1 = a[0], a[1]
        q1 = b[0], b[1]
        p2 = c[0], c[1]
        q2 = d[0], d[1]
        if self.do_intersect(p1, q1, p2, q2, ignore_endpoints):
            return True
        return False


class NetworkGenerator:
    defaults = {
        "random_state": None,
        "nodes": 30,
        "knn": 4,
        "node_space_ul": 350,
        "node_space_ll": 0,
        "p_space": 100,
        "spacing": 50,
        "start_rect": None,
        "end_rect": None,
        "min_edge_angle": 5,
        "shapes": None,
    }

    def __init__(self, x, y, data):
        fields = ["random_state", "nodes", "knn", "node_space_ul", "node_space_ll", "p_space", "spacing", "start_rect",
                  "end_rect", "min_edge_angle", "shapes"]
        for key, value in NetworkGenerator.defaults.items():
            setattr(self, key, value)
        self.shapes = [((0, 0), (x, 0), (x, y), (0, y))]
        for key, value in data.items():
            if key in fields:
                setattr(self, key, value)
        self.x_bound = x
        self.y_bound = y
        self.node_list = []
        self.spacing_compare = self.spacing**2
        self.ul_compare = self.node_space_ul**2
        self.data = data

    def get_region(self):
        x, y = self.get_point(rect_bound=self.start_rect)
        self.node_list.append(Node(x, y, 1))
        x, y = self.get_point(rect_bound=self.end_rect)
        self.node_list.append(Node(x, y, 0))
        polygons = [Polygon(**x) for x in self.shapes]
        multigon = MultiPolygon(polygons)

        while len(self.node_list) < self.nodes:
            point = Point(self.get_point(spacing=True))
            if multigon.contains(point):
                self.node_list.append(Node(point.x, point.y, len(self.node_list)))

        self.edge_list = set()
        for node in self.node_list:
            candidates = [x for x in self.node_list
                                       if self.ul_compare > node.get_distance(x.x, x.y) > self.spacing_compare]
            for i in range(self.knn):
                if candidates:
                    c_node = candidates.pop(candidates.index(random.choice(candidates)))
                    if node.index > c_node.index:
                        new_edge = Edge(node, c_node)
                    else:
                        new_edge = Edge(c_node, node)
                    for edge in self.edge_list:
                        if not edge.share_node(new_edge):
                            if edge.cross(new_edge):
                                break
                    else:
                        self.edge_list.add(new_edge)
        graph = {node.index: {edge.neighbor(node).index for edge in self.edge_list if edge.has_node(node)}
                 for node in self.node_list}

        valid_path = 0 in self.depth_first_search(graph, 1)

        edge_list = [(x.node_1.index, x.node_2.index) for x in self.edge_list]

        self.data["random_state"] = random.getstate()

        return self.node_list, graph, edge_list, valid_path, self.data

    def depth_first_search(self, graph, start, visited=None):
        if visited is None:
            visited = set()
        visited.add(start)

        for next in graph[start] - visited:
            self.depth_first_search(graph, next, visited)
        return visited

    def get_point(self, rect_bound=None, spacing=False):
        if spacing:
            while 1:
                x = random.randint(0, self.x_bound)
                y = random.randint(0, self.y_bound)
                for node in self.node_list:
                    if node.get_distance(x, y) < self.spacing_compare:
                        break
                else:
                    return x, y
        elif rect_bound:
            x = random.randint(rect_bound[0], rect_bound[2])
            y = random.randint(rect_bound[1], rect_bound[3])
            return x, y
        x = random.randint(0, self.x_bound)
        y = random.randint(0, self.y_bound)
        return x, y


