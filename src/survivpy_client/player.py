from survivpy_client import LevelLayer, load_texture, scale_texture, rotate_vector, num_to_colour
from survivpy_net import configs

import arcade
from arcade import gui

from math import atan2, sqrt, sin, cos, pi

from random import choice as rand_choice

PLAYER_SCALE_FACTOR = 2


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
    # TODO fist anims are always same fist, should be random
    # TODO check duals

    def __init__(self, sprite_list: arcade.SpriteList, gun_sprite: arcade.Sprite, mag_sprite: arcade.Sprite, parent):
        self.sprite_list = sprite_list
        self.gun_sprite = gun_sprite
        self.mag_sprite = mag_sprite
        self.set_sprite_pos = parent.set_child_pos
        self.move_sprite = parent.move_child
        self.max_scale_shoot = 0  # Something to do with the rainbow blaster
        self.mag_top = False  # Use unknown

    def set_type(self, name, scale, loaded):
        gtype_data = configs.gtypes[name]
        worldimg_data = gtype_data["worldImg"]

        if loaded:
            self.gun_sprite.texture = load_texture(worldimg_data["onLoadComplete"], rotation=270)
        else:
            self.gun_sprite.texture = load_texture(worldimg_data["sprite"], rotation=270)

        self.set_sprite_pos(self.gun_sprite, self.gun_sprite.width * 0.2, 0)

        if worldimg_data["scale"]["x"] != worldimg_data["scale"]["y"]:
            self.gun_sprite.texture = scale_texture(self.gun_sprite.texture, worldimg_data["scale"]["x"],
                                                    worldimg_data["scale"]["y"])
        else:
            self.gun_sprite.scale = worldimg_data["scale"]["x"] / scale

        self.gun_sprite.color = num_to_colour(worldimg_data["tint"])
        self.gun_sprite.visible = True

        if not loaded:
            if "magImg" in worldimg_data:
                mag_img = worldimg_data["magImg"]
                self.mag_sprite.texture = load_texture(mag_img["sprite"], rotation=270)
                self.set_sprite_pos(self.mag_sprite, -(0.5 + (mag_img["pos"]["y"] / scale)) * 2,
                                    0.5 + (mag_img["pos"]["x"] / scale))
                self.mag_sprite.scale = 0.5 * scale
                self.mag_sprite.color = (255, 255, 255)
                self.mag_sprite.visible = True

                self.sprite_list.remove(self.mag_sprite)
                pos = self.sprite_list.index(self.gun_sprite)
                if "top" in mag_img and mag_img["top"]:
                    self.sprite_list.insert(pos + 1, self.mag_sprite)
                else:
                    self.sprite_list.insert(pos, self.mag_sprite)

            else:
                self.mag_sprite.visible = False

        self.mag_top = "magImg" in worldimg_data and "top" in worldimg_data["magImg"] and worldimg_data["magImg"]["top"]

        # TODO some stuff related to rainbow blaster here

        if "gunOffset" in worldimg_data:
            offset = [-5.95, 0] if gtype_data["isDual"] else [-4.25, -1.75]
            offset[0] += worldimg_data["gunOffset"]["x"]
            offset[1] += worldimg_data["gunOffset"]["y"]

            for sprite in [self.gun_sprite, self.mag_sprite]:
                self.move_sprite(sprite, *offset)

    def hide(self):
        self.gun_sprite.visible = False
        self.mag_sprite.visible = False

    def show(self):
        self.gun_sprite.visible = True
        self.mag_sprite.visible = True


