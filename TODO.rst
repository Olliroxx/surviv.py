 * More tests
 * Add json parsing to deobfuscator scripts
 * Add the ability to use proxies and allow arbitrary config locations
 * Migrate deobfuscation scripts to /src and add 1-click deobfuscation with VCS, assets and configs
 * Client
    * Frame trees
        * Define a tree with all nodes having a get_frame() method
        * Calling get_frame() on a node that isn't on the bottom calls get_frame() on it's children, merges the result and returns it
    * Frame sources
        * Name of a python script/class that has a get_frame() function/method, possibly with args
    * skin.json/config.json
        * Defines what the tree looks like and some arguments
