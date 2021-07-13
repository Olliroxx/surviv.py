NPC decoders
============
"NPC" just means the mothership in contact

Part decoder:

 * pos: vec16
 * ori: float(-4, 4, 8)
 * scale: float(constants["mapObjectMinScale"], constants["mapObjectMaxScale"], 8)
 * state: string(8)
 * invisibleTicker: bool
 * align to next byte

Full decoder:

 * healthT: float(0, 1, 8)
 * type: mapType
 * obstacleType: string
 * layer: bits(2)
 * dead: bool
 * teamId: uint8
 * align to next byte
