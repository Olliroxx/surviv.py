Projectile decoders
===================

Part decoder:

 * pos: vec16
 * posZ: float(0, constants["projectile"]["maxHeight"], 10)
 * dir: unitVec(7)
 * bombArmed: bool
 * bits(7) for alignment

Full decoder:

 * type: gameType
 * layer: bits(2)
 * readBits(4) for alignment
