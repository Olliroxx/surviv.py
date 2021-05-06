"""
Joins a game and then does nothing but print the raw responses
"""
from src.survivpy.netManager import pregame

profile = pregame.Profile()
print("Joining game")
game = profile.join_game()
print("Joined")

try:
    while True:
        messages = game.get_decoded_messages()
        for message in messages:
            if message == game.EXIT:
                print("Exiting")
                quit()
            else:
                print(message)
except KeyboardInterrupt:
    exit()
