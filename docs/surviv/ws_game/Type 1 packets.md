Direction: up  
Contains:
* "protocol" int : Netcode version
* "matchPriv" str : (Probably) encrypted data, received from api (find_game)
* "loadoutPriv" str : (Probably) encrypted data, received from api (profile_unlinked)
* "loadoutStats" str : (Probably) encrypted data, received from api (profile_unlinked)
* "hasGoldenBP" bool : If player has purchased premium pass
* "questPriv" str : (Probably) encrypted data, received from api (get_pass_unlinked)
* "name" str : If player is unlinked, must be "surviv#" and then the player if (from profile_unlinked)
* "isUnlinked" bool : Unknown where this is defined
* "useTouch" bool : Use alternate input method (direction instead of 4 bools) (assumed)
* "isMobile" bool : Use mobile servers (assumed)
* "proxy" bool : Using one of the proxy sites (assumed)
* "otherProxy" bool : Using one of the proxy sites (assumed)
* "bot" bool : Is player a bot (used to fill slots when there aren't enough players) (assumed)
* "autoMelee" bool : Anticheat or something to do with the mobile version? (unsure)
* "aimAssist" bool : Anticheat or something to do with the mobile version? (unsure)
* "kpg" str : Kills per game, used as a ranking (assumed)
* "progressNotificationActive" bool : Show quest progress updates (assumed)

This is the first (websocket) packet sent in a session. The server will not send any packets back without sending this
