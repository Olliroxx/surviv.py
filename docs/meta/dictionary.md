 * app.js/vendor.js/manifest.js: the main js files of the surviv.io website.  Are actually app.xxxxxxxx.js (and vendor and manifest), where the Xs represent a random hex string, which is assumed to be the hash. Most of the interesting stuff is in app.js, but there is a little in vendor.
 * Websocket: Different to sockets, protocol used by the game to communicate when actually playing.
 * Type x packet: In the game websocket, every send packet has the first byte set to a number, which is like a type.
   * Type 1: The first packet sent (upwards), is a kind of "join" packet
   * Type 2: Sent if there is an error
   * Type 3: Client to server updates
   * Type 5: ??
   * Type 6: Server to client updates
   * Type 10(0x0a): Provides initial state of the game
   * Type 18(0x12): ??
   