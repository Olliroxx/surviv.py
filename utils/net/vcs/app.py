"""
Needs deobfuscate.py to run, then copies input and output and creates a diff between the latest version and previous version.
"""


def unwrap(text):
    """
    Turns:

    * This te
    * xt is w
    * rapped

    into:

    * This text is wrapped

    :param text: wrapped text
    :return: unwrapped text
    """

    out = ""

    lines = text.split("\r\n")
    prev_line_wrapped = True

    for line in lines[1:]:
        if not prev_line_wrapped or (False if not line else line[0] == "*"):
            # (False if not line else line[0] == "*")
            # Means protects against empty lines raising an error
            out = out + "\n"
        out = out + line

        if len(line) == 127:
            prev_line_wrapped = True
        else:
            prev_line_wrapped = False

    out = out + "\n"

    return out


def diff(a_path, b_path):
    from platform import system
    from subprocess import run, PIPE

    if system() in ("Linux", "Darwin"):
        result = run(["sdiff", "-l", a_path, b_path], stdout=PIPE).stdout
        result = run(["cat", "-n"], input=result, stdout=PIPE).stdout
        result = run(["grep", "-v", "-e", "'($'"], input=result, stdout=PIPE).stdout
        return result
        # Diff, then adding line numbers, then removing lines with no changes
    elif system() == "Windows":
        from os.path import dirname

        result = run(["fc", a_path, b_path], stdout=PIPE).stdout.decode("utf-8")

        result = unwrap(result)
        # Text is wrapped so it fits in the terminal, we don't want that

        path = dirname(__file__)
        path = path.upper()
        path = path.replace("/", "\\")
        path = path + "\\"
        result = result.replace(path, "")
        # Remove path text

        result = result.replace("\\r\\n", "\n")
        # Output has newlines escaped like this

        return result
        # Windows diff
    else:
        raise RuntimeError("Unsupported OS")


def get_small_hash(string):
    lines = string.split("\n")
    last_line = lines[-1]
    small_hash = last_line[28:36]
    return small_hash


def get_json():
    """
    Loads and returns app/changelog_changelog.json
    """

    from json import load
    from os.path import join, dirname

    try:
        file = open(join(dirname(__file__), "changelogs/app_changelog.json"), "r")
        data = load(file)
        file.close()
    except FileNotFoundError:
        return {
            "newest": None,
            "updates": {}
        }

    return data


def write_json(data):
    """
    Writes data to changelogs/app_changelog.json
    """

    from json import dump
    from os.path import join, dirname

    file = open(join(dirname(__file__), "./changelogs/app_changelog.json"), "w")
    dump(data, file, indent=4)
    file.close()


def get_complex_app():
    """
    Gets deobfuscated and diffable versions of app.js
    """

    from os import listdir
    from os.path import abspath, dirname, join
    from re import sub

    result = {}

    file = None
    for script in listdir(join(dirname(abspath(__file__)), "../../asset_processing/deobfuscated/js/")):
        if script.count("app"):
            if file is not None:
                raise RuntimeError("There must be exactly one app.js script in out/code/js")
            file = open(join(dirname(abspath(__file__)), "../../asset_processing/deobfuscated/js/" + script), "r",
                        encoding="utf-8")
    if file is None:
        raise RuntimeError("There must be exactly one app.js script in out/code/js")
    script = file.read()
    file.close()
    del file

    result["deobfuscated"] = script

    diffable = script
    diffable = sub(r"_0x[\da-f]{4,6}", "_0xxxxxx", diffable)
    diffable = sub(r"'[\da-f]{8}'", "'xxxxxxxx'", diffable)

    result["diffable"] = diffable

    return result


