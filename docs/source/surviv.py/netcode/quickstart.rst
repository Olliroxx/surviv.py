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
