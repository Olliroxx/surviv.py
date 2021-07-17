 * Add surviv version control script
    * Writes current app, vendor and manifest hashes to a file, along with first and last seen
    * Writes surviv.io/changelog.html to a file as well?
    * Maybe saves app, vendor and manifest to a file?
 * More tests
 * Client
    * Frame trees
        * Define a tree with all nodes having a get_frame() method
        * Calling get_frame() on a node that isn't on the bottom calls get_frame() on it's children, merges the result and returns it
    * Frame sources
        * Name of a python script/class that has a get_frame() function/method, possibly with args
    * skin.json/config.json
        * Defines what the tree looks like and some arguments
