"""
This script grabs most of the svgs (guns, melees and other items), most of them don't have .svg at the end of their names
"""

from json import load
from requests import get
from os import mkdir


def grab_svgs():
    master_dict = {}
    sources = [
        "throwables",
        "nonweapons",
        "outfits",
    ]
    # The names of the json files to read from

    for file in sources:
        file = open("jsons/" + file + ".json", "r")
        data = load(file)
        file.close()
        master_dict = master_dict | data
    del data, file, sources
    # Load the data into a single dict

    svg_names = set()
    for key, value in master_dict.items():
        if "lootImg" in value:
            if "sprite" in value["lootImg"]:
                if value["lootImg"]["sprite"]:
                    svg_names.add(value["lootImg"]["sprite"])
    del key, value, master_dict
    # Get all the sprite names
    print(str(len(svg_names)) + " sprites to download")

    try:
        mkdir("./out/svgs/loot")
    except FileExistsError:
        pass

    sprite_number = 0
    for name in svg_names:
        sprite_number += 1
        print("Downloading " + name + ".svg, " + str(sprite_number) + "/" + str(len(svg_names)))
        resp = get("https://surviv.io/img/loot/" + name + ".svg")
        with open("./out/svgs/loot/" + name + ".svg", "bw") as file:
            file.write(resp.content)
    # Get and write all the sprites

    print("Done getting SVGs")


if __name__ == '__main__':
    grab_svgs()
