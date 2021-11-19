from survivpy_net import Point, EndpointLine, Rect, Poly, SeededRandGenerator
from survivpy_net import configs
from logging import getLogger

logger = getLogger("survivpy_net")

JS_MAX_VALUE = 2 ** 1024 - 1
RIVER_JOIN_DIST = 1.5


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

    def __init__(self, points, width, looped, other_rivers, min_max: Rect, shore_poly):

        configs.update_configs()

        self.points = []
        for point in points:
            if not type(point) == Point:
                point = Point(*point)
            self.points.append(point)
        points = self.points.copy()

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

        self.rect = None
        self.water_poly = []
        self.shore_poly = []

        self.point_gen(points, looped, other_rivers, shore_poly)

    def point_gen(self, points, looped, other_rivers, shore_poly):
        l_dirs, r_dirs, closest = self.gen_directions(points, looped, other_rivers)
        water_widths, shore_widths = self.gen_widths(points, looped, closest)

        l_water = []
        r_water = []
        l_shore = []
        r_shore = []

        for left, right, shore, water, source in zip(l_dirs, r_dirs, shore_widths, water_widths, points):
            l_water.append(left.mul(water).add_point(source))
            r_water.append(right.mul(water).add_point(source))
            l_shore.append(left.mul(shore + water).add_point(source))
            r_shore.append(right.mul(shore + water).add_point(source))

        l_shore = self.trim_to_shore(l_shore, shore_poly)
        r_shore = self.trim_to_shore(r_shore, shore_poly)

        self.water_poly = l_water + r_water[::-1]
        self.shore_poly = l_shore + r_shore[::-1]

    @staticmethod
    def trim_to_shore(points, shore_poly):
        in_poly = []
        shore_poly = Poly(shore_poly)
        for point in points:
            in_poly.append(shore_poly.point_in_poly(point))

        points_outside_start = 0
        for point in in_poly:
            if point:
                break
            else:
                points_outside_start += 1

        if points_outside_start:
            points = points[points_outside_start-1:]
            edge_intersect = EndpointLine(points[0], points[1])
            for poly_edge in shore_poly.edges:
                if edge_intersect.ep_line_intersect(poly_edge):
                    points[0] = edge_intersect.ep_line_intersect(poly_edge)
                    break

        points_outside_end = 0
        for point in in_poly[::-1]:
            if point:
                break
            else:
                points_outside_end += 1

        if points_outside_end:
            points = points[:-points_outside_end+1]
            edge_intersect = EndpointLine(points[-1], points[-2])
            for poly_edge in shore_poly.edges:
                if edge_intersect.ep_line_intersect(poly_edge):
                    points[-1] = edge_intersect.ep_line_intersect(poly_edge)
                    break

        return points

    @staticmethod
    def gen_directions(points, looped, other_rivers):
        lines = [(), ()]
        closest_river = None

        if other_rivers:
            # Work out if this river is a fork of another river
            closest = [None, None, None]
            for river in other_rivers:
                for point_num in [0, -1]:
                    point = river.get_closest(points[point_num])
                    dist = point.sub_point(points[point_num]).length()
                    if closest[1] is None or dist < closest[1]:
                        closest = [point, dist, bool(point_num+1), river]
            # Make the line from the first/last point of the current window to the closest point on the other river
            closest_river = closest[3]
            # noinspection PyTypeChecker
            if closest[1] < RIVER_JOIN_DIST:
                if closest[2]:
                    line = (closest[0], points[0])
                    lines = [line, ()]
                else:
                    line = (points[-1], closest[0])
                    lines = [(), line]

        # Make the line that connects the first and last point, if looped
        if looped:
            lines = [(points[0], points[-1]), ()]

        # Make the remainder of the lines
        for point_num in range(1, len(points)):
            prev = points[point_num-1]
            current = points[point_num]
            line = EndpointLine(prev, current)
            lines.insert(-1, line)

        # Turn the list of lines into a list of line pairs. Example:
        # ["a", "b", "c"] -> [("a", "b"), ("b", "c")]
        line_pairs = []
        for line_num in range(1, len(lines)):
            prev = lines[line_num-1]
            current = lines[line_num]
            line_pairs.append((prev, current))

        # Get the gradient perpendicular to the points where each pair meets (if its the end/start, only use one line)
        gradients = []
        for line_1, line_2 in line_pairs:

            if not (line_1 and line_2):
                non_empty = line_1 if line_1 else line_2
                av_gradient = non_empty.get_mx_plus_c().m
                gradients.append(-1/av_gradient)
            else:
                prev_point = line_1.start
                next_point = line_2.end
                to_bisect = EndpointLine(prev_point, next_point)

                try:
                    m = to_bisect.get_mx_plus_c().m
                    if not m:
                        gradients.append("infinity")
                    else:
                        gradients.append(-1/m)
                except ZeroDivisionError:
                    gradients.append(0)

        l_vectors = []
        r_vectors = []
        for grad_num, grad in enumerate(gradients):
            if grad == "infinity":
                pos_vec = Point(0, 1)
                alt_vec = Point(0, -1)
            else:
                pos_vec = Point(1, grad).normalise()
                alt_vec = Point(-1, -grad).normalise()

            r_vectors.append(pos_vec)
            l_vectors.append(alt_vec)

        new_r = [r_vectors[0]]
        new_l = [l_vectors[0]]
        for num in range(1, len(r_vectors)):
            r_line = EndpointLine(new_r[-1], r_vectors[num])
            l_line = EndpointLine(new_l[-1], l_vectors[num])

            if r_line.ep_line_intersect(l_line):
                new_l.append(r_vectors[num])
                new_r.append(l_vectors[num])
            else:
                new_l.append(l_vectors[num])
                new_r.append(r_vectors[num])

        return new_l, new_r, closest_river

    def gen_widths(self, points, looped, closest_river):
        if looped:
            water_widths = [self.water_width] * len(points)
        else:
            water_widths = []
            for point_num, point in enumerate(points):
                dist_to_end = len(points) - point_num
                dist_to_start = point_num
                base_thickness = (2 * (max(dist_to_start, dist_to_end) / len(points))) - 1
                water_widths.append((1 + base_thickness**3 * 1.5) * self.water_width)

        shore_widths = []

        for point_num, point in enumerate(points):
            width = self.shore_width
            if closest_river:
                closest_point = closest_river.get_closest(point)
                dist = closest_point.sub_point(point).length()
                if dist < closest_river.water_width * 2:
                    width = max(width, closest_river.shore_width)

                if point_num in (0, len(points)-1) and dist < 1.5 and not looped:  # Another condition here, idk what
                    # parent_river = closest_river  # TODO check this works the same as official
                    pass

            if point_num:
                width = (shore_widths[-1] + width)/2
            shore_widths.append(width)

        return water_widths, shore_widths

    def __str__(self):
        return str((self.water_width, self.looped, self.points))


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
        self.map_def = configs.map_defs[self.map_name]

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
        return str(self.get_dict())

    def __repr__(self):
        return repr(self.get_dict())

    def get_dict(self):
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
        }

    def __getitem__(self, item):
        return self.get_dict()[item]

    @staticmethod
    def _gen_terrain(width, height, shore_inset, grass_inset, rivers, seed):

        def generate_jagged_points(rect: Rect, side_point_count, variation, rand_gen: SeededRandGenerator):
            output = []
            point_spacing = rect.width / (side_point_count + 1)

            output.append(rect.bl.copy())
            for point_num in range(1, side_point_count + 1):
                output.append(Point(
                    rect.bl.x + point_spacing * point_num,
                    rect.bl.y + rand_gen.gen(-variation, variation)))

            output.append(rect.br.copy())
            for point_num in range(1, side_point_count + 1):
                output.append(Point(
                    rect.br.x + rand_gen.gen(-variation, variation),
                    rect.br.y + point_spacing * point_num))

            output.append(rect.tr.copy())
            for point_num in range(1, side_point_count + 1):
                output.append(Point(
                    rect.tr.x - point_spacing * point_num,
                    rect.tr.y + rand_gen.gen(-variation, variation)))

            output.append(rect.tl.copy())
            for point_num in range(1, side_point_count + 1):
                output.append(Point(
                    rect.tl.x + rand_gen.gen(-variation, variation),
                    rect.tl.y - point_spacing * point_num))

            return output

        shore_variation = configs.constants["map"]["shoreVariation"]
        grass_variation = configs.constants["map"]["grassVariation"]
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
            rivers_out.append(River(river["points"], river["width"], river["looped"], rivers_out, min_max, shore_points))

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

        self.status = "opening"
        self.team_size = 0
        self.player_id = 0
        self.player_infos = {}
        self.active_player = {}
        self.active_player_id = 0

    def __getitem__(self, item):
        return self.get_dict()[item]

    def get_dict(self):
        return {
            "status": self.status,
            "team_size": self.team_size,
            "player_id": self.player_id,
            "player_infos": self.player_infos,
            "active_player": self.active_player,
            "active_player_id": self.active_player_id,
            "map": self.map
        }

    def __str__(self):
        return str(self.get_dict())

    def __repr__(self):
        return repr(self.get_dict())

    def init_map(self, map_dict):
        self.map = Map(map_dict)
        self.status = "open"
