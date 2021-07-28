def split_bracket_level(data: str, trim_start=True, ignore_unbalanced=False, bracket_type=("{", "}")):
    """
    Splits the input string at every point where there are no surrounding brackets

    :param bracket_type: a tuple containing the open and close bracket characters to look for
    :param data: input string
    :param trim_start: Remove whitespace and newlines at the start of each split
    :param ignore_unbalanced: Ignore unbalanced brackets, otherwise throw RuntimeError
    :return: List of strings
    """

    if not data:
        raise ValueError("Data is empty")

    bracket_level = 0
    split_points = [0]
    new_text = False

    for pos in range(0, len(data)):
        if data[pos] == bracket_type[0]:
            bracket_level += 1
            new_text = True
        elif data[pos] == bracket_type[1]:
            bracket_level -= 1
        # Adjust the bracket level if the character is an open/close bracket

        if bracket_level == 0 and new_text:
            split_points.append(pos + 1)
            new_text = False

        if bracket_level < 0 and not ignore_unbalanced:
            raise RuntimeError("Unbalanced close bracket at pos " + str(pos))
    if bracket_level > 0 and not ignore_unbalanced:
        raise RuntimeError("Unbalanced open bracket")

    if split_points[-1] != len(data):
        split_points.append(len(data))
    # Create a list of ints representing the indexes bordering each function/dictionary in the string

    split = []
    for i in range(len(split_points) - 1):
        start = split_points[i]
        stop = split_points[i + 1]
        split.append(data[start:stop])
    # Create split, a list of strings by splitting the string at the indexes in split_points

    if trim_start:
        for i in range(len(split)):
            if split[i].startswith("\n"):
                split[i] = split[i].lstrip("\n")
                split[i] = split[i].lstrip(" ")
    # Clean up the strings

    return split


