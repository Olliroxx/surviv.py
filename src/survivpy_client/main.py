import arcade
from arcade import gui

from survivpy_net.ingame import GameConnection
from logging import getLogger

logger = getLogger("survivpy_client")


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
