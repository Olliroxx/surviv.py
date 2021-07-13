Type 0x5/5 packet (joined)
==========================
Direction: down

Contains:

 * "teamMode" uint8 : amount of team members (one for solos)
 * "playerId" uint16
 * "started" bool : has the game started (always true)
 * emoteCount uint8
 * for emoteCount:
     * emote gameType
     * emotes.append(emote)
