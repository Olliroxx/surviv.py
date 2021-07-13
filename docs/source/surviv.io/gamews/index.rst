Game websockets
===============
The main game websocket contains all data relevant to a game (anything that isn't in a menu)

Each packet contains one or more messages. No more messages are decoded if there is a null byte after a message

.. toctree::
   :maxdepth: 2

   packets/index
   types
