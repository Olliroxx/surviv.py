 * docs/: documentation for this project and surviv.io
   * code/: documentation for things in src/ and utils/
   * surviv/: documentation for the surviv api and the websocket connection that happens during games
     * api/: surviv.io api documentation
     * ws/: Documentation of the websocket connection that is opened when you join a game
 * src/: source for the python client
   * netManager.py: Manages network things like api calls and websocket communication
 * utils/: General utilities, mostly just to automate a bit of the reverse engineering
    * out/: the output of the downloader functions
    * autoindent.py: Uses the jsbeautifier lib to space out and indent app.js, vendor.js and manifest.js
    * char_code_remover.py: occasionally there are lists of numbers (charcodes) in place of strings (each number is a single character). This script finds the function that turns them back, renames it and solves some of the lists.
    * deobfuscate.py: just calls the other scripts, if you want to get a deobfuscated copy of the js (or the assets), run this
    * get_app.py: contains a helper function that finds the path to app.js
    * grab_assets: gets the mp3s, some of the svgs and the split pngs from the indented code
    * grab_code: gets the index.html of surviv.io, then scans it with a regex to find js files, and downloads them
   