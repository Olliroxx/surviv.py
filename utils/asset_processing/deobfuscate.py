from misc_utils import get_app
import re


def grab_code():
    """
    Downloads the index.html of surviv.io, and the current js files
    """

    import os
    from os.path import join, dirname
    import requests

    import shutil
    folders = [".\\deobfuscated", ".\\out\\code"]
    for folder in folders:
        try:
            shutil.rmtree(folder)
        except FileNotFoundError:
            pass
    del folder, folders

    folders = [".\\deobfuscated", ".\\out", ".\\out\\code", ".\\out\\code\\js"]
    for folder in folders:
        try:
            os.mkdir(folder)
        except FileExistsError:
            pass

    print("Downloading HTML...")
    resp = requests.get("https://surviv.io/")
    if resp.status_code != 200:
        raise RuntimeError("Server returned non-200 code: " + str(resp.status_code))
    else:
        resp = resp.text
    print("HTML retrieved\n")
    # Get HTML, and ensure nothing went horribly wrong

    file = open(join(dirname(__file__), ".\\out\\code\\index.html"), "w", encoding="utf-8")
    file.write(resp)
    file.close()
    # Write HTML file

    files = re.findall(r"js/[a-z]*\.[\da-f]{8}\.js", resp)

    for script in files:
        print("Downloading " + script)
        file = open(join(dirname(__file__), ".\\out\\code\\" + script), "bw")

        resp = requests.get("https://surviv.io/" + script, stream=True)
        length = resp.headers.get("content-length")

        if length is None:
            file.write(resp.content)
        else:
            dl = 0
            length = int(length)

            for data in resp.iter_content(chunk_size=4096):
                dl += len(data)
                file.write(data)
                done = int(50 * dl / length)
                print(str(done) + "% complete")

        file.close()

    shutil.rmtree(".\\deobfuscated")
    shutil.copytree(".\\out\\code", ".\\deobfuscated")
    print("Done downloading\n")


def eval_exp(exp: str):
    """
    Evaluates simple expressions (eg. 1+2)

    :param exp: the expression to evaluate, as a string
    :return: The result
    """
    from io import StringIO
    from tokenize import generate_tokens, untokenize, NAME, NUMBER, OP, STRING
    import ast

    def is_float(s: str):
        if "." in s:
            return True
        else:
            return False

    def deci_statement(s: str):
        result = []
        g = generate_tokens(StringIO(s).readline)  # tokenize the string
        for toknum, tokval, _, _, _ in g:
            if toknum == NUMBER and is_float(tokval):
                result.extend([
                    (NAME, 'Decimal'),
                    (OP, '('),
                    (STRING, repr(tokval)),
                    (OP, ')')
                ])
            else:
                result.append((toknum, tokval))
        return untokenize(result)

    tree = ast.parse(deci_statement(exp))

    return eval_(tree)


def eval_(node):
    import ast
    import operator as op
    operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
                 ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
                 ast.USub: op.neg}

    if isinstance(node, ast.Num):
        return node.n
    elif isinstance(node, ast.BinOp):
        # noinspection PyTypeChecker
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp):
        # noinspection PyTypeChecker
        return operators[type(node.op)](eval_(node.operand))
    elif isinstance(node, ast.Module):
        return eval_(node.body[0])
    elif isinstance(node, ast.Expr):
        return eval_(node.value)
    elif isinstance(node, ast.Call):
        if node.func.id != "Decimal":
            raise RuntimeError("Function that isn't decimal")
        from decimal import Decimal
        return Decimal(node.args[0].s)
    else:
        raise TypeError(node)


def find_usages(solved_items, script):
    """
    Used for adding multithreading to float processing, adds context characters to each match.

    Without this, `1 + 2` would replace `1 + 20` with `30`. Adding context characters avoids that.

    :param solved_items: List of values to add context to
    :param script: string that to take context from
    """

    from re import findall, escape
    result = {}

    for old, new in solved_items:
        for each in findall(r"([^\d])" + escape(old) + r"([^\d])", script):
            result[each[0] + old + each[1]] = each[0] + new + each[1]

    return result


def split_list(to_split, size):
    for i in range(0, len(to_split), size):
        yield tuple(to_split)[i:i + size]


