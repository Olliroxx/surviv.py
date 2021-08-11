from json import load
from src.survivpy_net.custom_types import Point, EndpointLine, Rect, Poly, MxPlusCLine, lerp, SeededRandGenerator
from logging import getLogger

logger = getLogger("survivpy_net")

JS_MAX_VALUE = 2 ** 1024 - 1

map_definitions = {}
constants = {}


def update_definitions():
    """
    Updates map definitions and constants, run by Map on __init__
    """

    global map_definitions
    global constants

    def_file = open("../../utils/net/configs/map_data.json")
    map_definitions = load(def_file)
    constants_file = open("../../utils/net/configs/constants.json")
    constants = load(constants_file)


class River:
    """
    Most of this is translated JS, so I don't know what most of it does
    The original used a spline, but this one doesn't because it's hard

    :param points: center points of the river
    :param width: river width
    :param looped: is the river a circle?
    :param other_rivers: Other rivers on the map that could be sources for this
    :param min_max: Top right map corner to center
    """

    def __init__(self, points, width, looped, other_rivers, min_max: Rect):

        if not constants:
            update_definitions()

        def _0x46712b(point1: Point, point2: Point, poly: Poly):
            point3 = point1.add_point(point2)
            if not poly.point_in_poly(point3):
                num = poly.ray_poly_intersect(EndpointLine(point1, point2))
                if num:
                    return point2.mul(num)
            return point2

        self.points = []
        for point in points:
            if not type(point) == Point:
                point = Point(*point)
            self.points.append(point)
        points = self.points

        self.water_width = width
        self.shore_width = sorted((4, 8, width * 0.75))[1]
        # Use sorted as clamp
        self.looped = looped
        self.min_max = min_max

        self.center = Point(0, 0)
        for point in points:
            self.center.add_point(point)
        self.center.div(len(points))
        # Average all points to make a center

        total_length = 0
        for point in points:
            point = point.copy()
            point.sub_point(self.center)
            total_length += point.length()
        average_length = total_length / len(points)

        halfway = min_max.bl.copy()
        halfway = halfway.sub_point(min_max.tr)
        halfway = halfway.mul(0.5)
        halfway = halfway.add_point(min_max.tr)

        lines = []
        for number, point in enumerate(points[:-1]):
            next_point = points[number + 1]
            lines.append(MxPlusCLine.from_line_and_offset(MxPlusCLine.from_points(point, next_point), 1))

        lines.insert(0, MxPlusCLine.perp_line_and_point(lines[0], points[0]))
        lines.insert(-1, MxPlusCLine.perp_line_and_point(lines[-1], points[-1]))
        # Add first and last lines

        normalised_points = []
        for number, line in enumerate(lines[:-1]):
            normalised_points.append(line.get_intersect(lines[number + 1]))
        # Make "normalised" (offset) points
        # If there are list of points representing a track, the normalised points are the points for the edge of the road

        water_poly = []
        shore_poly = []
        water_widths = []
        shore_widths = []

        for point_number, point in enumerate(points):
            normalised_point = normalised_points[point_number]
            modified_endpoint = False
            if not looped and (point_number == 0 or point_number == (len(points) - 1)):
                # If the point is the last or first point of a (non-looped) river
                halfway_subbed = point.sub_point(halfway)
                _0x867030 = Point(0, 0)
                _0x50e90b = Point(1, 0)
                if abs(halfway_subbed.x) > abs(halfway_subbed.y):
                    if halfway_subbed.x > 0:
                        x = min_max.tr.x
                    else:
                        x = min_max.bl.x
                    _0x867030 = Point(x, point.y)
                    _0x50e90b = Point(1 if halfway_subbed.x > 0 else -1, 0)
                else:
                    if halfway_subbed.y > 0:
                        y = min_max.tr.y
                    else:
                        y = min_max.bl.y
                    _0x867030 = Point(point.x, y)
                    _0x50e90b = Point(0, 1 if halfway_subbed.y > 0 else -1)
                if _0x867030.sub_point(point).length() ** 2 < 1:
                    _0x826f0 = _0x50e90b.perp()
                    if (normalised_point.x * _0x826f0.x + normalised_point.y * _0x826f0.y) < 0:
                        _0x826f0 = _0x826f0.mul(-1)
                        normalised_point = _0x826f0
                        modified_endpoint = True
                # Maybe something with if the start/end of a river is horizontal/vertical?
                # Possible incomplete

            water_width = self.water_width
            if not looped:
                _0x15454d = 2 * max(1 - point_number / len(points), point_number / len(points))
                water_width = (1 + _0x15454d ** 3 * 1 / 5) * self.water_width
            water_widths.append(water_width)

            shore_width = self.shore_width
            source_river = None
            for river in other_rivers:
                closest_pos = river.get_closest(point)
                source_river_dist = closest_pos.sub_point(point).length()
                if source_river_dist < water_width * 2:
                    shore_width = max(shore_width, self.shore_width)
                if (point_number == 0 or point_number == len(
                        points) - 1) and source_river_dist < 1.5 and not modified_endpoint:
                    source_river = river

            if point_number > 0:
                shore_width = (shore_widths[point_number - 1] + shore_width) / 2
            shore_widths.append(shore_width)
            shore_width += water_width

            if looped:
                _0xb6810b = point.sub_point(self.center)
                _0x473647 = _0xb6810b.length()
                _0xb6810b = _0xb6810b.div(_0x473647) if _0x473647 > 0.000 else Point(1, 0)
                _0x29a0be = lerp(min(water_width / average_length, 1) ** 0.5, water_width,
                                 (1 - (average_length - water_width) / _0x473647) * _0x473647)
                _0x2bde26 = lerp(min(shore_width / average_length, 1) ** 0.5, shore_width,
                                 (1 - (average_length - shore_width) / _0x473647) * _0x473647)
                water_corner1 = point.add_point(_0xb6810b.mul(water_width))
                water_corner2 = point.add_point(_0xb6810b.mul(-_0x29a0be))
                shore_corner1 = point.add_point(_0xb6810b.mul(water_width))
                shore_corner2 = point.add_point(_0xb6810b.mul(-_0x2bde26))
            else:
                water_corner1 = point.mul(water_width)
                water_corner2 = point.mul(-water_width)
                shore_corner1 = point.mul(shore_width)
                shore_corner2 = point.mul(-shore_width)

                if source_river:

                    water_corner1 = _0x46712b(point, water_corner1, Poly(water_poly))
                    water_corner2 = _0x46712b(point, water_corner2, Poly(water_poly))
                    shore_corner1 = _0x46712b(point, shore_corner1, Poly(shore_poly))
                    shore_corner2 = _0x46712b(point, shore_corner2, Poly(shore_poly))

                    water_corner1 = point.add_point(water_corner1)
                    water_corner2 = point.add_point(water_corner2)
                    shore_corner1 = point.add_point(shore_corner1)
                    shore_corner2 = point.add_point(shore_corner2)

            water_corner1 = min_max.clamp_point(water_corner1)
            water_corner2 = min_max.clamp_point(water_corner2)
            shore_corner1 = min_max.clamp_point(shore_corner1)
            shore_corner2 = min_max.clamp_point(shore_corner2)

            water_poly.insert(point_number, water_corner1)
            water_poly.insert(len(water_poly) - point_number, water_corner2)
            shore_poly.insert(point_number, shore_corner1)
            shore_poly.insert(len(shore_poly) - point_number, shore_corner2)
        # Make shore+river polys
        furthest_bottom_left = Point(JS_MAX_VALUE, JS_MAX_VALUE)
        furthest_top_right = Point(-JS_MAX_VALUE, -JS_MAX_VALUE)
        for point_num in range(len(shore_poly)):
            furthest_bottom_left = furthest_bottom_left.min(shore_poly[point_num])
            furthest_top_right = furthest_top_right.max(shore_poly[point_num])

        self.rect = Rect(furthest_bottom_left, furthest_top_right)
        self.water_widths = water_widths
        self.shore_widths = shore_widths
        self.water_poly = water_poly
        self.shore_poly = shore_poly

    def __str__(self):
        return str((self.water_width, self.looped, self.points))

    def get_closest(self, target):
        closest = self.points[0]
        for point in self.points:
            if target.distance_to(point) < target.distance_to(closest):
                closest = point
        if self.points.index(closest) + 1 == len(self.points):
            second = self.points[self.points.index(closest) - 1]
        elif self.points.index(closest) - 1 == -1:
            second = self.points[self.points.index(closest) + 1]
        else:
            pre = self.points[self.points.index(closest) - 1]
            post = self.points[self.points.index(closest) + 1]
            second = pre if target.distance_to(pre) < target.distance_to(post) else post

        inf_line = MxPlusCLine.from_points(closest, second)
        perp_line = MxPlusCLine.perp_line_and_point(inf_line, target)
        intersection = inf_line.get_intersect(perp_line)
        if (second.x > intersection.x > closest.x or second.x < intersection.x < closest.x) and (
                second.y > intersection.y > closest.y or second.y < intersection.y < closest.y):
            return intersection
        else:
            return closest

    def distance_to_shore(self, target):
        shore_point = self.get_closest(target)
        dist_to_point = target.sub_point(shore_point).length()
        return max(dist_to_point, 0)


