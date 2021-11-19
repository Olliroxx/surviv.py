JS_MAX_VALUE = 2**1024-1


def lerp(point, low, high):
    return low * (1 - point) + high * point


class GenericXYObject:
    """
    An object with an x and a y component
    """
    def __init__(self, x, y):
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError
        self.x = x
        self.y = y

    def __getitem__(self, item):
        items = {
            "x": self.x,
            "y": self.y,
            0: self.x,
            1: self.y
        }
        if item in items:
            return items[item]
        raise KeyError(item)

    def __str__(self):
        return str((self.x, self.y))

    def __repr__(self):
        return str(self)

    def __iter__(self):
        return iter((self.x, self.y))

    def __eq__(self, other):
        other = Point(*other)
        return self.x == other.x and self.y == other.y


class Point(GenericXYObject):
    def copy(self):
        return Point(self.x, self.y)

    def length(self):
        from math import sqrt
        return sqrt(self.x * self.x + self.y * self.y)

    def add_point(self, point):
        return Point(self.x + point.x, self.y + point.y)

    def sub_point(self, point):
        return Point(self.x - point.x, self.y - point.y)

    def mul_point(self, point):
        return Point(self.x * point.x, self.y * point.y)

    def div_point(self, point):
        return Point(self.x / point.x, self.y / point.y)

    def add(self, val):
        return Point(self.x + val, self.y + val)

    def sub(self, val):
        return Point(self.x - val, self.y - val)

    def mul(self, val):
        return Point(self.x * val, self.y * val)

    def div(self, val):
        return Point(self.x / val, self.y / val)

    def normalise(self):
        threshold = 0.000001
        length = self.length()
        x = self.x / length if length > threshold else self.x
        y = self.y / length if length > threshold else self.y
        return Point(x, y)

    def perp(self):
        return self.rot_90_aclk()

    def distance_to(self, point):
        from math import sqrt
        diff_x = abs(self.x - point.x)
        diff_y = abs(self.y - point.y)
        return sqrt(diff_x ** 2 + diff_y ** 2)

    def min(self, point):
        return Point(
            min(self.x, point.x),
            min(self.y, point.y)
        )

    def max(self, point):
        return Point(
            max(self.x, point.x),
            max(self.y, point.y)
        )

    def dot(self, point):
        return self.x*point.x + self.y*point.y

    def rot_90_clk(self):
        """
        If you made a shape and used this on all the points, the shape would rotate 90 degrees around the origin
        """
        return Point(self.y, -self.x)

    def rot_90_aclk(self):
        """
        This is the same as rot_90_clk, but anticlockwise
        """
        return Point(-self.y, self.x)

    def rot_180(self):
        return Point(-self.x, -self.y)


class Vector:
    # You just got vectored
    """
    A vector class, nothing special
    """
    def __init__(self, *args, **kwargs):
        if args:
            if len(args) == 2:
                self.x = args[0]
                self.y = args[1]
                return

            elif type(args[0]) in (tuple, list):
                self.x = args[0][0]
                self.y = args[0][1]

            elif type(args[0]) == dict:
                self.x = args[0]["x"] if "x" in args[0] else args[0]["X"]
                self.y = args[0]["y"] if "y" in args[0] else args[0]["Y"]

            elif type(args[0]) == Vector:
                self.x = args[0].x
                self.y = args[0].y

            else:
                raise ValueError

        elif kwargs:
            self.x = kwargs["x"] if "x" in kwargs else kwargs["X"]
            self.y = kwargs["y"] if "y" in kwargs else kwargs["Y"]

        else:
            raise ValueError

    def __getitem__(self, item):
        items = {
            "x": self.x,
            "y": self.y,
            0: self.x,
            1: self.y
        }
        if item in items:
            return items[item]
        raise KeyError(item)

    @staticmethod
    def get_degrees(x, y):
        """
        Get degrees between "north" and vector
        """
        from math import atan2, degrees
        return degrees(atan2(y, x))

    @staticmethod
    def from_degrees(degrees):
        """
        Make a unit vector from degrees
        """
        from math import sin, cos, radians
        return Vector(cos(radians(degrees)), sin(radians(degrees)))

    @staticmethod
    def to_unit(x, y):
        """
        Scales the input vector to a unit vector
        """
        return Vector.from_degrees(Vector.get_degrees(x, y))


