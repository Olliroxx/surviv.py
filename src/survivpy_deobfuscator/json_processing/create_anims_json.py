from re import findall


def get_anims(script, root_dir):
    """
    Gets animations
    """
    import re
    from json import dump

    print("Starting anims.json")

    regex = r""" {8}'[\da-f]{8}': function\(_0x[\da-f]{4,6}, _0x[\da-f]{4,6}, _0x[\da-f]{4,6}\) \{(
 {12}'use strict';
 {12}var (?:_0x[\da-f]{4,6} = _0x[\da-f]{4,6}\('[\da-f]{8}'\),
 {16}_0x[\da-f]{4,6} = _0x[\da-f]{4,6}\(_0x[\da-f]{4,6}\),
 {16})+_0x[\da-f]{4,6}(?:, _0x[\da-f]{4,6})+;

 {12}function _0x[\da-f]{4,6}\(_0x[\da-f]{4,6}\) \{
 {16}return _0x[\da-f]{4,6} && _0x[\da-f]{4,6}\['__esModule'] \? _0x[\da-f]{4,6} : \{
 {20}'default': _0x[\da-f]{4,6}
 {16}};
 {12}}
 {12}var _0x[\da-f]{4,6} = _0x[\da-f]{4,6}\('[\da-f]{8}'\),
 {16}_0x[\da-f]{4,6} = (_0x[\da-f]{4,6})\['Anim'],(?:
 {16}_0x[\da-f]{4,6} = _0x[\da-f]{4,6}\('[\da-f]{8}'\),)*
 {16}_0x[\da-f]{4,6} = function.*?}),
 {8}'[\da-f]{8}': function"""

    source, player_timings = re.findall(regex, script, re.DOTALL)[0]

    attack_mappings = dict(re.findall(r"(_0x[\da-f]{4,6}) = _0x[\da-f]{4,6}\['(.*?)']\['attack']", source))
    for key, value in attack_mappings.items():
        attack_mappings[key] = "[\"" + value + "\"]"
    attack_mappings[player_timings] = "[\"player\"]"

    for old, new in attack_mappings.items():
        source = source.replace(old, new)
    del old, new

    exports_raw = re.findall(r""" {12}_0x[\da-f]{4,6}\['exports'] = {
 {16}'(\w*?)': (_0x[\da-f]{4,6}),
 {16}'(\w*?)': (_0x[\da-f]{4,6}),
 {16}'(\w*?)': (_0x[\da-f]{4,6}),
 {16}'(\w*?)': (_0x[\da-f]{4,6})
 {12}};""", source)[0]
    exports = dict(zip(exports_raw[::2], exports_raw[1::2]))
    effect_constructor = get_effect_constructor(source)

    idles_raw = re.findall(exports["IdlePoses"] + r" = {(.*?)\n {16}}", source, re.DOTALL)[0]
    idles = process_idles(idles_raw)

    anims_raw = re.findall(exports["Animations"] + r" = {\n(.*?\n {16})}", source, re.DOTALL)[0]
    anims = process_anims(anims_raw, effect_constructor)

    with open(root_dir+"anims.json", "w") as file:
        dump({"idles": idles, "animations": anims}, file, indent=4)

    print("Finished anims.json")


def process_idles(idles_raw):
    idles_split = [i.lstrip(" ") for i in idles_raw.split("\n")[1:-1]]
    idles = {}
    regex = r"\(0, _0x[\da-f]{4,6}\['default']\)\(_0x[\da-f]{4,6}, _0x[\da-f]{4,6}\['(\w+?)']," \
            r" new _0x[\da-f]{4,6}\(_0x[\da-f]{4,6}\['create']\((-?\d+(?:\.\d+?)?), (-?\d+(?:\.\d+)?)\)\)\)"
    for idle in idles_split:
        out = {}
        idle_name = idle.split("'")[1]
        pos_list = findall(regex, idle)
        for name, x, y in pos_list:
            out[name] = (float(x), float(y))
        idles[idle_name] = out
    return idles


def process_anims(anims_raw, effect_constructor):
    from re import split, findall, DOTALL
    from textwrap import dedent

    anims_raw = dedent(anims_raw)
    anims_split = split(",\n(?! )", anims_raw)
    anims = {}

    frame_constructor = findall(r"(_0x[\da-f]{4,6})\(0, ", anims_raw)[0]

    for anim_text in anims_split:
        anim = {}
        name = anim_text.split("'", 2)[1]

        keyframes_str = findall(r"keyframes': \[(.*)],\n {4}'effects'", anim_text, DOTALL)[0]
        anim["keyframes"] = parse_keyframes(keyframes_str, frame_constructor) if keyframes_str else []

        effects_str = findall(r"'effects': \[(.*)]\n}", anim_text, DOTALL)[0]
        anim["effects"] = parse_effects(effects_str, effect_constructor) if effects_str else []
        anims[name] = anim
    return anims


