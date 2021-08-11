def split_bracket_level(data: str, trim_start=True, ignore_unbalanced=False):
    """
    Splits the input string at every point where there are no surrounding brackets

    :param data: input string
    :param trim_start: Remove whitespace and newlines at the start of each split
    :param ignore_unbalanced: Ignore unbalanced brackets, otherwise throw RuntimeError
    :return: List of strings
    """

    if not data:
        raise ValueError("Data is empty")

    bracket_level = 0
    split_points = [0]

    for pos in range(0, len(data)):
        if data[pos] in ["(", "{"]:
            bracket_level += 1
        elif data[pos] in [")", "}"]:
            bracket_level -= 1
        # Adjust the bracket level if the character is an open/close bracket

        if bracket_level == 0 and data[pos] == "\n":
            split_points.append(pos+1)

        if bracket_level < 0 and not ignore_unbalanced:
            raise RuntimeError("Unbalanced close bracket at pos " + str(pos))
    if bracket_level > 0 and not ignore_unbalanced:
        raise RuntimeError("Unbalanced open bracket")

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
            while split[i].startswith((" ", "\n", ",")) or split[i].endswith((" ", "\n", ",")):
                split[i] = split[i].strip("\n")
                split[i] = split[i].strip(" ")
                split[i] = split[i].strip(",")
        # Clean up the strings

    return split


def single_to_double_quote(s: str):
    s = s.replace(r"\'", r"\x27")
    lines = s.split("\n")
    solved_lines = []
    for line in lines:
        if "'" in line and ":" in line and "function" not in line:
            key, value = line.split(":", 1)
            key = key.replace("'", '"')
            if "'" in value:
                if "[" in value:
                    value = value.replace("'", '"')
                    # List handling code
                else:
                    first_pos = value.index("'")
                    last_pos = len(value)-value[::-1].index("'")
                    value = value[:first_pos] + '"' + value[first_pos+1:last_pos-1].replace('"', "'") + '"' + value[last_pos:]
            line = key + ":" + value
        solved_lines.append(line)
    return "\n".join(solved_lines)
    # 'a': 'ab"c"de'
    # becomes
    # "a": "ab'c'de"


def basic_simplify(data):
    """
    This function replaces ' with " and solves expressions, among other things

    :param data: Input string
    :return: Input string with small, simple modifications
    """
    import re

    import textwrap
    data = textwrap.dedent(data)
    del textwrap
    #    A
    # Becomes
    # A

    regex = r"[^_]0x[\da-f]+"
    hex_matches = re.findall(regex, data)
    for hex_data in hex_matches:
        data = data.replace(hex_data, hex_data[0] + str(int(hex_data[1:], 16)), 1)
    del hex_matches
    # 0x123
    # becomes
    # 291

    data = re.sub("Math\\[[\"']PI[\"']]", "3.141592653589793", data)
    data = solve_expressions(data)
    # Math["Pi"] * 5
    # Becomes
    # 15.7079632679

    replacements = {
        r"\\x20": " ",
        " 1:": " \"1\":",
        " 2:": " \"2\":",
        r"[^\\]\\x": r"\\\\x",
    }
    for pattern, new in replacements.items():
        data = re.sub(pattern, new, data)
    data = single_to_double_quote(data)
    # Small changes

    data = data.rstrip(", \n")
    # Remove trialing whitespace and commas

    return data


def solve_expressions(data: str):
    """
    Solves all the expressions in the input string, including an infinite amount of nested brackets. Example: 1+(1+(-1))

    :param data: The input string
    :return: The solved input string
    """
    import re

    changed = True
    while changed:
        changed = False
        regex = r"(?:-?[\d\.]+ ?[+*\-/] )+-?[\d\.]+"
        expression_matches = re.findall(regex, data)
        for match in expression_matches:
            solved = solve_expression(match)
            data = data.replace(match, str(solved), 1)
            changed = True
        # Solve expressions (like 2+1)

        regex = r"-?\(-?[\d\.]+\)"
        bracket_matches = re.findall(regex, data)
        for match in bracket_matches:
            solved = str(solve_expression(match))
            data = data.replace(match, solved, 1)
            changed = True
        # Remove redundant brackets around numbers
    return data


