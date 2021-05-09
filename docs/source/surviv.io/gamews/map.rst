Type 0xa/10 packet (map)
========================
Direction: Down

Contains:

 * "mapName" str : has a set size (MapNameMaxLen), which was 24 at time of writing
 * "seed" uint32 : seed for rng? (not yet reverse engineered)
 * "width" uint16 : width of map
 * "height" uint16 : height of map
 * "shoreInset" uint16 : distance from edge of map to land
 * "grassInset" uint16 : distance from land to grass (width of beach)
 * riverCount uint8 : amount of rivers
 * For each river:
    * "width" uint8(read 8 bits): width of the river
    * "looped" uint8 : seems like it should be a bool
    * pointCount uint8 : amount of points in the line that makes the river
    * For each point:
        * point vec16 : the x/y coords of the point
 * placeCount: amount of "places" (blocks of text on the map)
 * For each place:
    * "name" str : The text that is displayed
    * "pos" vec16 : The position of the text (center? top right?)
 * objectCount: amount of objects (walls, buildings, loot)
 * For each object:
    * "pos" vec16 : The position of the object (center makes the most sense)
    * "scale" float8 : The size of the object (stuff gets smaller as you damage it(
    * "type" 12 bits : ???
    * "ori" 2 bits : Orientation?
    * "obstacleType" str : What kind of wall/loot/building is it?
    * ??? 2 bits : ???
 * patchCount: amount of ground patches (different coloured terrain, think the towns in desert)
 * For each patch:
    * "min" vec16 : One of the corners?
    * "max" vec16 : The opposite corner?
    * "colour" uint32 : Unknown why this needs 32 bits and not 48
    * "roughness" uint32 : Something to do with the edges?
    * "offsetDist" uint32 : Something to do with the edges?
    * "order" 7 bits : ???
    * "useAsMapShape" bool : If the ground patch can be seen from the map?

Contains the initial state of the game