def write_objects_json(script, root_dir):
    import re
    import json
    import os

    regex = r"""(?:_0x[0-9a-f]{4,6} = _0x[0-9a-f]{4,6}\('[0-9a-f]{8}'\),
 +)+_0x[0-9a-f]{4,6} = 'production' === 'dev'[,;](?:
 +_0x[0-9a-f]{4,6} = _0x[0-9a-f]{4,6}\('[0-9a-f]{8}'\)[,;])*"""
    matches = re.findall(regex, script, re.DOTALL)
    if len(matches) != 1:
        raise RuntimeError
    match = matches[0]
    function_names = re.findall("'[0-9a-f]{8}'", match)
    # There is an easily findable function which contains the name of the function containing the info we are interested in

    functions = []
    for name in function_names:
        regex = name + r""": function\(_0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}\) {
 {12}'use strict';
.*?(?= {8}'[0-9a-f]{8}': function\((?:_0x[0-9a-f]{4,6}, ){1,2}_0x[0-9a-f]{4,6}\) {
 {12}'use strict';\n)"""
        matches = re.findall(regex, script, re.DOTALL)
        if len(matches) == 1:
            functions.append(matches[0])
    # Get a list of possible functions

    highest = 0
    highest_text = ""
    for function in functions:
        function_count = function.count("function")
        if function_count > highest:
            highest = function_count
            highest_text = function
    main_function = highest_text
    # Get the function containing the object info

    function_regex_base = "\n {12}function _0x[0-9a-f]{4,6}\\(_0x[0-9a-f]{4,6}(?:, _0x[0-9a-f]{4,6})+\\) {\n.*?\n {12}}"
    weighted_random_regex = r"""
 {12}function _0x[0-9a-f]{4,6}\(_0x[0-9a-f]{4,6}\) {
 {16}var _0x[0-9a-f]{4,6} = \[];
 {16}for \(var _0x[0-9a-f]{4,6} in _0x[0-9a-f]{4,6}\) {
 {20}_0x[0-9a-f]{4,6}\['hasOwnProperty']\(_0x[0-9a-f]{4,6}\) && _0x[0-9a-f]{4,6}\['push']\({
 {24}'type': _0x[0-9a-f]{4,6},
 {24}'weight': _0x[0-9a-f]{4,6}\[_0x[0-9a-f]{4,6}]
 {20}}\);
 {16}}
 {16}if \(_0x[0-9a-f]{4,6}\['length'] == 0\) throw new Error\('Invalid(?:\\x20| )obstacle(?:\\x20| )types'\);
 {16}var _0x[0-9a-f]{4,6} = 0;
 {16}for \(var _0x[0-9a-f]{4,6} = 0; _0x[0-9a-f]{4,6} < _0x[0-9a-f]{4,6}\['length']; _0x[0-9a-f]{4,6}\+\+\) {
 {20}_0x[0-9a-f]{4,6} \+= _0x[0-9a-f]{4,6}\[_0x[0-9a-f]{4,6}]\['weight'];
 {16}}
 {16}return function\(\) {
 {20}var _0x[0-9a-f]{4,6} = _0x[0-9a-f]{4,6}\['random']\(0, _0x[0-9a-f]{4,6}\),
 {24}_0x[0-9a-f]{4,6} = 0;
 {20}while \(_0x[0-9a-f]{4,6} > _0x[0-9a-f]{4,6}\[_0x[0-9a-f]{4,6}]\['weight']\) {
 {24}_0x[0-9a-f]{4,6} -= _0x[0-9a-f]{4,6}\[_0x[0-9a-f]{4,6}]\['weight'], _0x[0-9a-f]{4,6}\+\+;
 {20}}
 {20}return _0x[0-9a-f]{4,6}\[_0x[0-9a-f]{4,6}]\['type'];
 {16}};"""
    shipping_container_function_regex = r"""
 {12}function _0x[0-9a-f]{4,7}\(_0x[0-9a-f]{4,7}\) {
 {16}var _0x[0-9a-f]{4,7} = \[{.*?container.*?
 {20}}],
 {20}_0x[0-9a-f]{4,7} = \[\{.*?container.*? {20}}];
 {16}return \{.*?container.*?
 {12}}"""
    function_regex = function_regex_base + "|" + weighted_random_regex + "|" + shipping_container_function_regex
    var_regex = """
 {12}var _0x[0-9a-f]{4,6} = {
.*?
 {12}}"""
    template_regex = r""" {12}function _0x[0-9a-f]{4,6}\(_0x[0-9a-f]{4,6}\) {
 {16}var _0x[0-9a-f]{4,6} = (?:_0x[0-9a-f]{4,6}\()?{.*?
 {12}}"""
    function_matches = re.findall(function_regex, main_function, re.DOTALL)
    template_matches = re.findall(template_regex, main_function, re.DOTALL)
    var_matches = re.findall(var_regex, main_function, re.DOTALL)
    # Find a bunch of things using regexes

    if len(var_matches) != 2:
        raise RuntimeError

    result = {}

    if var_matches[0].count("metal") > var_matches[1].count("metal"):
        result["materials"] = json.loads(var_matches[1][29:].replace("'", '"'))
        main_list = var_matches[0]
    else:
        result["materials"] = json.loads(var_matches[0][29:].replace("'", '"'))
        main_list = var_matches[1]
    # Find the variable that contains the material properties

    main_list = main_list[29:]

    functions = function_list_to_dict(function_matches)
    functions = add_extended_functions(script, functions)
    functions, solve_at_runtime = simplify_template_functions(template_matches, functions)
    # Get functions and templates that use args

    result["objects"] = solve_main(main_list, functions, solve_at_runtime)

    file = open(os.path.join(os.path.dirname(__file__), root_dir + "objects.json"), "w")
    json.dump(result, file, indent=4)
    print("Done writing objects")
    # Write file