class MxPlusCLine:
    """
    Infinitely long line
    """
    def __init__(self, m, c):
        """
        A line with the equation y=mx+c

        :param m: Gradient
        :param c: Offset
        """
        self.m = m
        self.c = c

    def get_y(self, x):
        return self.m * x + self.c

    def get_x(self, y):
        return (y - self.c) / self.m

    def get_intersect(self, line):
        if line.m == self.m:
            raise ValueError("Lines with the same gradient")
        x = (line.c - self.c) / (self.m - line.m)
        y = line.get_y(x)
        return Point(x, y)

    @staticmethod
    def from_points(point1, point2):
        diff_x = point1.x - point2.x
        diff_y = point1.y - point2.y
        m = diff_y / diff_x
        if not m:
            c = point1.y
        else:
            c = point1.y - (point1.x * m)
        return MxPlusCLine(m, c)

    @staticmethod
    def perp_line_and_point(line, point):
        m = -1 / line.m
        c = point.y / (point.x * m)
        return MxPlusCLine(m, c)

    @staticmethod
    def from_line_and_offset(line, offset):
        import math
        angle_at_y = math.atan(line.m)
        c = offset / math.sin(angle_at_y + 90)
        return MxPlusCLine(line.m, c)


class EndpointLine:
    """
    Finite length line
    """
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str((self.start, self.end))

    def get_mx_plus_c(self):
        return MxPlusCLine.from_points(self.start, self.end)

    def is_point_on_line(self, point):
        mxc = self.get_mx_plus_c()
        # Have to use strings because rounding errors can mess with things
        if str(point.y)[:5] == str(mxc.get_y(point.x))[:5] and sorted((point.x, self.start.x, self.end.x))[1] == point.x:
            # Check if point is on mx+c line and point is between endpoints
            return True
        else:
            return False

    def ep_line_intersect(self, line):
        mxc1 = self.get_mx_plus_c()
        mxc2 = line.get_mx_plus_c()
        try:
            intersect = mxc1.get_intersect(mxc2)
        except ValueError:
            return None
        if self.is_point_on_line(intersect) and line.is_point_on_line(intersect):
            return intersect
        else:
            return None

    @staticmethod
    def lines_from_poly(poly):
        if isinstance(poly, Poly):
            poly = poly.points
        lines = []
        for num, point in enumerate(poly):
            lines.append(EndpointLine(point, poly[num - 1]))
        return lines


class Poly:
    def __init__(self, points=None):
        """
        Can take a list of points or a list of x/y coordinates
        """
        if points:
            if isinstance(points[0], Point):
                self.points = points
            else:
                self.points = []
                for point in points:
                    self.points.append(Point(*point))

            x, y = zip(*points)
            self.mid = Point(sum(x) / len(x), sum(y) / len(y))
            self.edges = EndpointLine.lines_from_poly(self.points)

        else:
            self.points = []

    def __getitem__(self, item):
        return self.points[item]

    def __setitem__(self, key, value):
        self.points[key] = value
        self.edges = EndpointLine.lines_from_poly(self.points)

    def __len__(self):
        return len(self.points)

    def point_in_poly(self, point):
        point_in_poly = False
        source_x = max([x[0] for x in self.points]) + 1
        source_y = max([x[1] for x in self.points]) + 1
        source = Point(source_x, source_y)
        ray = EndpointLine(point, source)

        for edge in self.edges:
            if ray.ep_line_intersect(edge) and ray.ep_line_intersect(edge) != edge.end:
                point_in_poly = not point_in_poly

        return point_in_poly


class SeededRandGenerator:
    """
    Not very random, same algo as the shore line generator
    """
    def __init__(self, seed):
        self.seed = seed

    def gen(self, min_val=0, max_val=1):
        self.seed = self.seed * 16807 % 2147483647
        return lerp((self.seed / 2147483647), min_val, max_val)


class Rect:
    def __init__(self, bl: Point, tr: Point):
        self.bl = bl
        self.tr = tr
        self.br = Point(tr.x, bl.y)
        self.tl = Point(bl.x, tr.y)

        self.width = tr.x - bl.x
        self.height = tr.y - bl.y

        self.max_x = tr.x
        self.max_y = tr.y
        self.min_x = bl.x
        self.min_y = bl.y

    @staticmethod
    def from_corners(p1, p2):
        """
        A rectangle from opposite corners
        """
        p3 = Point(p1.x, p2.y)
        p4 = Point(p2.x, p1.y)
        highest = p1
        lowest = p1
        for point in (p2, p3, p4):
            if point.x + point.y > highest.x + highest.y:
                highest = point
            if point.x + point.y < lowest.x + lowest.y:
                lowest = point
        return Rect(lowest, highest)

    def clamp_point(self, point):
        """
        Return the point in the rectangle closest to the input point (the returned point could be the same as the input)
        """
        y = sorted((self.min_y, self.max_y, point.y))[1]
        x = sorted((self.min_x, self.max_x, point.x))[1]
        return Point(x, y)

    def to_poly(self):
        return Poly([self.br, self.bl, self.tl, self.tr])
