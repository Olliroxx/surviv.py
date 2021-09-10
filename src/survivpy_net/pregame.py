from logging import getLogger
from ws4py.client.threadedclient import WebSocketClient
from json import loads, dumps
from time import time
logger = getLogger("survivpy_net")

KNOWN_SAFE_VERSION = 108


class Profile:
    """
    Some attributes of note:
    * pass_data: dict containing levels, xp and unlocks
    * kpg, total_wins, total_games: some stats
    * loadout: skins, starting melee, emotes, particles and crosshair

    :param id_: Optional, the user id to use. If not set will make a new account
    """

    def __init__(self, id_=None, ):

        self.id = id_
        import requests
        self.session = requests.session()
        del requests
        self.loadout_priv = None
        self.loadout_stats = None
        self.quest_priv = None

        self.unlinked = True
        self.use_touch = False
        self.is_mobile = False
        self.proxy = False
        self.other_proxy = False
        self.bot = False
        self.auto_melee = False
        self.aim_assist = False
        self.kpg = "0.0"
        self.progress_notification_active = True
        self.ign = "Player"
        # Defaults for joining a game

        self.total_games = 0
        self.total_wins = 0
        if id_ is None:
            self.set_user_id_new()
        self.loadout = None
        self.loadout_ids = None

        self.user_currency_info = []
        self.user_pass_max_level = []
        self.user_transaction_data = []

        self.pass_data = None
        self.quests = []

        self.update_profile()
        self.reset_prestige()
        self.update_pass()
        self.update_currency()

        from json import load
        with open("./configs/constants.json") as file:
            data = load(file)

        self.version = data["protocolVersion"]
        if self.version != KNOWN_SAFE_VERSION:
            raise RuntimeWarning("Protocol version is not known safe, things may break or work fine")

    def update_currency(self):
        """
        Update local copy of currency and transaction data
        """
        resp = self.session.post("https://surviv.io/api/user/get_user_currency_total").json()

        if not resp:
            raise RuntimeError("Currency update was not successful")

        self.user_currency_info = resp["userCurrencyInfo"]
        self.user_pass_max_level = resp["userPassMaxLevel"]
        self.user_transaction_data = resp["userTransactionData"]

    def reset_prestige(self):
        self.session.post("https://surviv.io/api/user/reset_prestige_points")

    @staticmethod
    def _gen_user_id():
        import random

        bytelist = []
        for i in range(16):
            bytelist.append(random.randbytes(1).hex())
        bytelist[6] = format(15 & int(bytelist[6], 16) | 64, "x")  # Set to value so that byte 7 is between 64 and 79
        bytelist[8] = format(63 & int(bytelist[8], 16) | 128, "x")  # Set to value so that byte 9 is between 128 and 191
        user_id = "".join(bytelist[0:4]) + str(random.randint(0, 9)) + "".join(bytelist[4:6]) + str(
            random.randint(0, 9)) + "".join(bytelist[6:8]) + "-" + "".join(bytelist[8:10]) + "-" + "".join(
            bytelist[10:])

        return user_id

    def set_user_id_new(self, force=False):

        if not force and self.id is not None:
            raise RuntimeError("User ID already set")

        self.id = self._gen_user_id()

    def update_profile(self):
        resp = self._get_profile_unlinked()

        if not resp["success"]:
            raise RuntimeError("Profile retrieval unsuccessful")

        profile = resp["profile"]

        self.kpg = str(profile["kpg"])
        self.total_wins = profile["wins"]
        self.total_games = profile["games"]
        self.loadout = resp["loadout"]
        self.loadout_ids = resp["loadoutIds"]
        self.loadout_priv = resp["loadoutPriv"]
        self.loadout_stats = resp["loadoutStats"]

        if profile["username"] != "Player":
            self.ign = profile["username"]
        else:
            self.ign = "surviv#" + profile["id"]

    def _get_profile_unlinked(self):
        """
        Gets profile info of user with [user_id]
        :return: parsed server response, session
        """

        if self.id is None:
            return NameError("Need user ID")

        resp = self.session.post("https://surviv.io/api/user/profile_unlinked", json={"userId": self.id}).json()

        return resp

    def update_pass(self):
        """
        Update local copy of pass
        :return:
        """
        resp = self._get_pass_unlinked()
        if not resp["success"]:
            raise (IOError("Pass retrieval unsuccessful"))
        self.pass_data = resp["pass"]
        self.quests = resp["quests"]
        self.quest_priv = resp["questPriv"]

    def _get_pass_unlinked(self, tryRefreshQuests=True, forceUpdate=False, resetTeams=True):
        """
        Gets pass and related info
        :param tryRefreshQuests: try to refresh quests, at a price (small amount of supporting evidence)
        :param forceUpdate: force update (server side) of pass info (assumed)
        :param resetTeams: unknown
        :return: parsed server response
        """

        settings = {"forceUpdate": forceUpdate,
                    "resetTeams": resetTeams,
                    "tryRefreshQuests": tryRefreshQuests,
                    "userId": self.id}
        resp = self.session.post("https://surviv.io/api/user/get_pass_unlinked", json=settings).json()

        return resp

    def _update_game_settings(self):
        self.game_settings = {
            "loadoutPriv": self.loadout_priv,
            "loadoutStats": self.loadout_stats,
            "questPriv": self.quest_priv,
            "name": self.ign,
            "isUnlinked": self.unlinked,
            "useTouch": self.use_touch,
            "isMobile": self.is_mobile,
            "proxy": self.proxy,
            "otherProxy": self.other_proxy,
            "bot": self.bot,
            "autoMelee": self.auto_melee,
            "aimAssist": self.aim_assist,
            "kpg": self.kpg,
            "progressNotificationActive": self.progress_notification_active
        }

    def join_game(self, settings=None):
        """
        Contacts matchmaking server, finds game and server
        :param settings: settings, needed for game mode other than standard solos, or regions other than eu
        :return: game object
        """

        if settings is None:
            settings = {
                "autoFill": False,
                "gameModeIdx": 0,
                "isMobile": False,
                "playerCount": 1,
                "region": "eu",
                "version": self.version,
                "zones": ["fra", "waw"]
            }

        if str(type(settings)) != "<class 'dict'>":
            raise TypeError("Settings must be a dictionary")

        resp = self.session.post("https://surviv.io/api/find_game", json=settings).json()

        if "res" not in resp:
            if resp == {"err": "invalid_protocol"}:
                raise IOError("Configs are out of date, cannot join.")
            raise IOError("Server returned non-ok response: " + str(resp))

        self._update_game_settings()
        settings = self.game_settings
        settings["matchPriv"] = resp["res"][0]["data"]
        settings["hasGoldenBP"] = False

        uri = "wss://" + resp["res"][0]["hosts"][0] + "/play?gameId=" + resp["res"][0]["gameId"]

        self.update_profile()
        self.reset_prestige()
        self.update_pass()
        # The vanilla js client does this before each game

        from survivpy_net import ingame
        return ingame.GameConnection(uri, settings, self.version)

    def build_player_data(self):
        return {
            "isMobile": self.is_mobile,
            "loadout": {
                "melee": self.loadout["melee"],
                "outfit": self.loadout["outfit"]
            },
            "name": self.ign,
            "unlinked": self.unlinked
        }

    def join_lobby(self, lobby_url):
        return JoinLobbyClient(lobby_url, self.build_player_data())

    def create_lobby(self, room_data):
        """
        Example ``room_data``:

            .. code-block:: py

            {
                "autoFill": True,
                "findingGame": False,
                "gameModeIdx": 1,
                "lastError": "",
                "region": "eu",
                "roomUrl": ""
            }

        """
        return CreateLobbyClient(room_data, self.build_player_data())