def add_extended_functions(data: str, solved_functions: dict):
    """
    Add functions contained in a dict. Example:
    _0x123["a"]()

    :param data: list of extended functions to look through
    :param solved_functions: functions already solved
    :return: solved_functions but with more functions solved
    """

    import re

    def create_rect(args, functions):
        from json import loads

        args = recursive_simplify("[" + args + "]", functions)
        if type(args) == str:
            args = loads(args)
        return {
            "type": "rect",
            "corners": args,
        }

    def create_circle(args, functions):
        from json import loads, dumps
        args = recursive_simplify("[" + args + "]", functions)
        if type(args) == list:
            args = dumps(args)
        args = args[1:-1]

        center, radius = split_bracket_level(args)
        radius = radius.replace(" ", "")
        radius = radius.replace(",", "")
        center = loads(center)
        return {
            "type": "circle",
            "center": center,
            "radius": float(radius)
        }

    def create_point(args, functions):
        result = args.split(", ")
        return {
            "type": "coord",
            "x": float(result[0]),
            "y": float(result[1])
        }

    def copy_point(args, functions):
        return args

    def object_assign(args, functions):
        from json import loads, dumps
        args = split_bracket_level(args, False)
        target = loads(args[0])
        source = recursive_simplify(args[1].lstrip(", "), functions)
        return dumps(target | source)

    replacements = {
        "_0x[0-9a-f]{4,6}\\['createAabbExtents'\\]": create_rect,
        "_0x[0-9a-f]{4,6}\\['create'\\]": create_point,
        "_0x[0-9a-f]{4,6}\\['createCircle'\\]": create_circle,
        "_0x[0-9a-f]{4,6}\\['copy'\\]": copy_point,
        "Object\\['assign']": object_assign
    }

    for var_regex in replacements:
        matches = re.findall(var_regex, data)
        if matches:
            name = matches[0]
            solved_functions[name] = replacements[var_regex]
            solved_functions[name.replace("'", '"')] = replacements[var_regex]
    # For each in replacements, find the name that matches the regex and assign that to the function

    return solved_functions


def add_functions_with_regex(regex, handler_function, functions_list, functions_dict=None, dotall=False):
    """
    If there is something in functions_list that matches regex, then function_dict will have the handler function added to it

    :param dotall: Use re.DOTALL flag
    :param regex: The regex for the wanted function
    :param handler_function: the function to add to functions_dict
    :param functions_list: A list of strings
    :param functions_dict: The list of solved functions
    :return:
    """
    if functions_dict is None:
        functions_dict = {}

    import re

    if dotall:
        flags = re.DOTALL
    else:
        flags = 0

    output_function = None
    for function in functions_list:
        matches = re.findall(regex, function, flags)
        if len(matches) == 1:
            if output_function is None:
                output_function = matches[0]
            else:
                raise RuntimeError
        elif len(matches) > 1:
            raise RuntimeError
    if output_function is None:
        raise RuntimeError
    # Find the function

    if output_function not in functions_list:
        raise RuntimeError("Regex does not match whole string")
    functions_list.remove(output_function)
    # Remove the solved function

    name = re.findall("_0x[0-9a-f]{4,6}", output_function)[0]
    functions_dict[name] = handler_function

    return functions_dict