def solve_hex():
    """
    In app.js there are simple expression written in hex, instead of ints and some floats.
    This function swaps them out for the results (currently only ints)
    """

    from multiprocessing import Pool
    from os import cpu_count
    from math import ceil

    print("Simplifying hex")

    file = get_app()
    line = file.readline()
    if line != "// Indented\n":
        file.close()
        raise RuntimeError("This should be run right after auto indentation")
    script = line + file.read()
    file.close()
    del file
    # Check that auto indent was run just before this, and read the file

    to_solve = set(re.findall(r"[^_](-?0x[\da-f]+(?: ?[*+/-] ?-?0x[\da-f]*)+)", script))
    print(str(len(to_solve)) + " ints to simplify")
    for element in to_solve:
        script = script.replace(element, str(eval_exp(element)))

    regex = r"-?[\d.]+ [+/*\-] -?[\d.]+"
    matches = set(re.findall(regex, script))
    print(str(len(matches)) + " decimals")

    solved = {}
    for match in matches:
        solved[match] = str(eval_exp(match))

    split_size = ceil(len(solved) / cpu_count())
    split = split_list(solved.items(), split_size)

    p = Pool()
    result = p.starmap(find_usages, zip(split, [script] * cpu_count()))
    p.join()
    p.close()

    context_added = {}
    for item in result:
        context_added = context_added | item

    for old, new in context_added.items():
        script = script.replace(old, new)

    regex = r"-\([\d\.]+\)"
    matches = set(re.findall(regex, script))
    print(str(len(matches)) + " expressions to simplify")

    for match in matches:
        script = script.replace(match, str(eval_exp(match)))

    script = script.replace("// Indented\n", "//Hex simplified\n", 1)

    file = get_app("w")
    file.write(script)
    file.close()

    print("Hex simplified\n")


def autoindent():
    """
    Indents and spaces out app.js
    """
    import jsbeautifier
    from os.path import join, dirname
    from os import listdir

    for script in listdir(".\\deobfuscated\\js"):

        file = open(join(dirname(__file__), ".\\deobfuscated\\js\\" + script), "r", encoding="utf-8")
        text = file.readline()
        file.close()
        if text.startswith("//"):
            print(script + " already processed, skipping")
            continue

        print("Indenting " + script)
        opts = jsbeautifier.default_options()
        result = jsbeautifier.beautify_file(".\\deobfuscated\\js\\" + script, opts)
        result = "// Indented\n" + result

        with open(join(dirname(__file__),
                       ".\\deobfuscated\\js\\" + script), "w", encoding="utf-8", newline="\n") as writer:
            print("Writing " + script)
            writer.write(result)
            writer.close()

        print("Done indenting " + script)
        print()


def fill_strings():
    """
    On the first line (2nd after indentation), there is a big list.
    Many strings are instead references to this list.
    This script changes the list references into strings.
    """
    import ast

    file = get_app()
    line = file.readline()
    if line != "//Hex simplified\n":
        file.close()
        raise RuntimeError("This script should be run right after the hex has been simplified")
    script = line + file.read()
    file.close()
    del file, line

    print("Filling strings")

    line = script.split("\n")[1][:-1]
    # Get the big list that starts with a0_, and return it's name and the content of the list

    regex = r"a0_0x[\da-f]+"
    list_name = re.findall(regex, line)[0]
    big_list = ast.literal_eval(line[line.find("["):])
    # Get the list and parse it

    regex = "\\(" + list_name + r", ([\d]+?)\)"
    shift_amount = int(re.findall(regex, script)[0]) * -1
    del regex
    from collections import deque
    big_list = deque(big_list)
    del deque
    big_list.rotate(shift_amount)
    big_list = list(big_list)
    # The list is shifted by a certain amount, this finds the amount and shifts it

    script_as_list = script.split("\n")
    script_as_list.pop(1)
    script = "\n".join(script_as_list)
    del script_as_list
    # Remove the list

    regex = r"""var (a0_0x[\da-f]{3,7}) = function\(_0x[\da-f]{6}, _0x[\da-f]{6}\) \{
    _0x[\da-f]{6} = _0x[\da-f]{6} - \(0\);
    var _0x[\da-f]{6} = """ + list_name + r"""\[_0x[\da-f]{6}];
    return _0x[\da-f]{6};
};"""
    alt_name = re.findall(regex, script)[0]
    del regex
    # There is a a function that (as far as I can tell) does nothing except rename it
    # This finds the new name

    regex = r"""var a0_[\da-f]{3,7} = function\(_0x[\da-f]{6}, _0x[\da-f]{6}\) \{
        _0x[\da-f]{6} = _0x[\da-f]{6} - \(0\);
        var _0x[\da-f]{6} = """ + list_name + r"""\[_0x[\da-f]{6}];
        return _0x[\da-f]{6};
    };"""
    script = re.sub(regex, "", script)
    del regex
    # Delete the function

    regex = alt_name + r"\('(0x[\da-f]+?)'\)"
    matches = re.findall(regex, script)
    del regex
    # Find usages of the alternate name

    print(str(len(matches)) + " strings to fill")

    for match in matches:
        script = script.replace(alt_name + "('" + match + "')",
                                "'" + big_list[int(match, 16)].replace("\n", r"\x0a").replace("'",
                                                                                              r"\'") + "'")  # noqa: E501
        # More readable, slower version:
        # number = int(match, 16)
        # to_replace = alt_name + "('" + match + "')"
        # string = big_list[number]
        # string = string.replace("\n", r"\x0a")
        # string = string.replace("'", r"\'")
        # string = "'" + string + "'"
        # script = script.replace(to_replace, string, 1)

    # Replace usages
    script = script.replace("//Hex simplified\n", "//Strings filled\n", 1)

    script = re.sub(r"https://web\.archive\.org/web/\d{14}/", "", script)
    # Make scripts from archive.org diffable

    file = get_app("w")
    file.write(script)
    file.close()

    print("Strings filled\n")


