"""
Joins a game and then does nothing but print the raw responses
"""
from src.survivpy_net import pregame

profile = pregame.Profile()
game_connection = profile.prep_game()
print("Joining game")
game_connection.start()
print("Joined")

try:
    while True:
        messages = game_connection.get_messages()
        for message in messages:
            if message == game_connection.EXIT:
                print("Exiting")
                quit()
            else:
                print(message)
except KeyboardInterrupt:
    exit()
