def write_constants_json(script: str, root_dir):
    """
    There is a function which contains constants and version numbers which the netcode can't run without

    :param script: the text of app.js
    :param root_dir: the directory to write constants.json to
    :return:
    """
    import re
    from json import loads, dump

    print("Starting constants.json")

    regex = r"""'[\da-f]{8}': function\(_0x[\da-f]{4,6}, _0x[\da-f]{4,6}, _0x[\da-f]{4,6}\) {
 {12}'use strict';
 {12}_0x[\da-f]{4,6}\['exports'] = ({.*?});"""

    function = re.findall(regex, script, re.DOTALL)[0]
    del regex, script

    function = function.replace("'", '"')
    regex = r"[^_]0x[\da-f]+"
    hex_matches = re.findall(regex, function)
    for hex_function in hex_matches:
        function = function.replace(hex_function, str(int(hex_function, 16)), 1)
    del hex_matches, regex, hex_function

    function = loads(function)
    file = open(root_dir + "constants.json", "w")
    dump(function, file, indent=4)
    file.close()

    print("Finished constants.json")
