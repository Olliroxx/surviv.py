import arcade
from arcade import gui

from survivpy_net.ingame import GameConnection
from survivpy_net import configs

from math import sin, cos, pi, atan2, sqrt

from random import choice as rand_choice
from logging import getLogger

logger = getLogger("survivpy_client")

ASSET_ROOT = "./assets/imgs_world/"
PLAYER_SCALE_FACTOR = 2

# TODO bag colours
# TODO hand rotation


def load_texture(name: str, rotation=0, scale=(1, 1), *args, **kwargs):
    if name.endswith(".img"):
        name = name[:-4]+".png"
    tex = arcade.load_texture(ASSET_ROOT + name, *args, **kwargs)
    if rotation:
        tex = arcade.Texture(tex.name + "-rot" + str(rotation), tex.image.rotate(rotation, expand=True))

    if scale != (1, 1):
        raw = tex.image
        new_size = (i*j for i, j in zip(scale, tex.size))
        new = raw.resize(new_size)
        tex = arcade.Texture(tex.name+"-scale"+str(scale), new)

    return tex


def scale_texture(tex: arcade.Texture, x, y):
    raw = tex.image
    new_size = [round(i*j) for i, j in zip([x, y], raw.size)]
    new = raw.resize(new_size)
    tex = arcade.Texture(tex.name+"-scale"+str((x, y)), new)
    return tex


def rotate_vector(x, y, angle):
    new_x = x*cos(angle)-y*sin(angle)
    new_y = y*cos(angle)+x*sin(angle)
    return new_x, new_y


def normalise_vec(x, y, center=(400, 300)):
    mx, my = x-center[0], y-center[1]
    mag = sqrt(mx**2 + my**2)

    if not mag:
        return -1, 0

    return mx/mag, my/mag


def num_to_colour(num) -> tuple[int, int, int]:
    """
    In surviv, colours are stored as a single number, the decimal representation of the hex colour code. This function
    reverses that

    :param num:
    :return:
    """

    all_ones = (1 << 8) - 1
    return (num & (all_ones << 16)) >> 16, (num & (all_ones << 8)) >> 8, num & all_ones


class RootLayer:
    def setup(self):
        pass

    def first_frame(self, state):
        pass


class Layer(RootLayer):
    def __init__(self):
        """
        A layer in the rendering process (like ceilings, walls, floor, players, emotes, particles, items....)

        source: The mod that added this layer (use main for vanilla)
        """
        self.name = "template"
        self.source = "main"
        self.loader = None

    def __str__(self):
        return str(self.source) + "/" + str(self.name)

    def __repr__(self):
        return str(self.source) + "/" + str(self.name)

    def render(self, state, surface: gui.surface.Surface):
        pass


class LevelLayer(RootLayer):
    def __init__(self, level=1):
        self.name = "template"
        self.source = "main"
        self.level = level
        self.loader = None

    def __str__(self):
        return str(self.source) + "/" + str(self.name) + "/" + str(self.level)

    def __repr__(self):
        return str(self.source) + "/" + str(self.name) + "/" + str(self.level)

    def render(self, state, surface: gui.surface.Surface, layer):
        pass


class PlayerLayer(LevelLayer):
    def __init__(self):
        super().__init__()

    def first_frame(self, state):
        pass

    def render(self, state, surface: gui.surface.Surface, layer):
        pass


class PlayerList:
    pass