def get_app():
    """
    Gets raw, minified app.js
    """

    from requests import get
    from re import findall
    from time import time

    resp = get("https://surviv.io")
    resp_time = time()
    if not resp.ok:
        raise RuntimeError("Got non-ok response")
    html = resp.content.decode("utf-8")
    app_name = findall(r"js/app\.[\da-f]{8}\.js", html)[0]
    resp = get("https://surviv.io/" + app_name)

    return resp.content.decode("utf-8"), resp_time


def check_full(changelog, app, time):
    from hashlib import sha3_256

    # Get the xxxxxxxx part of app.xxxxxxxx.js
    # You can do this with only the script by
    # Using the "//sourceMappingUrl" line at
    # the end of the script.

    big_hash = get_small_hash(app) + "_" + sha3_256(app.encode("utf-8")).hexdigest()

    result = big_hash not in changelog["updates"]

    if not result:
        changelog["updates"][big_hash]["last_seen"] = time

    return result


def check_complex_ver(app_dict):
    simple_ver = get_small_hash(app_dict["raw"])
    complex_ver = get_small_hash(app_dict["deobfuscated"])
    if simple_ver != complex_ver:
        raise RuntimeError("Newest and deobfuscated are different versions (try re-deobfuscating)")


def update_changelog(changelog, app_dict, time):
    from os import mkdir
    from os.path import dirname, join, realpath
    from hashlib import sha3_256

    small_hash = get_small_hash(app_dict["raw"])
    mkdir(join(dirname(__file__), "./changelogs/" + small_hash))

    file = open(join(dirname(__file__), "./changelogs/" + small_hash + "/raw_" + small_hash + ".js"), mode="w",
                encoding="utf-8")
    file.write(app_dict["raw"])
    file.close()

    file = open(join(dirname(__file__), "./changelogs/" + small_hash + "/deob_" + small_hash + ".js"), mode="w",
                encoding="utf-8")
    file.write(app_dict["deobfuscated"])
    file.close()

    diffable_path = join(dirname(__file__), "./changelogs/" + small_hash + "/diff_" + small_hash + ".js")
    file = open(diffable_path, mode="w", encoding="utf-8")
    file.write(app_dict["diffable"])
    file.close()

    big_hash = small_hash + "_" + sha3_256(app_dict["raw"].encode("utf-8")).hexdigest()

    node = {
        "prev": changelog["newest"],
        "versions": {
            "raw": {
                "hash": sha3_256(app_dict["raw"].encode("utf-8")).hexdigest(),
                "location": "./changelogs/" + small_hash + "/raw_" + small_hash + ".js"
            },
            "deob": {
                "hash": sha3_256(app_dict["deobfuscated"].encode("utf-8")).hexdigest(),
                "location": "./changelogs/" + small_hash + "/deob_" + small_hash + ".js"
            },
            "diff": {
                "hash": sha3_256(app_dict["diffable"].encode("utf-8")).hexdigest(),
                "location": "./changelogs/" + small_hash + "/diff_" + small_hash + ".js"
            }
        },
        "first_seen": time,
        "last_seen": time,
    }

    if changelog["newest"] is not None:
        prev_diffable_hash = changelog["newest"]
        prev_diffable_path = changelog["updates"][prev_diffable_hash]["versions"]["diff"]["location"]
        prev_diffable_path = join(dirname(__file__), prev_diffable_path)
        prev_diffable_path = realpath(prev_diffable_path)
        # Get the diffable version of the previous script

        diffable_path = realpath(diffable_path)

        # Get difference between current and previous version
        node["diff"] = diff(prev_diffable_path, diffable_path)

    else:
        node["diff"] = "Source, diff does not make sense"

    changelog["updates"][big_hash] = node
    changelog["newest"] = big_hash

    return changelog


def main():
    changelog = get_json()
    app, time = get_app()
    needs_full = check_full(changelog, app, time)

    if needs_full:
        app_dict = get_complex_app()
        app_dict["raw"] = app
        check_complex_ver(app_dict)
        changelog = update_changelog(changelog, app_dict, time)

    write_json(changelog)


if __name__ == '__main__':
    main()
