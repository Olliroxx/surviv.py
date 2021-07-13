Structure decoder
=================

Structures only have a full decoder:

 * pos: vec16
 * type: mapType
 * ori: bits(2)
 * interiorSoundEnabled: bool
 * interiorSoundAlt: bool
 * for each in constants.structureLayerCount:
    * layerObjIds.append(uint16)
