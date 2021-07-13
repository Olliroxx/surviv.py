Objects and their decoders
==========================

There are many object types:

 * Invalid : 0
 * Player : 1
 * Obstacle : 2
 * Loot : 3
 * LootSpawner : 4
 * Dead body : 5
 * Building : 6
 * Structure : 7
 * Decal : 8
 * Projectile : 9
 * Smoke : 10
 * Airdrop : 11
 * NPC : 12
 * Skitternade : 13

Invalid is only used for objects that have already been deleted

Skitternade has a number but no decoders

Most types have two decoders, a part and a full. They must called in that order.

.. toctree::

    player
    obstacle
    loot
    lootSpawner
    deadBody
    building
    structure
    decal
    projectile
    smoke
    airdrop
    npc
