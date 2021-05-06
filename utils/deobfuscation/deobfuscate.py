def grab_code():
    import os
    import requests
    import re
    """
    Gets the index.html of surviv.io, and the current js files
    """

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

    file = open(".\\out\\code\\index.html", "w", encoding="utf-8")
    file.write(resp)
    file.close()
    # Write HTML file

    files = re.findall("js/[a-z]*\\.[0-9a-f]{8}\\.js", resp)

    for script in files:
        print("Downloading " + script)
        file = open(".\\out\\code\\" + script, "bw")

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


def eval_exp(exp):
    import ast
    return eval_(ast.parse(exp, mode='eval').body)


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
    else:
        raise TypeError(node)


def solve_hex_string(string):
    import ast
    components = string.split()
    numbers_as_strings = components[::2]
    operations = components[1::2]
    numbers = []
    for i in numbers_as_strings:
        numbers.append(ast.literal_eval(i))

    for operation in operations:
        x = numbers[0]
        numbers.pop(0)
        y = numbers[0]
        numbers.pop(0)
        if operation == "+":
            numbers.insert(0, x + y)
        elif operation == "-":
            numbers.insert(0, x - y)
        elif operation == "*":
            numbers.insert(0, x * y)
        elif operation == "/":
            numbers.insert(0, x / y)
    result = str(numbers[0])
    return result


def solve_hex():
    """
    In app.js, there a multiple locations where instead of using a number, a bunch of hex and some math is used to get the actual number
    This script changes all of it back to a single hex value
    """

    import re
    from get_app import get_app

    print("Simplifying hex")

    file = get_app()
    line = file.readline()
    if line != "// Indented\n":
        raise RuntimeError("This should be run right after auto indentation")
    script = line + file.read()
    file.close()
    del file
    # Check that auto indent was run just before this, and read the file

    to_solve = []
    for match in re.findall("[^_](-?0x[0-9a-f]+(?: ?[*+/-] ?-?0x[0-9a-f]*)+)", script):
        to_solve.append(match.strip(" "))
    print(str(len(to_solve)) + " changes to make")
    for element in to_solve:
        script = script.replace(element, str(eval_exp(element)))

    script = script.replace("// Indented\n", "//Hex simplified\n", 1)

    file = get_app("w")
    file.write(script)
    file.close()

    print("Hex simplified\n")


def autoindent():
    """
    Indents and spaces out app.js
    :return:
    """
    import jsbeautifier
    import os

    for script in os.listdir(".\\deobfuscated\\js"):

        file = open(".\\deobfuscated\\js\\" + script, "r", encoding="utf-8")
        text = file.readline()
        file.close()
        if text.startswith("//"):
            print(script + " already processed, skipping")
            continue

        print("Indenting " + script)
        opts = jsbeautifier.default_options()
        result = jsbeautifier.beautify_file(".\\deobfuscated\\js\\" + script, opts)
        result = "// Indented\n" + result

        with open(".\\deobfuscated\\js\\" + script, "w", encoding="utf-8") as writer:
            print("Writing " + script)
            writer.write(result)
            writer.close()

        print("Done indenting " + script)
        print()


def fill_strings():
    """
    On the first line (2nd after indentation), there is a big list
    Many strings are instead references to this list
    This script changes the list references into strings
    :return:
    """
    import ast
    import re
    from get_app import get_app

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

    regex = "a0_0x[0-9a-f]+"
    list_name = re.findall(regex, line)[0]
    big_list = ast.literal_eval(line[line.find("["):])
    del line

    regex = "\\(" + list_name + ", ([0-9]+?)\\)"
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

    regex = """var (a0_0x[0-9a-f]{3,7}) = function\\(_0x[0-9a-f]{6}, _0x[0-9a-f]{6}\\) \\{
    _0x[0-9a-f]{6} = _0x[0-9a-f]{6} - \\(0\\);
    var _0x[0-9a-f]{6} = """ + list_name + """\\[_0x[0-9a-f]{6}];
    return _0x[0-9a-f]{6};
};"""
    alt_name = re.findall(regex, script)[0]
    del regex
    # There is a a function that (as far as I can tell) does nothing except rename it
    # This finds the new name

    regex = """var a0_[0-9a-f]{3,7} = function\\(_0x[0-9a-f]{6}, _0x[0-9a-f]{6}\\) \\{
        _0x[0-9a-f]{6} = _0x[0-9a-f]{6} - \\(0\\);
        var _0x[0-9a-f]{6} = """ + list_name + """\\[_0x[0-9a-f]{6}];
        return _0x[0-9a-f]{6};
    };"""
    script = re.sub(regex, "", script)
    del regex
    # Delete the function

    regex = alt_name + "\\('(0x[0-9a-f]+?)'\\)"
    matches = re.findall(regex, script)
    del regex
    # Find usages of the alternate name

    print(str(len(matches)) + " strings to fill")

    for match in matches:
        number = ast.literal_eval(match)
        to_replace = alt_name + "('" + match + "')"
        string = big_list[number]
        string = string.replace("\n", "\\x0a")
        string = string.replace("'", "\\'")
        string = "'" + string + "'"
        script = script.replace(to_replace, string, 1)
    del match, number, string, to_replace
    # Replace usages

    script = script.replace("//Hex simplified\n", "//Strings filled\n", 1)

    file = get_app("w")
    file.write(script)
    file.close()

    print("Strings filled\n")