def solve_expression(to_solve: str):
    """
    Solves and individual expression, nothing else can be in the string

    :param to_solve: input string
    :return: solved input string, as an int
    """
    import ast
    # noinspection PyUnresolvedReferences
    return _eval(ast.parse(to_solve, mode="eval").body)


def _eval(node):
    import operator as op
    import ast
    operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
                 ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
                 ast.USub: op.neg}
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        # noinspection PyTypeChecker
        return operators[type(node.op)](_eval(node.left), _eval(node.right))
    elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        # noinspection PyTypeChecker
        return operators[type(node.op)](_eval(node.operand))
    else:
        raise TypeError(node)
    # Ast magic from stackoverflow, slightly modified to handle floats


def solve_vars(data: list, functions=None, solved=None):
    """
    Tries to solve as many variables as possible

    :param solved:
    :param data: A list of strings containing a variable declaration, example: "_0x1234 = 1,
    :param functions: A dictionary of conversion functions. Format:  "name in code": function
    :return: A dictionary in the format "function name": solved value
    """

    if solved is None:
        solved = {}
    import re
    from survivpy_deobfuscator.misc_utils import DataNeededError

    if functions is None:
        functions = {}

    needs_solving_regex = r"_0x[\da-f]{4,}[\[\(]"

    unsolved = {}
    for var in data:
        name, content = re.split(r"(?<=[\da-f]) = ", var, 1)
        name = name.strip(" ")
        content = content.strip(" ")
        unsolved[name] = content
    del var
    # Split each string into the variable name and the variable content, and add that to unsolved

    while unsolved:
        keys_to_delete = []
        for key in unsolved:
            value = unsolved[key]

            matches = re.findall(needs_solving_regex, value)
            # Example match: _0x123 = {5},

            if matches:
                match = matches[0]
                fname = match[:-1]
                args = match + value.split(match, 1)[1]
                args = split_bracket_level(args, ignore_unbalanced=True)[0]
                # Get function args
                if fname in functions:
                    try:
                        function = functions[fname]
                        result = str(function(args, solved=solved))
                        value = value.replace(args, result)
                        unsolved[key] = value
                    except DataNeededError:
                        pass
                    # Try to use the handler function, if there isn't enough data do nothing
                    # This could lead to an infinite loop, but I don't know enough to implement graphs

                elif fname not in unsolved:
                    raise RuntimeError("No way to handle function " + fname)
            else:
                keys_to_delete.append(key)
                solved[key] = handler_generic(return_processed=True)(value)
                # If there are no matches, then it must be solved

        for key in keys_to_delete:
            del unsolved[key]

    return solved


def handler_generic(filename="", return_processed=False):
    """
    Handles any function which has only a single variable to solve. Example:

    .. code-block::

        _0x123456 = function (_0x123456) {
            var _0x123456 = {};
        }

    returns

    .. code-block::

        {}

    :param filename: The output file name
    :param return_processed: Return the solved value instead of writing to disk
    :return:
    """

    def handler(data: str):
        import re
        import json

        data = data.split("var ")
        for i in data:
            if re.findall(r"_0x[\da-f]{4,6} = {", i):
                data = i
                break
        if type(data) == list:
            data = data[-1]

        data = re.sub(r"_0x[\da-f]{4,6} = ", "", data, count=1)
        data = re.sub(";.*", "", data, flags=re.DOTALL)
        data = basic_simplify(data)
        # General cleaning
        data = json.loads(data)

        if return_processed:
            return data
        else:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)

    return handler