class Melee:
    # TODO fix offset bug
    def __init__(self, sprite_list: arcade.SpriteList, sprite: arcade.Sprite, parent: arcade.Sprite):
        self.list = sprite_list
        self.sprite = sprite
        self.parent = parent
        self.pos_offset = (0, 0)
        self.dir_offset = 0

    def update_pos(self):
        target_pos = rotate_vector(*self.pos_offset, self.parent.radians)
        target_pos = [i + j for i, j in zip(target_pos, self.parent.position)]
        self.sprite.position = target_pos

        self.sprite.radians = self.parent.radians - self.dir_offset

    def update_sprite(self, held_item):
        world_img = held_item["worldImg"]

        if "baseType" in held_item:
            world_img = configs.gtypes[held_item["baseType"]]["worldImg"] | world_img
        self.sprite.texture = load_texture(world_img["sprite"])
        x_scale = (world_img["scale"]["x"] * PLAYER_SCALE_FACTOR) / configs.constants["player"]["radius"]
        y_scale = (world_img["scale"]["y"] * PLAYER_SCALE_FACTOR) / configs.constants["player"]["radius"]
        self.sprite.texture = scale_texture(self.sprite.texture, x_scale, y_scale)
        self.sprite.color = num_to_colour(world_img["tint"])
        self.pos_offset = (-world_img["pos"]["x"]*world_img["scale"]["x"], -world_img["pos"]["y"]*world_img["scale"]["y"])
        self.dir_offset = world_img["rot"]


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
        # self.sprite_footL.scale = 0.45 * PLAYER_SCALE_FACTOR
        # self.sprite_footL.radians = 0.5
        self.sprite_footL_submerge = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_footR = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_footR.texture = load_texture("player-feet-01.png", hit_box_algorithm="None")
        # self.sprite_footR.scale = 0.45 * PLAYER_SCALE_FACTOR
        # self.sprite_footR.radians = 0.5
        self.sprite_footR_submerge = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_backpack = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_body = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_body_submerge = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_chest = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_chest.texture = load_texture("player-armor-base-01.png", hit_box_algorithm="None")
        self.sprite_chest.scale = 0.25 * PLAYER_SCALE_FACTOR
        # self.sprite_flak = arcade.Sprite(hit_box_algorithm="None")
        # self.sprite_steelskin = arcade.Sprite(hit_box_algorithm="None")
        # self.sprite_hip = arcade.Sprite(hit_box_algorithm="None")
        # self.sprite_bodyEffect = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_gunL = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_magL = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_handL = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_handL_submerge = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_objectL = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_gunR = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_magR = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_handR = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_handR.angle = 0
        self.sprite_handR_submerge = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_objectR = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_melee = arcade.Sprite(hit_box_algorithm="None")
        self.melee = Melee(self.sprite_list, self.sprite_melee, self.sprite_handR)
        # self.sprite_visor = arcade.Sprite(hit_box_algorithm="None")
        # self.sprite_accessory = arcade.Sprite(hit_box_algorithm="None")
        # self.sprite_patch = arcade.Sprite(hit_box_algorithm="None")
        self.sprite_helmet = arcade.Sprite(hit_box_algorithm="None")
        # self.sprite_slime = arcade.Sprite(hit_box_algorithm="None")
        # self.sprite_aim = arcade.Sprite(hit_box_algorithm="None")
        # self.sprite_phoenix = arcade.Sprite(hit_box_algorithm="None")
        # self.sprite_pyro = arcade.Sprite(hit_box_algorithm="None")

        self.gunL = Gun(self.sprite_list, self.sprite_gunL, self.sprite_magL, self)
        self.gunR = Gun(self.sprite_list, self.sprite_gunR, self.sprite_magR, self)

        self.sprites = [
            self.sprite_footL, self.sprite_footL_submerge, self.sprite_footR, self.sprite_footR_submerge,
            self.sprite_backpack, self.sprite_body, self.sprite_body_submerge, self.sprite_chest,
            self.sprite_gunL, self.sprite_magL, self.sprite_objectL, self.sprite_gunR, self.sprite_magR,
            self.sprite_melee, self.sprite_handL, self.sprite_handL_submerge, self.sprite_handR,
            self.sprite_handR_submerge, self.sprite_objectR, self.sprite_helmet
        ]

        self.sprite_list.extend(self.sprites)

        self.skin = None
        self.backpack = None
        self.helmet = None
        self.chest = None
        self.curWeapType = None
        self.layer = None
        self.dead = None
        self.downed = False
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

        # TODO add way to get ghillie colour

        self.update_netdata()
        self.update_sprites()
        self.skip_anim()

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

            rads_diff = self.dir_radians - self.prev_dir
            for sprite in self.sprites:
                rel_x = sprite.position[0] - self.pos[0]
                rel_y = sprite.position[1] - self.pos[1]

                radius = sqrt((rel_x ** 2) + (rel_y ** 2))
                angle = atan2(rel_y, rel_x) + rads_diff

                new_rel_x = radius * cos(angle)
                new_rel_y = radius * sin(angle)

                new_x = new_rel_x + self.pos[0]
                new_y = new_rel_y + self.pos[1]

                sprite.position = (new_x, new_y)
                sprite.radians = (sprite.radians + rads_diff) % (2 * pi)
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

    def update_sprites(self):
        skin_img = configs.gtypes[self.skin]["skinImg"]

        self.sprite_body.texture = load_texture(skin_img["baseSprite"])
        self.sprite_body.color = num_to_colour(skin_img["baseTint"])
        self.sprite_body.scale = 0.25 * PLAYER_SCALE_FACTOR
        self.sprite_body.visible = True
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
        self.sprite_footL.color = tint
        self.sprite_footL.visible = self.downed
        self.sprite_footR.color = tint
        self.sprite_footR.visible = self.downed

        # TODO draw flak if not ghillie

        # TODO ghillie stuff
        if self.chest:
            self.sprite_chest.visible = True
            self.sprite_chest.color = num_to_colour(configs.gtypes[self.chest]["skinImg"]["baseTint"])
        else:
            self.sprite_chest.visible = False

        # TODO draw steelskin if not ghillie

        # TODO draw phoenix

        # TODO draw pyro

        # TODO ghillie
        if self.helmet:
            self.sprite_helmet.visible = True
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
            self.sprite_helmet.visible = False

        # TODO ghillie

        # Update backpack
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
            self.sprite_backpack.visible = True
        else:
            self.sprite_backpack.visible = False

        # TODO draw pan

        held_item = configs.gtypes[self.curWeapType]
        # Update gun
        if held_item["type"] == "gun" and not (self.downed or self.animType == configs.constants["Anim"]["Revive"]):
            self.gunR.show()
            self.gunR.set_type(self.curWeapType, self.body_rad / configs.constants["player"]["radius"], self.gun_loaded)
        else:
            self.gunR.hide()
            self.gunL.hide()

        # Update held melee
        # TODO if downed/reviving, hide sprites
        if held_item["type"] == "melee" and self.curWeapType != "fists" and "handSprites" not in held_item:
            self.melee.update_sprite(held_item)
            self.sprite_melee.visible = True
        else:
            self.sprite_melee.visible = False

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
        pos = self.pos[0] + rotated[0], self.pos[1] + rotated[1]
        sprite.position = pos

    def set_rotation(self, sprite: arcade.Sprite, rads):
        sprite.radians = (self.dir_radians + rads) % (2 * pi)

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
            self.update_idle(str_to_sprite)
        else:
            pose = self.lerp_anim(times)
            pose = self.strip_dict_to_limbs(pose)

            for limb, value in pose.items():
                for sprite in str_to_sprite[limb]:
                    if value is not None:
                        target = rotate_vector(pose[limb][0], pose[limb][1],
                                               (pose[limb][2] + (0.5 if "Leg" in limb else 0)) * pi)
                        self.set_child_pos(sprite, target[0], -target[1])
                        self.set_rotation(sprite, (-pose[limb][2] + (0.5 if "Leg" in limb else 0)) * pi)

        self.melee.update_pos()

    def select_idle(self) -> dict:
        if self.downed:
            return configs.anims["idles"]["downed"]

        cur_weap_gdata = configs.gtypes[self.curWeapType]
        if "anim" in cur_weap_gdata and "idlePose" in cur_weap_gdata["anim"]:
            return configs.anims["idles"][cur_weap_gdata["anim"]["idlePose"]]

        if cur_weap_gdata["type"] == "gun":
            if "pistol" in cur_weap_gdata:
                return configs.anims["idles"]["dualPistol" if "isDual" in cur_weap_gdata else "pistol"]

            if "isBullpup" in cur_weap_gdata:
                return configs.anims["idles"]["bullpup"]
            if "isLauncher" in cur_weap_gdata:
                return configs.anims["idles"]["launcher"]

            return configs.anims["idles"]["rifle"]

        elif cur_weap_gdata["type"] == "throwable":
            return configs.anims["idles"]["throwable"]

        return configs.anims["idles"]["fists"]

    def update_idle(self, str_to_sprite):
        cur_weap_gtype = configs.gtypes[self.curWeapType]
        pose = self.select_idle()

        l_hand_offset = [0, 0]
        if cur_weap_gtype["type"] == "gun" and not self.downed:
            l_hand_offset[0] += cur_weap_gtype["worldImg"]["leftHandOffset"]["x"]
            l_hand_offset[1] += cur_weap_gtype["worldImg"]["leftHandOffset"]["y"]

        for limb, pos in pose.items():
            for sprite in str_to_sprite[limb]:
                if pos is not None:
                    sprite.visible = True
                    self.set_rotation(sprite, pos[2] * pi)

                    if limb == "HandL":
                        target = rotate_vector(pos[0] + l_hand_offset[0], -(pos[1] + l_hand_offset[1]), pos[2] * pi)
                    else:
                        target = rotate_vector(pos[0], -pos[1], pos[2] * pi)

                    self.set_child_pos(sprite, *target)
                else:
                    sprite.visible = False

    def skip_anim(self):
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
        diff_tl = target - lower
        diff_ut = upper - target
        return diff_tl / (diff_tl + diff_ut)

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
            if frame["time"][0] == "player":
                value = configs.constants
            else:
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
            self.get_weap_anim,
            lambda x: ("cook", False),
            lambda x: ("throw", False),
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
    def get_weap_anim(cur_weap):
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
        from survivpy_client import normalise_vec

        self.dummy_map.objects[0]["dir"] = normalise_vec(x, y)
        self.player_sprite.update_netdata()

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        self.player_sprite.start_anim()


class DummyMap:
    def __init__(self):
        self.objects = {0: {
            "outfit": "outfitParmaPrestige",
            "backpack": "",
            "helmet": "",
            "chest": "",
            "curWeapType": "machete",
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


if __name__ == '__main__':
    configs.update_configs()

    window = PlayerTestWindow()
    arcade.run()
