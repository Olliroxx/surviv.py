Loot decoders
=============

Part decoder:

 * pos: vec16

Full decoder:

 * type: gameType
 * count: uint8
 * layer: bits(2)
 * isOld: bool
 * isPreloadedGun: bool
 * hasOwner: bool
 * if hasOwner
    * ownerId: uint16
 * bits(1) for alignment