def get_coords(text):
    return findall(r"_0x[\da-f]{4,6}\['create']\((-?\d+(?:\.\d+?)?), (-?\d+(?:\.\d+?)?)\)", text)[0]


def get_time(time):
    abs_time = is_digits(time)
    length = len(time)

    if " * " in time:
        time, time_mult = time.split(" * ")
        time_mult = numberify(time_mult)
    else:
        time_mult = 1

    if " + " in time:
        time, offset = time.split(" + ")
    else:
        offset = 0

    if "][" in time:
        time = time.rstrip("]")
        time = time.lstrip("[")
        time = time.split("][")
        time = [i.strip("'\"") for i in time]
        time = [numberify(i) if is_digits(i) else i for i in time]

    if type(time) == list and time[0] == time[1] == "player":
        time.pop(0)

    return time, offset, abs_time, time_mult, length


def is_digits(text):
    """
    Normal str.isdigit can't be used because it returns false if there is a decimal point
    """
    from re import fullmatch
    return bool(fullmatch(r"-?\d+(?:\.\d+?)?", text))


def numberify(num):
    if "." in num:
        return float(num)
    else:
        return int(num)


def parse_keyframes(text, frame_constructor):
    keyframes = []

    args = [frame_constructor+i.lstrip(", ") for i in text.split(frame_constructor)[:-1] if i]

    for arg in args:
        arg = findall(frame_constructor + r"\((?:-?\d+(?:\.\d+?)?, |\[\").+?\)\),", arg)[0]

        limb = None
        for possible_limb in ["HandR", "HandL", "FootL", "FootR"]:
            if possible_limb in arg:
                if limb:
                    raise RuntimeError
                limb = possible_limb
        if not limb:
            raise RuntimeError

        pos = get_coords(arg)

        time_raw = findall(frame_constructor + r"\((.*?),", arg)[0]
        time, time_offset, abs_time, time_mult, _ = get_time(time_raw)

        if abs_time:
            time = numberify(time)

        keyframes.append({
            "time": time,
            "time_mult": time_mult,
            "time_offset": time_offset,
            "pos": [numberify(i) for i in pos],
            "absolute_time": abs_time,
            "limb": limb,
            "transform": process_transform(arg)
        })

    return keyframes


def process_transform(text):
    text = text.rstrip(",")
    transforms_raw = findall(r"\['rotate']\(.+?\)\)\)$", text)
    # Offset and copy are also implemented, but not used
    if not transforms_raw:
        return None
    transforms = []
    for transform_raw in transforms_raw:
        transform = {
            "type": transform_raw.lstrip("['").split("']")[0]
        }
        amount_raw = transform_raw[5+len(transform["type"]):-3]
        sign = -1 if amount_raw[0] == "-" else 1
        exponent = numberify(amount_raw.split(" * ")[1])
        transform["amount"] = 3.141592653589793 * exponent * sign
        transforms.append(transform)

    return transforms


def parse_effects(text, effect_constructor):
    from json import loads

    effects = []
    raw_effects = [i for i in text.split(effect_constructor) if i]

    for raw in raw_effects:
        if is_digits(raw[1:].split(",")[0]):
            effect = {
                "time": raw[1:].split(",")[0],
                "abs_time": True,
                "time_mult": 1
            }
            raw = raw[len(str(effect["time"]))+4:]
        else:
            effect = {}
            effect["time"], _, effect["abs_time"], effect["time_mult"], length = get_time(raw[1:].split(",")[0])
            raw = raw[length+4:]
        effect["func"] = raw.split("'")[0]
        raw = raw[len(effect["func"])+3:]
        raw = raw.rstrip("), ")
        effect["args"] = loads(raw.replace("'", '"'))
        effects.append(effect)

    return effects


def get_effect_constructor(script):
    return findall(r""" {12}function (_0x[\da-f]{4,6})\(_0x[\da-f]{4,6}, _0x[\da-f]{4,6}, _0x[\da-f]{4,6}\) {
 {16}return {
 {20}'time': _0x[\da-f]{4,6},
 {20}'fn': _0x[\da-f]{4,6},
 {20}'args': _0x[\da-f]{4,6}
 {16}};
 {12}}""", script)[0]


if __name__ == '__main__':
    from survivpy_deobfuscator.misc_utils import get_app
    with get_app() as infile:
        in_data = infile.read()
    get_anims(in_data, "./jsons/")
