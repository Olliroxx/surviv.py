def get_anims(script, root_dir):
    """
    Gets animation data and writes to root_dir/anims.json
    """
    from re import findall, DOTALL, split
    from json import dump

    # Find module, the bit that starts with '[8 hex chars]': function(3 variables) {[newline]'use strict'
    module = findall(r""" {8}'[\da-f]{8}': function\(_0x[\da-f]{4,6}, _0x[\da-f]{4,6}, _0x[\da-f]{4,6}\) {
 {12}'use strict';
 {12}var (?:_0x[\da-f]{4,6} = _0x[\da-f]{4,6}\('[\da-f]{8}'\),
 {16}_0x[\da-f]{4,6} = _0x[\da-f]{4,6}\(_0x[\da-f]{4,6}\),
 {16})+(?:_0x[\da-f]{4,6}, )+_0x[\da-f]{4,6};(.*
 {12}_0x[\da-f]{4,6}\['exports'] = {
 {16}'Pose': _0x[\da-f]{4,6},
 {16}'Bones': _0x[\da-f]{4,6},
 {16}'IdlePoses': _0x[\da-f]{4,6},
 {16}'Animations': _0x[\da-f]{4,6}
 {12}};
 {8}},)
 {8}'[\da-f]{8}': function""", script, DOTALL)[0]

    # Theres a lot of wrapper code (module imports, points, stuff like that), this removes it
    target_data = findall(r"""
 {12}_0x[\da-f]{4,6}\(\(.*?
 {12}var (.*) {12}_0x[\da-f]{4,6}\['exports']""", module, DOTALL)[0]

    # First element is idle pose data, second is weapon renames and anims
    idles_raw, target_data = split(r""",\n(?! {16} )""", target_data, 1, DOTALL)

    weap_renames_raw, anims_raw = split(r"""\n {16}(?!_0x[\da-f]{4,6} = _)""", target_data, 1, DOTALL)

    # Some timing values are accessed from a dict, but most of those dicts are renamed
    renames = process_weap_renames(weap_renames_raw)
    player_rename = findall(r"(_0x[\da-f]{4,6})\['player']", anims_raw)[0]
    renames[player_rename] = []

    anims = process_anims(anims_raw, renames)
    idles = process_idles(idles_raw)

    with open(root_dir+"anims.json", "w") as file:
        dump({"idles": idles, "animations": anims}, file, indent=4)

    print("Finished anims.json")


def process_anims(anims_raw, renames):
    from textwrap import dedent
    from re import split, DOTALL

    # Remove first line and last 2
    anims_raw = "\n".join(anims_raw.split("\n")[1:-2])
    anims_raw = dedent(anims_raw)

    anims_raw = split(r"""(?<=\n}),\n""", anims_raw, flags=DOTALL)

    anims = dict([process_anim(anim, renames) for anim in anims_raw])
    return anims


def process_anim(raw, renames):
    from textwrap import dedent

    name = raw.split("'")[1]

    frames_raw, effects_raw = raw.split("\n    'effects': [")
    effects_raw = effects_raw[:-3]

    frames_raw = frames_raw.split("\n    'keyframes': [")[1][:-2]
    frames_raw = dedent(frames_raw)

    frames = process_frames(frames_raw, renames)
    effects = process_effects(effects_raw, renames)

    return name, {"keyframes": frames, "effects": effects}


def process_frames(raw, renames):
    if not raw:
        return []

    from re import findall
    constructor = findall(r"_0x[\da-f]{4,6}", raw)[0]
    raw = raw[len(constructor)+1:-1]

    frames_raw = raw.split(", "+constructor)
    frames = []
    for frame_raw in frames_raw:

        time_raw = frame_raw.split(", ")[0]
        frame_raw = frame_raw[len(time_raw)+2:]
        frame = parse_time(time_raw, renames)

        limbs = parse_point_set(frame_raw)
        frame = frame | limbs

        frames.append(frame)

    return frames


def process_effects(raw, renames):
    from re import findall

    if not raw:
        return []

    effect_constructor = findall(r"_0x[\da-f]{4,6}", raw)[0]
    effects_raw = raw.split(effect_constructor)[1:]
    effects_raw = [string.strip(" ,\n")[1:-1] for string in effects_raw]

    effects = []
    for effect_raw in effects_raw:

        time_raw = effect_raw.split(",")[0]
        effect = parse_time(time_raw, renames)

        effect_raw = effect_raw[len(time_raw)+2:]
        effect["func"] = effect_raw.split("'")[1]

        effect_raw = effect_raw[len(effect["func"])+5:-1]

        # noinspection PyTypeChecker
        effect["args"] = {}

        for line in effect_raw.split("\n"):
            line = line.strip(" ")
            if line:
                key, value = line.split(": ")
                key = key.strip("'")
                value = value.strip("'")
                effect["args"][key] = value

        effects.append(effect)

    return effects


