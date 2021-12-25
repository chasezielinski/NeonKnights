from shapely.geometry import Point, MultiPolygon, Polygon
import random
import time


class Test:
    test_list = ["shapely", "composite"]
    @staticmethod
    def start_test(bound, n_points, shapes, n_tests):
        tests = []
        for i in range(n_tests):
            tests += Test.test_list

        random.shuffle(tests)

        for test in tests:
            if test == "shapely":
                t1 = time.perf_counter()
                p = ShapelyTest().start_test(bound, n_points, shapes)
                t2 = time.perf_counter()
                print(f"test: {test}, percentage: {p}, time: {t2-t1}")

            elif test == "composite":
                t1 = time.perf_counter()
                p = CompositeTest().start_test(bound, n_points, shapes)
                t2 = time.perf_counter()
                print(f"test: {test}, percentage: {p}, time: {t2-t1}")


class ShapelyTest:
    def __init__(self):
        self.shapes = []
        self.collection = None
        self.points = []

    def start_test(self, bound, n, shapes):
        for shape in shapes:
            self.shapes.append(Polygon(shape))

        self.collection = MultiPolygon(self.shapes)

        for i in range(n):
            point = Point(self.get_point(bound))
            if self.collection.contains(point):
                self.points.append(point)

        return len(self.points) / n

    def get_point(self, bound):
        return random.randint(0, bound[0]), random.randint(0, bound[1])


class CompositeTest:
    def __init__(self):
        self.points = []

    def start_test(self, bound, n, shapes) -> float:
        for i in range(n):
            point = self.get_point(bound)
            for shape in shapes:
                if self.polygon_check(point, shape):
                    self.points.append(point)
                    break
        return len(self.points) / n

    def get_point(self, bound):
        return random.randint(0, bound[0]), random.randint(0, bound[1])

    def polygon_check(self, point, polygon):
        check_point = (point[0] + 5000, point[1])
        check_point_b = (point[0], point[1] + 5000)
        n = 0
        a = None
        b = None
        for i in range(len(polygon)):
            if self.cross_check_2(point, check_point, polygon[i - 1], polygon[i]):
                n += 1
        if n % 2 == 1:
            a = True
        n = 0
        for i in range(len(polygon)):
            if self.cross_check_2(point, check_point_b, polygon[i - 1], polygon[i]):
                n += 1
        if n % 2 == 1:
            b = True
        if a and b:
            return True
        return False

    def on_segment(self, p, q, r):
        if ((q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
                (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
            return True
        return False

    def orientation(self, p, q, r):
        val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
        if val > 0:
            return 1
        elif val < 0:
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

    def cross_check_2(self, a, b, c, d):
        p1 = a[0], a[1]
        q1 = b[0], b[1]
        p2 = c[0], c[1]
        q2 = d[0], d[1]
        if self.do_intersect(p1, q1, p2, q2):
            return True
        return False

