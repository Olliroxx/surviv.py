Game related API calls
======================

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
            ],
            "adminCreate": bool,  # For making tournaments maybe?
            "privCode": bool  # For joining tournaments?
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

.. py:function:: api/site_info?language=en

    Method: GET

    Returns current modes and active youtube/twitch streamers
