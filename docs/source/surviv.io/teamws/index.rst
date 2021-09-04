Team websocket
==============
A websocket connection is established between the client and the surviv.io/team_v2 endpoint to create a team. JSON
encoded text messages are used to communicate. Every message is a dictionary with a ``type``(a string) and a ``data``
(a dictionary) field. The only exception is ``gameComplete`` which does not have a ``data`` field.

Downward types:
---------------

keepAlive
^^^^^^^^^
``data`` is empty, sent every 30 seconds

state
^^^^^
 * localPlayerId : int (NOT slot number, [number]th player to ever join that room, including reloads)
 * players : list(dict)
    * ingame : bool
    * isLeader : bool
    * loadout : dict
        * melee : str
        * outfit : str
    * name : str
    * playerId : int (localPlayerId but for other people)
    * unlinked : bool
 * room : dict
    * autofill : bool
    * enabledGameModeIdxs: list(int)
    * findingGame : bool
    * gmaeModeIdx : int
    * gameModeSelected : list(int)
    * lastError : str
    * maxPlayers : int
    * region : str
    * roomUrl : str

joinGame
^^^^^^^^
Same as a find_game request when not in the team menu, sets ``findingGame`` in ``state`` messages to ``false``.

kicked
^^^^^^

error
^^^^^
Possibly other fields, only seen in code?

* type : str


Upward types:
-------------

create
^^^^^^
First message of a room. Format:

 * playerData : dict
    * isMobile: bool
    * loadout : dict
        * melee : str
        * outfit : str
    * name : str
    * unlinked : bool
 * roomData : dict
    * autoFill : bool
    * findingGame : bool
    * gameModeIdx : int
    * gameModeSelected : list(int)
    * lastError : str
    * region : str
    * roomUrl : str

join
^^^^
Same as ``create``, but ``roomUrl`` is used instead of ``roomData``

setRoomProps
^^^^^^^^^^^^
 * autofill : bool
 * enabledGameModeIdxs : list(int)
 * findingGame : bool
 * gameModeIdx : int
 * gameModeSelected : list(int)
 * lastError : str
 * maxPlayers : int
 * region : str
 * roomUrl : str

playGame
^^^^^^^^
Same as a find_game request when not in the team menu, sets ``findingGame`` in ``state`` messages to ``true``.

gameComplete
^^^^^^^^^^^^
Does not have ``data`` dictionary, called when a game has finished (the play again button is pressed)

kick
^^^^
 * playerId : str(int)

keepAlive
^^^^^^^^^
``data`` is empty. Sent every 45 seconds as long as an unknown condition is met
