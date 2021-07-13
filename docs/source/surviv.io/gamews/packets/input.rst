Type 0x3/3 packets (input)
==========================
Direction: up

Contains:

 * seq uint8 : A sequence number, increments every time packet is sent and the next packet is received
 * moveLeft bool : Does the player have left button pressed?
 * moveRight bool : Does the player have right button pressed?
 * moveUp bool : Does the player have up button pressed?
 * moveDown bool : Does the player have down button pressed?
 * shootStart bool : Has the user started shooting? (rising edge)
 * shootHold bool : Is the shoot button pressed?
 * portrait bool : Is the screen portrait?
 * touchMoveActive bool : Are touch-style controls being used? (2 joysticks)
 * if touchMoveActive
     * touchMoveDir unitVec(8) : movement direction, for touch controls
     * touchMoveLen uint8 : joystick distance from center
 * len(inputs) 4 bits : Inputs is a list of uint8s, see constants["Input"] for mappings
 * for inputs:
     * inputs: uint8
 * useItem gameType : gameType of the current item being used (bandages, soda, painkillers, medkit and event specific items)
 * 6 filler bits