class Map:
    """
    Contains bullets, objects and everything else seen in the main view area.

    Properties of note:
     * map_name: gamemode, like classic, potato, cobalt
     * places: list of pieces of text that appear on the minimap
     * ground_patches: list of differently coloured patches on the ground (does not include shore, water or riverbanks)
     * static_objects: object used to make the map view, probably out of date near the end of the game
     * objects: (most) objects close enough to the player to be rendered, always up to date
     * gas: state of the circle
     * bullets
     * explosions
     * emotes: includes gun emotes in potato
     * planes: plane shadows
     * airstrike_zones: airstrike circles from 50v50
     * map_indicators: pings, airdrops and airstrikes
    """

    def __init__(self, map_dict):
        logger.debug("Map dict: " + str(map_dict))

        self.map_name = map_dict["mapName"]
        self.map_def = map_definitions[self.map_name]

        self.special_modes = {}
        modes = (
            "faction", "cinco", "may", "beach", "contact", "rain",
            "perk", "turkey", "snow", "valentine", "saintPatrick", "inferno"
        )
        for mode in modes:
            mode = mode + "Mode"
            if mode in self.map_def["gameMode"]:
                self.special_modes[mode] = self.map_def["gameMode"][mode]
            else:
                self.special_modes[mode] = False

        self.seed = map_dict["seed"]
        self.width = map_dict["width"]
        self.height = map_dict["height"]
        self.terrain = self._gen_terrain(self.width, self.height, map_dict["shoreInset"], map_dict["grassInset"],
                                         map_dict["rivers"], self.seed)

        self.places = map_dict["places"]
        self.ground_patches = map_dict["groundPatches"]

        self.static_objects = map_dict["objects"]

        self.objects = {}
        self.gas = {}
        self.gasT = 0
        self.bullets = []
        self.explosions = []
        self.emotes = []
        self.planes = []
        self.airstrike_zones = []
        self.map_indicators = []

    def __str__(self):
        return str(dict(self))

    def __repr__(self):
        return repr(dict(self))

    def __getitem__(self, item):
        return {
            "name": self.map_name,
            "def": self.map_def,
            "special_modes": self.special_modes,
            "width": self.width,
            "height": self.height,
            "terrain": self.terrain,
            "places": self.places,
            "ground_patches": self.ground_patches,
            "static_objs": self.static_objects,
            "objects": self.objects,
            "gas": self.gas,
            "gas_time": self.gasT,
            "bullets": self.bullets,
            "explosions": self.explosions,
            "emotes": self.emotes,
            "planes": self.planes,
            "airstrike_zones": self.airstrike_zones,
            "pings": self.map_indicators
        }[item]

    @staticmethod
    def _gen_terrain(width, height, shore_inset, grass_inset, rivers, seed):

        def generate_jagged_points(rect: Rect, side_point_count, variation, rand_gen: SeededRandGenerator):
            output = []
            point_spacing = rect.width / (side_point_count + 1)

            output.append(rect.bl.copy())
            for point_num in range(side_point_count):
                output.append(Point(
                    rect.bl.x + point_spacing * point_num,
                    rect.bl.y + rand_gen.gen(-variation, variation)))

            output.append(rect.br.copy())
            for point_num in range(side_point_count):
                output.append(Point(
                    rect.br.x + rand_gen.gen(-variation, variation),
                    rect.br.y + point_spacing * point_num))

            output.append(rect.tr.copy())
            for point_num in range(side_point_count):
                output.append(Point(
                    rect.tr.x + point_spacing * point_num,
                    rect.tr.y + rand_gen.gen(-variation, variation)))

            output.append(rect.tl.copy())
            for point_num in range(side_point_count):
                output.append(Point(
                    rect.tl.x + rand_gen.gen(-variation, variation),
                    rect.tl.y + point_spacing * point_num))

            return output

        shore_variation = constants["map"]["shoreVariation"]
        grass_variation = constants["map"]["grassVariation"]
        rand_generator = SeededRandGenerator(seed)

        shore_corner_bl = Point(shore_inset, shore_inset)
        shore_corner_tr = Point(width - shore_inset, height - shore_inset)

        rect_bl_point = shore_corner_bl.copy()
        rect_tr_point = shore_corner_tr.copy()
        shore_rect = Rect(rect_bl_point, rect_tr_point)

        shore_points = generate_jagged_points(shore_rect, 64, shore_variation, rand_generator)
        normaliser_point = Point(width * 0.5, height * 0.5)
        grass_points = []
        for point in shore_points:
            subbed = normaliser_point.sub_point(point)
            normalised = subbed.normalise()
            multiplier = rand_generator.gen(-grass_variation, grass_variation) + grass_inset
            grass_points.append(point.add_point(normalised.mul(multiplier)))

        min_max = Rect(Point(0, 0), Point(width, height))

        rivers_out = []
        for river in rivers:
            rivers_out.append(River(river["points"], river["width"], river["looped"], rivers_out, min_max))

        return {
            "shore": shore_points,
            "grass": grass_points,
            "rivers": rivers_out
        }


class GameInstance:
    """
    This is mostly just things to do with the current player/team

    Properties of note:
    * status: status of the connection (connecting, connected, closed)
    * team_size: solos, duos or sqauds
    * player_infos: teammates
    * active_player: info about the player controlled by the user or the player that is being spectated
    * active_player_id: id of the focused player
    * map: most of the interesting data, can be none if the map packet hasn't been received yet

    """

    def __init__(self):
        self.map = None

        self.status = "open"
        self.team_size = 0
        self.player_id = 0
        self.player_infos = {}
        self.active_player = {}
        self.active_player_id = 0

    def __getitem__(self, item):
        return {
            "status": self.status,
            "team_size": self.team_size,
            "player_id": self.player_id,
            "player_infos": self.player_infos,
            "active_player": self.active_player,
            "active_player_id": self.active_player_id,
            "map": self.map
        }[item]

    def __str__(self):
        return str(dict(self))

    def __repr__(self):
        return repr(dict(self))

    def init_map(self, map_dict):
        self.map = Map(map_dict)