class _LobbyClient(WebSocketClient):
    def __init__(self):
        super().__init__("wss://surviv.io/team_v2")
        self.state = {"state": "opening", "reason": ""}
        self.local_player_id = 0
        self.players = []
        self.room = {}
        self.game_data = None
        self.time_since_packet = time()
        self.connect()

    def set_props(self, props):
        self.send(dumps({"type": "setRoomProps", "data": props}))

    def received_message(self, message):
        message = message.data.decode("utf-8")

        def keep_alive(data):
            pass

        def state(data):
            self.local_player_id = data["localPlayerId"]
            self.players = data["players"]
            self.room = data["room"]

        def join_game(data):
            self.game_data = data

        def kicked(data):
            self.close(reason="Kicked")

        def error(data):
            self.close(reason="Error of type " + str(data["type"]))

        self.time_since_packet = time()
        message_handlers = {
            "keepAlive": keep_alive,
            "state": state,
            "joinGame": join_game,
            "kicked": kicked,
            "error": error
        }
        message = loads(message)
        if message["type"] not in message_handlers:
            raise RuntimeError("Unexpected message type: " + str(message["type"]))
        else:
            message_handlers[message["type"]](message["data"])

    def opened(self):
        self.state = {"state": "open", "reason": ""}

    def closed(self, code, reason=None):
        self.state = {"state": "closed", "reason": reason}
        self.game_data = None

    def play_game(self, data):
        self.send(dumps({"type": "playGame", "data": data}))

    def game_complete(self):
        self.send(dumps({"type": "gameComplete"}))
        self.game_data = None

    def kick(self, player_id):
        self.send(dumps({"type": "kick", "data": {"playerId": str(player_id)}}))


class CreateLobbyClient(_LobbyClient):
    def __init__(self, room, player):
        super().__init__()
        self.join_data = {"playerData": player, "roomData": room}

    def opened(self):
        super().opened()
        self.send(dumps({"type": "create", "data": self.join_data}))


class JoinLobbyClient(_LobbyClient):
    def __init__(self, room_url, player):
        super().__init__()
        self.join_data = {"playerData": player, "roomUrl": room_url}

    def opened(self):
        super().opened()
        self.send(dumps({"type": "join", "data": self.join_data}))