def function_list_to_dict(data: list):
    """
    Uses a list of non-template functions to create a function mapping dict

    :param data: List of strings, each string is a non-template function
    :return: dictionary in the format "function name": function
    """

    def tinted_image(args, functions_):
        args = args.split(", ")
        sprite = args[0].strip("'").strip('"')
        try:
            tint = int(args[1])
        except IndexError:
            tint = 16777215
        try:
            alpha = args[2]
        except IndexError:
            alpha = 1
        try:
            z_idx = args[3]
        except IndexError:
            z_idx = 10
        return {
            "type": "tinted_image",
            "sprite": sprite,
            "scale": 0.5,
            "alpha": alpha,
            "tint": tint,
            "zIdx": z_idx
        }

    tinted_regex = """\n {12}function _0x[0-9a-f]{4,6}\\(_0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}\\) {
 {16}return {
 {20}'sprite': _0x[0-9a-f]{4,6},
 {20}'scale': 0\\.5,
 {20}'alpha': _0x[0-9a-f]{4,6} \\|\\| 1,
 {20}'tint': _0x[0-9a-f]{4,6} \\|\\| 16777215,
 {20}'zIdx': _0x[0-9a-f]{4,6} \\|\\| 10
 {16}};
 {12}}"""
    functions = add_functions_with_regex(tinted_regex, tinted_image, data)

    def loot_table(args, functions_):
        args = args.split(", ")
        tier = args[0].replace("'", "")
        lowest = int(args[1])
        highest = int(args[2])
        if len(args) == 4:
            props = recursive_simplify(args[3], functions_)
        else:
            props = {}
        return {
            "type": "loot_table",
            "tier": tier,
            "min": lowest,
            "max": highest,
            "props": props
        }

    loot_table_regex = """\n {12}function _0x[0-9a-f]{4,6}\\(_0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}\\) {
 {16}return _0x[0-9a-f]{4,6} = _0x[0-9a-f]{4,6} \\|\\| {}, {
 {20}'tier': _0x[0-9a-f]{4,6},
 {20}'min': _0x[0-9a-f]{4,6},
 {20}'max': _0x[0-9a-f]{4,6},
 {20}'props': _0x[0-9a-f]{4,6}
 {16}};
 {12}}"""
    functions = add_functions_with_regex(loot_table_regex, loot_table, data, functions)

    def item_dict(args, functions_):
        args = args.split(", ")
        item = args[0].strip("'")
        amount = int(args[1], 0)
        if len(args) == 3:
            props = args[2]
        else:
            props = {}
        return {
            "type": "item",
            "item_type": item,
            "count": amount,
            "props": props
        }

    item_dict_regex = """\n {12}function _0x[0-9a-f]{4,6}\\(_0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}, _0x[0-9a-f]{4,6}\\) {
 {16}return _0x[0-9a-f]{4,6} = _0x[0-9a-f]{4,6} \\|\\| {}, {
 {20}'type': _0x[0-9a-f]{4,6},
 {20}'count': _0x[0-9a-f]{4,6},
 {20}'props': _0x[0-9a-f]{4,6}
 {16}};
 {12}}"""
    functions = add_functions_with_regex(item_dict_regex, item_dict, data, functions)

    def weighted_random(args, functions_):
        from json import dumps
        args = recursive_simplify(args, functions_)
        return dumps({
            "type": "weighted_random_obstacle",
            "value": args
        })

    weighted_random_regex = r"""
 {12}function _0x[0-9a-f]{4,6}\(_0x[0-9a-f]{4,6}\) {
 {16}var _0x[0-9a-f]{4,6} = \[];
 {16}for \(var _0x[0-9a-f]{4,6} in _0x[0-9a-f]{4,6}\) {
 {20}_0x[0-9a-f]{4,6}\['hasOwnProperty']\(_0x[0-9a-f]{4,6}\) && _0x[0-9a-f]{4,6}\['push']\({
 {24}'type': _0x[0-9a-f]{4,6},
 {24}'weight': _0x[0-9a-f]{4,6}\[_0x[0-9a-f]{4,6}]
 {20}}\);
 {16}}
 {16}if \(_0x[0-9a-f]{4,6}\['length'] == 0\) throw new Error\('Invalid(?:\\x20| )obstacle(?:\\x20| )types'\);
 {16}var _0x[0-9a-f]{4,6} = 0;
 {16}for \(var _0x[0-9a-f]{4,6} = 0; _0x[0-9a-f]{4,6} < _0x[0-9a-f]{4,6}\['length']; _0x[0-9a-f]{4,6}\+\+\) {
 {20}_0x[0-9a-f]{4,6} \+= _0x[0-9a-f]{4,6}\[_0x[0-9a-f]{4,6}]\['weight'];
 {16}}
 {16}return function\(\) {
 {20}var _0x[0-9a-f]{4,6} = _0x[0-9a-f]{4,6}\['random']\(0, _0x[0-9a-f]{4,6}\),
 {24}_0x[0-9a-f]{4,6} = 0;
 {20}while \(_0x[0-9a-f]{4,6} > _0x[0-9a-f]{4,6}\[_0x[0-9a-f]{4,6}]\['weight']\) {
 {24}_0x[0-9a-f]{4,6} -= _0x[0-9a-f]{4,6}\[_0x[0-9a-f]{4,6}]\['weight'], _0x[0-9a-f]{4,6}\+\+;
 {20}}
 {20}return _0x[0-9a-f]{4,6}\[_0x[0-9a-f]{4,6}]\['type'];
 {16}};"""
    functions = add_functions_with_regex(weighted_random_regex, weighted_random, data, functions)

    def shipping_container_template(args, functions_):
        from json import dumps
        args = recursive_simplify(args, functions_)

        def if_exists(potential, fallback):
            try:
                result = potential()
            except KeyError:
                result = fallback
            return result

        open_container = [{
            "type": "container_wall_side_open",
            "pos": {"type": "coord", "x": 2.35, "y": 0},
            "scale": 1,
            "ori": 0
        }, {
            "type": "container_wall_side_open",
            "pos": {"type": "coord", "x": -2.35, "y": 0},
            "scale": 1,
            "ori": 0
        }, {
            "type": "loot_tier_2",
            "pos": {"type": "coord", "x": 0, "y": -0.05},
            "scale": 1,
            "ori": 0
        }, {
            "type": {"type": "weighted_random_obstacle", "value": {"loot_tier_1": 1, "": 1}},
            "pos": {"type": "coord", "x": 0, "y": 0.05},
            "scale": 1,
            "ori": 0
        }]
        closed_container = [{
            "type": "container_wall_top",
            "pos": {"type": "coord", "x": 0, "y": 7.95},
            "scale": 1,
            "ori": 0
        }, {
            "type": "container_wall_side",
            "pos": {"type": "coord", "x": 2.35, "y": 2.1},
            "scale": 1,
            "ori": 0
        }, {
            "type": "container_wall_side",
            "pos": {"type": "coord", "x": -2.35, "y": 2.1},
            "scale": 1,
            "ori": 0
        }, {
            "type": if_exists(lambda: args["loot_spawner_01"], "loot_tier_2"),
            "pos": {"type": "coord", "x": 0, "y": 3.25},
            "scale": 1,
            "ori": 0
        }, {
            "type": if_exists(lambda: args["loot_spawner_02"],
                              {"type": "weighted_random_obstacle", "value": {"loot_tier_1": 1, "": 1}}),
            "pos": {"type": "coord", "x": 0, "y": 0.05},
            "scale": 1,
            "ori": 0
        }]

        ceiling_imgs = [{
            "sprite": if_exists(lambda: args["ceilingSprite"], None),
            "scale": 0.5,
            "alpha": 1,
            "tint": args["tint"]
        }]  # Need to use lambda because some have ceilings but no sprite
        collision_closed = {
            "type": "rect",
            "corners": [{
                "type": "coord",
                "x": 0,
                "y": 0
            }, {
                "type": "coord",
                "x": 2.5,
                "y": 8
            }]
        }
        collision_open = {
            "type": "rect",
            "corners": [{
                "type": "coord",
                "x": 0,
                "y": 0
            }, {
                "type": "coord",
                "x": 2.5,
                "y": 11
            }]
        }
        zoom_in_open = {
            "type": "rect",
            "corners": [{
                "type": "coord",
                "x": 0,
                "y": 0
            }, {
                "type": "coord",
                "x": 2.5,
                "y": 5.75
            }]
        }
        zoom_in_closed = {
            "type": "rect",
            "corners": [{
                "type": "coord",
                "x": 0,
                "y": 2.25
            }, {
                "type": "coord",
                "x": 2.5,
                "y": 5.5
            }]
        }
        zoom_out_open = {
            "type": "rect",
            "corners": [{
                "type": "coord",
                "x": 0,
                "y": 0
            }, {
                "type": "coord",
                "x": 2.5,
                "y": 11
            }]
        }
        zoom_out_closed = {
            "type": "rect",
            "corners": [{
                "type": "coord",
                "x": 0,
                "y": 0.5
            }, {
                "type": "coord",
                "x": 2.5,
                "y": 8.75
            }]
        }

        return dumps({
            "type": "building",
            "map": {
                "display": True,
                "color": if_exists(lambda: args["mapTint"], 2703694),
                "scale": 1
            },
            "terrain": {
                "grass": True,
                "beach": True,
                "riverShore": True
            },
            "zIdx": 1,
            "floor": {
                "surfaces": [{
                    "type": "container",
                    "collision": [
                        collision_open if args["open"] else collision_closed
                    ]
                }],
                "imgs": [{
                    "sprite": "map-building-container-open-floor.img" if args[
                        "open"] else "map-building-container-floor-01.img",
                    "scale": 0.5,
                    "alpha": 1,
                    "tint": args["tint"]
                }]
            },
            "ceiling": {
                "zoomRegions": [{
                    "zoomIn": zoom_in_open if args["open"] else zoom_in_closed,
                    "zoomOut": zoom_out_open if args["open"] else zoom_out_closed
                }],
                "imgs": if_exists(lambda: args["ceilingImgs"], ceiling_imgs)
            },
            "mapObjects": open_container if args["open"] else closed_container
        })

    shipping_container_function_regex = r"""
 {12}function _0x[0-9a-f]{4,7}\(_0x[0-9a-f]{4,7}\) {
 {16}var _0x[0-9a-f]{4,7} = \[{.*?container.*?
 {20}}],
 {20}_0x[0-9a-f]{4,7} = \[\{.*?container.*? {20}}];
 {16}return \{.*?container.*?
 {12}}"""
    functions = add_functions_with_regex(shipping_container_function_regex, shipping_container_template, data,
                                         functions, True)

    if data:
        raise RuntimeError("Leftover functions")

    return functions