def list_to_string(input_):
    """
    Turns a list of ints into a string made up of the characters with the unicode value of each int in the list
    :param input_: A list of ints
    :return:
    """
    string = ""
    for x in input_:
        string = string + chr(x)
    return string


def remove_char_code_lists():
    """
    Occasionally, instead of strings, lists of the char codes are used instead
    This replaces those lists with the actual strings
    :return:
    """
    import re
    from get_app import get_app

    with get_app() as file:
        line = file.readline()
        if line != "//Strings filled\n":
            file.close()
            raise RuntimeError("This script should be run right after the strings have been filled")
        script = line + file.read()
    del line

    print("Removing (some) charcode lists")

    usages = len(re.findall("fromCharCode", script))

    regex = """(_0x[0-9a-f]{3,6}) = function _0x[0-9a-f]{3,6}\\(_0x[0-9a-f]{3,6}\\) \\{
 {20}return _0x[0-9a-f]{3,6}\\['map'\\]\\(function\\(_0x[0-9a-f]{3,6}\\) \\{
 {24}return String\\['fromCharCode'\\]\\(_0x[0-9a-f]{3,6}\\);
 {20}\\}\\)\\['join'\\]\\(''\\);
 {16}},"""
    functions = re.findall(regex, script)
    del regex

    if len(functions) < usages:
        print("More usages than functions")
    del usages

    for i in functions:
        regex = i + "\\((\\[(?:[0-9]+, )+[0-9]+?\\])\\)"
        matches = re.findall(regex, script)

        if len(matches) + 1 == len(re.findall(i, script)):
            regex = i + """ = function _0x[0-9a-f]{3,6}\\(_0x[0-9a-f]{3,6}\\) \\{
 {20}return _0x[0-9a-f]{3,6}\\['map'\\]\\(function\\(_0x[0-9a-f]{3,6}\\) \\{
 {24}return String\\['fromCharCode'\\]\\(_0x[0-9a-f]{3,6}\\);
 {20}\\}\\)\\['join'\\]\\(''\\);
 {16}},"""
            script = re.sub(regex, "", script)
        # If all the usages are either ones this script can handle or the definition, remove the definition

        script = re.sub(i, "list_to_string", script)
        for x in matches:
            import ast
            x = ast.literal_eval(x)
            del ast
            script = re.sub("list_to_string\\(" + re.escape(str(x)) + "\\)", "'" + list_to_string(x) + "'", script)
    del regex, x, functions, matches, i

    script = script.replace("//Strings filled\n", "//Unicode lists filled\n", 1)

    with get_app("w") as file:
        file.write(script)
    print("Charcode lists removed\n")


def add_bools():
    """
    ![] and !![] are used instead of False and True respectively
    :return:
    """
    from get_app import get_app

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


def main(dl_assets=False, redownload=True, deobfuscate=True):
    """
    Downloads and deobfuscates primarily app.js, but also other scripts and assets to a lesser degree
    """
    from grab_assets import grab_assets

    if redownload:
        grab_code()
    else:
        import os
        try:
            os.mkdir("deobfuscated")
        except FileExistsError:
            pass
        del os
        import shutil
        shutil.rmtree("../overrides/surviv.io")
        shutil.copytree("../out/code", "overrides\\surviv.io")
        del shutil
    del redownload

    autoindent()
    if dl_assets:
        grab_assets(True)
    del dl_assets
    if deobfuscate:
        solve_hex()
        fill_strings()
        remove_char_code_lists()
        add_bools()


if __name__ == "__main__":
    main()
    # main(dl_assets=True)
    # main(redownload=False)
