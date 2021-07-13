Building decoders
=================

Part decoder:

 * ceilingDead: bool
 * occupied: bool
 * ceilingDamaged: bool
 * hasPuzzle: bool
 * if hasPuzzle:
    * puzzleSolved: bool
    * puzzleErrSeq: bits(7)
 * bits(4) for alignment

Full decoder:

 * pos: vec16
 * type: mapType
 * ori: bits(2)
 * layer: bits(2)
