Obstacle decoders
=================

part decoder:

 * pos: vec16
 * ori: bits(2)
 * scale: float(constants[mapObjectMinScale], constants[mapObjectMaxScale], 8)
 * bits(6) for alignment

full decoder:

 * health: float(0, 1, 8)
 * type: mapType
 * obstacleType: str
 * layer: bits(2)
 * dead: bool
 * isDoor: bool
 * teamId: uint8
 * if isDoor:
    * door[open]: bool
    * door[canUse]: bool
    * door[locked]: bool
    * door[seq]: bits(5)
 * isButton: bool
 * if isButton:
    * button[onOff]: bool
    * button[canUse]: bool
    * button[seq]: bits(6)
 * isPuzzlePiece: bool
 * if isPuzzlePiece:
    * parentBuildingId: uint16
 * isSkin: bool
 * if isSkin:
    * skinPlayerId: uint16
 * bits(5) for alignment