class Gun:
    # TODO add support for "gunBall" (rainbow blaster)
    # TODO add casing particles
    # TODO add recoil

    def __init__(self, sprite_list: arcade.SpriteList, gun_sprite: arcade.Sprite, mag_sprite: arcade.Sprite, set_pos,
                 rel_move):
        self.sprite_list = sprite_list
        self.gun_sprite = gun_sprite
        self.mag_sprite = mag_sprite
        self.set_sprite_pos = set_pos
        self.move_sprite = rel_move

        self.max_scale_shoot = 0  # Something to do with the rainbow blaster
        self.mag_top = False  # Use unknown

    def set_type(self, name, scale, loaded):
        gtype_data = configs.gtypes[name]
        worldimg_data = gtype_data["worldImg"]

        if loaded:
            self.gun_sprite.texture = load_texture(worldimg_data["onLoadComplete"], rotation=270)
        else:
            self.gun_sprite.texture = load_texture(worldimg_data["sprite"], rotation=270)

        self.set_sprite_pos(self.gun_sprite, self.gun_sprite.width*0.2, 0)

        if worldimg_data["scale"]["x"] != worldimg_data["scale"]["y"]:
            self.gun_sprite.texture = scale_texture(self.gun_sprite.texture, worldimg_data["scale"]["x"],
                                                    worldimg_data["scale"]["y"])
        else:
            self.gun_sprite.scale = worldimg_data["scale"]["x"] / scale

        self.gun_sprite.color = num_to_colour(worldimg_data["tint"])
        self.gun_sprite.alpha = 255

        if not loaded:
            if "magImg" in worldimg_data:
                mag_img = worldimg_data["magImg"]
                self.mag_sprite.texture = load_texture(mag_img["sprite"], rotation=270)
                self.set_sprite_pos(self.mag_sprite, 0.5+(mag_img["pos"]["x"]/scale), 0.5+(mag_img["pos"]["y"]/scale))
                self.mag_sprite.scale = 0.5*scale
                self.mag_sprite.color = (255, 255, 255)
                self.mag_sprite.alpha = 255

                self.sprite_list.remove(self.mag_sprite)
                pos = self.sprite_list.index(self.gun_sprite)
                if "top" in mag_img and mag_img["top"]:
                    self.sprite_list.insert(pos+1, self.mag_sprite)
                else:
                    self.sprite_list.insert(pos, self.mag_sprite)

            else:
                self.mag_sprite.alpha = 0

        self.mag_top = "magImg" in worldimg_data and "top" in worldimg_data["magImg"] and worldimg_data["magImg"]["top"]

        # TODO some stuff related to rainbow blaster here

        if "gunOffset" in worldimg_data:
            offset = [-5.95, 0] if gtype_data["isDual"] else [-4.25, -1.75]
            offset[0] += worldimg_data["gunOffset"]["x"]
            offset[1] += worldimg_data["gunOffset"]["y"]

            for sprite in [self.gun_sprite, self.mag_sprite]:
                self.move_sprite(sprite, *offset)

    def hide(self):
        self.gun_sprite.alpha = 0
        self.mag_sprite.alpha = 0

    def show(self):
        self.gun_sprite.alpha = 255
        self.mag_sprite.alpha = 255