def list_to_string(data):
    """
    Turns a list of ints into a string made up of the characters with the unicode value of each int in the list

    :param data: A list of ints
    """
    string = ""
    for x in data:
        string = string + chr(x)
    return string


def remove_char_code_lists():
    """
    In one or two places, instead of strings, lists of the char codes are used instead.
    This replaces those lists with the actual strings.
    """

    with get_app() as file:
        line = file.readline()
        if line != "//Strings filled\n":
            file.close()
            raise RuntimeError("This script should be run right after the strings have been filled")
        script = line + file.read()
    del line

    print("Removing (some) charcode lists")

    usages = len(re.findall("fromCharCode", script))

    regex = r"""(_0x[\da-f]{3,6}) = function _0x[\da-f]{3,6}\(_0x[\da-f]{3,6}\) \{
 {20}return _0x[\da-f]{3,6}\['map'\]\(function\(_0x[\da-f]{3,6}\) \{
 {24}return String\['fromCharCode'\]\(_0x[\da-f]{3,6}\);
 {20}\}\)\['join'\]\(''\);
 {16}},"""
    functions = re.findall(regex, script)
    del regex

    if len(functions) < usages:
        print("More usages than functions")
    del usages

    for i in functions:
        regex = i + r"\((\[(?:[\d]+, )+[\d]+?\])\)"
        matches = re.findall(regex, script)

        if len(matches) + 1 == len(re.findall(i, script)):
            regex = i + r""" = function _0x[\da-f]{3,6}\(_0x[\da-f]{3,6}\) \{
 {20}return _0x[\da-f]{3,6}\['map'\]\(function\(_0x[\da-f]{3,6}\) \{
 {24}return String\['fromCharCode'\]\(_0x[\da-f]{3,6}\);
 {20}\}\)\['join'\]\(''\);
 {16}},"""
            script = re.sub(regex, "", script)
        # If all the usages are either ones this script can handle or the definition, remove the definition

        script = re.sub(i, "list_to_string", script)
        for x in matches:
            import ast
            x = ast.literal_eval(x)
            del ast
            script = re.sub("list_to_string\\(" + re.escape(str(x)) + "\\)", "'" + list_to_string(x) + "'", script)

    script = script.replace("//Strings filled\n", "//Unicode lists filled\n", 1)

    with get_app("w") as file:
        file.write(script)
    print("Charcode lists removed\n")


def add_bools():
    """
    Replaces !![] with true and ![] with false
    """
    with get_app() as file:
        line = file.readline()
        if line != "//Unicode lists filled\n":
            file.close()
            raise RuntimeError("This script should be run right after the charcode lists have been filled")
        script = line + file.read()
    del line

    script = script.replace("!![]", "true")
    script = script.replace("![]", "false")
    script = script.replace("//Unicode lists filled\n", "//Bools added\n", 1)

    with get_app("w") as file:
        file.write(script)
    print("Bools added\n")


def process_jsons():
    """
    Parses json
    """
    from json import loads, dumps
    from textwrap import indent

    with get_app() as file:
        line = file.readline()
        if line != "//Bools added\n":
            file.close()
            raise RuntimeError("This script should be run right after the charcode lists have been filled")
        script = line + file.read()
    del line

    print("Parsing json")

    regex = r" \= JSON\[\'parse\'\]\(\'.*\'\);"
    replacements = {}
    for to_parse in re.findall(regex, script):
        parse_data = to_parse[18:-3]
        parse_data = parse_data.replace("\\'", "'")
        parse_data = parse_data.replace("\\x22", "\x22")
        parse_data = parse_data.replace("\\x20", "\x20")
        parsed = loads(parse_data)
        result = dumps(parsed, indent=4)
        result = indent(result, " " * 12)
        replacements[to_parse] = result

    for old, new in replacements.items():
        script = script.replace(old, new)

    script = script.replace("//Bools added\n", "//Json parsed\n")
    with get_app("w") as file:
        file.write(script)
    print("Json parsed")


def main(dl_assets=False, redownload=True, deobfuscate=True):
    """
    Downloads and deobfuscates primarily app.js, but also other scripts and assets to a lesser degree

    .. warning::
        This takes a long time (~15m on my quad core 3.6Ghz with 60Mbps down)

    .. warning::
        dl_assets does not download all svgs, you need to use grab_svgs.py in json_processing it

    :param dl_assets: If true will download and slice .pngs, mp3s and svgs, using :doc:`grab_assets`
    :param redownload: If false will use already downloaded copies
    :param deobfuscate: If you don't want to deobfuscate, set to false (just for assets)
    """
    from grab_assets import grab_assets

    if redownload:
        grab_code()
    else:
        from os import mkdir
        try:
            mkdir("deobfuscated")
        except FileExistsError:
            pass
        del mkdir

    autoindent()
    if dl_assets:
        grab_assets(True)
    if deobfuscate:
        solve_hex()
        fill_strings()
        remove_char_code_lists()
        add_bools()
        process_jsons()


if __name__ == "__main__":
    main(dl_assets=True)
