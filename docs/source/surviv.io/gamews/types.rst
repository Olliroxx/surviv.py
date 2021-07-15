Types used
==========

Map+Game types:

Map types are a way of converting everything in objects.json to numbers, game types are for every other json made by create_jsons.py.
The names of each object to be converted (plus an empty string) are added to a list. The number is the index of that object.  

Floats+vectors:

Floats smaller than 32 bits are are represented differently to float32/64s.
They are in the format (min, max, size).
Size is the number of bits used to represent the float.

The they work is:

 * An int is read
 * The integer is divided by the maximum number it could be (for 8 bits this is 255)
 * The resulting decimal is multiplied by the difference between the minimum and the maximum
 * The minimum is added

A vector is two floats together, each with the precision of the vector (a vec16 has two float16s, it is 32 bits long)

All vectors (here) could be represented in the format (xmin, ymin, xmax, ymax, size), xmin is the minimum for the x float, ymax is the maximum for the y float

There are 2 special types that could be represented by this, but are used often enough to have their own categories:

A vec16 is a map coordinate, shorthand for (0, 0, 1024, 1024, 16)

A unitvec is shorthand for (-1.0001, -1.0001, 1.0001, 1.0001, size), they can be multiple sizes  