def handler_multidict(filename: str, categories=(0, 0, 1)):
    """
    :param filename: The name of the output file, including extension (.json)
    :param categories: The keys for the output dicts.

        Has 2 modes:

        Use keys:

         * Write a dict with the each value in categories used as the key
         * Any keys that are 0s are discarded

        Normal:

         * All keys must either be 0s or 1s
         * There can only be one 1
         * The result of value of 1 must be a dict
         * The keys of the result dict are used instead of the values from categories
    """
    from survivpy_deobfuscator.misc_utils import DataNeededError

    def op_bullet_setup(source_dict_name: str):
        """
        Not just used for overpressure bullets, but that is the best example

        :param source_dict_name:
        :return:
        """
        def op_bullet(args: str, solved: dict):
            import json

            if not type(source_dict_name) == dict:
                if source_dict_name not in solved:
                    raise DataNeededError("Source dict not solved")
                source_dict = solved[source_dict_name]
            else:
                source_dict = source_dict_name

            args = args.rstrip(",)")
            args = args[10:].split(",", 1)
            args[0] = args[0].strip("\"'")
            # Get args from function+args

            if args[0] not in source_dict:
                raise RuntimeError

            args[1] = basic_simplify(args[1])

            parsed = json.loads(args[1])
            result_dict = {"baseType": args[0]}

            # noinspection PyTypeChecker
            for key in source_dict[args[0]]:
                # noinspection PyTypeChecker
                result_dict[key] = source_dict[args[0]][key]
            for key in parsed:
                result_dict[key] = parsed[key]

            return json.dumps(result_dict, indent=4)

        return op_bullet

    def merge_dicts(args: str, solved: dict):
        import json

        args = args.split(",")[1:]
        for i in range(len(args)):
            args[i] = args[i].strip(" ,()")
            if args[i] not in solved:
                raise DataNeededError
        # General cleaning

        result_dict = {}
        for i in args:
            result_dict.update(solved[i])

        return json.dumps(result_dict)

    def dict_ref_setup(source: dict):
        # noinspection PyUnusedLocal
        def dict_ref(args: str, solved: dict):
            args = args.split("][")
            args[-1] = args[-1][:-2]
            args[0] = args[0].split("[")[1][1:]
            result = source
            for target in args:
                result = result[target]
            return result
        return dict_ref

    def handler(data: str):
        import re
        import json

        data = basic_simplify(data)

        data = data.split("var ")
        functions_string = []
        longest = ""
        function_regex = r"""[\"'][\da-f]{8}[\"']: function\(_0x[\da-f]{4,6}, _0x[\da-f]{4,6}, _0x[\da-f]{4,6}\) \{
 {12}[\"']use strict[\"'];"""
        for i in data:
            if len(i) > len(longest):
                longest = i
            if "function" in i and not re.findall(function_regex, i):
                functions_string.append(i)
        data = longest
        data = data.split(";")[0]
        # Split the function, with "var " at the split points
        # Find the longest one and discard everything else, except functions which might need a handler

        op_bullet_regex = r"""function _0x[\da-f]{4,6}\(_0x[\da-f]{4,6}, _0x[\da-f]{4,6}\) \{
 {16}return _0x[\da-f]{4,6}\[[\"']mergeDeep[\"']\]\(\{\}. _0x[\da-f]{4,6}\[_0x[\da-f]{4,6}\], \{
 {20}[\"']baseType[\"']: _0x[\da-f]{4,6}
 {16}\}, _0x[\da-f]{4,6}\);
 {12}\}"""
        merge_dicts_regex = r"(_0x[\da-f]{4,6})\[[\"']mergeDeep[\"']\]"
        functions = {}
        for function in functions_string:
            has_handler = False
            if re.findall(op_bullet_regex, function):
                key = re.findall(r"function (_0x[\da-f]{4,6})", function)[0]
                source_dict = re.findall(r"(_0x[\da-f]{4,6})\[_0x[\da-f]{4,6}]", function)[0]
                value = op_bullet_setup(source_dict)
                functions[key] = value
                has_handler = True
            # Set up dict usages. Example:
            # _0x123["property"]

            if re.findall(merge_dicts_regex, function):
                key = re.findall(merge_dicts_regex, function)[0]
                value = merge_dicts
                if key not in functions:
                    functions[key] = value
                    has_handler = True
            # Set up dict merging functions

            if not has_handler:
                raise RuntimeError("Function without handler")
        del merge_dicts_regex, op_bullet_regex, functions_string

        data = split_bracket_level(data, trim_start=True)

        simple_value_regex = r"_0x[\da-f]{4,6} = (?:-?[\d.]+|{(?:(?!_0x).)*})"
        simple_values = {}
        to_remove = []
        solved = {}
        from json import loads
        for variable in data:
            if re.findall(simple_value_regex, variable, re.DOTALL):
                split = variable.split(" = ")
                key = split[0]
                value = split[1][:-1]
                if "{" not in value:
                    value = basic_simplify(value)
                    simple_values[key] = value
                else:
                    key = re.findall(r"_0x[\da-f]{4,6}", variable)[0]
                    start = variable.index("{")
                    value = variable[start-1:]
                    value = basic_simplify(value)
                    value = loads(value)
                    solved[key] = value
                    if key not in functions:
                        functions[key] = dict_ref_setup(value)
                to_remove.append(variable)
        # Find "simple variables" (eg _0x123 = 0.5) and add them to a list

        for variable in to_remove:
            data.remove(variable)
        # Remove simple values from data

        data_solved = []
        for i in range(len(data)):
            variable = data[i]
            for key, value in simple_values.items():
                variable = variable.replace(key, str(value))

            variable = basic_simplify(variable)
            data_solved.append(variable)
        data = data_solved
        del data_solved, variable, i
        # Replace the simple variables with their values

        result = solve_vars(data, functions, solved)
        del data, functions

        if len(result) < len(categories):
            raise RuntimeError("Too many categories")
        elif len(result) > len(categories):
            raise RuntimeError("Too few categories")

        has_1 = False
        for category in categories:
            if category == 1:
                if has_1:
                    raise ValueError("More than one \"1\" category")
                else:
                    has_1 = True

        if has_1:
            for category in categories:
                if category not in (0, 1):
                    raise ValueError("Cannot have categories other than 0 or 1 in normal mode")
        # Input validation

        with open(filename, "w") as file:
            if has_1:
                for i in range(len(result)):
                    if categories[i]:
                        key = tuple(result.keys())[i]
                        result = result[key]
                        break
                # Get the wanted dict
                json.dump(result, file, indent=4)

            else:
                output = {}
                for i in range(len(result)):
                    key = categories[i]
                    if key != 0:
                        value = tuple(result.keys())[i]
                        value = result[value]
                        output[key] = value

                json.dump(output, file, indent=4)

    return handler


