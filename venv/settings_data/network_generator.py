import math
import random
from itertools import product, permutations, combinations
from dataclasses import dataclass
import networkx as nx
import settings
import numpy as np


@dataclass(eq=True, frozen=True)
class Node:
    x: int
    y: int
    index: int

    def get_distance(self, x, y) -> float:
        return pythag(self.x, self.y, x, y)

    def __post_init__(self):
        object.__setattr__(self, "pos", np.array([float(self.x), float(self.y)]))


@dataclass(eq=True, frozen=True)
class Edge:
    node_1: Node
    node_2: Node

    def get_length(self) -> float:
        return pythag(self.node_1.x, self.node_1.y, self.node_2.x, self.node_2.y)

    def get_angle(self) -> float:
        return theta_calc((0, 0, 1, 0), (self.node_1.x, self.node_1.y, self.node_2.x, self.node_2.y))
    
    def has_node(self, node):
        return node == self.node_1 or node == self.node_2
    
    def __lt__(self, other):
        return self.get_length() < other.get_length()
    
    # def cross(self, other, ignore_endpoints=False):
    #     return cross_check_2((self.node_1.x, self.node_1.y), (self.node_2.x, self.node_2.y),
    #                          (other.node_1.x, other.node_1.y), (other.node_2.x, other.node_2.y))

    def cross(self, other):
        return segment_intersect(self.node_1.pos, self.node_2.pos, other.node_1.pos, other.node_2.pos)


def polygon_test(x, y, polygon, positive):
    if polygon_check((x, y), polygon) and positive:
        return True
    elif not polygon_check((x, y), polygon) and not positive:
        return True
    return False


def network_gen(X, Y, data):
    fields = ["seed", "random_state", "nodes", "knn", "node_space_ll", "node_space_ul", "p_space", "spacing",
              "start_rect", "end_rect", "min_edge_angle", "shapes", "positive"]
    nodes = 30
    if "random_state" in data:
        random.setstate(data["random_state"])
    if "nodes" in data:
        nodes = data["nodes"]
    node_list = []  # list to hold nodes
    edge_list = []  # list to hold edges
    knn = 5
    if "knn" in data:
        knn = data["knn"]
    ul = 350  # parameter, upper limit of edge length
    if "node_space_ul" in data:
        ul = data["node_space_ul"]
    ll = 0  # parameter, lower limit of path length
    if "node_space_ll" in data:
        ll = data["node_space_ll"]
    p_space = 99  # parameter, probability of ignoring spacing parameter
    if "p_space" in data:
        p_space = data["p_space"]
    spacing = 90  # parameter, defines minimum node spacing
    if "spacing" in data:
        spacing = data["spacing"]
    # calculate mandatory region for starting node, based on xy_bounds
    start_bound = None
    if "start_rect" in data:
        start_bound = data["start_rect"]
    end_bound = None
    if "end_rect" in data:
        end_bound = data["end_rect"]
    theta_min = 15  # parameter, defines angular spacing minimum for edges around a node
    if "min_edge_angle" in data:
        theta_min = data["min_edge_angle"]
    shapes = None
    if "shapes" in data:
        shapes = data["shapes"]
    positive = True
    if "positive" in data:
        positive = data["positive"]
    theta_flag = False  # shouldn't be needed, simplify code
    flag = False

    # start node
    x = random.randint(start_bound[0], start_bound[2])
    y = random.randint(start_bound[1], start_bound[3])
    node_list.append(Node(x, y, 1))

    # end node
    x = random.randint(end_bound[0], end_bound[2])
    y = random.randint(end_bound[1], end_bound[3])
    node_list.append(Node(x, y, 0))

    count = 0
    index = 2
    while len(node_list) < nodes:
        # print(count)
        count += 1
        if count % nodes == 0:
            spacing -= 1
        x = random.randint(0, X)
        y = random.randint(0, Y)

        valid = [True]
        if shapes:
            valid = [True if polygon_test(x, y, polygon, positive) else False for polygon in shapes]

        if True in valid:
            for node in node_list:
                if node.get_distance(x, y) < spacing:
                    break
            else:
                node_list.append(Node(x, y, index))
                index += 1

    edge_list_ = set()

    for node in node_list:
        candidates = [x for x in node_list if ul > node.get_distance(x.x, x.y) > ll]
        for i in range(knn):
            if candidates:
                c_node = random.choice(candidates)
                candidates.remove(c_node)
                if node.index > c_node.index:
                    new_edge = Edge(node, c_node)
                else:
                    new_edge = Edge(c_node, node)
                for edge in edge_list_:
                    if share_node((new_edge.node_1.x, new_edge.node_1.y,new_edge.node_2.x,new_edge.node_2.y),
                                  (edge.node_1.x, edge.node_1.y, edge.node_2.x, edge.node_2.y)):
                        pass
                    elif edge.cross(new_edge):
                        break
                else:
                    edge_list_.add(new_edge)


    g = nx.Graph()

    for node in node_list:
        g.add_node(node.index, x=node.x, Y=node.y)

    for edge in edge_list_:
        g.add_edge(edge.node_1.index, edge.node_2.index)

    valid_path = nx.has_path(g, 0, 1)
    num_isolates = nx.number_of_isolates(g)
    set_island_check = set()
    number_islands = 0
    for i, value in enumerate(node_list):
        if set_island_check.__contains__(i):
            list_island_check = list(nx.dfs_preorder_nodes(g, i))
            for i, value in enumerate(list_island_check):
                set_island_check.remove(value)
            number_islands += 1
    if nx.is_connected(g):
        average_shortest_path_length = nx.average_shortest_path_length(g)
    else:
        average_shortest_path_length = "N/A"

    edge_connectivity = nx.edge_connectivity(g)
    for i, value in enumerate(node_list):
        set_island_check.add(i)

    neighbors_dict = {}
    edge_dict = []

    for i, value in enumerate(node_list):
        neighbors_dict[value.index] = [n for n in g.neighbors(value.index)]
        edge_dict = [i for i in g.edges]

    data["random_state"] = random.getstate()

    return [node_list, edge_list, neighbors_dict, edge_dict, valid_path], data


