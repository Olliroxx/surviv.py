Type 0x6/6 packet (update)
==========================
Most common type of packet, this is more complex than most.

Different object types have different decoders:

.. toctree::
    :maxdepth: 2

    object_decoders/index

The first 2 non-packet-type bytes represent a uint16, that says what operations are taking place
The operations are:

 * Deleted objects (1<<0)
 * Full objects (1<<1)
 * Active player id (1<<2)
 * Gas (You get the idea)
 * Gas circle
 * Player infos
 * Delete player ids
 * Player status
 * Bullets
 * Explosions
 * Emotes
 * Planes
 * Airstrike zones
 * Map indicators
 * Kill leader

If the deleted objects bit is set:

 * deleted_obj_count: uint16
 * for each deleted object
    * deleted_obj_ids.append: uint16

If the full objects bit is set:

 * full_obj_count: uint16
 * for each full object:
    * full_obj[type]: uint8
    * full_obj[id]: uint16
    * full_obj | part_decoder(full_obj_type)
    * full_obj | full_decoder(full_obj_type)
    * full_objects.append((full_obj_type, full_obj_id))

This is executed even if no operation bits are set

 * part_obj_count: uint16
 * for each part object:
    * part_obj[id]: uint16
    * part_obj[type]: id_to_type(part_obj_id)
    * part_obj | part_decoder(full_obj[type])
    * part_objs.append(part_obj)

If the active player id bit is set:

 * activePlayerId: uint16

This is executed even if no operation bits are set

 * healthDirty: bool
 * if healthDirty:
    * health: float(0, 100, 8)
 * boostDirty: bool
 * if boostDirty:
    * boost: float(0, 100, 8)
 * specialModeEffect: bits(3)
 * if specialModeEffects == 1 (st patricks)
    * luckDirty: bool
    * if luckDirty:
        * luck: float(0, 100, 8)
 * if specialModeEffects == 2 (beach)
    * wetDirty: bool
    * if wetDirty:
        * wetPercentage: float(0, 100, 8)
 * if specialModeEffects == 3 (contact)
    * contactDirty: bool
    * if contactDirty:
        * contactPercentage: float(0, 100, 8)
 * if specialModeEffects == 4 (inferno)
    * burningDirty: bool
    * if burningDirty:
        * burningPercentage: float(0, 100, 8)
    * nitroLaceDirty: bool
    * if nitroLaceDirty:
        * nitroLacePercentage: float(0, 100, 8)
 * zoomDirty: bool
 * if zoomDirty:
    * zoom: uint8
 * actionDirty: bool
 * if actionDirty:
    * action[time]: float(0, constants[ActionMaxDuration)], 8)
    * action[duration]: float(0, constants[ActionMaxDuration)], 8)
    * action[targetId]: uint16
 * inventoryDirty: bool
 * if inventoryDirty:
    * scope: gameType
    * for each item in nonweapons:
        * hasItem: bool
        * if hasItem:
            * amount: bits(9)
            * inventory[item] = amount
 * weaponsDirty: bool
 * if weaponsDirty:
    * curWeaponIdx: bits(2)
    * for constants[weaponSlot][count]:
        * weapon[type]: gameType
        * weapon[ammo]: uint8
        * weapons.append(weapon)
 * spectatorCountDirty: bool
 * if spectatorCountDirty:
    * spectatorCount: uint8
 * align to next byte

If the gas bit is set:

 * mode: uint8
 * duration: bits(8)
 * posOld: vec16
 * posNew: vec16
 * radOld: float(0, 2048, 16)
 * radNew: float(0, 2048, 16)

If the gas circle bit is set:

 * gasT: float(0, 1, 16)

If the player infos bit is set:

 * playerInfoCount: uint8
 * for each playerInfo:
    * player[id]: uint16
    * player[teamId]: uint8
    * player[groupId]: uint8
    * player[name]: str
    * player[loadout][outfit]: gameType
    * player[loadout][heal]: gameType
    * player[loadout][boost]: gameType
    * player[loadout][melee]: gameType
    * player[loadout][deathEffect]: gameType
    * for each in constants[emoteSlot][count]:
        * player[loadout][emotes].append(gameType)
    * player[userId]: uint32
    * player[isUnlinked]: bool
    * align to next byte
    * playersInfos.append(player)

