"""
Joins a game and then does nothing but print the raw responses
"""
from src.survivpy_net import pregame

profile = pregame.Profile()
print("Joining game")
gameConnection = profile.join_game()
print("Joined")

try:
    while True:
        messages = gameConnection.get_decoded()
        for message in messages:
            if message == gameConnection.EXIT:
                print("Exiting")
                quit()
            else:
                print(message)
except KeyboardInterrupt:
    exit()
