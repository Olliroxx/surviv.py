Game related API calls
======================
.. py:function:: api/game_modes
    Method: GET

    Response structure:

    .. code-block:: py

        resp = [
            {
                "mapName": "classic",
                "teamMode": 1
            },
            {
                "mapName": "classic",
                "teamMode": 2
            },
            {
                "mapName": "classic",
                "teamMode": 4
            },
            {
                "mapName": "woods",
                "teamMode": 2
            }
        ]

.. py:function:: api/find_game

    Method: POST

    Request structure:

    .. code-block:: py

        req = {
            "autoFill": bool,
            "gameModeIdx": int,  # There is a code for each game mode
            "isMobile": bool,  # Possibly allows analog inpu
            "playerCount": int,
            "region": str,  # eu for europe
            "version": int,  # Protocol version
            "zones": [
                str  # What servers are options, like fra or waw
            ]
        }

    Response structure:

    .. code-block:: py

        resp = {
            "res": [
                {
                    "addrs": [
                        "ip with port",
                        "ip"
                    ],
                    "data": str,  # This is matchPriv
                    "gameId": str,
                    "hosts": [
                        "server with port",
                        "server"
                    ],
                    "useHttps": bool,  # Usually true
                    "zone": str
                }
            ]
        }
