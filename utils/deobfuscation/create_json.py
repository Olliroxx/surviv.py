import ast
import json
import re


class DataNeededError(RuntimeError):
    """
    This is the error used when there isn't enough information to turn a function into a value
    """
    pass


def basic_simplify(data):
    import textwrap
    data = textwrap.dedent(data)

    regex = "[^_]0x[0-9a-f]+"
    hex_matches = re.findall(regex, data)
    for hex_data in hex_matches:
        data = data.replace(hex_data, str(int(hex_data, 16)), 1)
    del hex_matches

    data = re.sub("Math\\[[\"']PI[\"']]", "3.141592653589793", data)
    data = solve_expressions(data)

    replacements = {
        "\\\\x20": " ",
        " 1:": " \"1\":",
        " 2:": " \"2\":",
        "[^\\\\]\\\\x": "\\\\\\\\x",
        "'": "\"",
    }
    for pattern, new in replacements.items():
        data = re.sub(pattern, new, data)

    data = data.rstrip(", \n")

    return data


def solve_expressions(data: str):
    changed = True
    while changed:
        changed = False
        regex = "(?:-?[0-9\\.]+ ?[+*\\-/] )+-?[0-9\\.]+"
        expression_matches = re.findall(regex, data)
        for match in expression_matches:
            solved = solve_expression(match)
            data = data.replace(match, str(solved), 1)
            changed = True
        # Solve expressions (eg. 2+1)

        regex = "-?\\(-?[0-9\\.]+\\)"
        bracket_matches = re.findall(regex, data)
        for match in bracket_matches:
            solved = str(solve_expression(match))
            data = data.replace(match, solved, 1)
            changed = True
        # Remove redundant brackets around ints
    return data


def solve_expression(to_solve: str):
    return eval_(ast.parse(to_solve, mode="eval").body)


def eval_(node):
    import operator as op
    operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
                 ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
                 ast.USub: op.neg}
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        # noinspection PyTypeChecker
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        # noinspection PyTypeChecker
        return operators[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)


def split_bracket_level(data: str, trim_start=True, ignore_unbalanced=False):
    if not data:
        raise ValueError("data is empty")

    bracket_level = 0
    split_points = [0]
    new_text = True
    pos = 0

    for pos in range(len(data)):

        if data[pos] == "{":
            bracket_level += 1
        elif data[pos] == "}":
            bracket_level -= 1
        elif data[pos] == "\n" and bracket_level == 0 and new_text:
            split_points.append(pos)
            new_text = False

        if data[pos] != " ":
            new_text = True

        if bracket_level < 0 and not ignore_unbalanced:
            raise RuntimeError("Unbalanced close bracket at pos " + str(pos))
    if bracket_level > 0 and not ignore_unbalanced:
        raise RuntimeError("Unbalanced open bracket as pos" + str(pos))

    split_points.append(len(data))

    split = []
    for i in range(len(split_points) - 1):
        start = split_points[i]
        stop = split_points[i + 1]
        split.append(data[start:stop])

    if trim_start:
        for i in range(len(split)):
            if split[i].startswith("\n"):
                split[i] = split[i].lstrip("\n")
                split[i] = split[i].lstrip(" ")

    return split


def solve_vars(data: list, functions=None):
    """
    :param data: the string to split and convert
    :param functions: a dictionary of conversion functions. Format:  "name in code": function
    :return:
    """

    if functions is None:
        functions = {}

    needs_solving_regex = "_0x[0-9a-f]{4,}[\\[\\(]"

    solved = {}
    unsolved = {}
    for var in data:
        name, content = var.split(" = ", 1)
        unsolved[name] = content
    del var

    while unsolved:
        keys_to_delete = []
        for key in unsolved:
            value = unsolved[key]

            matches = re.findall(needs_solving_regex, value)

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
                        if len(value.split(fname)) > 2:
                            result = result + ","
                        value = value.replace(args, result)
                        unsolved[key] = value
                    except DataNeededError:
                        pass

                elif fname not in unsolved:
                    raise RuntimeError("No way to handle function " + fname)
            else:
                keys_to_delete.append(key)
                solved[key] = value

        for key in keys_to_delete:
            del unsolved[key]

    return solved