def create_jsons(root_dir="jsons/", skip_simple=False, skip_objects=False, skip_constants=False, skip_game_modes=False):
    """
    This is the main function of create_jsons.py

    :param skip_game_modes: skips making map_data.json
    :param skip_constants: skips making constants.json
    :param skip_objects: skips making objects.json
    :param skip_simple: skips straight to objects
    :param root_dir: The output directory
    """
    from survivpy_deobfuscator.misc_utils import get_app
    from survivpy_deobfuscator.json_processing import create_constants_json
    from survivpy_deobfuscator.json_processing import create_objects_json
    from survivpy_deobfuscator.json_processing import create_gamemodes_json
    import re
    import os

    try:
        os.mkdir("jsons")
    except FileExistsError:
        pass
    del os

    with get_app() as file:
        line = file.readline()
        if line != "//Json parsed\n":
            raise RuntimeError("The script should be run right after the boolean adder")
        script = line + file.read()
    del line, file
    # Check at what stage this is being run

    regex = r"""'[\da-f]{8}': function\(_0x[\da-f]{4,6}, _0x[\da-f]{4,6}, _0x[\da-f]{4,6}\) {
 {12}'use strict';
 {12}var _0x[a-f\d]{4,6} = \[(_0x[\da-f]{4,6}\('[\da-f]{8}'\)(?:, _0x[\da-f]{4,6}\('[\da-f]{8}'\))*)]"""
    matches = re.findall(regex, script)
    if len(matches) != 1:
        raise RuntimeError
    regex = r"[a-f\d]{8}"
    matches = re.findall(regex, matches[0])
    del regex
    # There's a function that contains the names of other functions with the data we want in them. This finds that function

    filters = [
        ("quest", 20, handler_generic(root_dir + "quests.json")),  # Quests
        ("falloff", 5, handler_multidict(root_dir + "bullets.json")),  # Bullets
        ("explosionEffectType", 10, handler_generic(root_dir + "explosions.json")),  # Explosions
        ("playerRad", 1, handler_multidict(root_dir + "nonweapons.json")),  # Nonweapons
        ("'name': 'VSS'", 1, handler_generic(root_dir + "guns.json")),  # Guns
        ("melee", 30, handler_multidict(root_dir + "melee_weapons.json")),  # Melee
        ("noDropOnDeath", 30, handler_multidict(root_dir + "outfits.json")),  # Outfits
        ("perk", 30, handler_generic(root_dir + "perks.json")),  # Perks
        ("pass_survivr", 5, handler_generic(root_dir + "passes.json")),  # Passes
        ("ping", 6, handler_generic(root_dir + "pings.json")),  # Pings
        ("role", 15, handler_generic(root_dir + "roles.json")),  # Roles
        ("'type': 'throwable',", 1, handler_generic(root_dir + "throwables.json")),  # Throwables
        ("crosshair", 90, handler_generic(root_dir + "crosshairs.json")),  # Crosshairs
        ("heal", 60, handler_generic(root_dir + "heal_effects.json")),  # Heal + boost particles
        ("emote", 700, handler_multidict(root_dir + "emotes.json", categories=(0, 1))),  # Emotes
        ("new-account", 1, handler_generic(root_dir + "default_unlocks.json")),  # Default account unlocks
        ("Cake Donut", 1, handler_multidict(root_dir + "xp_sources.json")),  # XP sources
        ("deathEffect", 15, handler_generic(root_dir + "death_effects.json")),  # Death effects
        ("loot_box", 7, handler_generic(root_dir + "lootbox_tables.json")),  # Item pools for lootboxes
        ("itemPool", 6, handler_generic(root_dir + "item_pools.json")),  # Item pools
        ("rescheduled", 3, handler_generic(root_dir + "xp_boost_events.json")),  # XP boost times and amounts
        ("price", 16, handler_generic(root_dir + "market_min_values.json")),  # Black market minimum prices (and taxes?)
        ("motherShip", 3, handler_generic(root_dir + "npcs.json")),  # NPCs (so far only mothership+skitters from contact
    ]
    # Format : string, threshold, handler function
    # If [string] is found more times than (or equal to) [threshold], then [handler function] is used

    if not skip_simple:
        print(str(len(matches)) + " matches, " + str(len(filters)) + " filters")

        for match in matches:
            print("Starting match " + str(matches.index(match)+1) + " of " + str(len(matches)))
            regex = "'" + match + r"""': function\(_0x[\da-f]{4,6}(?:, _0x[\da-f]{4,6})*\) {
 {12}'use strict';.*?
(?= {8}'[\da-f]{8}')"""
            matches_function = re.findall(regex, script, flags=re.DOTALL)
            if len(matches_function) != 1:
                raise RuntimeError
            function = str(matches_function[0])
            del matches_function
            function = "\n".join(function.split("\n")[:-2])
            # Gets function text

            for filter_string, threshold, handler in filters:
                if function.count(filter_string) >= threshold:
                    handler(function)
                    filters.remove((filter_string, threshold, handler))
                    print("Match found")
                    break

        del match, function, matches, filters
        # Write every json except for objects
        print("Simple jsons written, starting objects.json")
    else:
        print("Skipping simple")

    if skip_objects:
        print("Skipping objects")
    else:
        create_objects_json.write_objects_json(script, root_dir)

    if skip_constants:
        print("Skipping constants")
    else:
        create_constants_json.write_constants_json(script, root_dir)

    if skip_game_modes:
        print("Skipping gamemodes")
    else:
        create_gamemodes_json.create_game_modes(script, root_dir)

    print("Finished")


if __name__ == '__main__':
    create_jsons("jsons/")