def solve_hex(args: str):
    import re
    regex = "(?<!_)0x[0-9a-f]+"
    matches = re.findall(regex, args)
    matches = set(matches)
    for match in matches:
        solved = int(match, 0)
        args = re.sub("(?<!_)" + match + "(?![0-9a-f])", str(solved), args)
    # Find all hex values that aren't variable names and convert them to ints

    return args


def recursive_simplify(args, functions):
    from utils.asset_processing.misc_utils import DataNeededError
    import re
    import json

    matches = set(re.findall("_0x[0-9a-f]{4,6}", args))
    for match in matches:
        solvable = False
        for function_name in functions.keys():
            if match in function_name:
                solvable = True
        if not solvable:
            raise DataNeededError
    # Check that all variables used are solved

    args = solve_hex(args)

    while any(function in args for function in functions):
        for function in functions:
            if function in args:
                pos = args.index(function)
                old = split_bracket_level(args[pos:], True, True, ("(", ")"))[0]
                result = old.lstrip(function)[1:-1]
                result = functions[function](result, functions)
                result = json.dumps(result)
                args = args.replace(old, result)
    # While any function is in args, try and solve

    args = args.replace("'", '"')
    result = json.loads(args)
    return result


def template_mapper_setup(source_dict: dict):
    def template_mapper(args, functions):
        if args == "":
            args = {}
        else:
            args = recursive_simplify(args, functions)
        return source_dict | args

    return template_mapper