class Player:
    def __init__(self, player_id, map_obj, sprite_list: arcade.SpriteList):
        super().__init__()

        self.id = player_id
        self.map = map_obj
        self.sprite_list = sprite_list

        self.loadout = {
            "melee": {
                "scale": {
                    "x": 0.175,
                    "y": 0.175
                }
            }
        }

        self.sprite_footL = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_footL.texture = load_texture("player-feet-01.png", hit_box_algorithm="None")
        self.sprite_footL.scale = 0.45 * PLAYER_SCALE_FACTOR
        self.sprite_footL.radians = 0.5
        self.sprite_footL_submerge = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_footR = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_footR.texture = load_texture("player-feet-01.png", hit_box_algorithm="None")
        self.sprite_footR.scale = 0.45 * PLAYER_SCALE_FACTOR
        self.sprite_footR.radians = 0.5
        self.sprite_footR_submerge = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_backpack = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_body = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_body_submerge = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_chest = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_chest.texture = load_texture("player-armor-base-01.png", hit_box_algorithm="None")
        self.sprite_chest.scale = 0.25 * PLAYER_SCALE_FACTOR
        self.sprite_flak = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_steelskin = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_hip = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_bodyEffect = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_gunL = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_magL = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_handL = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_handL_submerge = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_objectL = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_gunR = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_magR = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_melee = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_handR = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_handR.angle = 0
        self.sprite_handR_submerge = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_objectR = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_visor = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_accessory = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_patch = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_helmet = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_slime = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_aim = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_phoenix = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_pyro = arcade.Sprite(hit_box_algorithm="None")

        self.sprites = [self.sprite_footL, self.sprite_footL_submerge, self.sprite_footR, self.sprite_footR_submerge,
                        self.sprite_backpack, self.sprite_body, self.sprite_body_submerge, self.sprite_chest,
                        self.sprite_flak, self.sprite_steelskin, self.sprite_hip, self.sprite_bodyEffect,
                        self.sprite_gunL, self.sprite_handL, self.sprite_handL_submerge, self.sprite_objectL,
                        self.sprite_gunR, self.sprite_melee, self.sprite_handR, self.sprite_handR_submerge,
                        self.sprite_objectR, self.sprite_visor, self.sprite_accessory, self.sprite_patch,
                        self.sprite_helmet, self.sprite_slime, self.sprite_aim, self.sprite_phoenix, self.sprite_pyro]
        self.sprite_list.extend(self.sprites)

        self.gunL = Gun(self.sprite_list, self.sprite_gunL, self.sprite_magL, self.move_child, self.set_child_pos)
        self.gunR = Gun(self.sprite_list, self.sprite_gunR, self.sprite_magR, self.move_child, self.set_child_pos)

        self.skin = None
        self.backpack = None
        self.helmet = None
        self.chest = None
        self.curWeapType = None
        self.layer = None
        self.dead = None
        self.downed = None
        self.animType = None
        self.animSeq = None
        self.wearingPan = None
        self.hasActionItem = None
        self.actionItem = None
        self.playerScale = None
        self.dir = (-1, 0)
        self.dir_radians = 0
        self.prev_dir = 0
        self.pos = (0, 0)
        self.prev_pos = (0, 0)
        self.body_rad = configs.constants["player"]["radius"]
        self.gun_loaded = False

        self.active = True
        self.prev_active = True

        self.anim = {
            "type": 0,
            "mirrored": False,
            "name": "fists",
            "seq": -1,
            "ticker": 0
        }

        # TODO anim stuff
        # TODO add way to get ghillie colour

        self.update_netdata()
        self.update_sprites()
        self.switch_to_idle()

    def update_netdata(self):
        self.prev_active = self.active
        if self.id in self.map.objects:
            self.active = True
            if self.active != self.prev_active:
                self.show()
            data = self.map.objects[self.id]
            self.skin = data["outfit"]
            self.backpack = data["backpack"]
            self.helmet = data["helmet"]
            self.chest = data["chest"]
            self.curWeapType = data["curWeapType"]
            self.layer = data["layer"]
            self.dead = data["dead"]
            self.downed = data["downed"]
            self.animType = data["animType"]
            self.animSeq = data["animSeq"]
            self.wearingPan = data["wearingPan"]
            self.hasActionItem = data["hasActionItem"]
            self.actionItem = data["actionItem"]
            self.playerScale = data["playerScale"]

            self.dir = data["dir"]
            self.prev_dir = self.dir_radians
            self.dir_radians = atan2(*self.dir[::-1])  # Reverse order because atan2 takes y then x for whatever reason

            # TODO move sprite to origin
            # TODO make this work (remove and reimplement) around origin

            rads_diff = self.dir_radians - self.prev_dir
            for sprite in self.sprites:
                rel_x = sprite.position[0]-self.pos[0]
                rel_y = sprite.position[1]-self.pos[1]

                radius = sqrt((rel_x**2) + (rel_y**2))
                angle = atan2(rel_y, rel_x) + rads_diff

                new_rel_x = radius * cos(angle)
                new_rel_y = radius * sin(angle)

                new_x = new_rel_x + self.pos[0]
                new_y = new_rel_y + self.pos[1]

                sprite.position = (new_x, new_y)
                sprite.radians = (sprite.radians + rads_diff) % (2*pi)
            # Move the sprites to new positions (player rotation)

            self.prev_pos = self.pos
            self.pos = data["pos"]
            diff = self.pos[0] - self.prev_pos[0], self.pos[1] - self.prev_pos[1]
            for sprite in self.sprites:
                sprite.position = tuple(map(sum, zip(diff, sprite.position)))
            # Move the sprites to new positions (player movement)

        else:
            self.active = False
            if self.active != self.prev_active:
                self.hide()

    def update_hand_sprite(self, sprite: arcade.Sprite, name, tint=(255, 255, 255), flipped=False):
        sprite.texture = load_texture(name, flipped_horizontally=flipped)
        sprite.color = tint

        # TODO This
        scale = {"x": 0.175, "y": 0.175}
        if tint == (255, 255, 255):
            try:
                scale = configs.gtypes[self.loadout["melee"]["name"]]["scale"]
            except KeyError:
                pass

        if scale["x"] != scale["y"]:
            raise RuntimeWarning("Non-uniform scale values")
        sprite.scale = scale["x"] * PLAYER_SCALE_FACTOR

        return sprite

    @staticmethod
    def update_foot_sprite(sprite: arcade.Sprite, tint, visible: bool):
        sprite.color = tint
        sprite.alpha = 255 * int(visible)

    def update_sprites(self):
        skin_img = configs.gtypes[self.skin]["skinImg"]

        self.sprite_body.texture = load_texture(skin_img["baseSprite"])
        self.sprite_body.color = num_to_colour(skin_img["baseTint"])
        self.sprite_body.scale = 0.25 * PLAYER_SCALE_FACTOR
        self.sprite_body.alpha = 255
        # TODO ghillie

        # TODO frozen effects
        # TODO 50v50 team markers

        # noinspection PyUnreachableCode
        if False:
            pass  # TODO if loadout melee/normal melee replaces hand sprites, do it
        else:
            self.sprite_handL = self.update_hand_sprite(self.sprite_handL, skin_img["handSprite"])

            self.sprite_handR = self.update_hand_sprite(self.sprite_handR, skin_img["handSprite"])

        # TODO "accessories" (Parts of body outside of circular sprite)

        tint = num_to_colour(skin_img["footTint"])
        # TODO change tint if using ghillie suit
        self.update_foot_sprite(self.sprite_footL, tint, self.downed)
        self.update_foot_sprite(self.sprite_footR, tint, self.downed)

        # TODO draw flak if not ghillie

        # TODO ghillie stuff
        if self.chest:
            self.sprite_chest.alpha = 255
            self.sprite_chest.color = num_to_colour(configs.gtypes[self.chest]["skinImg"]["baseTint"])
        else:
            self.sprite_chest.alpha = 0

        # TODO draw steelskin if not ghillie

        # TODO draw phoenix

        # TODO draw pyro

        # TODO ghillie
        if self.helmet:
            self.sprite_helmet.alpha = 255
            self.sprite_helmet.texture = load_texture(configs.gtypes[self.helmet]["skinImg"]["baseSprite"])
            offset = 3.33 * (1 if self.downed else -1)
            self.set_child_pos(self.sprite_helmet, offset, 0)

            self.sprite_helmet.color = num_to_colour(configs.gtypes[self.helmet]["skinImg"]["baseTint"])

            if "spriteScale" in configs.gtypes[self.helmet]["skinImg"]:
                scale = configs.gtypes[self.helmet]["skinImg"]["spriteScale"]
                self.sprite_helmet.scale = scale * PLAYER_SCALE_FACTOR
            else:
                self.sprite_helmet.scale = 0.15 * PLAYER_SCALE_FACTOR
            # TODO 50v50

        else:
            self.sprite_helmet.alpha = 0

        # TODO ghillie
        if self.backpack != "" and not self.downed:
            self.sprite_backpack.texture = load_texture(skin_img["backpackSprite"], hit_box_algorithm="None")
            pack_data = configs.gtypes[self.backpack]

            offsets = [10.25, 11.5, 12.75]
            offset = -offsets[pack_data["level"] - 1]
            scale = (0.4 + pack_data["level"] * 0.03) * 0.5
            self.set_child_pos(self.sprite_backpack, self.sprite_backpack.position[0] + offset,
                               self.sprite_backpack.position[1])
            self.sprite_backpack.color = num_to_colour(skin_img["backpackTint"])
            self.sprite_backpack.scale = scale * PLAYER_SCALE_FACTOR
            self.sprite_backpack.alpha = 255
        else:
            self.sprite_backpack.alpha = 0

        # TODO draw pan

        held_item = configs.gtypes[self.curWeapType]
        if held_item["type"] == "gun":
            self.gunR.show()
            self.gunR.set_type(self.curWeapType, self.body_rad/configs.constants["player"]["radius"], self.gun_loaded)
        else:
            self.gunR.hide()
            self.gunL.hide()
        # draw held gun CORE

        # update something if state of "downed" has changed CORE ?

        # draw held melee CORE

        # draw held throwable CORE

        # hide held object if downed or reviving CORE

        # TODO show heal/rev particles

        # TODO if cobalt mode and not ghillie, show per-role skin overlay

    def hide(self):
        for sprite in self.sprites:
            self.sprite_list.remove(sprite)

    def show(self):
        for sprite in self.sprites:
            self.sprite_list.append(sprite)

    def move_child(self, sprite: arcade.Sprite, x, y):
        x *= PLAYER_SCALE_FACTOR
        y *= PLAYER_SCALE_FACTOR
        sprite.position = tuple(map(sum, zip(rotate_vector(x, y, self.dir_radians), sprite.position)))

    def set_child_pos(self, sprite: arcade.Sprite, x, y):
        x *= PLAYER_SCALE_FACTOR
        y *= PLAYER_SCALE_FACTOR
        rotated = rotate_vector(x, y, self.dir_radians)
        pos = self.pos[0]+rotated[0], self.pos[1]+rotated[1]
        sprite.position = pos

    def update_anim(self, delta_time):
        self.anim["ticker"] += delta_time

        keyframe_data = configs.anims["animations"][self.anim["name"]]["keyframes"]
        if not keyframe_data:
            return

        str_to_sprite = {
            "HandL": (self.sprite_handL, self.sprite_handL_submerge),
            "HandR": (self.sprite_handR, self.sprite_handR_submerge),
            "FootL": (self.sprite_footL, self.sprite_footL_submerge),
            "FootR": (self.sprite_footR, self.sprite_footR_submerge)
        }

        times = {}
        for frame in keyframe_data:
            time = self.get_time(frame)
            times[time] = frame
        # Frames are sorted by the order they are played in, if the last frame has played then switch to idle anim
        # noinspection PyUnboundLocalVariable
        if 0 >= self.anim["ticker"] or self.anim["ticker"] > time:
            idle_anim = configs.anims["idles"][self.anim["name"]]
            for limb, value in idle_anim.items():
                sprite, submerge = str_to_sprite[limb]
                if value is not None:
                    self.set_child_pos(sprite, value[0], value[1])
                    self.set_child_pos(submerge, value[0], value[1])
        else:
            pose = self.lerp_anim(times)
            pose = self.strip_dict_to_limbs(pose)

            for limb, value in pose.items():
                for sprite in str_to_sprite[limb]:
                    if value is not None:
                        self.set_child_pos(sprite, pose[limb][0], pose[limb][1])
                        sprite.radians = (pose[limb][2]+self.dir_radians+(0.5 if "Leg" in limb else 0)) % (2*pi)

    def switch_to_idle(self):
        keyframe_data = configs.anims["animations"][self.anim["name"]]["keyframes"]
        time = max(self.get_time(frame) for frame in keyframe_data)
        self.anim["ticker"] = time
        self.update_anim(0)

    def lerp_anim(self, times):
        if self.anim["ticker"] in times:
            pose = times[self.anim["ticker"]]
        else:
            pose = {}
            prev_time, next_time = self.get_closest_numbers(self.anim["ticker"], sorted(times.keys()))
            ratio = self.get_ratio(prev_time, self.anim["ticker"], next_time)
            prev = self.strip_dict_to_limbs(times[prev_time])
            next_ = self.strip_dict_to_limbs(times[next_time])

            for name, value in prev.items():
                if value is None:
                    pose[name] = None
                else:
                    x = prev[name][0] * (1 - ratio) + next_[name][0] * ratio
                    y = prev[name][1] * (1 - ratio) + next_[name][1] * ratio
                    r = prev[name][2] * (1 - ratio) + next_[name][2] * ratio
                    pose[name] = [x, y, r]
        return pose

    @staticmethod
    def get_ratio(lower, target, upper):
        """
        Given two numbers (imagine on a number line) and number between them, get the ratio between the gaps between them
        """
        diff_tl = target-lower
        diff_ut = upper-target
        return diff_tl/(diff_tl+diff_ut)

    @staticmethod
    def strip_dict_to_limbs(in_dict):
        """
        Removes all keys from the input dict, except for HandL, HandR, FootL and FootR
        """
        return {
            "HandL": in_dict["HandL"],
            "HandR": in_dict["HandR"],
            "FootL": in_dict["FootL"],
            "FootR": in_dict["FootR"]
        }

    @staticmethod
    def get_closest_numbers(target, numbers):
        """
        Given an array of numbers and a target, find the two numbers in the array closest to the target.

        Conditions:
         * array is sorted
         * target is not higher than the highest number in the array, same thing with lowest number
         * the target is not in the array

        """
        prev = 0
        for number in numbers:
            if number > target:
                return prev, number
            else:
                prev = number

    @staticmethod
    def get_time(frame):
        if frame["abs_time"]:
            return frame["time"]
        if type(frame["time"]) == list:
            value = configs.gtypes_subcategories["melee_weapons"]
            for key in frame["time"]:
                value = value[key]
            return value * frame["time_mult"] + frame["time_offset"]

        raise RuntimeError

    def start_anim(self):
        name, mirrored = self._get_anim_name()
        self.anim = {
            "type": self.animType,
            "mirrored": mirrored,
            "name": name,
            "seq": self.animSeq,
            "ticker": 0
        }

    def _get_anim_name(self):
        """
        Gets animation data for current state
        """
        anim_name_functions = [
            lambda x: ("none", False),
            self._get_melee_anim,
            lambda x: ("cook", False),
            lambda x: ("throw", False),
            lambda x: ("revive", False),
            lambda x: ("crawl_forward", True),
            lambda x: ("crawl_backward", True),
            lambda x: ("revive", True),
            self._get_change_pose_anim
        ]
        # Each function takes `self.curWeapType` and returns a 2-tuple containing the animation name and
        # if mirroring should be used (eg. cook always needs to hold the grenade in the right hand, crawling doesn't care)
        translation_dict = dict(zip(configs.constants["Anim"].values(), anim_name_functions))
        # Creates a dictionary that maps from `animType`s (ints) to 2-tuple functions (see above)
        anim_type, mirrorable = translation_dict[self.animType](self.curWeapType)

        if mirrorable:
            mirrored = rand_choice([True, False])
        else:
            mirrored = False

        return anim_type, mirrored

    @staticmethod
    def _get_melee_anim(cur_weap):
        gtype_data = configs.gtypes[cur_weap]
        if "anim" not in gtype_data or "attackAnims" not in gtype_data["anim"]:
            return "fists", True
        attack_anims = gtype_data["anim"]["attackAnims"]
        return rand_choice(attack_anims), attack_anims == ["fists"]

    @staticmethod
    def _get_change_pose_anim(cur_weap):
        """
        Used for lightsabers?
        """
        gtype_data = configs.gtypes[cur_weap]
        if "anim" not in gtype_data or "poseAnims" not in gtype_data["anim"]:
            return "none", True
        attack_anims = gtype_data["anim"]["poseAnims"]
        return rand_choice(attack_anims), attack_anims == ["fists"]

