def get_proxies(script, root_dir):
    from json import loads, dump
    from re import findall, DOTALL

    print("Starting proxies.json")

    regex = r""" {12}var _0x[\da-f]{4,6} = _0x[\da-f]{4,6}\(('[\da-f]{8}')\),
 {16}_0x[\da-f]{4,6} = \{
 {20}'getProxyDef': function _0x[\da-f]{4,6}\(\) \{"""
    match = findall(regex, script)[0]

    regex = " {8}" + match + r""": function\(_0x[\da-f]{4,6}\) \{
 {12}_0x[\da-f]{4,6}\['exports'\] = (\{.*?});"""
    match = findall(regex, script, DOTALL)[0]

    out_file = open(root_dir+"proxies.json", "w")
    dump(loads(match), out_file, indent=4)

    print("Finished proxies.json")


if __name__ == '__main__':
    from survivpy_deobfuscator.misc_utils import get_app
    with get_app() as file:
        in_data = file.read()
    get_proxies(in_data, "./jsons")
