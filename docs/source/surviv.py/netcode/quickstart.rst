Quickstart
==========

This is a tutorial on how to write a program that connects to a surviv game

The smallest possible script:

.. code-block:: py

    import surviv_net as spn

    profile = spn.pregame.Profile()
    # user_id = profile.id
    conn = profile.join_game()

    do_something(conn.state)

Currently, linked accounts and lobbies are not supported, but if you want to reuse an unlinked id you can just pass it to Profile  
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
