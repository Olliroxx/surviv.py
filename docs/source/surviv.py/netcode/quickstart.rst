Quickstart
==========

This is a tutorial on how to write a program that connects to a surviv game.

Before you can connect, you need to copy a set of .json files to ./configs (relative to your script).
A set of configs are bundled with every release, but they might be outdated when the script is run.
To generate a set of configs, run surviv_deob from the command line in the same directory as the script.
This will make a set of directories, delete all of them except for jsons and rename it to configs.
This takes a long time and is processor intensive at times.

The smallest possible script:

.. code-block:: py

    import survivpy_net as spn

    profile = spn.pregame.Profile()
    # user_id = profile.id
    conn = profile.prep_game()
    conn.start()

    do_something(conn.state)

Currently, linked accounts are not supported, but if you want to reuse an unlinked id you can just pass it to Profile
To change inputs:

.. code-block:: py
    
    msg = {
        "moveLeft": False,
        "moveRight": False,
        "moveUp": False,
        "moveDown": False,
        "shootStart": False,
        "shootHold": False,
        "toMouseDir": Vector(1, 0),
        "toMouseLen": 0,
        "useItem": ""
    }
    conn.send_input_msg(msg)

Lobbies:

.. code-block:: py


    import survivpy_net as spn

    profile = spn.pregame.Profile()

    lobby_data = {
        "autofill": True,
        "findingGame": False,
        "gameModeIdx": 1,
        "lastError": "",
        "region": "eu",
        "roomUrl": ""
    }
    lobby = profile.create_lobby(lobby_data)
    # lobby = profile.join_lobby("daWi")

    lobby.set_props, play_game, kick, game_complete