def process_weap_renames(raw: str):
    # General string cleaning, turns "    _0x1234 = _0x5678['foo']['bar'],\n" into "_0x1234=_0x5678[foo[bar"
    raw = raw.replace(" ", "")
    raw = raw.replace(",", "")
    raw = raw.replace("'", "")
    raw = raw.replace("]", "")
    lines = raw.split("\n")

    out = {}
    for line in lines:
        new, old_raw = line.split("=")
        _, *old = old_raw.split("[")
        out[new] = old[::-1]
    return out


def process_idles(idles_raw):
    from textwrap import dedent

    # Remove first and last lines
    idles_raw = "\n".join(idles_raw.split("\n")[1:-1])
    idles_raw = dedent(idles_raw)

    idles = {}
    for line in idles_raw.split("\n"):
        name = line.split("'")[1]
        line = line[len(name)+5:-1]

        parsed = parse_point_set(line)
        idles[name] = parsed

    return idles


def parse_time(raw, renames):
    raw = raw.lstrip(" (")

    out = {
        "time": None,
        "abs_time": False,
        "time_mult": 1,
        "time_offset": 0.0
    }

    if is_number(raw):
        out["abs_time"] = True
        # noinspection PyTypedDict
        out["time"] = float(raw)
        return out

    out["time"] = []

    if "*" in raw:
        item1, item2 = raw.split(" * ")
        if is_number(item1):
            out["time_mult"] = float(item1)
            raw = item2
        else:
            out["time_mult"] = float(item2)
            raw = item1

    if "+" in raw or "-" in raw:

        neg = False
        if "-" in raw:
            neg = True
            raw = raw.replace("-", "+")

        item1, item2 = raw.split(" + ")
        if is_number(item1):
            out["time_offset"] = float(item1)
            raw = item2
            if neg:
                out["time_mult"] *= -1
        else:
            out["time_offset"] = float(item2) * (-1 if neg else 1)
            raw = item1

    raw = raw.replace("]", "")

    for name, replacements in renames.items():
        if name in raw:
            raw = raw.replace(name, "")
            for item in replacements:
                raw = "[" + repr(item) + raw
            raw = raw[1:]
            break

    for element in raw.split("["):
        if element[0] == "'":
            out["time"].append(element[1:-1])
        else:
            out["time"].append(int(element))

    return out


def parse_point_set(raw):
    from re import findall
    frame = {
        "HandL": None,
        "HandR": None,
        "FootL": None,
        "FootR": None
    }

    limbs = findall(
        # This is treated as one string, but is spaced out to make it easier to read
        r"\(0, _0x[\da-f]{4,6}\['default']\)"  # Some wierd function that comes from the TS->JS conversion (I think)
        r"\((?:_0x[\da-f]{4,6}|{})"  # Either a dict or the name of a dict
        r", _0x[\da-f]{4,6}\['((?:Hand|Foot)[LR])']"  # Specifies which limb is being set (1st element in limb)
        r", new _0x[\da-f]{4,6}\(_0x[\da-f]{4,6}\['create']"  # Point-with-rotation constructor, then point constructor
        r"\((-?\d+(?:\.\d+)?), (-?\d+(?:\.\d+)?)\)\)"  # x/y coords (2nd/3rd element in limb)
        r"(?:\['rotate']\((-)?Math\['PI'] \* (\d+(?:\.\d+)?))?",  # Optional rotation amount and even more optional
        raw)                                                      # negative value (4th/5th element in limb)

    if not limbs:
        raise RuntimeError("No limbs in passed string")

    for limb in limbs:
        name = limb[0]
        x = float(limb[1])
        y = float(limb[2])

        # If ['rotate'] is used
        if limb[-1]:
            angle = float(limb[-1])

            # If there's a negative sign in front of Math['PI'], make the angle negative
            if limb[3]:
                angle *= -1

        else:
            angle = 0

        frame[name] = [x, y, angle]
    return frame


def is_number(string):
    from re import fullmatch
    return bool(fullmatch(r"-?\d+(?:\.\d+)?", string))


if __name__ == '__main__':
    from survivpy_deobfuscator.misc_utils import get_app
    with get_app() as infile:
        in_data = infile.read()
    get_anims(in_data, "./jsons/")
