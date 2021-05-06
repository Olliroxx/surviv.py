The main game websocket contains all data relevant to a game (anything that isn't in a menu)


### Packet types
The first byte contains the type of packet  
Types of packet:
* hex:dec InternalName
*  00:00 None
*  01:01 Join
*  02:02 Disconnect
*  03:03 Input
*  04:04 Edit
*  05:05 Joined
*  06:06 Update
*  07:07 Kill
*  08:08 GameOver
*  09:09 Pickup
*  0a:10 Map
*  0b:11 Spectate
*  0c:12 DropItem
*  0d:13 Emote
*  0e:14 PlayerStats
*  0f:15 AdStatus
*  10:16 Loadout
*  11:17 RoleAnnouncement
*  12:18 Stats
*  13:19 Update pass
*  14:20 AliveCounts
*  15:21 PerkModeRoleSelect
*  16:22 gamePlayerStat
*  17:23 battleResults