def simplify_template_functions(templates, functions):
    """
    Solve as many templates as possible, return the solved ones and ones that need args separately

    :param templates: list of template function
    :param functions: already solved functions
    :return:
    """
    from textwrap import dedent
    from utils.asset_processing.misc_utils import DataNeededError
    import re

    while templates:
        templates_to_remove = []
        changed = False
        for number, template in enumerate(templates):
            template_orig = template
            name = re.findall("_0x[0-9a-f]+", template)[0]
            regex = r""" {12}function _0x[0-9a-f]{4,6}?\(_0x[0-9a-f]{4,6}?\) {
 {16}var _0x[0-9a-f]{4,6}? = (?:_0x[0-9a-f]{4,6}?\()?\[?({.*?})\]?\)?;.*?mergeDeep.*?\);
 {12}}"""
            template = re.findall(regex, template, re.DOTALL)[0]
            template = dedent(template)
            # Get the main dictionary in a template function

            try:
                template = recursive_simplify(template, functions)
                function = template_mapper_setup(template)
                functions[name] = function
                templates_to_remove.append(template_orig)
                changed = True
            except DataNeededError:
                pass
            # Try to solve, do nothing if not possible

        for template in templates_to_remove:
            templates.remove(template)

        if not changed:
            break
            # If nothing has changed, no more progress can be made

    return functions, templates


def handle_or(s):
    """
    Splits a js logical or into two strings which can then be compared

    :param s: Input string, must contain a "||"
    :return: string that goes before and another that goes after
    """
    pos = s.index("||") - 2
    first_string = ""
    while s[pos] not in (" ", ",", "\n"):
        first_string = s[pos] + first_string
        pos -= 1
    # The string before tends to be less complicated than the second string,
    # so just go backwards until a newline, comma or space.

    pos = pos + len(first_string) + 5
    brackets = {
        "[": "]",
        "{": "}",
        "(": ")"
    }
    second_string = ""

    while s[pos] not in (" ", ",", "\n"):
        if s[pos] in brackets:
            open_br = s[pos]
            close_br = brackets[open_br]
            bracketed_text = split_bracket_level(s[pos:], True, True, (open_br, close_br))[0]
            second_string = second_string + bracketed_text
            pos += len(bracketed_text)
            # If the character is an open bracket, append the rest of the bracketed text and skip over it
        else:
            second_string = second_string + s[pos]
            pos += 1

    return first_string, second_string