def handler_generic(filename="", return_processed=False):
    def handler(data: str):

        nonlocal filename
        nonlocal return_processed

        data = data.split("var ")
        for i in data:
            if re.findall("_0x[0-9a-f]{6} = {", i):
                data = i
                break
        del i
        # Split and find the interesting variable

        data = re.sub("_0x[0-9a-f]{6} = ", "", data, count=1)
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
        Normal:
          Write a dict with the each value in categories used as the key
          Any keys that are 0s are discarded
        Expand:
          All keys must either be 0s or 1s
          There can only be one 1
          The result of value of 1 must be a dict
          The keys of the result dict are used instead of the values from categories
    :return:
    """

    def dict_ref_setup(source_dict: str):
        def dict_ref(args: str, solved: dict):

            nonlocal source_dict

            if not type(source_dict) == dict:
                if source_dict not in solved:
                    raise DataNeededError("Source dict not solved")
                source_dict = solved[source_dict]

            args = args.rstrip(",)")
            args = args[10:].split(",", 1)
            args[0] = args[0].strip("\"'")
            # Get args from function+args

            if args[0] not in source_dict:
                raise RuntimeError

            args[1] = basic_simplify(args[1])

            parsed = json.loads(args[1])
            result_dict = {}

            for key in source_dict[args[0]]:
                result_dict[key] = source_dict[args[0]][key]
            for key in parsed:
                result_dict[key] = parsed[key]

            return json.dumps(result_dict, indent=4)

        return dict_ref

    def merge_dicts(args: str, solved: dict):
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

    def handler(data: str):

        nonlocal filename
        nonlocal categories

        data = basic_simplify(data)

        data = data.split("var ")
        functions_string = []
        longest = ""
        function_regex = "[\"'][0-9a-f]{8}[\"']: function\\(_0x[0-9a-f]{6}, _0x[0-9a-f]{6}, _0x[0-9a-f]{6}\\) \\{\n {12}[\"']use strict[\"'];"
        for i in data:
            if len(i) > len(longest):
                longest = i
            if "function" in i and not re.findall(function_regex, i):
                functions_string.append(i)
        data = longest
        del longest, i, function_regex
        data = data.split(";")[0]
        # Split the function, with "var " at the split points
        # Find the longest one and discard everything else, except functions which might need a handler

        dict_ref_regex = """function _0x[0-9a-f]{6}\\(_0x[0-9a-f]{6}, _0x[0-9a-f]{6}\\) \\{
 {16}return _0x[0-9a-f]{6}\\["mergeDeep"\\]\\(\\{\\}. _0x[0-9a-f]{6}\\[_0x[0-9a-f]{6}\\], \\{
 {20}"baseType": _0x[0-9a-f]{6}
 {16}\\}, _0x[0-9a-f]{6}\\);
 {12}\\}"""
        merge_dicts_regex = "(_0x[0-9a-f]{6})\\[[\"']mergeDeep[\"']\\]"
        functions = {}
        for function in functions_string:
            has_handler = False
            if re.findall(dict_ref_regex, function):
                key = re.findall("function (_0x[0-9a-f]{6})", function)[0]
                source_dict = re.findall("_0x[0-9a-f]{6}\\[_0x[0-9a-f]{6}]", function)[0][:9]
                value = dict_ref_setup(source_dict)
                functions[key] = value
                has_handler = True
                del source_dict

            if re.findall(merge_dicts_regex, function):
                key = re.findall(merge_dicts_regex, function)[0]
                value = merge_dicts
                if key not in functions:
                    functions[key] = value
                    has_handler = True

            if not has_handler:
                raise RuntimeError("Function without handler")
        del merge_dicts_regex, dict_ref_regex, function, has_handler, key, functions_string

        data = split_bracket_level(data)

        simple_value_regex = "_0x[0-9a-f]{6} = -?[0-9.]+"
        simple_values = {}
        to_remove = []
        for variable in data:
            if re.findall(simple_value_regex, variable):
                split = variable.split(" = ")
                key = split[0]
                value = split[1][:-1]
                simple_values[key] = value
                to_remove.append(variable)
        # Find "simple variables" (eg _0x123 = 0.5) and add them to a list

        for variable in to_remove:
            data.remove(variable)
        # Remove simple values from data

        data_solved = []
        for i in range(len(data)):
            variable = data[i]
            for key, value in simple_values.items():
                variable = variable.replace(key, value)
            variable = basic_simplify(variable)
            data_solved.append(variable)
        data = data_solved
        del data_solved, key, value, variable, i
        # Replace the simple variables with their values

        result = solve_vars(data, functions)
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
                    raise ValueError("Cannot have categories other than 0 or 1 in expand mode")
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


def create_jsons(root_dir: str):
    from get_app import get_app

    with get_app() as file:
        line = file.readline()
        if line != "//Bools added\n":
            raise RuntimeError("The script should be run right after the boolean adder")
        script = line + file.read()
    del line, file
    # Check at what stage this is being run

    regex = """'[0-9a-f]{8}': function\\(_0x[0-9a-f]{6}, _0x[0-9a-f]{6}, _0x[0-9a-f]{6}\\) {
 {12}'use strict';
 {12}var _0x[a-f0-9]{6} = \\[(_0x[0-9a-f]{6}\\('[0-9a-f]{8}'\\)(?:, _0x[0-9a-f]{6}\\('[0-9a-f]{8}'\\))*)]"""
    matches = re.findall(regex, script)
    if len(matches) != 1:
        raise RuntimeError
    regex = "[a-f0-9]{8}"
    matches = re.findall(regex, matches[0])
    del regex
    # There's a function that contains the names of other functions with the data we want in them. This finds that function

    filters = [
        ("quest", 20, handler_generic(root_dir + "quests.json")),  # Quests
        ("falloff", 5, handler_multidict(root_dir + "bullets.json", categories=("a", "b", "c"))),  # Bullets
        ("explosionEffectType", 10, handler_generic(root_dir + "explosions.json")),  # Explosions
        ("playerRad", 1, handler_multidict(root_dir + "nonweapons.json")),  # Nonweapons
        ("'name': 'VSS'", 1, handler_generic(root_dir + "guns.json")),  # Guns
        ("melee", 30, handler_multidict(root_dir + "melee_weapons.json")),  # Melee
        ("noDropOnDeath", 30, handler_multidict(root_dir + "outfits.json")),  # Outfits
        ("perk", 30, handler_generic(root_dir + "perks.json")),  # Perks
        ("pass_survivr", 5, handler_generic(root_dir + "passes.json")),  # Passes
        ("ping", 6, handler_generic(root_dir + "pings.json")),  # Pings
        ("role", 15, handler_generic(root_dir + "roles.json")),  # Roles
        ("'type': 'throwable',", 1, handler_generic(root_dir + "explosives.json")),  # Throwables
        ("'unlock_default'", 1, handler_generic(root_dir + "default_unlocks.json")),  # Default unlocks
    ]
    # Format : string, threshold, handler function
    # If [string] is found more times than (or equal to) [threshold], then [handler function] is called

    for match in matches:
        regex = "'" + match + "': function\\(_0x[0-9a-f]{6}(?:, _0x[0-9a-f]{6})*\\) {\n {12}'use strict';.*?'use strict';"
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
                continue

    del match, function, script, matches
    pass


if __name__ == '__main__':
    import os

    try:
        os.mkdir("./jsons")
    except FileExistsError:
        pass
    del os

    create_jsons("./jsons/")