# def polygon_check(point, polygon):
#     check_point = (point[0] + 5000, point[1])
#     check_point_b = (point[0], point[1] + 5000)
#     n = 0
#     a = None
#     b = None
#     for i in range(len(polygon)):
#         if cross_check_2(point, check_point, polygon[i - 1], polygon[i]):
#             n += 1
#     if n % 2 == 1:
#         a = True
#     n = 0
#     for i in range(len(polygon)):
#         if cross_check_2(point, check_point_b, polygon[i - 1], polygon[i]):
#             n += 1
#     if n % 2 == 1:
#         b = True
#     if a and b:
#         return True
#     return False


def polygon_check(point, polygon):
    check_point = np.array([point[0] + 5000, point[1]])
    check_point_b = np.array([point[0], point[1] + 5000])
    n = 0
    a = None
    b = None
    for i in range(len(polygon)):
        if segment_intersect(point, check_point, np.array(polygon[i - 1]), np.array(polygon[i])):
            n += 1
    if n % 2 == 1:
        a = True
    n = 0
    for i in range(len(polygon)):
        if segment_intersect(point, check_point_b, np.array(polygon[i - 1]), np.array(polygon[i])):
            n += 1
    if n % 2 == 1:
        b = True
    if a and b:
        return True
    return False


def theta_calc(a, b):
    avx = a[0] - a[2]
    avy = a[1] - a[3]
    bvx = b[0] - b[2]
    bvy = b[1] - b[3]
    num = (avx * bvx) + (avy * bvy)
    den = (math.sqrt((avx ** 2) + (avy ** 2)) * math.sqrt((bvx ** 2) + (bvy ** 2)))
    if abs(num / den) > 1:
        qot = 1
    else:
        qot = num / den
    rad = math.acos(qot)
    deg = rad * 180 / 3.14159
    return deg


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def on_segment(p, q, r, ignore_endpoints=False):
    if ((q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
            (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
        return True
    return False


def orientation(p, q, r):
    val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
    if (val > 0):
        return 1
    elif (val < 0):
        return 2
    else:
        return 0


def perp(a):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


def segment_intersect(a1, a2, b1, b2) -> bool:
    da = a2 - a1
    db = b2 - b1
    dp = a1 - b1
    dap = perp(da)
    denom = np.dot(dap, db)
    num = np.dot(dap, dp)
    if denom != 0:
        point = (num / denom) * db + b1
    else:
        point = (num / 0.01) * db + b1
    if point[0] > a1[0] and point[0] > a2[0]:
        return False
    elif point[0] < a1[0] and point[0] < a2[0]:
        return False
    return True


def do_intersect(p1, q1, p2, q2, ignore_endpoints=False):
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if (o1 != o2) and (o3 != o4):
        return True

    if not ignore_endpoints:
        if (o1 == 0) and on_segment(p1, p2, q1):
            return True
        if (o2 == 0) and on_segment(p1, q2, q1):
            return True
        if (o3 == 0) and on_segment(p2, p1, q2):
            return True
        if (o4 == 0) and on_segment(p2, q1, q2):
            return True
    return False


def cross_check_2(a, b, c, d, ignore_endpoints=False):
    p1 = a[0], a[1]
    q1 = b[0], b[1]
    p2 = c[0], c[1]
    q2 = d[0], d[1]
    if do_intersect(p1, q1, p2, q2, ignore_endpoints):
        return True
    return False


def share_node(value, pair):
    A = (value[0], value[1])
    B = (value[2], value[3])
    C = (pair[0], pair[1])
    D = (pair[2], pair[3])
    if A[0] == C[0] and A[1] == C[1]:
        return True
    elif A[0] == D[0] and A[1] == D[1]:
        return True
    elif B[0] == C[0] and B[1] == C[1]:
        return True
    elif B[0] == D[0] and B[1] == D[1]:
        return True


def cross_check(elist):
    for i, value in enumerate(elist):
        elist[i][5] = 0
    for i, value in enumerate(elist):
        for j, pair in enumerate(elist[i + 1:]):
            A = (value[0], value[1])
            B = (value[2], value[3])
            C = (pair[0], pair[1])
            D = (pair[2], pair[3])
            if share_node(value, pair):
                pass
            elif cross_check_2(A, B, C, D):
                elist[i][5] += 1
    elist = sorted(elist, key=lambda x: x[5])
    return elist


def pythag(a, b, c, d):
    distance = int(math.sqrt(((a - c) ** 2) + ((b - d) ** 2)))
    return distance
