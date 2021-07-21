def create_game_modes(script, root_dir):
    import re
    from json import loads, dump
    import os

    print("Starting map_data.json")

    regex = r""" {8}'[0-9a-f]{8}': function\(_0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}\) {
 {12}'use strict';
 {12}var _0x[0-9a-f]{4,6} = (\{(?:
 {16}'.*': _0x[0-9a-f]{4,6}\('[0-9a-f]{8}'\),)+
 {16}'.*': _0x[0-9a-f]{4,6}\('[0-9a-f]{8}'\)
 {12}});
 {12}_0x[0-9a-f]{4,6}\['exports'] = _0x[0-9a-f]{4,6};
 {8}},"""
    match = re.findall(regex, script)[0]
    friendly_names = re.findall("'(.*)':", match)
    function_names = re.findall("'([0-9a-f]{8})'", match)
    names = dict(zip(friendly_names, function_names))
    # There is a function that contains a list of map names and function that list properties, this block gets that

    derived_function_names = {}
    for friendly_name, name in names.items():
        if friendly_name.endswith(("_spring", "_summer", "_snow")):
            derived_function_names[friendly_name] = name
    # Some modes (derived) are other modes but with different particles/tree colours/etc

    output = {}
    function_to_friendly = {}
    simple_replacements = {
        r'_0x[0-9a-f]{4,6}\["Plane"]\["Airdrop"]': "1",
        r"\\x": r"\\\\x"
    }
    for friendly_name, name in names.items():
        function_regex = " {8}'" + name + r"""': function\(_0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}\) {
 {12}'use strict';
.*? = ({.*?);"""
        function_text = re.findall(function_regex, script, re.DOTALL)[0]
        function_text = re.sub(r"(?<!\\)'", '"', function_text)
        regex = "[^_]0x[0-9a-f]+"
        hex_matches = re.findall(regex, function_text)
        for hex_data in hex_matches:
            function_text = function_text.replace(hex_data, str(int(hex_data, 16)), 1)
        for old, new in simple_replacements.items():
            function_text = re.sub(old, new, function_text)
        parsed = loads(function_text)
        output[friendly_name] = parsed
        function_to_friendly[name] = friendly_name
    # Solve base modes

    for friendly_name, name in derived_function_names.items():
        dependencies_regex = " {8}'" + name + r"""': function\(_0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}\) {
 {12}'use strict';
 {12}var ((?:_0x[0-9a-f]{4,6} = _0x[0-9a-f]{4,6}\('[0-9a-f]{8}'\),
 {16})+_0x[0-9a-f]{4,6} = _0x[0-9a-f]{4,6}\('[0-9a-f]{8}'\))"""
        deps_string = re.findall(dependencies_regex, script)[0]
        deps_pairs = {}
        for assignment in deps_string.split(",\n" + " "*16):
            pair = re.split(r" = _0x[0-9a-f]{4,6}\('", assignment)
            deps_pairs[pair[0]] = pair[1][:-2]
        merge_regex = " {8}'" + name + r"""': function\(_0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}\) {
 {12}'use strict';
.*? = {.*?};
 {12}_0x[0-9a-f]{4,6}\['exports'] = _0x[0-9a-f]{4,6}\['mergeDeep'\]\(\{}, (_0x[0-9a-f]{4,6}), _0x[0-9a-f]{4,6}"""
        base_function = re.findall(merge_regex, script, re.DOTALL)[0]
        module_name = deps_pairs[base_function]
        base_function_friendly = function_to_friendly[module_name]
        output[friendly_name] = output[base_function_friendly] | output[friendly_name]
    # Solve derived modes

    map_json_file = open(os.path.join(os.path.dirname(__file__), root_dir+"map_data.json"), "w")
    dump(output, map_json_file, indent=4)
    map_json_file.close()

    print("Finished map_data.json")
