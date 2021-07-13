Player decoders
===============

part decoder:

 * pos: vec16
 * dir: unitVec(8)

full decoder:

 * outfit: game type
 * backpack: game type
 * helmet: game type
 * chest: game type
 * curWeapType: game type
 * layer: bits(2)
 * dead: bool
 * downed: bool
 * animType: bits(3)
 * animSeq: bits(3)
 * actionType: bits(3)
 * actionSeq: bits(3)
 * wearingPan: bool
 * playerIndoors: bool
 * gunLoaded: bool
 * passiveHeal: bool
 * healByItemEffect: bool
 * hasHaste: bool
 * if hasHaste:
    * hasteType: bits(3)
    * hasteSeq: bits(3)
 * else:
    * hasteType: 0
    * hasteSeq: -1
 * hasActionItem: bool
 * if hasActionItem:
    * actionItem: gameType
 * else:
    * actionItem: ""
 * isScaled: bool
 * if isScaled:
    * playerScale: float(constants['PlayerMinScale'], constants['PlayerMaxScale'], 8)
 * else:
    * playerScale: 1
 * hasRole: bool
 * if hasRole:
    * role: readGameType
 * else:
    * role: ""
 * perks: []
 * hasPerks: bool
 * if hasPerks:
    * perkCount: bits(3)
    * for each perk:
        * perks.append:
            * type: game type
            * droppable: bool
 * specialModeEffects: bits(4)
 * switch specialModeEffects:
 * case 1 (may 4th)
    * wearingLasrSwrd: bool
    * pulseBoxEffect: bool
    * movedByPulseEffect: bool
 * case 2 (contact)
    * isTarget: bool
    * infectedEffect: bool
    * playerTransparent: bool
    * biteEffect: bool
 * case 3 (snow)
    * frozen: bool
    * frozenOri: bits(2)
    * freezeLevel: float(0, 5, 8)
    * freezeActive: bool
    * flaskEffect: bool
 * case 4 (valentines)
    * frenemy: bool
    * chocolateBoxEffect: bool
 * case 5 (st patricks)
    * luckyEffect: bool
    * savedByLuckEffect: bool
    * loadingBlaster: float(0, 1, 7)
 * case 6 (beach)
    * wetEffect: bool
    * watermelonEffect: bool
 * case 7 (cinco de mayo)
    * gunchildaEffect: bool
 * case 8 (easter)
    * sugarRush: bool
    * playSoundSugarRush: bool
 * case 9 (storm)
    * windDir: bits(2)
    * hailDamageEffect: bool
 * case 10 (inferno)
    * burningEffect: bool
    * nitroLaceEffect: bool
 * if inGameNotificationActive (in game quest updates)
    * questCount: bits(2)
    * for each quest:
        * questsInfo.append
            * type: bits(5)
            * progress: bits(11)
 * align to next byte