def solve_runtime(arg, solved, unsolved):
    import re
    import json

    function_name = re.findall("_0x[0-9a-f]{4,7}", arg)[0]
    function = unsolved[function_name]
    function_text = function[1]
    arg_name = function[0]
    arg = arg[len(function_name)+1:-1]
    arg = split_bracket_level(arg)[0]
    # Remove brackets

    arg = recursive_simplify(arg, solved)

    main_dict = re.findall("var _0x[0-9a-f]{4,6} = ({.*?});", function_text, re.DOTALL)[0]

    while "||" in main_dict:
        first, second = handle_or(main_dict)
        orig = first + " || " + second
        try:
            second = recursive_simplify(second, solved)
        except json.JSONDecodeError as e:
            if str(e) != "Expecting value: line 1 column 1 (char 0)":
                raise RuntimeError
        if arg_name not in first:
            raise RuntimeError(arg_name + " not in " + first)
        first = first.strip("']")
        first = first.strip(arg_name + "['")
        if first in arg:
            new = arg[first]
        else:
            new = second
        if type(new) == str:
            if new.startswith(("'", '"')):
                new = new[1:]
            if new.endswith(("'", '"')):
                new = new[:-1]
        new = json.dumps(new)
        main_dict = main_dict.replace(orig, new)
    # If there are ||s in the main dict, solve them

    regex = arg_name + "(?:\\['.*?'\\])*"
    matches = set(re.findall(regex, main_dict))
    replacements = {}
    for match in matches:
        if match == arg_name:
            replacements[match] = arg
            continue
        orig = match
        match = match[:-2]
        match = match[len(arg_name) + 2:]
        match = match.split("']['")
        result = arg
        for key in match:
            result = result[key]
        main_dict = main_dict.replace(orig, json.dumps(result))
    # Solve arg usages

    for name in unsolved:
        if name in main_dict:
            raise RuntimeError

    result = recursive_simplify(main_dict, solved)
    return result | arg


def solve_main(main_dict, solved, solve_at_runtime):
    import re
    from json import dumps

    unsolved = {}
    for function in solve_at_runtime:
        name = re.findall("_0x[0-9a-f]{4,6}", function)[0]
        arg_name = re.findall("_0x[0-9a-f]{4,6}", function[22+len(name):])[0]
        unsolved[name] = (arg_name, function[25+len(arg_name)+len(name):])
    # Split function content into arg name and content

    matches = True
    old_matches = 0
    while matches:

        matches = re.findall("_0x[0-9a-f]{4,6}", main_dict)
        if matches:
            if len(matches) == old_matches:
                raise RuntimeError("Unsolvable")
            print(str(len(matches)) + " to simplify")
            old_matches = len(matches)
        match_num = 0
        prev_amount = 0
        for match in matches:
            if match_num > prev_amount + 50:
                print(str(match_num) + "/" + str(len(matches)))
                prev_amount = match_num
                # Progress updates

            elif match in unsolved and match in main_dict:
                old = split_bracket_level(main_dict[main_dict.index(match):], True, True, ("(", ")"))[0]
                new = solve_runtime(old, solved, unsolved)
                main_dict = main_dict.replace(old, dumps(new))
            # Solve, find and replace (for templates that need args)
            else:
                for name in solved:
                    if match in name and name in main_dict:
                        function = solved[name]
                        old = split_bracket_level(main_dict[main_dict.index(name):], True, True, ("(", ")"))[0]
                        new = function(old[len(name) + 1:-1], solved)
                        while old in main_dict:
                            main_dict = main_dict.replace(old, dumps(new), 1)
                            match_num += 1
            # Solve, find and replace (for everything else)
    return recursive_simplify(main_dict, {})