# TODO layer classes


class WorldView(gui.UIInteractiveWidget):
    def __init__(self,
                 layers: list[Layer],
                 level_layers: list[LevelLayer],
                 conn: GameConnection,  # Game connection
                 x: float = 0,
                 y: float = 0,
                 width: float = 100,
                 height: float = 50,
                 size_hint=(1, 1),  # Preferred ratio
                 size_hint_min=(640, 480),  # Pixels
                 size_hint_max=None):
        """
        Main world view (widget that show bullets, players....), NOT the UI

        Uses a layer based system for rendering:
         * Layers are added/inserted to the list
         * Two setup functions exist for each layer: `setup` and `first frame`:
            * `setup` runs when the view is being initialised (can run before the connection to the game is established)
            * `first_frame` runs on the first frame, when the map data has been received
         * When a frame is rendered, go through the list (starting with the ground) and call `render`
         * Layers are duplicated on floor levels (main and underground), so level_layers exist and are called on each layer
        """
        super().__init__(x, y, width, height,
                         size_hint=size_hint,
                         size_hint_min=size_hint_min,
                         size_hint_max=size_hint_max)

        self.conn = conn

        self.cam = arcade.Camera(round(width), round(height))

        self.layers = layers
        self.level_layers = level_layers
        # noinspection PyTypeChecker
        for layer in self.layers + self.level_layers:
            layer.setup()

        self.state = self.conn.state
        self.map = None
        self.map_def = None
        self.first_frame = True

        self.conn.start()

    def first_frame_setup(self):
        self.map = self.state.map
        self.map_def = self.map.map_def
        # noinspection PyTypeChecker
        for layer in self.layers + self.level_layers:
            layer.first_frame(self.state)

    def do_render(self, surface: gui.surface.Surface):
        if self.conn.state.status == "open":

            if self.first_frame:
                self.first_frame = False
                self.first_frame_setup()

            self.prepare_render(surface)
            surface.clear((0, 0, 0, 255))
            self.cam.use()

            for layer in self.level_layers:
                layer.render(self.state, surface, 1)

            for layer in self.level_layers:
                layer.render(self.state, surface, 0)

            for layer in self.layers:
                layer.render(self.state, surface)

    # def on_event(self, event: gui.UIEvent):
    #     if type(event) in [gui.UIKeyReleaseEvent, gui.UIKeyPressEvent]:
    #     self.conn.
    # TODO this (inputs)

    def print_layers(self):
        for layer in self.layers:
            print(layer)
        # TODO level layers


class RootWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Surviv.py")

        self.manager = gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.WHITE)
        self.v_box = gui.UIBoxLayout()

        button = gui.UIFlatButton(text="Start")
        self.v_box.add(button)

        # noinspection PyUnusedLocal
        @button.event("on_click")
        def on_click_button(event):
            self.v_box.remove(button)

            from survivpy_net import pregame
            self.prof = pregame.Profile()
            self.conn = self.prof.prep_game()
            game_view = WorldView([], [], self.conn, width=800, height=600)
            self.v_box.add(game_view)

        self.manager.add(gui.UIAnchorWidget(anchor_x="center_x", anchor_y="center_y", child=self.v_box))

    def on_draw(self):
        arcade.start_render()
        self.manager.draw()


class DummyMap:
    def __init__(self):
        self.objects = {0: {
            "outfit": "outfitParmaPrestige",
            "backpack": "backpack01",
            "helmet": "",
            "chest": "",
            "curWeapType": "m9",
            "layer": 1,
            "dead": False,
            "downed": False,
            "animType": 1,
            "animSeq": 1,
            "wearingPan": False,
            "hasActionItem": False,
            "actionItem": "",
            "playerScale": 1.,
            "dir": (0, -1),
            "pos": (0, 0)
        }}


class PlayerTestWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Player test window")
        self.sprite_list = arcade.SpriteList()
        self.dummy_map = DummyMap()
        self.player_sprite = Player(0, self.dummy_map, self.sprite_list)
        self.cam = arcade.Camera(800, 600)
        # noinspection PyTypeChecker
        self.cam.move((-400, -300))

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color((127, 127, 127))
        self.cam.use()
        self.sprite_list.draw()

    def on_update(self, delta_time: float):
        self.player_sprite.update_anim(delta_time)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.dummy_map.objects[0]["dir"] = normalise_vec(x, y)
        self.player_sprite.update_netdata()

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        self.player_sprite.start_anim()


class GunTestWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Gun test window")

        self.gun_sprite = arcade.Sprite(hit_box_algorithm="None")
        self.mag_sprite = arcade.Sprite(hit_box_algorithm="None")

        self.sprite_list = arcade.SpriteList()
        self.sprite_list.append(self.gun_sprite)
        self.sprite_list.append(self.mag_sprite)

        self.dir = 0
        self.prev_dir = 0

        self.gun = Gun(self.sprite_list, self.gun_sprite, self.mag_sprite, self.set_pos, self.rel_move)
        self.gun.set_type("pkp", 1, False)

        self.cam = arcade.Camera(800, 600)
        # noinspection PyTypeChecker
        self.cam.move((-400, -300))

    def set_pos(self, sprite: arcade.Sprite, x, y):
        new_x = x * sprite.width
        new_y = y * sprite.height
        sprite.position = rotate_vector(new_x, new_y, self.dir)

    def rel_move(self, sprite, x, y):
        new_x = x * sprite.width
        new_y = y * sprite.height
        sprite.position = tuple(map(sum, zip(rotate_vector(new_x, new_y, self.dir), sprite.position)))

    # def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
    #     x, y = normalise_vec(x, y)
    #     self.prev_dir = self.dir
    #     self.dir = atan2(y, x)
    #
    #     rads_diff = self.dir - self.prev_dir
    #     for sprite in [self.gun_sprite, self.mag_sprite]:
    #         radius = sqrt((sprite.position[0] ** 2) + (sprite.position[1] ** 2))
    #         angle = atan2(sprite.position[1], sprite.position[0]) + rads_diff
    #
    #         new_x = radius * cos(angle)
    #         new_y = radius * sin(angle)
    #
    #         sprite.position = (new_x, new_y)
    #         sprite.radians = (sprite.radians + rads_diff) % (2 * pi)

    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color((127, 127, 127))
        self.cam.use()
        self.sprite_list.draw()


# TODO `default_layer_list` function
# TODO layer order:
# ping markers
# gas
# flares
# plane shadows
# Layers to remember: bullets

# Height level layers order seems to be:
# emotes  TODO work out what causes the emotes to stop showing
# roofs
# particles
# players
# throwables
# objects
# decals
# walls
# floors
# ground


if __name__ == '__main__':
    configs.update_configs()

    # window = RootWindow()
    window = PlayerTestWindow()
    arcade.run()
