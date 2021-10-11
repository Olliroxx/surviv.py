"""
General architecture:
There is a list of layers, iterated (.draw() is called, so sprite lists cna be used)over each frame
list of level_layers which is iterated over twice (for ground floor and underground)

Player layer:
sprite list of `player` class (inherits arcade.sprite)?
"""


import arcade
from arcade import gui

from survivpy_net.ingame import GameConnection
from survivpy_net import configs

from math import sin, cos, pi, atan2, atan, sqrt

# from random import choice as rand_choice
from logging import getLogger

logger = getLogger("survivpy_client")

ASSET_ROOT = "./assets/imgs_world/"


def rotate_vector(x, y, angle):
    new_x = x*cos(angle)-y*sin(angle)
    new_y = y*cos(angle)+x*sin(angle)
    return new_x, new_y


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


class Player:
    def __init__(self, player_id, map_obj, sprite_list: arcade.SpriteList):
        super().__init__()

        self.id = player_id
        self.map = map_obj
        self.sprite_list = sprite_list

        # TODO this
        self.loadout = {
            "melee": {
                "scale": {
                    "x": 0.175,
                    "y": 0.175
                },
                "name": "fists"
            }
        }

        self.sprite_footL = arcade.Sprite()
        self.sprite_footL.texture = arcade.load_texture(ASSET_ROOT+"player-feet-01.png")
        self.sprite_footL.scale = 0.45
        self.sprite_footL.radians = 0.5
        self.sprite_footL_submerge = arcade.Sprite()
        self.sprite_footR = arcade.Sprite()
        self.sprite_footR.texture = arcade.load_texture(ASSET_ROOT+"player-feet-01.png")
        self.sprite_footR.scale = 0.45
        self.sprite_footR.radians = 0.5
        self.sprite_footR_submerge = arcade.Sprite()
        self.sprite_backpack = arcade.Sprite()
        self.sprite_backpack.texture = arcade.load_texture(ASSET_ROOT+"player-circle-base-01.png")
        self.sprite_body = arcade.Sprite()
        self.sprite_body_submerge = arcade.Sprite()
        self.sprite_chest = arcade.Sprite()
        self.sprite_chest.texture = arcade.load_texture(ASSET_ROOT+"player-armor-base-01.png")
        self.sprite_chest.scale = 0.25
        self.sprite_flak = arcade.Sprite()
        self.sprite_steelskin = arcade.Sprite()
        self.sprite_hip = arcade.Sprite()
        self.sprite_bodyEffect = arcade.Sprite()
        self.sprite_gunL = arcade.Sprite()
        self.sprite_handL = arcade.Sprite()
        self.sprite_handL_submerge = arcade.Sprite()
        self.sprite_objectL = arcade.Sprite()
        self.sprite_gunR = arcade.Sprite()
        self.sprite_melee = arcade.Sprite()
        self.sprite_handR = arcade.Sprite()
        self.sprite_handR_submerge = arcade.Sprite()
        self.sprite_objectR = arcade.Sprite()
        self.sprite_visor = arcade.Sprite()
        self.sprite_accessory = arcade.Sprite()
        self.sprite_patch = arcade.Sprite()
        self.sprite_helmet = arcade.Sprite()
        self.sprite_slime = arcade.Sprite()
        self.sprite_aim = arcade.Sprite()
        self.sprite_phoenix = arcade.Sprite()
        self.sprite_pyro = arcade.Sprite()

        self.sprites = [self.sprite_footL, self.sprite_footL_submerge, self.sprite_footR, self.sprite_footR_submerge,
                        self.sprite_backpack, self.sprite_body, self.sprite_body_submerge, self.sprite_chest,
                        self.sprite_flak, self.sprite_steelskin, self.sprite_hip, self.sprite_bodyEffect,
                        self.sprite_gunL, self.sprite_handL, self.sprite_handL_submerge, self.sprite_objectL,
                        self.sprite_gunR, self.sprite_melee, self.sprite_handR, self.sprite_handR_submerge,
                        self.sprite_objectR, self.sprite_visor, self.sprite_accessory, self.sprite_patch,
                        self.sprite_helmet, self.sprite_slime, self.sprite_aim, self.sprite_phoenix, self.sprite_pyro]
        self.sprite_list.extend(self.sprites)

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

        self.active = True
        self.prev_active = True

        # self.anim = {
        #     "type": 0,
        #     "mirrored": False,
        #     "name": None,
        #     "seq": -1,
        #     "ticker": 0
        # }
        # self.bones = {
        #     "HandR": {"pos": (18.0, -8.25), "weight": 0},
        #     "HandL": {"pos": (6.0, 20.25), "weight": 0},
        #     "FootR": None,
        #     "FootL": None
        # }
        # TODO anim stuff
        # TODO add way to get ghillie colour

        self.update_data()
        self.update_sprites()

    def update_data(self):
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
            self.dir_radians = atan2(*self.dir[::-1])
            rads_diff = self.dir_radians - self.prev_dir
            for sprite in self.sprites:
                x_offset = sprite.position[0]-self.pos[0]
                y_offset = sprite.position[1]-self.pos[1]

                try:
                    angle = atan(y_offset/x_offset)
                except ZeroDivisionError:
                    angle = 0.5 * pi if y_offset > 0 else -0.5 * pi

                distance = sqrt(y_offset**2+x_offset**2)
                new_angle = angle+rads_diff

                new_x = distance * cos(new_angle)
                new_y = distance * sin(angle)

                x_diff = new_x-x_offset
                y_diff = new_y-y_offset

                sprite.position += (x_diff, y_diff)
                sprite.radians = (sprite.radians + rads_diff) % (2*pi)

            self.prev_pos = self.pos
            self.pos = data["pos"]
            diff = self.pos[0] - self.prev_pos[0], self.pos[1] - self.prev_pos[1]
            for sprite in self.sprites:
                sprite.position += diff

            # Move the sprites to new positions

        else:
            self.active = False
            if self.active != self.prev_active:
                self.hide()

    def update_hand_sprite(self, sprite: arcade.Sprite, name, tint=(255, 255, 255), flipped=False):
        sprite.texture = arcade.load_texture(ASSET_ROOT+name, flipped_horizontally=flipped)
        sprite.radians = pi * 0.5
        sprite.color = tint
        scale = {"x": 0.175, "y": 0.175}
        if tint == (255, 255, 255):
            try:
                scale = configs.gtypes[self.loadout["melee"]["name"]]["scale"]
            except KeyError:
                pass

        if scale["x"] != scale["y"]:
            raise RuntimeWarning("Non-uniform scale values")
        sprite.scale = scale["x"]

        return sprite

    @staticmethod
    def update_foot_sprite(sprite: arcade.Sprite, tint, visible: bool):
        sprite.color = tint
        sprite.alpha = 255 * int(visible)

    def update_sprites(self):

        skin_img = configs.gtypes[self.skin]["skinImg"]

        self.sprite_body.texture = arcade.load_texture(ASSET_ROOT+skin_img["baseSprite"])
        self.sprite_body.color = num_to_colour(skin_img["baseTint"])
        self.sprite_body.scale = 0.25
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
            self.sprite_helmet.texture = arcade.load_texture(ASSET_ROOT+configs.gtypes[self.helmet]["skinImg"]["baseSprite"])
            offset = 3.33 * -1 if self.downed else 1
            self.move_child(self.sprite_helmet, offset, 0, self.dir_radians)

            self.sprite_helmet.color = num_to_colour(configs.gtypes[self.helmet]["skinImg"]["baseTint"])

            if "spriteScale" in configs.gtypes[self.helmet]["skinImg"]:
                scale = configs.gtypes[self.helmet]["skinImg"]["spriteScale"]
                self.sprite_helmet.scale = scale
            else:
                self.sprite_helmet.scale = 0.15
            # TODO 50v50

        else:
            self.sprite_helmet.alpha = 0

        # TODO ghillie
        if self.backpack != "" and not self.downed:
            pack_data = configs.gtypes[self.backpack]

            offsets = [10.25, 11.5, 12.75]
            offset = offsets[pack_data["level"] - 1]
            scale = (0.4 + pack_data["level"] * 0.03) * 0.5
            self.sprite_backpack.position = self.sprite_backpack.position[0] + offset, self.sprite_backpack.position[1]
            self.sprite_backpack.color = num_to_colour(pack_data["tint"])
            self.sprite_backpack.scale = scale
            self.sprite_backpack.alpha = 255
        else:
            self.sprite_backpack.alpha = 0

        # TODO draw pan

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

    @staticmethod
    def move_child(sprite: arcade.Sprite, x, y, parent_angle):
        sprite.position += rotate_vector(x, y, parent_angle)

    # def start_anim(self):
    #     name, mirrored = self._get_anim_name()
    #     self.anim = {
    #         "type": self.animType,
    #         "mirrored": mirrored,
    #         "name": name,
    #         "seq": self.animSeq,
    #         "ticker": 0
    #     }
    #
    # def _get_anim_name(self):
    #     """
    #     Gets animation data for current state
    #     """
    #     anim_name_functions = [
    #         lambda x: ("none", False),
    #         lambda x: ("cook", False),
    #         lambda x: ("throw", False),
    #         lambda x: ("revive", False),
    #         lambda x: ("crawl_forward", True),
    #         lambda x: ("crawl_backward", True),
    #         self._get_melee_anim,
    #         self._get_change_pose_anim
    #     ]
    #     Each function takes `self.curWeapType` and returns a 2-tuple containing the animation name and
    #     # if it mirroring should be used (eg. cook always needs to hold the grenade in the right hand, crawling doesn't care)
    #     translation_dict = dict(zip(configs.constants["Anim"], anim_name_functions))
    #     # Creates a dictionary that maps from `animType`s (ints) to 2-tuple functions (see above)
    #     anim_type, mirrorable = translation_dict[self.animType](self.curWeapType)
    #
    #     if mirrorable:
    #         mirrored = rand_choice([True, False])
    #     else:
    #         mirrored = False
    #
    #     return anim_type, mirrored
    #
    # @staticmethod
    # def _get_melee_anim(cur_weap):
    #     gtype_data = configs.gtypes[cur_weap]
    #     if "anim" not in gtype_data or "attackAnims" not in gtype_data["anim"]:
    #         return "fists", True
    #     attack_anims = gtype_data["anim"]["attackAnims"]
    #     return rand_choice(attack_anims), attack_anims == ["fists"]
    #
    # @staticmethod
    # def _get_change_pose_anim(cur_weap):
    #     """
    #     Used for lightsabers?
    #     """
    #     gtype_data = configs.gtypes[cur_weap]
    #     if "anim" not in gtype_data or "poseAnims" not in gtype_data["anim"]:
    #         return "none", True
    #     attack_anims = gtype_data["anim"]["poseAnims"]
    #     return rand_choice(attack_anims), attack_anims == ["fists"]

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
            "outfit": "outfitBase",
            "backpack": "backpack03",
            "helmet": "helmet02",
            "chest": "chest02",
            "curWeapType": "fists",
            "layer": 1,
            "dead": False,
            "downed": False,
            "animType": 1,
            "animSeq": 1,
            "wearingPan": False,
            "hasActionItem": False,
            "actionItem": "",
            "playerScale": 1.,
            "dir": (1, 0),
            "pos": (0, 0)
        }}


class TestWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Test window")
        self.sprite_list = arcade.SpriteList()
        self.dummy_map = DummyMap()
        self.player_sprite = Player(0, self.dummy_map, self.sprite_list)
        self.cam = arcade.Camera(800, 600)
        # noinspection PyTypeChecker
        self.cam.move((-400, -300))

    def on_draw(self):
        arcade.start_render()
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
    window = TestWindow()
    arcade.run()