If the delete player ids bit is set:

 * delPlayerIdCount: uint8
 * for each delPlayerIdCount:
    * delPlayerIds.append(uint16)

If the player status bit is set:

 * playerCount: uint8
 * for each player:
    * hasData: bool
    * if hasData:
        * player[pos]: vec(0, 0, 1024, 1024, 11)
        * player[visible]: bool
        * player[dead]: bool
        * player[downed]: bool
        * hasRole: bool
        * if hasRole:
            * player[role]: gameType
    * playersStatuses.append(player)
 * align to next byte

If the group status bit is set:

 * playerCount: uint8
 * for each playerCount:
    * player[health]: float(0, 100, 7)
    * player[disconnected]: bool
    * groupStatus.append(player)

If the bullets bit is set:

 * bulletCount: uint8
 * for each in bulletCount:
    * bullet[playerId]: uint16
    * bullet[pos]: vec16
    * bullet[dir]: unitVec(8)
    * bullet[type]: gameType
    * bullet[layer]: bits(2)
    * bullet[varianceT]: float(0, 1, 4)
    * bullet[distAdjIdx]: bits(4)
    * bullet[clipDistance]: bool
    * if bullet[clipDistance]:
        * bullet[distance]: float(0, 1024, 16)
    * bullet[shotFx]: bool
    * if bullet[shotFx]:
        * bullet[shotSourceType]: gameType
        * bullet[shotOffhand]: bool
        * bullet[lastShot]: bool
    * bullet[hasReflected]: bool
    * if bullet[hasReflected]:
        * bullet[reflectCount]: bits(2)
        * bullet[reflectObjId]: uint16
    * bullet[hasSpecialFx]: bool
    * if bullet[hasSpecialFx]:
        * bullet[shotAlt]: bool
        * bullet[splinter]: bool
        * bullet[trailSaturated]: bool
        * bullet[trailSmall]: bool
        * bullet[trailThick]: bool
    * bullets.append(bullet)
 * align to next byte

If the explosions bit is set:

 * explosionCount: uint8
 * for each in explosionCount:
    * explosion[pos]: vec16
    * explosion[type]: gameType
    * explosion[layer]: bits(2)
    * explosions.append(explosion)
    * align to next byte

If the emotes bit is set:

 * emoteCount: uint8
 * for each in emoteCount:
    * emote[playerId]: uint16
    * emote[type]: gameType
    * emote[itemType]: gameType
    * emote[isPing]: bool
    * if emote[isPing]:
        * emote[pos]: vec16
    * emotes.append(emote)
    * bits(3) for alignment

If the planes bit is set:

 * planeCount: uint8
 * for each in planeCount:
    * plane[id]: uint8
    * pos: vec(0, 0, 2048, 2048, 10)
    * plane[pos]: point(pos[x]-512, pos[y]-512)
    * plane[dir]: unitVec(8)
    * plane[actionComplete]: bool
    * plane[action]: bits(3)
    * planes.append(plane)

If the airstrike zones bit is set:

 * airstrikeZoneCount: uint8
 * for each in airstrikeZoneCount:
    * zone[pos]: vec(0, 0, 1024, 1024, 12)
    * zone[rad]: float(0, constants[AirstrikeZoneMaxRad], 8)
    * zone[duration]: float(0, constants[AirstrikeZoneMaxDuration], 8)
    * airstrikeZones.append(zone)

If the map indicators bit is set:

 * mapIndicatorCount: uint8
 * for each in mapIndicatorCount:
    * ind[id]: bits(4)
    * ind[dead]: bool
    * ind[equipped]: bool
    * ind[type]: gameType
    * ind[pos]: vec16
    * mapIndicators.append(ind)
 * align to next byte

If the kill leader bit is set:

 * killLeader[id]: uint16
 * killLeader[kills]: uint8

This is executed even if no operation bits are set:

 * ack: uint8, Incremented by one every time an upward packet is received
