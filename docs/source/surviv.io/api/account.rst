Account API calls
=================
.. py:function::  api/user/get_user_currency_total

    Method: POST

    Response structure:

    .. code-block:: py

      resp = {
        "success" : bool,
        "userCurrencyInfo": list,
        "userPassMaxLevel": list,
        "userTransactionData": list,
      }

.. py:function::  api/user/reset_prestige_points

    Method: POST

.. py:function::  api/user/profile_unlinked

    Method: POST

    Request structure:

    .. code-block:: py

       req = {
        "userId": str
       }

    A user ID can be generated using this code:

    .. code-block:: py

        def gen_user_id():
            import random

            bytelist = []
            for i in range(16):
                bytelist.append(random.randbytes(1).hex())
            bytelist[6] = format(15 & int(bytelist[6], 16) | 64, "x")  # Set to value so that byte 7 is between 64 and 79
            bytelist[8] = format(63 & int(bytelist[8], 16) | 128, "x")  # Set to value so that byte 9 is between 128 and 191
            user_id = "".join(bytelist[0:4]) + str(random.randint(0, 9)) + "".join(bytelist[4:6]) + str(
                random.randint(0, 9)) + "".join(bytelist[6:8]) + "-" + "".join(bytelist[8:10]) + "-" + "".join(
                bytelist[10:])

            return user_id

    Response structure:

    .. code-block:: py

      resp = {
        "success": True,
        "profile": {
           "errorFlash": [],
           "id": "22028189",
           "slug": None,
           "kpg": 0,
           "wins": 0,
           "games": 0,
           "username": "Player",
           "usernameSet": False,
           "usernameChangeTime": -1619853519756,
           "userCreated": "2021-05-08T07: 18: 39.000Z",
           "linkedFacebook": False,
           "linkedGoogle": False,
           "linkedTwitch": False,
           "linkedDiscord": False,
           "linkedApple": False,
           "linkedSteam": False,
           "gpTotal": 0,
           "offerwallGpWon": None,
           "forteUserId": None,
           "prestige": "0",
           "prestigeChangeTime": "1970-01-01T00: 00: 00.000Z",
           "endorsePoints": 3,
           "reportPoints": 3,
           "unlinked": True,
           "gift": {
               "hasPendingGift": False,
               "gp": 0,
               "description": None
           },
           "banStrikes": 0,
           "prestigeResetTime": "2021-05-08T07: 18: 39.000Z"
        },
        "loadout": {
          "outfit": "outfitBase",
          "melee": "fists",
          "heal": "heal_basic",
          "boost": "boost_basic",
          "player_icon": "",
          "crosshair": {
            "type": "crosshair_default",
            "color": 16777215,
            "size": "1.00",
            "stroke": "0.00"
          },
          "emotes": [
            "emote_happyface",  # Top slot
            "emote_thumbsup",  # Right slot
            "emote_surviv",  # Bottom slot
            "emote_sadface",  # Left slot
            "", # One of these is the win slot, one is the death slot
            ""
          ],
          "deathEffect": "regularDeath"
        },
        "loadoutIds": {
          "heal": "0",
          "boost": "0",
          "melee": "0",
          "emotes": [
            "0",
            "0",
            "0",
            "0",
            "0",
            "0"
          ],
          "outfit": "0",
          "deathEffect": "0"
        },
        "loadoutPriv": "A very long string",
        "loadoutStats": "A very long string",
        "items": [
        ],
       "error":  None
      }

.. py:function::  api/user/get_pass_unlinked

    Method: POST

    There are two uses of this.
    This first is called once every time you visit the website:

    .. code-block:: py

       req = {
           "forceUpdate": bool,  # Normally false
           "resetTeams": bool,  # Normally true
           "tryRefreshQuests": bool,  # Normally true
           "userId": str,  # See api/user/profile_unlinked on how to generate this
       }

    The second type is called more often, at the start of games and periodically:

    .. code-block:: py

       req = {
          "tryRefreshQuests": bool,  # Normally false
          "userId": str,
       }

    They have the same response structure:

    .. code-block:: py

      resp = {
        "success":True,
        "pass":{
          "type":"pass_survivrX",  # X is the season
          "level":1,
          "xp":0,
          "unlocks":{
          },
          "newItems":False,
          "newGP":False,
          "items":[],
          "lvlUpItems":[],
          "newPass":True,
          "gpChange":0,
          "premium":False,
          "xp_rewards":False,
          "xp_reward_timestamp":None,
          "newDiscount":False,
          "discount_level":None,
          "discount_time":None,
          "team_members":0,
          "newItemsData":None
        },
        "quests":[
          {
            "idx":0,
            "type":"quest_crates",
            "args":{
              "xp":36,
              "random":0.6347462007415983
            },
            "progress":0,
            "target":31,
            "complete":False,
            "rerolled":False,
            "timeToRefresh":2479869,
            "xpReward":36,
            "timeAcquired":1620458320000
          },
          {
            "idx":1,
            "type":"quest_damage_762mm",
            "args":{
              "xp":36,
              "random":0.6441083358572901
            },
            "progress":0,
            "target":293,
            "complete":False,
            "rerolled":False,
            "timeToRefresh":2479869,
            "xpReward":36,
            "timeAcquired":1620458320000
          }
        ],
        "questPriv":"A very long string"}
      }
