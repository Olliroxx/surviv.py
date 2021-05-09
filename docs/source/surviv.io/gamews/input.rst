Type 0x3/3 packets (input)
==========================
Direction: up

Contains:

 * "seq" uint8 : ???
 * "moveLeft" bool : Does the player have left button pressed?
 * "moveRight" bool : Does the player have right button pressed?
 * "moveUp" bool : Does the player have up button pressed?
 * "moveDown" bool : Does the player have down button pressed?
 * "shootStart" bool : ???
 * "shootHold" bool : ???
 * "portrait" bool : ???
 * "touchMoveActive" bool : ???
 * "touchMoveDir" vec8 : movement direction, for touch controls
 * "touchMoveLen" uint8 : ???
 * len("inputs") 4 bits : ???
 * for inputs:
     * "inputs": uint8 : ???
 * "useItem" "writeGameType" : ???
 * 6 filler bits
